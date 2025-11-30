#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KORNIA VIDEO PIPELINE V2.0 - Thread-Safe GPU Accelerated Video Processing
==========================================================================

FFmpeg decode → Kornia GPU filters → FFmpeg encode

V2.0 Değişiklikler:
- Thread-based pipe I/O (deadlock önleme)
- Queue-based frame buffering
- Timeout protection
- Proper cleanup

Author: Claude
Date: November 2025
Version: 2.0
"""

import subprocess
import numpy as np
import logging
import os
import shutil
import threading
import queue
import time
from typing import Dict, List, Optional, Tuple, Generator

logger = logging.getLogger(__name__)

# FFmpeg path
FFMPEG_PATH = r"C:\ffmpeg\bin\ffmpeg.exe"
FFPROBE_PATH = r"C:\ffmpeg\bin\ffprobe.exe"

if not os.path.exists(FFMPEG_PATH):
    FFMPEG_PATH = shutil.which('ffmpeg') or 'ffmpeg'
    FFPROBE_PATH = shutil.which('ffprobe') or 'ffprobe'

# Kornia import
try:
    from kornia_filters import (
        KorniaGPUFilters,
        get_gpu_filters,
        parse_ffmpeg_filter_to_kornia,
        KORNIA_AVAILABLE,
        CUDA_AVAILABLE,
    )
except ImportError:
    KORNIA_AVAILABLE = False
    CUDA_AVAILABLE = False
    logger.warning("⚠️ Kornia filters not available")


class VideoInfo:
    """Video metadata"""
    def __init__(self, path: str):
        self.path = path
        self.width = 1920
        self.height = 1080
        self.fps = 30.0
        self.duration = 0.0
        self.total_frames = 0
        self._probe()

    def _probe(self):
        """FFprobe ile video bilgisi al"""
        try:
            cmd = [
                FFPROBE_PATH, '-v', 'error',
                '-select_streams', 'v:0',
                '-show_entries', 'stream=width,height,r_frame_rate,duration',
                '-of', 'csv=p=0',
                self.path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                parts = result.stdout.strip().split(',')
                if len(parts) >= 3:
                    self.width = int(parts[0])
                    self.height = int(parts[1])
                    fps_parts = parts[2].split('/')
                    if len(fps_parts) == 2:
                        self.fps = float(fps_parts[0]) / float(fps_parts[1])
                    else:
                        self.fps = float(fps_parts[0])
                    if len(parts) >= 4 and parts[3]:
                        self.duration = float(parts[3])
                        self.total_frames = int(self.duration * self.fps)
        except Exception as e:
            logger.warning(f"FFprobe failed: {e}")


class KorniaVideoPipeline:
    """
    GPU accelerated video processing pipeline.

    V2.0: Thread-safe implementation to prevent pipe deadlocks.
    """

    def __init__(self, use_gpu: bool = True):
        """
        Args:
            use_gpu: Use GPU for filtering (True) or CPU fallback (False)
        """
        self.use_gpu = use_gpu and KORNIA_AVAILABLE and CUDA_AVAILABLE
        self.gpu_filters = None
        self.batch_size = 4 if self.use_gpu else 1  # Smaller batch for stability

        # Lazy GPU init (don't load until needed)
        self._gpu_initialized = False

    def _init_gpu(self):
        """Lazy GPU initialization"""
        if not self._gpu_initialized and self.use_gpu:
            try:
                self.gpu_filters = get_gpu_filters()
                self._gpu_initialized = True
                logger.debug("🚀 Kornia GPU filters initialized")
            except Exception as e:
                logger.warning(f"⚠️ GPU init failed: {e}")
                self.use_gpu = False
                self.gpu_filters = None

    def get_video_info(self, input_path: str) -> VideoInfo:
        """Video bilgisi al"""
        return VideoInfo(input_path)

    def process_clip_gpu(self, input_path: str, output_path: str,
                         ffmpeg_filter_string: str,
                         audio_filter_string: Optional[str] = None,
                         use_nvenc: bool = False,
                         timeout: int = 120) -> bool:
        """
        Klip işleme - Thread-safe GPU pipeline.

        V2.0: Deadlock önlemek için threading kullanır.

        Args:
            input_path: Input video path
            output_path: Output video path
            ffmpeg_filter_string: FFmpeg -vf filter string
            audio_filter_string: FFmpeg -af filter string
            use_nvenc: Use NVENC for encoding
            timeout: Process timeout in seconds

        Returns:
            True if successful
        """
        # Lazy GPU init
        self._init_gpu()

        # Parse FFmpeg filter to Kornia params
        effect_params = parse_ffmpeg_filter_to_kornia(ffmpeg_filter_string) if self.use_gpu else {}

        try:
            # ===== DECODE COMMAND =====
            decode_cmd = [
                FFMPEG_PATH, '-v', 'error',
                '-i', input_path,
                '-vf', 'scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=30',
                '-pix_fmt', 'bgr24',
                '-f', 'rawvideo',
                '-'
            ]

            # ===== ENCODE COMMAND =====
            encode_cmd = [
                FFMPEG_PATH, '-v', 'error', '-y',
                '-f', 'rawvideo',
                '-pix_fmt', 'bgr24',
                '-s', '1920x1080',
                '-r', '30',
                '-i', '-',
                '-i', input_path,  # Audio source
                '-map', '0:v',
                '-map', '1:a?',
            ]

            # Video codec
            if use_nvenc:
                encode_cmd.extend([
                    '-c:v', 'h264_nvenc',
                    '-preset', 'p2',  # Fast preset
                    '-rc', 'vbr',
                    '-b:v', '5M',
                    '-maxrate', '8M',
                ])
            else:
                encode_cmd.extend([
                    '-c:v', 'libx264',
                    '-preset', 'veryfast',
                    '-crf', '18',
                ])

            # Audio
            if audio_filter_string:
                encode_cmd.extend(['-af', audio_filter_string])
            encode_cmd.extend([
                '-c:a', 'aac',
                '-b:a', '192k',
                '-pix_fmt', 'yuv420p',
                '-movflags', '+faststart',
                output_path
            ])

            # ===== FRAME QUEUE (prevents deadlock) =====
            frame_queue = queue.Queue(maxsize=16)  # Buffer 16 frames
            decode_error = [None]  # Mutable container for thread
            decode_done = threading.Event()

            # ===== DECODER THREAD =====
            def decoder_thread(proc):
                """Read frames from decoder in separate thread"""
                frame_size = 1920 * 1080 * 3
                try:
                    while True:
                        raw_frame = proc.stdout.read(frame_size)
                        if len(raw_frame) != frame_size:
                            break
                        # Put frame in queue (blocks if full)
                        frame_queue.put(raw_frame, timeout=30)
                except Exception as e:
                    decode_error[0] = str(e)
                finally:
                    frame_queue.put(None)  # Signal end
                    decode_done.set()

            # ===== START PROCESSES =====
            decoder = subprocess.Popen(
                decode_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                bufsize=1920 * 1080 * 3 * 4
            )

            encoder = subprocess.Popen(
                encode_cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                bufsize=1920 * 1080 * 3 * 4
            )

            # Start decoder thread
            dec_thread = threading.Thread(target=decoder_thread, args=(decoder,))
            dec_thread.daemon = True
            dec_thread.start()

            # ===== PROCESS FRAMES =====
            frame_count = 0
            batch_frames = []
            start_time = time.time()

            while True:
                # Check timeout
                if time.time() - start_time > timeout:
                    raise TimeoutError(f"Processing timeout ({timeout}s)")

                # Get frame from queue
                try:
                    raw_frame = frame_queue.get(timeout=5)
                except queue.Empty:
                    if decode_done.is_set():
                        break
                    continue

                if raw_frame is None:
                    break  # End of stream

                # Convert to numpy
                frame = np.frombuffer(raw_frame, dtype=np.uint8).reshape(1080, 1920, 3)

                if self.use_gpu and self.gpu_filters:
                    # Batch processing
                    batch_frames.append(frame.copy())

                    if len(batch_frames) >= self.batch_size:
                        # Process batch on GPU
                        processed = self.gpu_filters.process_batch(batch_frames, effect_params)
                        for pframe in processed:
                            encoder.stdin.write(pframe.tobytes())
                        batch_frames = []
                        frame_count += self.batch_size
                else:
                    # Direct write (no GPU processing)
                    encoder.stdin.write(frame.tobytes())
                    frame_count += 1

            # Process remaining batch
            if batch_frames and self.use_gpu and self.gpu_filters:
                processed = self.gpu_filters.process_batch(batch_frames, effect_params)
                for pframe in processed:
                    encoder.stdin.write(pframe.tobytes())
                frame_count += len(batch_frames)

            # ===== CLEANUP =====
            # Wait for decoder thread
            dec_thread.join(timeout=5)

            # Close decoder
            if decoder.poll() is None:
                decoder.terminate()
            decoder.wait(timeout=5)

            # Close encoder
            encoder.stdin.close()
            encoder.wait(timeout=30)

            # Clear GPU cache
            if self.gpu_filters:
                self.gpu_filters.clear_cache()

            # Check for errors
            if decode_error[0]:
                logger.warning(f"Decode error: {decode_error[0]}")

            success = encoder.returncode == 0
            if success:
                logger.debug(f"✅ Processed {frame_count} frames")
            else:
                stderr = encoder.stderr.read().decode()[:500]
                logger.warning(f"Encoder failed: {stderr}")

            return success

        except TimeoutError as e:
            logger.error(f"❌ Timeout: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Clip processing failed: {e}")
            return False
        finally:
            # Ensure cleanup
            try:
                if 'decoder' in locals() and decoder.poll() is None:
                    decoder.kill()
                if 'encoder' in locals() and encoder.poll() is None:
                    encoder.kill()
            except:
                pass


# =============================================================================
# SIMPLE API
# =============================================================================

def process_video_gpu(input_path: str, output_path: str,
                      ffmpeg_filter_string: str,
                      audio_filter_string: Optional[str] = None,
                      use_nvenc: bool = True) -> bool:
    """
    Simple API for GPU video processing.
    """
    pipeline = KorniaVideoPipeline(use_gpu=True)
    return pipeline.process_clip_gpu(
        input_path, output_path,
        ffmpeg_filter_string,
        audio_filter_string,
        use_nvenc
    )


# =============================================================================
# TEST
# =============================================================================

if __name__ == '__main__':
    print("Kornia Video Pipeline V2.0 - Thread-Safe")
    print(f"KORNIA_AVAILABLE: {KORNIA_AVAILABLE}")
    print(f"CUDA_AVAILABLE: {CUDA_AVAILABLE}")

    import sys
    if len(sys.argv) > 1:
        input_video = sys.argv[1]
        output_video = input_video.replace('.mp4', '_kornia_v2.mp4')

        print(f"\nProcessing: {input_video}")

        pipeline = KorniaVideoPipeline(use_gpu=True)
        success = pipeline.process_clip_gpu(
            input_video,
            output_video,
            'eq=brightness=0.05:contrast=1.1:saturation=1.05',
            None,
            use_nvenc=False
        )

        print(f"✅ Success: {success}")
        print(f"   Output: {output_video}")
    else:
        print("\nUsage: python kornia_video_pipeline.py input.mp4")
