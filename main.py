#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
✅ YOUTUBE ULTRA PRO V4.5 - SEÇİLEBİLİR EFEKT EDITION ✅

🎬 KULLANICI SEÇİMİ İLE CİNEMATİC EFEKTLER (30+)
🎬 YENİ TRANSİTİON EFEKTLER (35+ GEÇİŞ)
🎬 İSTEDİĞİNİZ EFEKTLERİ SEÇİN!
🎬 SLOW MOTION + AUTO SUBS + 320kbps AUDIO

%100 ÇALIŞMA GARANTİSİ + KİŞİSELLEŞTİRİLEBİLİR ÖZELLİKLER!
"""

import os
import sys
import subprocess
import random
import json
import time
import multiprocessing
import hashlib
import logging
import glob
from pathlib import Path
from datetime import datetime, timedelta
from concurrent.futures import ProcessPoolExecutor, as_completed
import shutil

# ==================== FFMPEG PATH (RTX 50 serisi için güncel FFmpeg) ====================
FFMPEG_PATH = r"C:\ffmpeg\bin\ffmpeg.exe"
FFPROBE_PATH = r"C:\ffmpeg\bin\ffprobe.exe"

# Fallback: PATH'te ara
if not os.path.exists(FFMPEG_PATH):
    FFMPEG_PATH = shutil.which('ffmpeg') or 'ffmpeg'
    FFPROBE_PATH = shutil.which('ffprobe') or 'ffprobe'

# ==================== LOGGING SETUP (İLK ÖNCE!) ====================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('video_process.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Import config files
from config import *
from effects import CINEMATIC_EFFECTS, TRANSITION_EFFECTS, ADVANCED_CONFIG, DYNAMIC_SUBTITLE_CONFIG
from error_handler import (
    ErrorCategory,
    GracefulErrorHandler,
    PartialSuccessTracker,
    parse_ffmpeg_error,
    retry_on_failure,
)

# ==================== 🚀 FFMPEG HUMANIZATION V2.0 ====================
try:
    from ffmpeg_humanization import (
        build_complete_ffmpeg_params,
        init_encoding_log,
        encoding_stats,
        print_encoding_dashboard,
        detect_available_encoders,
    )
    FFMPEG_HUMANIZATION_AVAILABLE = True
    logger.info("✅ FFmpeg Humanization V2.0 loaded (18 features)")
except ImportError as e:
    FFMPEG_HUMANIZATION_AVAILABLE = False
    logger.warning(f"⚠️ FFmpeg Humanization V2.0 not available: {e}")

# ==================== 🎙️ AUDIO HUMANİZATION MODÜLÜ ====================
try:
    from audio_humanization import (
        build_humanized_audio_filter,
        init_audio_log,
        AUDIO_HUMANIZATION_CONFIG,
    )
    AUDIO_HUMANIZATION_AVAILABLE = True
    logger.info("✅ Audio Humanization V1.0 loaded (ElevenLabs → Real Voice)")
except ImportError as e:
    AUDIO_HUMANIZATION_AVAILABLE = False
    logger.warning(f"⚠️ Audio Humanization not available: {e}")

# ==================== 🚀 GPU OPTIMIZER V1.0 (NVENC Hardware Acceleration) ====================
try:
    from gpu_optimizer import (
        detect_nvenc_support,
        get_optimal_encoding_params,
        translate_x264_to_nvenc,
        get_hardware_accel_params,
        monitor_gpu_performance,
        init_gpu_log,
    )
    GPU_OPTIMIZER_AVAILABLE = True

    # Initialize GPU logging (reduced verbosity for parallel workers)
    init_gpu_log('WARNING')  # Only show warnings/errors, not INFO

    # Detect NVENC on startup
    NVENC_INFO = detect_nvenc_support()

    if NVENC_INFO['available']:
        logger.info("✅ GPU Optimizer V1.0 loaded")
        logger.info(f"✅ NVENC ready: {NVENC_INFO['gpu_name']} (v{NVENC_INFO.get('nvenc_version', 'N/A')})")
        logger.info("✅ Expected speedup: 5-10x faster encoding")
    else:
        logger.info(f"⚠️ GPU Optimizer loaded (NVENC unavailable: {NVENC_INFO['reason']})")
        logger.info("ℹ️ Will use CPU encoding (libx264)")

except ImportError as e:
    GPU_OPTIMIZER_AVAILABLE = False
    NVENC_INFO = {'available': False, 'reason': 'Module not found'}
    logger.warning(f"⚠️ GPU Optimizer not available: {e}")
    logger.info("ℹ️ Will use CPU encoding (libx264)")

# ==================== 🚀 KORNIA GPU FILTERS (8-10x faster filtering) ====================
try:
    from kornia_video_pipeline import (
        KorniaVideoPipeline,
        process_video_gpu,
        KORNIA_AVAILABLE,
        CUDA_AVAILABLE,
    )
    from kornia_filters import parse_ffmpeg_filter_to_kornia

    KORNIA_GPU_AVAILABLE = KORNIA_AVAILABLE and CUDA_AVAILABLE
    if KORNIA_GPU_AVAILABLE:
        logger.info("✅ Kornia GPU Filters loaded (8-10x faster)")
    else:
        logger.info("⚠️ Kornia loaded but CUDA not available")
except ImportError as e:
    KORNIA_GPU_AVAILABLE = False
    logger.warning(f"⚠️ Kornia GPU Filters not available: {e}")
    logger.info("ℹ️ Will use FFmpeg CPU filters")

# ==================== 🚀 YOUTUBE OPTİMİZASYON MODÜLLERİ ====================
try:
    from youtube_optimization_addon import (
        post_render_quality_check,
        enhanced_metadata_injection,
        generate_video_fingerprint,
        save_fingerprint_database,
        apply_effect_balancing,
        suggest_upload_time,
        apply_youtube_optimizations,
        generate_optimization_report
    )

    YOUTUBE_OPTIMIZATION_ENABLED = True
    logger.info("✅ YouTube optimizasyon modülü yüklendi")
except ImportError as e:
    logger.warning(f"⚠️  YouTube optimizasyon modülü yüklenemedi: {e}")
    logger.warning("⚠️  Program normal modda çalışacak")
    YOUTUBE_OPTIMIZATION_ENABLED = False

# Import yeni config modülleri
try:
    from config import METADATA_RANDOMIZATION, UPLOAD_STRATEGY, ADVANCED_QUALITY_CHECKS, TURBO_MODE, GPU_SCALE_ENABLED, KORNIA_GPU_FILTERS
    from effects import EFFECT_MODE, EFFECT_BALANCING
except ImportError:
    # Eski config kullanılıyor, varsayılan değerler
    METADATA_RANDOMIZATION = {'enabled': False}
    UPLOAD_STRATEGY = {'enabled': False}
    ADVANCED_QUALITY_CHECKS = {'enabled': False}
    EFFECT_MODE = 'medium'
    EFFECT_BALANCING = {'enabled': False}
    TURBO_MODE = False
    GPU_SCALE_ENABLED = False
    KORNIA_GPU_FILTERS = False

# ==================== FONT GENİŞLİK HESAPLAMA SİSTEMİ ====================

# Font metrik tablosu - Her font için gerçek ölçümler
FONT_METRICS = {
    'Impact': {'base_width': 52, 'spacing_factor': 1.0, 'category': 'wide'},
    'Arial Black': {'base_width': 48, 'spacing_factor': 0.95, 'category': 'wide'},
    'Verdana Bold': {'base_width': 45, 'spacing_factor': 1.1, 'category': 'medium'},
    'Arial Bold': {'base_width': 42, 'spacing_factor': 0.9, 'category': 'medium'},
    'Tahoma Bold': {'base_width': 40, 'spacing_factor': 0.95, 'category': 'medium'},
    'Trebuchet MS Bold': {'base_width': 43, 'spacing_factor': 1.0, 'category': 'medium'},
    'Georgia Bold': {'base_width': 44, 'spacing_factor': 1.05, 'category': 'medium'},
    'Times New Roman Bold': {'base_width': 38, 'spacing_factor': 0.95, 'category': 'narrow'},
    'Garamond Bold': {'base_width': 36, 'spacing_factor': 0.9, 'category': 'narrow'},
    'Courier New Bold': {'base_width': 50, 'spacing_factor': 1.0, 'category': 'monospace'},
    'Consolas Bold': {'base_width': 48, 'spacing_factor': 1.0, 'category': 'monospace'},
    'Helvetica Bold': {'base_width': 42, 'spacing_factor': 0.95, 'category': 'medium'},
    'Calibri Bold': {'base_width': 40, 'spacing_factor': 1.0, 'category': 'medium'},
    'Segoe UI Bold': {'base_width': 41, 'spacing_factor': 1.0, 'category': 'medium'},
    'default': {'base_width': 45, 'spacing_factor': 1.0, 'category': 'medium'},
}


def calculate_max_chars_dynamic(font_name, font_size, outline_width, screen_width=1920, margin_left=200,
                                margin_right=200):
    """
    🆕 DİNAMİK maksimum karakter sayısı hesapla (her font için özel)

    Args:
        font_name: Font adı (örn: "Impact", "Arial Bold")
        font_size: Font boyutu (pt)
        outline_width: Outline kalınlığı (px)
        screen_width: Ekran genişliği (px)
        margin_left: Sol margin (px)
        margin_right: Sağ margin (px)

    Returns:
        max_chars: Maksimum karakter sayısı (font'a özel hesaplanmış)
    """
    # Font metriğini al
    font_key = font_name
    if font_key not in FONT_METRICS:
        # Benzer font bul
        for key in FONT_METRICS.keys():
            if key.lower() in font_name.lower() or font_name.lower() in key.lower():
                font_key = key
                break
        else:
            font_key = 'default'

    metrics = FONT_METRICS[font_key]

    # Kullanılabilir genişlik
    available_width = screen_width - margin_left - margin_right

    # Karakter genişliği hesapla
    base_char_width = metrics['base_width'] * (font_size / 100.0)
    spacing_char_width = base_char_width * metrics['spacing_factor']
    outline_effect = outline_width * 2
    total_char_width = spacing_char_width + outline_effect

    # Maksimum karakter sayısı
    max_chars = int(available_width / total_char_width)

    # Güvenlik marjı (%10 azalt)
    safe_max_chars = int(max_chars * 0.9)

    # Minimum ve maksimum limitler
    safe_max_chars = max(15, safe_max_chars)  # Min 15 karakter
    safe_max_chars = min(50, safe_max_chars)  # Max 50 karakter

    return safe_max_chars


# ==================== GPU DETECTION ====================

def gpu_durumunu_tespit_et():
    """GPU encoder'ları tespit et ve en iyisini seç"""
    gpu_encoders = {
        'nvidia': {'video': 'h264_nvenc', 'priority': 1},
        'amd': {'video': 'h264_amf', 'priority': 2},
        'intel': {'video': 'h264_qsv', 'priority': 3},
        'cpu': {'video': 'libx264', 'priority': 4}
    }

    available = []

    # NVIDIA kontrolü
    try:
        result = subprocess.run(['nvidia-smi'],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                timeout=3)
        if result.returncode == 0:
            test_cmd = [FFMPEG_PATH, '-hide_banner', '-encoders']
            test_result = subprocess.run(test_cmd,
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE,
                                         text=True,
                                         timeout=3)
            if 'h264_nvenc' in test_result.stdout:
                # RTX 50 serisi yeni preset (p1-p7), eski GPU'lar eski preset (fast/medium)
                # Her ikisini de dene
                presets_to_try = ['p4', 'p5', 'fast', 'medium']  # Yeni presetler önce
                nvenc_working = False

                for test_preset in presets_to_try:
                    try:
                        test_encode = [
                            FFMPEG_PATH, '-f', 'lavfi', '-i', 'testsrc=duration=1:size=256x256:rate=1',
                            '-c:v', 'h264_nvenc', '-preset', test_preset, '-t', '0.5',
                            '-f', 'null', '-'
                        ]
                        test_result = subprocess.run(test_encode,
                                                     stdout=subprocess.PIPE,
                                                     stderr=subprocess.PIPE,
                                                     timeout=10)
                        if test_result.returncode == 0:
                            available.append(('nvidia', gpu_encoders['nvidia']))
                            logger.info(f"✅ NVIDIA GPU tespit edildi (h264_nvenc, preset: {test_preset})")
                            nvenc_working = True
                            break
                    except Exception as e:
                        continue

                if not nvenc_working:
                    logger.warning(f"⚠️  NVIDIA GPU var ama NVENC encoder test edilemedi (FFmpeg güncellemesi gerekebilir)")
    except:
        pass

    # AMD kontrolü
    try:
        test_cmd = [FFMPEG_PATH, '-hide_banner', '-encoders']
        result = subprocess.run(test_cmd,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True,
                                timeout=3)
        if 'h264_amf' in result.stdout:
            try:
                test_encode = [
                    FFMPEG_PATH, '-f', 'lavfi', '-i', 'testsrc=duration=1:size=1280x720:rate=1',
                    '-c:v', 'h264_amf', '-quality', 'speed', '-t', '1',
                    '-f', 'null', '-'
                ]
                test_result = subprocess.run(test_encode,
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE,
                                             timeout=10)
                if test_result.returncode == 0:
                    available.append(('amd', gpu_encoders['amd']))
                    logger.info("✅ AMD GPU tespit edildi (h264_amf)")
            except:
                pass
    except:
        pass

    # Intel QSV kontrolü
    try:
        test_cmd = [FFMPEG_PATH, '-hide_banner', '-encoders']
        result = subprocess.run(test_cmd,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True,
                                timeout=3)
        if 'h264_qsv' in result.stdout:
            try:
                test_encode = [
                    FFMPEG_PATH, '-f', 'lavfi', '-i', 'testsrc=duration=1:size=1280x720:rate=1',
                    '-c:v', 'h264_qsv', '-preset', 'fast', '-t', '1',
                    '-f', 'null', '-'
                ]
                test_result = subprocess.run(test_encode,
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE,
                                             timeout=10)
                if test_result.returncode == 0:
                    available.append(('intel', gpu_encoders['intel']))
                    logger.info("✅ Intel QSV tespit edildi (h264_qsv)")
            except:
                pass
    except:
        pass

    # CPU fallback
    available.append(('cpu', gpu_encoders['cpu']))

    # En yüksek önceliğe sahip olanı seç
    available.sort(key=lambda x: x[1]['priority'])
    selected = available[0]

    if selected[0] == 'cpu':
        logger.info(f"⚠️  GPU bulunamadı - CPU kullanılacak")
    else:
        logger.info(f"🎯 Seçilen encoder: {selected[0].upper()} ({selected[1]['video']})")

    return selected[0], selected[1]


# ==================== POST-RENDER SIKISTIRMA ====================

def post_render_compress(input_path: str, target_size_mb: int = 500) -> bool:
    """
    Render sonrası video sıkıştırma - Dosya boyutunu küçültür (İlerleme çubuğu ile)
    """
    import os
    import subprocess
    import shutil
    import sys
    import re

    if not os.path.exists(input_path):
        return False

    current_size_mb = os.path.getsize(input_path) / (1024 * 1024)

    if current_size_mb <= target_size_mb:
        print(f"   ✅ Dosya zaten yeterince küçük: {current_size_mb:.0f} MB")
        return True

    print(f"\n   🗜️  SIKISTIRMA BAŞLIYOR...")
    print(f"   📊 Mevcut boyut: {current_size_mb:.0f} MB")
    print(f"   🎯 Hedef boyut: ~{target_size_mb} MB")

    # Video süresini al
    try:
        probe_cmd = [
            FFPROBE_PATH, '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            input_path
        ]
        result = subprocess.run(probe_cmd, capture_output=True, text=True, timeout=30)
        duration = float(result.stdout.strip())
    except:
        duration = 1800

    target_bitrate_kbps = int((target_size_mb * 8 * 1024 * 0.85) / duration)
    target_bitrate_kbps = max(target_bitrate_kbps, 1000)

    # Tahmini süre hesapla (gerçek sürenin ~2-3 katı)
    estimated_time_min = (duration / 60) * 2.5  # Her pass için ~1.25x
    print(f"   📐 Video süresi: {duration/60:.1f} dakika")
    print(f"   📐 Hedef bitrate: {target_bitrate_kbps} kbps")
    print(f"   ⏱️  Tahmini süre: ~{estimated_time_min:.0f} dakika")

    output_path = input_path + '.compressed.mp4'
    pass_log = input_path + '_2pass'

    def run_ffmpeg_with_progress(cmd, pass_num, total_duration):
        """FFmpeg'i ilerleme çubuğu ile çalıştır"""
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )

        bar_width = 40
        start_time = time.time()

        while True:
            line = process.stderr.readline()
            if not line and process.poll() is not None:
                break

            # FFmpeg time= çıktısını parse et
            time_match = re.search(r'time=(\d+):(\d+):(\d+\.?\d*)', line)
            if time_match:
                hours = int(time_match.group(1))
                minutes = int(time_match.group(2))
                seconds = float(time_match.group(3))
                current_time = hours * 3600 + minutes * 60 + seconds

                progress = min(current_time / total_duration, 1.0)
                filled = int(bar_width * progress)
                bar = '█' * filled + '░' * (bar_width - filled)

                elapsed = time.time() - start_time
                if progress > 0:
                    eta = (elapsed / progress) - elapsed
                    eta_str = f"{int(eta//60)}:{int(eta%60):02d}"
                else:
                    eta_str = "--:--"

                print(f"\r   Pass {pass_num}/2 [{bar}] {progress*100:5.1f}% | ETA: {eta_str}  ", end='', flush=True)

        print()  # Yeni satır
        return process.returncode

    try:
        # Pass 1 - Analiz
        print(f"\n   ⏳ Pass 1/2 - Analiz başlıyor...")
        pass1_cmd = [
            FFMPEG_PATH, '-y', '-i', input_path,
            '-c:v', 'libx264',
            '-preset', 'fast',  # Daha hızlı analiz
            '-b:v', f'{target_bitrate_kbps}k',
            '-pass', '1',
            '-passlogfile', pass_log,
            '-an',
            '-f', 'null',
            '/dev/null' if os.name != 'nt' else 'NUL'
        ]
        run_ffmpeg_with_progress(pass1_cmd, 1, duration)

        # Pass 2 - Encoding
        print(f"\n   ⏳ Pass 2/2 - Encoding başlıyor...")
        pass2_cmd = [
            FFMPEG_PATH, '-y', '-i', input_path,
            '-c:v', 'libx264',
            '-preset', 'medium',
            '-b:v', f'{target_bitrate_kbps}k',
            '-pass', '2',
            '-passlogfile', pass_log,
            '-c:a', 'aac',
            '-b:a', '128k',
            '-movflags', '+faststart',
            output_path
        ]
        returncode = run_ffmpeg_with_progress(pass2_cmd, 2, duration)

        # Temizlik
        for ext in ['.log', '-0.log', '-0.log.mbtree', '.log.mbtree']:
            try:
                os.remove(pass_log + ext)
            except:
                pass

        if returncode == 0 and os.path.exists(output_path):
            new_size_mb = os.path.getsize(output_path) / (1024 * 1024)

            if new_size_mb < current_size_mb:
                os.remove(input_path)
                shutil.move(output_path, input_path)

                reduction = ((current_size_mb - new_size_mb) / current_size_mb) * 100
                print(f"\n   ✅ Sıkıştırma başarılı!")
                print(f"   📊 Yeni boyut: {new_size_mb:.0f} MB (-%{reduction:.0f})")
                return True
            else:
                os.remove(output_path)
                print(f"\n   ⚠️  Sıkıştırma fayda sağlamadı, orijinal korunuyor")
                return False
        else:
            print(f"\n   ❌ Sıkıştırma başarısız")
            if os.path.exists(output_path):
                os.remove(output_path)
            return False

    except Exception as e:
        print(f"\n   ❌ Sıkıştırma hatası: {e}")
        if os.path.exists(output_path):
            try:
                os.remove(output_path)
            except:
                pass
        return False


# ==================== FONT SEÇİM SİSTEMİ ====================

def font_secim_menusu():
    """Kullanıcının altyazı fontu seçmesini sağlar"""
    print("\n" + "=" * 100)
    print("✨ ALTYAZI FONT SEÇİM MENÜSÜ - 30+ PROFESYONEL FONT ✨".center(100))
    print("=" * 100)
    print("\n💡 Videolarınız için en uygun fontu seçin!")
    print("   • Varsayılan: Impact (en viral YouTube/TikTok fontu)")
    print("   • Her font kategoriye özel optimize edilmiş")
    print("   • Platform öneri ve açıklamalar mevcut")
    print("\n" + "=" * 100)

    # Kategorileri numaralandır
    kategoriler = list(SUBTITLE_FONTS.keys())
    font_listesi = []
    font_index = 1

    for kategori_adi in kategoriler:
        print(f"\n{kategori_adi}")
        print("-" * 80)

        kategori = SUBTITLE_FONTS[kategori_adi]
        for font_key, font_info in kategori.items():
            font_listesi.append((font_key, font_info, kategori_adi))

            # Platform bilgisi
            platforms_str = ", ".join(font_info['platforms'][:2])  # İlk 2 platform

            print(f"   [{font_index:2d}] {font_info['name']:25s} - {font_info['description']}")
            print(f"       ↳ {font_info['best_for']}")
            print(f"       ↳ İdeal: {platforms_str}")

            font_index += 1

    print("\n" + "=" * 100)
    print(f"💡 Toplam {len(font_listesi)} farklı profesyonel font mevcut!")
    print("=" * 100)

    # Kullanıcı seçimi
    while True:
        secim = input(f"\n   ✨ Font numarası seçin [1-{len(font_listesi)}] (Enter=1, Impact): ").strip()

        if secim == '':
            print(f"   ✅ Varsayılan seçildi: Impact (Viral YouTube/TikTok fontu)")
            return 'Impact', 1.0, 4, True

        try:
            secim_num = int(secim)
            if 1 <= secim_num <= len(font_listesi):
                font_key, font_info, kategori = font_listesi[secim_num - 1]

                print(f"\n   ✅ SEÇİLEN FONT:")
                print(f"      📝 Font: {font_info['name']}")
                print(f"      🎨 Kategori: {kategori}")
                print(f"      💡 Açıklama: {font_info['description']}")
                print(f"      🎯 En iyi: {font_info['best_for']}")
                print(f"      📱 Platformlar: {', '.join(font_info['platforms'])}")

                return (
                    font_info['name'],
                    font_info['size_multiplier'],
                    font_info['outline_width'],
                    font_info['shadow']
                )
            else:
                print(f"   ❌ Lütfen 1-{len(font_listesi)} arası bir sayı girin")
        except ValueError:
            print(f"   ❌ Geçersiz giriş. Lütfen sayı girin veya Enter'a basın")


# ==================== EFEKT SEÇİM SİSTEMİ ====================

def akilli_efekt_secimi():
    """🧠 Akıllı Efekt Seçimi - Her video için uyumlu rastgele efektler seçer (2-10 adet)

    Algoritma:
    - Her video için 2-10 arası rastgele sayıda efekt seçer
    - Efektlerin uyumluluğunu kontrol eder
    - Ağır efektleri dengeleyerek performansı optimize eder
    - Görsel uyumu sağlar (renk, hareket, distorsiyon dengesi)
    """

    # ===== 🎨 EFEKT KATEGORİLERİ VE ÖZELLİKLERİ =====
    efekt_ozellikleri = {
        # HAFIF EFEKTLER (her kombinasyonda kullanılabilir)
        'sharpen_boost': {
            'kategori': ['modern', 'quality'],
            'yogunluk': 'hafif',
            'performans': 'hafif',
            'tip': 'quality',
            'uyumluluk_skoru': 10  # Yüksek = her şeyle uyumlu
        },
        'vignette_advanced': {
            'kategori': ['modern', 'cinematic'],
            'yogunluk': 'hafif',
            'performans': 'hafif',
            'tip': 'overlay',
            'uyumluluk_skoru': 10
        },
        'dream_glow': {
            'kategori': ['modern', 'soft'],
            'yogunluk': 'hafif',
            'performans': 'orta',
            'tip': 'color',
            'uyumluluk_skoru': 9
        },
        'color_grading': {
            'kategori': ['modern', 'cinematic'],
            'yogunluk': 'hafif',
            'performans': 'hafif',
            'tip': 'color',
            'uyumluluk_skoru': 10
        },
        'motion_blur': {
            'kategori': ['modern', 'motion'],
            'yogunluk': 'hafif',
            'performans': 'orta',
            'tip': 'motion',
            'uyumluluk_skoru': 9
        },
        'light_leaks': {
            'kategori': ['modern', 'cinematic'],
            'yogunluk': 'hafif',
            'performans': 'hafif',
            'tip': 'overlay',
            'uyumluluk_skoru': 9
        },

        # ORTA EFEKTLER (dikkatli kullanılmalı)
        'camera_shake': {
            'kategori': ['modern', 'motion'],
            'yogunluk': 'orta',
            'performans': 'hafif',
            'tip': 'motion',
            'uyumluluk_skoru': 8
        },
        'zoom_pulse': {
            'kategori': ['modern', 'motion'],
            'yogunluk': 'orta',
            'performans': 'hafif',
            'tip': 'motion',
            'uyumluluk_skoru': 8
        },
        'lens_distortion': {
            'kategori': ['modern', 'distortion'],
            'yogunluk': 'orta',
            'performans': 'orta',
            'tip': 'distortion',
            'uyumluluk_skoru': 7
        },
        'chromatic_aberration': {
            'kategori': ['modern', 'color'],
            'yogunluk': 'orta',
            'performans': 'orta',
            'tip': 'color',
            'uyumluluk_skoru': 8
        },
        'neon_glow': {
            'kategori': ['modern', 'color'],
            'yogunluk': 'orta',
            'performans': 'orta',
            'tip': 'color',
            'uyumluluk_skoru': 8
        },
        'velocity_ramp': {
            'kategori': ['modern', 'motion'],
            'yogunluk': 'orta',
            'performans': 'orta',
            'tip': 'motion',
            'uyumluluk_skoru': 9
        },
        'ghost_trail': {
            'kategori': ['modern', 'motion'],
            'yogunluk': 'orta',
            'performans': 'agir',
            'tip': 'motion',
            'uyumluluk_skoru': 7
        },
        'overlay_particles': {
            'kategori': ['modern', 'overlay'],
            'yogunluk': 'orta',
            'performans': 'orta',
            'tip': 'overlay',
            'uyumluluk_skoru': 8
        },

        # AĞIR EFEKTLER (sınırlı kullanım)
        'glitch': {
            'kategori': ['digital', 'distortion'],
            'yogunluk': 'agir',
            'performans': 'orta',
            'tip': 'distortion',
            'uyumluluk_skoru': 6
        },
        'datamosh': {
            'kategori': ['digital', 'distortion'],
            'yogunluk': 'agir',
            'performans': 'agir',
            'tip': 'distortion',
            'uyumluluk_skoru': 5
        },
        'pixelate': {
            'kategori': ['digital', 'distortion'],
            'yogunluk': 'agir',
            'performans': 'hafif',
            'tip': 'distortion',
            'uyumluluk_skoru': 6
        },
        'posterize': {
            'kategori': ['artistic', 'color'],
            'yogunluk': 'agir',
            'performans': 'hafif',
            'tip': 'color',
            'uyumluluk_skoru': 6
        },
        'edge_detect': {
            'kategori': ['artistic', 'distortion'],
            'yogunluk': 'agir',
            'performans': 'orta',
            'tip': 'distortion',
            'uyumluluk_skoru': 5
        },
        'mirror_kaleidoscope': {
            'kategori': ['artistic', 'distortion'],
            'yogunluk': 'agir',
            'performans': 'orta',
            'tip': 'distortion',
            'uyumluluk_skoru': 5
        },
        'solarize': {
            'kategori': ['artistic', 'color'],
            'yogunluk': 'agir',
            'performans': 'hafif',
            'tip': 'color',
            'uyumluluk_skoru': 6
        },
        'halftone': {
            'kategori': ['retro', 'artistic'],
            'yogunluk': 'agir',
            'performans': 'orta',
            'tip': 'artistic',
            'uyumluluk_skoru': 6
        },
        'vhs_advanced': {
            'kategori': ['retro', 'distortion'],
            'yogunluk': 'agir',
            'performans': 'orta',
            'tip': 'distortion',
            'uyumluluk_skoru': 7
        },
        'prism': {
            'kategori': ['artistic', 'color'],
            'yogunluk': 'agir',
            'performans': 'orta',
            'tip': 'color',
            'uyumluluk_skoru': 6
        },
        'rgb_split_advanced': {
            'kategori': ['digital', 'color'],
            'yogunluk': 'agir',
            'performans': 'orta',
            'tip': 'color',
            'uyumluluk_skoru': 7
        },
        'shake_advanced': {
            'kategori': ['modern', 'motion'],
            'yogunluk': 'agir',
            'performans': 'orta',
            'tip': 'motion',
            'uyumluluk_skoru': 7
        },
        'vintage_styles': {
            'kategori': ['retro', 'color'],
            'yogunluk': 'agir',
            'performans': 'orta',
            'tip': 'color',
            'uyumluluk_skoru': 7
        },
    }

    # ===== 🎲 RASTGELE EFEKT SAYISI BELİRLE (2-10) =====
    hedef_efekt_sayisi = random.randint(2, 10)

    # ===== 🧮 UYUMLULUK KURALLARI =====
    def efekt_uyumlu_mu(secili_efektler, yeni_efekt):
        """İki efektin uyumlu olup olmadığını kontrol eder"""
        if not secili_efektler:
            return True

        yeni_ozellik = efekt_ozellikleri[yeni_efekt]

        # Seçili efektlerin özelliklerini topla
        agir_efekt_sayisi = sum(1 for e in secili_efektler if efekt_ozellikleri[e]['yogunluk'] == 'agir')
        motion_efekt_sayisi = sum(1 for e in secili_efektler if efekt_ozellikleri[e]['tip'] == 'motion')
        distortion_efekt_sayisi = sum(1 for e in secili_efektler if efekt_ozellikleri[e]['tip'] == 'distortion')
        color_efekt_sayisi = sum(1 for e in secili_efektler if efekt_ozellikleri[e]['tip'] == 'color')

        # Kural 1: Maksimum 3 ağır efekt
        if yeni_ozellik['yogunluk'] == 'agir' and agir_efekt_sayisi >= 3:
            return False

        # Kural 2: Maksimum 3 motion efekt
        if yeni_ozellik['tip'] == 'motion' and motion_efekt_sayisi >= 3:
            return False

        # Kural 3: Maksimum 2 distortion efekt (çok distortion kötü görünür)
        if yeni_ozellik['tip'] == 'distortion' and distortion_efekt_sayisi >= 2:
            return False

        # Kural 4: Maksimum 3 color efekt
        if yeni_ozellik['tip'] == 'color' and color_efekt_sayisi >= 3:
            return False

        # Kural 5: Stil uyumu kontrolü (retro + digital = kötü)
        secili_kategoriler = set()
        for efekt in secili_efektler:
            secili_kategoriler.update(efekt_ozellikleri[efekt]['kategori'])

        yeni_kategoriler = set(yeni_ozellik['kategori'])

        # Retro ve digital birlikte olmamalı
        if 'retro' in secili_kategoriler and 'digital' in yeni_kategoriler:
            return False
        if 'digital' in secili_kategoriler and 'retro' in yeni_kategoriler:
            return False

        return True

    # ===== 🎯 AKILLI SEÇİM ALGORİTMASI =====
    secilen_efektler = set()
    tum_efektler = list(efekt_ozellikleri.keys())

    # Önce hafif efektlerden başla (daha uyumlu)
    hafif_efektler = [e for e in tum_efektler if efekt_ozellikleri[e]['yogunluk'] == 'hafif']
    orta_efektler = [e for e in tum_efektler if efekt_ozellikleri[e]['yogunluk'] == 'orta']
    agir_efektler = [e for e in tum_efektler if efekt_ozellikleri[e]['yogunluk'] == 'agir']

    # Karıştır
    random.shuffle(hafif_efektler)
    random.shuffle(orta_efektler)
    random.shuffle(agir_efektler)

    # Dağılım: %40 hafif, %40 orta, %20 ağır
    hafif_hedef = int(hedef_efekt_sayisi * 0.4)
    orta_hedef = int(hedef_efekt_sayisi * 0.4)
    agir_hedef = hedef_efekt_sayisi - hafif_hedef - orta_hedef

    # Hafif efektleri ekle
    for efekt in hafif_efektler:
        if len(secilen_efektler) >= hedef_efekt_sayisi:
            break
        if efekt_uyumlu_mu(secilen_efektler, efekt):
            secilen_efektler.add(efekt)
            if len([e for e in secilen_efektler if efekt_ozellikleri[e]['yogunluk'] == 'hafif']) >= hafif_hedef:
                break

    # Orta efektleri ekle
    for efekt in orta_efektler:
        if len(secilen_efektler) >= hedef_efekt_sayisi:
            break
        if efekt_uyumlu_mu(secilen_efektler, efekt):
            secilen_efektler.add(efekt)
            if len([e for e in secilen_efektler if efekt_ozellikleri[e]['yogunluk'] == 'orta']) >= orta_hedef:
                break

    # Ağır efektleri ekle
    for efekt in agir_efektler:
        if len(secilen_efektler) >= hedef_efekt_sayisi:
            break
        if efekt_uyumlu_mu(secilen_efektler, efekt):
            secilen_efektler.add(efekt)
            if len([e for e in secilen_efektler if efekt_ozellikleri[e]['yogunluk'] == 'agir']) >= agir_hedef:
                break

    # Eğer hedef sayıya ulaşamadıysak, kalan efektlerden ekle
    kalan_efektler = [e for e in tum_efektler if e not in secilen_efektler]
    random.shuffle(kalan_efektler)

    for efekt in kalan_efektler:
        if len(secilen_efektler) >= hedef_efekt_sayisi:
            break
        if efekt_uyumlu_mu(secilen_efektler, efekt):
            secilen_efektler.add(efekt)

    # ===== 📊 SEÇİM İSTATİSTİKLERİ =====
    print("\n" + "=" * 100)
    print("🧠 AKILLI EFEKT SEÇİMİ - RASTGELE UYUMLU KOMBİNASYON".center(100))
    print("=" * 100)
    print(f"\n   🎲 Hedef efekt sayısı: {hedef_efekt_sayisi}")
    print(f"   ✅ Seçilen efekt sayısı: {len(secilen_efektler)}")

    # Kategorilere göre grupla
    hafif_secilen = [e for e in secilen_efektler if efekt_ozellikleri[e]['yogunluk'] == 'hafif']
    orta_secilen = [e for e in secilen_efektler if efekt_ozellikleri[e]['yogunluk'] == 'orta']
    agir_secilen = [e for e in secilen_efektler if efekt_ozellikleri[e]['yogunluk'] == 'agir']

    print(f"\n   📊 Dağılım:")
    print(f"      • Hafif efektler: {len(hafif_secilen)}")
    print(f"      • Orta efektler: {len(orta_secilen)}")
    print(f"      • Ağır efektler: {len(agir_secilen)}")

    # Efekt isimlerini göster
    efekt_isimleri = {
        'velocity_ramp': '🚀 Velocity/Speed Ramping',
        'ghost_trail': '👻 Ghost Trail',
        'neon_glow': '💡 Neon Glow',
        'vhs_advanced': '📼 VHS Advanced',
        'datamosh': '💥 Datamosh',
        'posterize': '🎨 Posterize',
        'edge_detect': '🖼️ Edge Detection',
        'mirror_kaleidoscope': '🪞 Mirror/Kaleidoscope',
        'pixelate': '🔲 Pixelate',
        'solarize': '☀️ Solarize',
        'halftone': '🖨️ Halftone',
        'shake_advanced': '💥 Shake Advanced',
        'overlay_particles': '✨ Particles',
        'vignette_advanced': '🌑 Vignette Advanced',
        'camera_shake': '📹 Camera Shake',
        'vintage_styles': '🕰️ Vintage Styles',
        'chromatic_aberration': '🌈 Chromatic Aberration',
        'light_leaks': '💡 Light Leaks',
        'glitch': '⚡ Glitch',
        'motion_blur': '🌀 Motion Blur',
        'zoom_pulse': '🔍 Zoom Pulse',
        'lens_distortion': '🔭 Lens Distortion',
        'prism': '🌈 Prism',
        'color_grading': '🎨 Color Grading',
        'dream_glow': '✨ Dream Glow',
        'rgb_split_advanced': '🔴🟢🔵 RGB Split',
        'sharpen_boost': '🔪 Sharpen Boost',
    }

    print(f"\n   🎨 Seçilen efektler:")
    for efekt in sorted(secilen_efektler):
        isim = efekt_isimleri.get(efekt, efekt)
        yogunluk = efekt_ozellikleri[efekt]['yogunluk']
        yogunluk_emoji = {'hafif': '🟢', 'orta': '🟡', 'agir': '🔴'}[yogunluk]
        print(f"      {yogunluk_emoji} {isim}")

    print("\n" + "=" * 100)

    return secilen_efektler


def efekt_secim_menusu():
    """Kullanıcının hangi efektleri kullanmak istediğini seçmesini sağlar"""
    print("\n" + "=" * 100)
    print("🎨 CİNEMATİC EFEKT SEÇİM MENÜSÜ".center(100))
    print("=" * 100)

    # ===== 🆕 SEÇİM MODU =====
    print("\n🎯 Efekt Seçim Modu:")
    print("   1. 🧠 AKILLI SEÇİM (Önerilen) - Her video için 2-10 uyumlu efekt otomatik seçilir")
    print("   2. ✋ MANUEL SEÇİM - Efektleri kendiniz seçin")
    print("   3. 🎲 TÜM EFEKTLER - Tüm efektler rastgele kullanılır")
    print("\n" + "=" * 100)

    secim_modu = input("\n🎬 Seçim modu (1/2/3) [Enter=1]: ").strip()

    # AKILLI SEÇİM
    if secim_modu == "" or secim_modu == "1":
        return akilli_efekt_secimi()

    # TÜM EFEKTLER
    elif secim_modu == "3":
        print("\n   ✅ TÜM efektler kullanılacak (random)")
        return None

    # MANUEL SEÇİM (eski sistem)
    print("\n💡 Video boyunca kullanılacak efektleri seçin.")
    print("   • Hiç seçim yapmazsanız TÜM efektler random kullanılır")
    print("   • Sadece seçtikleriniz kullanılır (daha kontrollü)")
    print("\n" + "=" * 100)

    # Tüm efektleri kategorize et
    efekt_kategorileri = {
        "⭐ CAPCUT POPÜLER EFEKTLER": [
            ("velocity_ramp", "🚀 Velocity/Speed Ramping", "Hız değişimi (yavaşlatma/hızlandırma)"),
            ("ghost_trail", "👻 Ghost Trail", "Hayalet iz efekti"),
            ("neon_glow", "💡 Neon Glow", "Parlayan kenar efekti"),
            ("vhs_advanced", "📼 VHS Advanced", "Gelişmiş VHS efekti"),
            ("datamosh", "💥 Datamosh", "Dijital bozulma"),
            ("posterize", "🎨 Posterize", "Poster efekti"),
            ("edge_detect", "🖼️ Edge Detection", "Kenar tespiti"),
            ("mirror_kaleidoscope", "🪞 Mirror/Kaleidoscope", "Ayna/kaleydoskop"),
            ("pixelate", "🔲 Pixelate", "Pikselleştirme"),
            ("solarize", "☀️ Solarize", "Solarize efekti"),
            ("halftone", "🖨️ Halftone", "Yarım ton efekti"),
            ("shake_advanced", "💥 Shake Advanced", "Gelişmiş sallama"),
            ("overlay_particles", "✨ Particles", "Parçacık efekti"),
            ("vignette_advanced", "🌑 Vignette Advanced", "Gelişmiş vignette"),
        ],
        "📹 KLASİK EFEKTLER": [
            ("camera_shake", "📹 Camera Shake", "Kamera sallanması"),
            ("vintage_styles", "🕰️ Vintage (70s/80s/90s)", "Retro stil efektleri"),
            ("chromatic_aberration", "🌈 Chromatic Aberration", "Renk sapması"),
            ("light_leaks", "💡 Light Leaks", "Işık kaçakları"),
            ("glitch", "⚡ Glitch", "Dijital hata efekti"),
            ("motion_blur", "🌀 Motion Blur", "Hareket bulanıklığı"),
            ("zoom_pulse", "🔍 Zoom Pulse", "Zoom titreşimi"),
            ("lens_distortion", "🔭 Lens Distortion", "Lens bozulması"),
            ("prism", "🌈 Prism", "Prizma efekti"),
            ("color_grading", "🎨 Color Grading", "Renk düzeltme"),
            ("dream_glow", "✨ Dream Glow", "Rüya parıltısı"),
            ("rgb_split_advanced", "🔴🟢🔵 RGB Split", "RGB ayırma"),
            ("sharpen_boost", "🔪 Sharpen Boost", "Keskinlik artırma"),
        ]
    }

    secilen_efektler = set()

    print("\n🎯 Efekt Seçimi:")
    print("   • Tüm efektleri kullanmak için: Enter (boş bırakın)")
    print("   • Özel seçim için: Numaraları girin (virgülle ayırın, örn: 1,3,5,7)")
    print("\n")

    # Efektleri listele
    efekt_no = 1
    efekt_map = {}

    for kategori, efektler in efekt_kategorileri.items():
        print(f"\n{kategori}:")
        for efekt_key, efekt_adi, aciklama in efektler:
            print(f"   {efekt_no:2d}. {efekt_adi:30s} - {aciklama}")
            efekt_map[efekt_no] = efekt_key
            efekt_no += 1

    print("\n" + "=" * 100)
    secim = input("\n🎬 Seçiminiz (örn: 1,2,5,8 veya Enter=hepsi): ").strip()

    if not secim:
        print("\n   ✅ TÜM efektler kullanılacak (random)")
        return None  # None = tüm efektler kullanılacak

    try:
        secilenler = [int(x.strip()) for x in secim.split(',') if x.strip().isdigit()]

        for no in secilenler:
            if no in efekt_map:
                secilen_efektler.add(efekt_map[no])

        if secilen_efektler:
            print(f"\n   ✅ {len(secilen_efektler)} efekt seçildi:")
            for kategori, efektler in efekt_kategorileri.items():
                secili_bu_kategoride = [e for e in efektler if e[0] in secilen_efektler]
                if secili_bu_kategoride:
                    for efekt_key, efekt_adi, _ in secili_bu_kategoride:
                        print(f"      • {efekt_adi}")

            # ===== 🆕 YOUTUBE OPTİMİZASYONU: EFEKT DENGELEME =====
            if YOUTUBE_OPTIMIZATION_ENABLED and EFFECT_BALANCING.get('enabled', False):
                try:
                    logger.info("\n⚖️  Efekt dengelemesi uygulanıyor (YouTube algoritması için)...")
                    original_count = len(secilen_efektler)
                    secilen_efektler = set(apply_effect_balancing(list(secilen_efektler), EFFECT_BALANCING))
                    if len(secilen_efektler) != original_count:
                        print(f"\n   ⚖️  Efekt dengelemesi uygulandı: {original_count} → {len(secilen_efektler)} efekt")
                        print(f"      💡 YouTube algoritması için optimize edildi")
                except Exception as e:
                    logger.warning(f"⚠️  Efekt dengeleme hatası: {e}, devam ediliyor...")
            # ===== EFEKT DENGELEME BİTİŞ =====

            return secilen_efektler
        else:
            print("\n   ⚠️ Geçersiz seçim, tüm efektler kullanılacak")
            return None
    except:
        print("\n   ⚠️ Geçersiz format, tüm efektler kullanılacak")
        return None


# ==================== CINEMATIC EFFECT FILTERS ====================

def velocity_ramp_filtre_olustur(velocity_params):
    """🆕 Velocity/Speed Ramping - CapCut'ın EN POPÜLER efekti!"""
    if not velocity_params:
        return []

    filters = []
    ramp_type = random.choice(velocity_params.get('type', ['slow_to_fast', 'fast_to_slow']))
    speed_min, speed_max = velocity_params.get('speed_range', (0.5, 2.5))

    # ✅ FIX: Basit speed adjustment (gerçek ramping için karmaşık math gerekir)
    # setpts ile basit hız ayarı
    if ramp_type == 'slow_to_fast':
        # Yavaşlatma efekti
        filters.append(f"setpts={random.uniform(1.1, 1.3)}*PTS")
    elif ramp_type == 'fast_to_slow':
        # Hızlandırma efekti
        filters.append(f"setpts={random.uniform(0.7, 0.9)}*PTS")
    else:  # fast_slow_fast
        # Orta hız
        filters.append(f"setpts={random.uniform(0.9, 1.1)}*PTS")

    return filters


def ghost_trail_filtre_olustur(ghost_params):
    """🆕 Echo/Ghost Trail - Hayalet iz efekti"""
    if not ghost_params:
        return []

    filters = []
    trail_count = random.randint(*ghost_params.get('trail_count', (2, 5)))
    opacity = random.uniform(*ghost_params.get('opacity', (0.2, 0.5)))

    # ✅ FIX: tmix basit kullanımı (weights olmadan)
    # Sadece frame sayısı ile basit mixing
    frames = min(trail_count, 5)  # Max 5 frame
    filters.append(f"tmix=frames={frames}")

    return filters


def neon_glow_filtre_olustur(neon_params):
    """🆕 Neon Glow - Parlayan kenar efekti"""
    if not neon_params:
        return []

    filters = []
    intensity = random.uniform(*neon_params.get('intensity', (0.5, 1.5)))
    color = random.choice(neon_params.get('color', ['cyan', 'magenta', 'rainbow']))
    blur_radius = random.randint(*neon_params.get('blur_radius', (5, 15)))

    # Edge detection + glow
    filters.append("edgedetect=low=0.1:high=0.4")

    # Glow effect - sigma sınırlı (CPU yükünü azalt)
    sigma = min(round(blur_radius / 3, 2), 2.5)
    filters.append(f"gblur=sigma={sigma}")

    # Color tint based on selection
    if color == 'cyan':
        filters.append("colorchannelmixer=rr=0.5:gg=1.2:bb=1.5")
    elif color == 'magenta':
        filters.append("colorchannelmixer=rr=1.5:gg=0.5:bb=1.5")
    elif color == 'yellow':
        filters.append("colorchannelmixer=rr=1.5:gg=1.5:bb=0.5")
    elif color == 'green':
        filters.append("colorchannelmixer=rr=0.5:gg=1.5:bb=0.5")
    elif color == 'purple':
        filters.append("colorchannelmixer=rr=1.2:gg=0.5:bb=1.5")

    # Brightness boost
    filters.append(f"eq=brightness={intensity / 10}:contrast=1.2")

    return filters


def vhs_advanced_filtre_olustur(vhs_params):
    """🆕 VHS Advanced - Gelişmiş VHS/VCR efekti"""
    if not vhs_params:
        return []

    filters = []

    # Color bleeding
    bleeding = random.uniform(*vhs_params.get('color_bleeding', (0.2, 0.5)))
    filters.append(f"boxblur=lr={int(bleeding * 5)}:lp=1")

    # Tracking lines (interlacing)
    if vhs_params.get('tracking_lines', True):
        filters.append("il=l=d:c=d")

    # VHS noise - azaltıldı (CPU optimize)
    filters.append("noise=alls=8:allf=t")

    # ✅ FIX: Tape crease - drawbox random() kaldırıldı
    # Sabit pozisyonda horizontal line (her çalıştırmada farklı görünmek için Python random kullan)
    if vhs_params.get('tape_crease', True):
        # Python'da random y pozisyonu hesapla
        import random as py_random
        y_pos = py_random.randint(100, 900)  # 1080p için orta bölge
        filters.append(f"drawbox=y={y_pos}:color=black@0.3:width=iw:height=2:t=fill")

    # Slight color shift
    filters.append("eq=saturation=1.1:contrast=1.05")

    # VHS color grading
    filters.append("curves=vintage")

    return filters


def datamosh_filtre_olustur(datamosh_params):
    """🆕 Datamosh - Compression glitch"""
    if not datamosh_params:
        return []

    filters = []
    intensity = random.uniform(*datamosh_params.get('intensity', (0.3, 0.8)))
    block_size = random.randint(*datamosh_params.get('block_size', (8, 32)))

    # Blocky compression artifact simulation
    # Scale down then up for blocky effect
    # ✅ FIX: Çift sayı garantisi ekle
    scale_factor = max(8, block_size)
    filters.append(f"scale='trunc(iw/{scale_factor}/2)*2:trunc(ih/{scale_factor}/2)*2':flags=neighbor")
    filters.append(f"scale='trunc(iw*{scale_factor}/2)*2:trunc(ih*{scale_factor}/2)*2':flags=neighbor")

    # Add noise for compression artifacts
    noise_val = int(intensity * 20)
    filters.append(f"noise=alls={noise_val}:allf=t")

    # RGB shift for glitch
    shift = int(intensity * 5)
    filters.append(f"chromashift=crh={shift}:cbh={-shift}")

    return filters


def posterize_filtre_olustur(posterize_params):
    """🆕 Posterize - Renk paletini azalt"""
    if not posterize_params:
        return []

    filters = []
    levels = random.randint(*posterize_params.get('levels', (3, 8)))

    # ✅ FIX: Basit posterize - histeq yerine curves kullan
    # levels'a göre step hesapla (0-1 aralığında)
    # curves filtresi 0-1 aralığında koordinat bekliyor

    # Curves ile posterize efekti
    # Her renk kanalı için basamak oluştur (0.0-1.0 arası)
    points = []
    for i in range(levels + 1):
        val = round(min(i / levels, 1.0), 3)
        points.append(f"{val}/{val}")

    curve_str = ' '.join(points)
    filters.append(f"curves=all='{curve_str}'")

    return filters


def edge_detect_filtre_olustur(edge_params):
    """🆕 Edge Detection - Kenar algılama"""
    if not edge_params:
        return []

    filters = []

    # ✅ FIX: FFmpeg'in tüm versiyonlarında çalışan basit edge detection
    # mode parametresi bazı FFmpeg build'lerinde desteklenmiyor
    # Basit edgedetect kullan (default: canny benzeri)

    threshold_low, threshold_high = edge_params.get('threshold', (0.1, 0.4))

    # Basit edge detection (tüm FFmpeg versiyonlarında çalışır)
    filters.append(f"edgedetect=low={threshold_low}:high={threshold_high}")

    # Invert if specified
    if edge_params.get('invert', False):
        filters.append("negate")

    return filters


def mirror_kaleidoscope_filtre_olustur(mirror_params):
    """🆕 Mirror/Kaleidoscope - Ayna efekti"""
    if not mirror_params:
        return []

    filters = []
    mode = random.choice(mirror_params.get('mode', ['horizontal', 'vertical']))

    # ✅ FIX: Karmaşık filter graph yerine basit mirror efektleri
    # Complex split/merge filter graph'lar bazı durumlarda hata verebilir

    if mode == 'horizontal':
        # Basit yatay ayna - crop + flip + stack yerine sadece flip
        filters.append("hflip")
    elif mode == 'vertical':
        # Basit dikey ayna
        filters.append("vflip")
    elif mode == 'quad':
        # Hem yatay hem dikey flip (180 derece döndürme)
        filters.append("transpose=2")  # Rotate 180
    # Kaleidoscope modunu devre dışı bırakıyoruz (çok karmaşık)

    return filters


def pixelate_filtre_olustur(pixelate_params):
    """🆕 Pixelate/Mosaic - Piksel efekti"""
    if not pixelate_params:
        return []

    filters = []
    block_size = random.randint(*pixelate_params.get('block_size', (8, 32)))

    # ✅ FIX: Çift sayı garantisi - FFmpeg bazı filtrelerde çift boyut ister
    # Pixelate: scale down then up - çift sayı kontrolü ile
    filters.append(f"scale='trunc(iw/{block_size}/2)*2:trunc(ih/{block_size}/2)*2':flags=neighbor")
    filters.append(f"scale='trunc(iw*{block_size}/2)*2:trunc(ih*{block_size}/2)*2':flags=neighbor")

    return filters


def solarize_filtre_olustur(solarize_params):
    """🆕 Solarize - Renk inversiyonu"""
    if not solarize_params:
        return []

    filters = []
    threshold = random.uniform(*solarize_params.get('threshold', (0.3, 0.7)))

    # Solarize effect using curves (0-1 aralığında)
    # curves filtresi 0.0-1.0 koordinat bekliyor
    threshold_norm = round(threshold, 3)
    filters.append(f"curves=all='0/0 {threshold_norm}/{threshold_norm} 1/0'")

    return filters


def halftone_filtre_olustur(halftone_params):
    """🆕 Halftone - Retro print efekti"""
    if not halftone_params:
        return []

    filters = []
    dot_size = random.randint(*halftone_params.get('dot_size', (2, 6)))

    # Basit halftone simülasyonu
    # 1. Brightness artır, kontrast azalt
    filters.append("eq=brightness=0.05:contrast=1.3")

    # 2. Pixelate effect
    # ✅ FIX: Çift sayı garantisi ekle
    filters.append(f"scale='trunc(iw/{dot_size}/2)*2:trunc(ih/{dot_size}/2)*2'")
    filters.append(f"scale='trunc(iw*{dot_size}/2)*2:trunc(ih*{dot_size}/2)*2':flags=neighbor")

    # 3. Threshold for dots
    filters.append("eq=gamma=1.5")

    return filters


def shake_advanced_filtre_olustur(shake_params):
    """🆕 Shake Advanced - Daha güçlü sallama"""
    if not shake_params:
        return []

    filters = []
    shake_type = random.choice(shake_params.get('type', ['earthquake', 'handheld']))
    intensity = random.uniform(*shake_params.get('intensity', (0.5, 1.5)))
    frequency = random.randint(*shake_params.get('frequency', (5, 20)))

    shake_amount = int(intensity * 20)  # Orta seviye sallama

    # ✅ FIX: FFmpeg'de random() fonksiyonu yok
    # Sabit sin/cos pattern kullan
    if shake_type == 'earthquake':
        # Güçlü, düzensiz sallama - daha yüksek amplitude
        # ✅ FIX: Crop boyutları çift sayı olmalı
        crop_w = f"2*trunc((iw-{shake_amount * 2})/2)"
        crop_h = f"2*trunc((ih-{shake_amount * 2})/2)"
        filters.append(
            f"crop={crop_w}:{crop_h}:"
            f"{shake_amount}+{shake_amount}*sin(n/{frequency}):"
            f"{shake_amount}+{shake_amount}*cos(n/{frequency * 1.3})"
        )
    elif shake_type == 'handheld':
        # Yumuşak, organik sallama
        # ✅ FIX: Crop boyutları çift sayı olmalı
        crop_w = f"2*trunc((iw-{shake_amount * 2})/2)"
        crop_h = f"2*trunc((ih-{shake_amount * 2})/2)"
        filters.append(
            f"crop={crop_w}:{crop_h}:"
            f"{shake_amount}+{shake_amount}*sin(n/{frequency}):"
            f"{shake_amount}+{shake_amount}*cos(n/{frequency})"
        )
    elif shake_type == 'explosion':
        # Ani, şiddetli sallama
        # ✅ FIX: Crop boyutları çift sayı olmalı
        crop_w = f"2*trunc((iw-{shake_amount * 3})/2)"
        crop_h = f"2*trunc((ih-{shake_amount * 3})/2)"
        filters.append(
            f"crop={crop_w}:{crop_h}:"
            f"{shake_amount}+{shake_amount}*sin(n*{frequency / 10}):"
            f"{shake_amount}+{shake_amount}*cos(n*{frequency / 10})"
        )
    else:  # impact
        # Basit sallama
        # ✅ FIX: Crop boyutları çift sayı olmalı
        crop_w = f"2*trunc((iw-{shake_amount * 2})/2)"
        crop_h = f"2*trunc((ih-{shake_amount * 2})/2)"
        filters.append(
            f"crop={crop_w}:{crop_h}:"
            f"{shake_amount}:"
            f"{shake_amount}"
        )

    return filters


def overlay_particles_filtre_olustur(overlay_params):
    """🆕 Overlay Particles - Işık parçacıkları"""
    if not overlay_params:
        return []

    filters = []
    particle_type = random.choice(overlay_params.get('type', ['dust', 'bokeh']))
    density = random.uniform(*overlay_params.get('density', (0.2, 0.6)))

    # Basit particle simülasyonu - noise kullanarak
    if particle_type in ['dust', 'sparkles']:
        # Küçük parçacıklar
        noise_strength = int(density * 20)
        filters.append(f"noise=alls={noise_strength}:allf=t")
        filters.append("eq=brightness=0.1:contrast=1.5")
    elif particle_type == 'bokeh':
        # Büyük, yumuşak parçacıklar - sigma optimize
        filters.append(f"noise=alls=5:allf=t")
        filters.append("gblur=sigma=2")
        filters.append(f"eq=brightness={density / 5}:contrast=0.8")

    return filters


def vignette_advanced_filtre_olustur(vignette_params):
    """🆕 Vignette Advanced - Güçlü vignette"""
    if not vignette_params:
        return []

    filters = []
    intensity = random.uniform(*vignette_params.get('intensity', (0.3, 0.8)))
    shape = random.choice(vignette_params.get('shape', ['circle', 'ellipse']))

    # Vignette with adjustable intensity
    angle = round(intensity * 1.5, 2)  # PI/6 to PI/2 range
    filters.append(f"vignette=angle=PI/{angle}")

    return filters


def glitch_filtre_olustur(glitch_params):
    """🆕 Glitch efekti - CapCut style digital glitch"""
    if not glitch_params:
        return []

    filters = []
    intensity = glitch_params['intensity']

    # Digital noise
    noise_range = glitch_params.get('noise', (5, 15))
    noise_val = int(random.uniform(*noise_range))
    if noise_val > 5:
        filters.append(f"noise=alls={noise_val}:allf=t")

    # RGB split (glitch effect)
    if glitch_params.get('rgb_split', True):
        shift = int(intensity * 8)
        filters.append(f"chromashift=crh={shift}:cbh={-shift}")

    # Scan lines effect
    if glitch_params.get('scan_lines', True):
        filters.append("il=l=d:c=d")

    # Contrast boost
    contrast_boost = 1.0 + (intensity * 0.2)
    filters.append(f"eq=contrast={contrast_boost}:saturation={1.1}")

    return filters


def motion_blur_filtre_olustur(blur_params):
    """🆕 Motion blur efekti - Sinematik hareket bulanıklığı"""
    if not blur_params:
        return []

    filters = []
    intensity = blur_params['intensity']

    blend_frames = max(2, min(6, int(2 + (intensity * 4))))

    # tmix ile motion blur simülasyonu
    filters.append(f"tmix=frames={blend_frames}")

    return filters


def zoom_pulse_filtre_olustur(zoom_params):
    """🆕 Zoom pulse efekti - Basit zoom in/out"""
    if not zoom_params:
        return []

    filters = []
    zoom_type = random.choice(zoom_params.get('type', ['in', 'out', 'pulse']))
    intensity = random.uniform(*zoom_params.get('intensity', (1.05, 1.15)))

    if zoom_type in ['in', 'pulse']:
        zoom_val = intensity
        # ✅ FIX: Çift sayı garantisi ekle
        filters.append(f"scale='trunc(iw*{zoom_val}/2)*2:trunc(ih*{zoom_val}/2)*2':flags=lanczos")
        filters.append(f"crop='trunc(iw/{zoom_val}/2)*2:trunc(ih/{zoom_val}/2)*2'")
    elif zoom_type == 'out':
        zoom_val = 1.0 / intensity
        # ✅ FIX: Çift sayı garantisi ekle
        filters.append(f"scale='trunc(iw*{zoom_val}/2)*2:trunc(ih*{zoom_val}/2)*2':flags=lanczos")

    return filters


def lens_distortion_filtre_olustur(dist_params):
    """🆕 Lens distortion - Balık gözü/barrel efekti"""
    if not dist_params:
        return []

    filters = []
    dist_type = random.choice(dist_params.get('type', ['barrel', 'pincushion']))
    strength = random.uniform(*dist_params.get('strength', (0.1, 0.3)))

    k1 = strength if dist_type == 'barrel' else -strength

    filters.append(f"lenscorrection=k1={k1}:k2=0")

    return filters


def prism_filtre_olustur(prism_params):
    """🆕 Prism efekti - Renk prizma"""
    if not prism_params:
        return []

    filters = []
    intensity = random.uniform(*prism_params.get('intensity', (0.2, 0.5)))

    shift = int(intensity * 10)
    filters.append(f"chromashift=crh={shift}:cbh={-shift}")

    # Hue rotation ile renk spektrumu
    hue_shift = int(intensity * 30)
    filters.append(f"hue=h={hue_shift}")

    # Saturation boost
    filters.append(f"eq=saturation={1.0 + intensity * 0.5}")

    return filters


def color_grading_filtre_olustur(grading_params):
    """🆕 Advanced color grading - CapCut presets"""
    if not grading_params:
        return []

    filters = []
    preset_type = grading_params['type']
    params = grading_params['params']

    if preset_type == 'cyberpunk':
        neon_boost = params.get('neon_boost', 25)
        contrast = params.get('contrast', 20)

        filters.append("curves=r='0/0 0.5/0.4 1/1':g='0/0 0.5/0.55 1/0.9':b='0/0.1 0.5/0.6 1/0.7'")
        filters.append(f"eq=contrast={1.0 + contrast / 100}:saturation=1.{neon_boost}")
        filters.append("unsharp=3:3:0.8:3:3:0")

    elif preset_type == 'moody':
        shadows = params.get('shadows', -15)
        saturation = params.get('saturation', -20)
        blue_tint = params.get('blue_tint', 10)

        filters.append(f"eq=brightness={shadows / 200}:saturation={1.0 + saturation / 100}")
        filters.append(f"colorchannelmixer=rr=0.95:gg=0.95:bb=1.{blue_tint}")
        filters.append("vignette=PI/5")

    elif preset_type == 'golden_hour':
        warm_boost = params.get('warm_boost', 20)
        saturation = params.get('saturation', 10)

        filters.append(f"eq=brightness={warm_boost / 400}:saturation={1.0 + saturation / 100}")
        filters.append("colorchannelmixer=rr=1.15:rg=0.1:gg=1.05:gb=-0.05:bb=0.85")
        filters.append("unsharp=5:5:-0.3:5:5:0")

        if params.get('soft_light', True):
            filters.append("gblur=sigma=2")

    elif preset_type == 'cinematic_teal':
        contrast = params.get('contrast', 15)

        if params.get('teal_shadows', True) and params.get('orange_highlights', True):
            filters.append("curves=r='0/0 0.5/0.45 1/1':g='0/0.05 0.5/0.5 1/0.95':b='0/0.15 0.5/0.55 1/0.8'")

        filters.append(f"eq=contrast={1.0 + contrast / 100}")

    elif preset_type == 'bleach_bypass':
        saturation = params.get('saturation', -30)
        contrast = params.get('contrast', 25)
        sharpness = params.get('sharpness', 0.8)

        filters.append(f"eq=saturation={1.0 + saturation / 100}:contrast={1.0 + contrast / 100}")
        filters.append(f"unsharp=3:3:{sharpness}:3:3:0")
        filters.append("noise=alls=5:allf=t")

    return filters


def dream_glow_filtre_olustur(glow_params):
    """🆕 Dream glow - Dreamy ethereal glow"""
    if not glow_params:
        return []

    filters = []
    intensity = random.uniform(*glow_params.get('intensity', (0.3, 0.6)))

    # Sigma sınırlı - CPU optimize
    sigma = min(round(intensity * 5, 2), 2.5)
    filters.append(f"gblur=sigma={sigma}")

    if glow_params.get('soft_light', True):
        brightness_boost = round(intensity / 10, 3)
        filters.append(f"eq=brightness={brightness_boost}:contrast=0.95")

    sat_boost = round(1.0 + intensity * 0.3, 2)
    filters.append(f"eq=saturation={sat_boost}")

    return filters


def rgb_split_advanced_filtre_olustur(split_params):
    """🆕 RGB Split Advanced - Gelişmiş RGB channel separation"""
    if not split_params:
        return []

    filters = []
    offset_x = random.randint(*split_params.get('offset_x', (2, 6)))
    offset_y = random.randint(*split_params.get('offset_y', (1, 3)))

    if split_params.get('diagonal', True):
        filters.append(f"chromashift=crh={offset_x}:cbh={-offset_x}:crv={offset_y}:cbv={-offset_y}")
    else:
        filters.append(f"chromashift=crh={offset_x}:cbh={-offset_x}")

    filters.append("eq=contrast=1.05")

    return filters


def sharpen_boost_filtre_olustur(sharpen_params):
    """🆕 Sharpen Boost - Ultra keskinlik (CapCut sharpness)"""
    if not sharpen_params:
        return []

    filters = []
    intensity = random.uniform(*sharpen_params.get('intensity', (0.6, 1.2)))

    # radius=7 çok yavaş, 3-5 ile sınırlandı
    odd_radii = [3, 5]
    radius = random.choice(odd_radii)

    filters.append(f"unsharp={radius}:{radius}:{intensity}:{radius}:{radius}:0")
    filters.append("eq=contrast=1.08")

    return filters


# ==================== 🆕 YENİ CAPCUT POPÜLER EFEKTLER ====================

def auto_velocity_filtre_olustur(velocity_params):
    """🆕 Auto Velocity - CapCut otomatik hız değişimi"""
    if not velocity_params:
        return []

    # Not: Velocity gerçek zamanlı speed değişimi gerektirir
    # FFmpeg'de setpts ile simüle edilebilir ama karmaşık
    # Şimdilik basit speed variation kullanıyoruz
    filters = []

    patterns = velocity_params.get('patterns', {})
    pattern_names = list(patterns.keys())
    weights = [patterns[p]['weight'] for p in pattern_names]

    chosen_pattern = random.choices(pattern_names, weights=weights, k=1)[0]

    if chosen_pattern == 'speed_ramp':
        # Hafif hız değişimi (setpts ile)
        params = patterns['speed_ramp']
        mid_speed = random.uniform(*params['peak_speed'])
        # Ortalama hız artışı
        filters.append(f"setpts={1 / mid_speed}*PTS")

    return filters


def flash_effect_filtre_olustur(flash_params):
    """🆕 Flash/Strobe - Parlama efekti"""
    if not flash_params:
        return []

    filters = []

    types = flash_params.get('types', {})
    type_names = list(types.keys())
    weights = [types[t]['weight'] for t in type_names]

    chosen_type = random.choices(type_names, weights=weights, k=1)[0]

    if chosen_type == 'white_flash':
        # Beyaz flaş efekti - parlama artışı
        params = types['white_flash']
        intensity = random.uniform(*params['intensity'])
        filters.append(f"eq=brightness={intensity}")

    elif chosen_type == 'color_flash':
        # Renkli flaş
        params = types['color_flash']
        color = random.choice(params['colors'])

        if color == 'red':
            filters.append("colorchannelmixer=rr=1.5:gg=0.5:bb=0.5")
        elif color == 'blue':
            filters.append("colorchannelmixer=rr=0.5:gg=0.5:bb=1.5")
        elif color == 'purple':
            filters.append("colorchannelmixer=rr=1.3:gg=0.5:bb=1.3")
        elif color == 'cyan':
            filters.append("colorchannelmixer=rr=0.5:gg=1.3:bb=1.3")

    return filters


def tilt_3d_filtre_olustur(tilt_params):
    """🆕 3D Perspective/Tilt - 3D derinlik efekti"""
    if not tilt_params:
        return []

    filters = []
    axis = random.choice(tilt_params.get('axis', ['x', 'y', 'both']))
    angle = random.uniform(*tilt_params.get('angle', (2, 8)))

    # Perspective transformation
    if axis == 'x':
        filters.append(
            f"perspective=x0=0:y0={angle * 2}:x1=W:y1={angle * 2}:x2=0:y2=H-{angle * 2}:x3=W:y3=H-{angle * 2}")
    elif axis == 'y':
        filters.append(
            f"perspective=x0={angle * 2}:y0=0:x1=W-{angle * 2}:y1=0:x2={angle * 2}:y2=H:x3=W-{angle * 2}:y3=H")

    # Zoom compensation
    if tilt_params.get('zoom_compensation', True):
        # ✅ FIX: Çift sayı garantisi ekle
        filters.append("scale='trunc(iw*1.05/2)*2:trunc(ih*1.05/2)*2'")

    return filters


def echo_trail_filtre_olustur(echo_params):
    """🆕 Echo/Ghost Trail - Hayalet iz efekti"""
    if not echo_params:
        return []

    filters = []

    # FFmpeg'de echo efekti - tmix veya blend ile
    trail_count = random.randint(*echo_params.get('trail_count', (2, 4)))

    # Basit echo - frame blending
    filters.append(f"tmix=frames={trail_count * 2}")

    return filters


def glow_bloom_filtre_olustur(glow_params):
    """🆕 Glow/Bloom - Profesyonel parlama"""
    if not glow_params:
        return []

    filters = []

    types = glow_params.get('types', {})
    type_names = list(types.keys())
    weights = [types[t]['weight'] for t in type_names]

    chosen_type = random.choices(type_names, weights=weights, k=1)[0]

    if chosen_type == 'soft_glow':
        params = types['soft_glow']
        intensity = random.uniform(*params['intensity'])
        radius = random.randint(*params['radius'])

        # Soft glow - gblur + blend (sigma sınırlı)
        sigma = min(round(radius / 5, 2), 2.5)
        filters.append(f"gblur=sigma={sigma}")
        filters.append(f"eq=brightness={intensity / 2}")

    elif chosen_type == 'bloom':
        params = types['bloom']
        intensity = random.uniform(*params['intensity'])

        # Bloom efekti - parlak alanları vurgula
        filters.append(f"eq=brightness={intensity}:saturation=1.2")

    elif chosen_type == 'edge_glow':
        params = types['edge_glow']
        color = random.choice(params['color'])

        # Edge glow - kenar parlama (kernel optimize)
        filters.append("unsharp=3:3:1.2:3:3:0")

        if color == 'blue':
            filters.append("colorchannelmixer=bb=1.3")
        elif color == 'purple':
            filters.append("colorchannelmixer=rr=1.2:bb=1.3")

    return filters


def edge_detection_filtre_olustur(edge_params):
    """🆕 Edge Detection/Outline - Kenar tespiti"""
    if not edge_params:
        return []

    filters = []

    types = edge_params.get('types', {})
    type_names = list(types.keys())
    weights = [types[t]['weight'] for t in type_names]

    chosen_type = random.choices(type_names, weights=weights, k=1)[0]

    if chosen_type == 'cartoon_outline':
        params = types['cartoon_outline']
        thickness = random.randint(*params['thickness'])

        # Cartoon outline - edge detection
        filters.append("edgedetect=mode=canny:low=0.1:high=0.4")

    elif chosen_type == 'neon_edges':
        params = types['neon_edges']
        color = random.choice(params['color'])

        # Neon kenarlar
        filters.append("edgedetect=mode=canny")

        if color == 'cyan':
            filters.append("colorchannelmixer=gg=1.5:bb=1.5")
        elif color == 'magenta':
            filters.append("colorchannelmixer=rr=1.5:bb=1.5")

    elif chosen_type == 'sketch':
        params = types['sketch']
        intensity = random.uniform(*params['intensity'])

        # Sketch efekti
        filters.append("edgedetect=mode=wires")
        filters.append(f"eq=contrast={1 + intensity}")

    return filters


def parallax_offset_filtre_olustur(parallax_params):
    """🆕 Offset/Parallax - Katman kaydırma"""
    if not parallax_params:
        return []

    filters = []
    direction = random.choice(parallax_params.get('direction', ['horizontal', 'vertical']))
    offset = random.randint(*parallax_params.get('offset', (5, 20)))

    # Basit parallax - crop ve overlay
    # ✅ FIX: Crop boyutları çift sayı olmalı
    if direction == 'horizontal':
        crop_w = f"2*trunc((iw-{offset * 2})/2)"
        filters.append(f"crop={crop_w}:ih:{offset}:0")
    elif direction == 'vertical':
        crop_h = f"2*trunc((ih-{offset * 2})/2)"
        filters.append(f"crop=iw:{crop_h}:0:{offset}")

    return filters


def kaleidoscope_filtre_olustur(kaleid_params):
    """🆕 Kaleidoscope - Kaleydoskop efekti"""
    if not kaleid_params:
        return []

    filters = []
    segments = random.randint(*kaleid_params.get('segments', (4, 8)))

    # FFmpeg'de tile filter ile kaleydoskop simülasyonu
    # Basit versiyon - symmetry
    filters.append("format=yuv420p,split[main][ref];[ref]hflip[flipped];[main][flipped]hstack")

    return filters


def mirror_symmetry_filtre_olustur(mirror_params):
    """🆕 Mirror/Symmetry - Ayna efekti"""
    if not mirror_params:
        return []

    filters = []
    axis = random.choice(mirror_params.get('axis', ['vertical', 'horizontal']))

    if axis == 'vertical':
        # Dikey ayna - sol yarı = sağ yarı
        filters.append("crop=iw/2:ih:0:0,split[left][right];[right]hflip[flipped];[left][flipped]hstack")
    elif axis == 'horizontal':
        # Yatay ayna - üst yarı = alt yarı
        filters.append("crop=iw:ih/2:0:0,split[top][bottom];[bottom]vflip[flipped];[top][flipped]vstack")

    return filters


def posterize_cartoon_filtre_olustur(poster_params):
    """🆕 Posterize/Cartoon - Karikatür efekti"""
    if not poster_params:
        return []

    filters = []

    types = poster_params.get('types', {})
    type_names = list(types.keys())
    weights = [types[t]['weight'] for t in type_names]

    chosen_type = random.choices(type_names, weights=weights, k=1)[0]

    if chosen_type == 'posterize':
        params = types['posterize']
        levels = random.randint(*params['levels'])

        # Posterize efekti - renk azaltma
        filters.append(f"eq=saturation=1.2")
        filters.append("curves=preset=strong_contrast")

    elif chosen_type == 'cartoon':
        params = types['cartoon']
        edge_thickness = random.randint(*params['edge_thickness'])

        # Cartoon efekti - kenar + renk azaltma
        filters.append("edgedetect=mode=canny")
        filters.append("eq=contrast=1.3")

    elif chosen_type == 'cel_shading':
        # Cel shading - anime tarzı
        filters.append("eq=contrast=1.4:saturation=1.3")

    return filters


def speed_ripple_filtre_olustur(ripple_params):
    """🆕 Speed Ripple - Hız dalgalanması"""
    if not ripple_params:
        return []

    filters = []

    # Speed ripple - hafif hız dalgalanması
    base_speed = random.uniform(*ripple_params.get('base_speed', (0.9, 1.1)))

    filters.append(f"setpts={1 / base_speed}*PTS")

    return filters


def time_displacement_filtre_olustur(time_params):
    """🆕 Time Displacement - Zaman kaydırma"""
    if not time_params:
        return []

    filters = []

    # Time displacement - frame offset
    # FFmpeg'de tblend veya tmix ile
    filters.append("tblend=all_mode=average")

    return filters


# ==================== VINTAGE/RETRO FILTERS ====================

def camera_shake_filtre_olustur(shake_params):
    """Kamera sallama filtresi - CapCut tarzı"""
    if not shake_params:
        return []

    intensity = shake_params['intensity']
    frequency = shake_params['frequency']

    filters = []

    shake_amount = int(intensity * 20)

    # ✅ FIX: Crop boyutları çift sayı olmalı
    crop_w = f"2*trunc((iw-{shake_amount * 2})/2)"
    crop_h = f"2*trunc((ih-{shake_amount * 2})/2)"

    shake_filter = (
        f"crop={crop_w}:{crop_h}:"
        f"{shake_amount}+{shake_amount}*sin(n/{frequency}):"
        f"{shake_amount}+{shake_amount}*cos(n/{frequency})"
    )

    filters.append(shake_filter)

    return filters


def vintage_70s_filtre_olustur(params):
    """70s vintage efekti - Warm tones, grain, soft focus"""
    filters = []

    warm = params.get('warm_tone', 15)
    filters.append(f"eq=brightness={warm / 200}:saturation={1 - params.get('saturation', -10) / 100}")

    soft_focus = params.get('soft_focus', 0.4)
    filters.append(f"unsharp=3:3:-{soft_focus}:3:3:0")

    grain = params.get('grain', 8)
    filters.append(f"noise=alls={grain}:allf=t+u")

    if params.get('vignette', True):
        filters.append("vignette=PI/4")

    filters.append("colorchannelmixer=rr=1.0:rg=0.1:rb=0.0:gr=0.3:gg=0.9:gb=0.0:br=0.0:bg=0.1:bb=0.8")

    return filters


def vintage_80s_filtre_olustur(params):
    """80s retro efekti - VHS, neon, scan lines"""
    filters = []

    sat = params.get('saturation', 20)
    cont = params.get('contrast', 15)
    filters.append(f"eq=saturation={1 + sat / 100}:contrast={1 + cont / 100}")

    if params.get('scan_lines', True):
        filters.append("il=l=d:c=d")

    vhs_noise = params.get('vhs_noise', 8)
    filters.append(f"noise=alls={vhs_noise}:allf=t")

    if params.get('color_bleed', 0.3) > 0:
        filters.append("boxblur=lr=1:lp=1")

    if params.get('neon_glow', True):
        filters.append("unsharp=3:3:1.2:3:3:0")

    filters.append("curves=vintage")

    return filters


def vintage_90s_filtre_olustur(params):
    """90s camcorder efekti - Home video look"""
    filters = []

    oversat = params.get('slight_oversaturate', 12)
    filters.append(f"eq=saturation={1 + oversat / 100}")

    sharp = params.get('sharpness', 0.6)
    filters.append(f"unsharp=3:3:{sharp}:3:3:0")

    grain = params.get('grain', 5)
    filters.append(f"noise=alls={grain}:allf=t")

    if params.get('camcorder_look', True):
        filters.append("colorchannelmixer=rr=1.1:gg=1.05:bb=0.95")

    if params.get('date_stamp', False):
        fake_date = "1996-08-15"
        filters.append(
            f"drawtext=text='{fake_date}':fontcolor=yellow:fontsize=24:"
            f"x=w-tw-10:y=h-th-10:fontfile=/Windows/Fonts/arial.ttf"
        )

    return filters


def film_grain_filtre_olustur(params):
    """Analog film grain efekti"""
    filters = []

    grain_min, grain_max = params.get('grain_strength', (8, 15))
    grain = random.randint(grain_min, grain_max)

    filters.append(f"noise=alls={grain}:allf=t+u")

    if params.get('keep_colors', True):
        filters.append("eq=gamma=1.0")

    return filters


def chromatic_aberration_filtre_olustur(aberration_params):
    """Chromatic aberration efekti - Lens bozulması"""
    if not aberration_params:
        return []

    shift = aberration_params['shift']

    filter_str = (
        f"split=3[r][g][b];"
        f"[r]lutrgb=r=val:g=0:b=0,pad=iw+{shift}:ih:0:0[r];"
        f"[g]lutrgb=r=0:g=val:b=0[g];"
        f"[b]lutrgb=r=0:g=0:b=val,pad=iw+{shift}:ih:{shift}:0[b];"
        f"[r][g]blend=all_mode=addition[rg];"
        f"[rg][b]blend=all_mode=addition,crop=iw-{shift}:ih"
    )

    return [filter_str]


def light_leak_filtre_olustur(leak_params):
    """Light leak efekti - Işık sızıntıları"""
    if not leak_params:
        return []

    intensity = leak_params['intensity']
    color = leak_params['color']

    filters = []

    if color == 'warm':
        color_values = "1.2:1.0:0.8"
    elif color == 'cool':
        color_values = "0.8:0.9:1.2"
    else:
        color_values = "1.1:1.0:1.1"

    leak_filter = (
        f"curves=all='0/0 0.5/{intensity} 1/1',"
        f"colorchannelmixer=rr={color_values.split(':')[0]}:"
        f"gg={color_values.split(':')[1]}:"
        f"bb={color_values.split(':')[2]}"
    )

    filters.append(leak_filter)

    return filters


# ==================== CINEMATIC EFFECTS GENERATOR ====================

def cinematic_effects_uret(klip_index, secilen_efektler=None):
    """🆕 Her klip için cinematic efekt parametreleri oluştur - CapCut Ultra (30+ efekt!)

    Args:
        klip_index: Klip numarası
        secilen_efektler: Kullanıcının seçtiği efektler (set) veya None (tüm efektler)
    """
    random.seed(hash(f"cinematic_{klip_index}_{time.time()}"))

    effects = {
        # 🎥 SUBTITLE-FRIENDLY EFFECTS (Story Channels Optimized)
        'ken_burns': None,
        'gradient_overlay': None,
        'soft_focus_background': None,

        # 🔥 VIRAL EFFECTS (Phase 1 - TikTok/CapCut/Reels)
        'beat_drop_shake': None,
        'beat_drop_zoom': None,
        'beat_drop_flash': None,
        'freeze_frame': None,
        'elastic_bounce': None,
        'wiggle_shake': None,
        'jello_effect': None,

        # Yeni efektler
        'velocity_ramp': None,
        'ghost_trail': None,
        'neon_glow': None,
        'vhs_advanced': None,
        'datamosh': None,
        'posterize': None,
        'edge_detect': None,
        'mirror_kaleidoscope': None,
        'pixelate': None,
        'solarize': None,
        'halftone': None,
        'shake_advanced': None,
        'overlay_particles': None,
        'vignette_advanced': None,

        # Eski efektler
        'camera_shake': None,
        'vintage_style': None,
        'chromatic_aberration': None,
        'light_leak': None,
        'glitch': None,
        'motion_blur': None,
        'zoom_pulse': None,
        'lens_distortion': None,
        'prism': None,
        'color_grading': None,
        'dream_glow': None,
        'rgb_split_advanced': None,
        'sharpen_boost': None,
    }

    cfg = CINEMATIC_EFFECTS

    # 🆕 Efekt kontrolü: Eğer secilen_efektler varsa, sadece o efektleri uygula
    def efekt_kullanilsin_mi(efekt_adi):
        """Efektin kullanılıp kullanılmayacağını kontrol et"""
        if secilen_efektler is None:
            # Hiçbir seçim yapılmamış, tüm efektler kullanılabilir
            return True
        else:
            # Sadece seçilen efektler kullanılabilir
            return efekt_adi in secilen_efektler

    # 🆕 Velocity/Speed Ramping
    if efekt_kullanilsin_mi('velocity_ramp') and cfg.get('velocity_ramp', {}).get('enabled',
                                                                                  False) and random.random() < cfg[
        'velocity_ramp'].get('olasilik', 0):
        effects['velocity_ramp'] = {
            'type': cfg['velocity_ramp']['type'],
            'speed_range': cfg['velocity_ramp']['speed_range'],
            'transition_duration': cfg['velocity_ramp']['transition_duration'],
        }

    # 🆕 Ghost Trail
    if efekt_kullanilsin_mi('ghost_trail') and cfg.get('ghost_trail', {}).get('enabled', False) and random.random() < \
            cfg['ghost_trail'].get('olasilik', 0):
        effects['ghost_trail'] = {
            'trail_count': cfg['ghost_trail']['trail_count'],
            'opacity': cfg['ghost_trail']['opacity'],
            'offset': cfg['ghost_trail']['offset'],
        }

    # 🆕 Neon Glow
    if efekt_kullanilsin_mi('neon_glow') and cfg.get('neon_glow', {}).get('enabled', False) and random.random() < cfg[
        'neon_glow'].get('olasilik', 0):
        effects['neon_glow'] = {
            'intensity': cfg['neon_glow']['intensity'],
            'color': cfg['neon_glow']['color'],
            'blur_radius': cfg['neon_glow']['blur_radius'],
        }

    # 🆕 VHS Advanced
    if efekt_kullanilsin_mi('vhs_advanced') and cfg.get('vhs_advanced', {}).get('enabled', False) and random.random() < \
            cfg['vhs_advanced'].get('olasilik', 0):
        effects['vhs_advanced'] = cfg['vhs_advanced'].copy()

    # 🆕 Datamosh
    if efekt_kullanilsin_mi('datamosh') and cfg.get('datamosh', {}).get('enabled', False) and random.random() < cfg[
        'datamosh'].get('olasilik', 0):
        effects['datamosh'] = {
            'intensity': cfg['datamosh']['intensity'],
            'block_size': cfg['datamosh']['block_size'],
            'direction': cfg['datamosh']['direction'],
        }

    # 🆕 Posterize
    if efekt_kullanilsin_mi('posterize') and cfg.get('posterize', {}).get('enabled', False) and random.random() < cfg[
        'posterize'].get('olasilik', 0):
        effects['posterize'] = {
            'levels': cfg['posterize']['levels'],
            'dithering': cfg['posterize']['dithering'],
        }

    # 🆕 Edge Detection
    if efekt_kullanilsin_mi('edge_detect') and cfg.get('edge_detect', {}).get('enabled', False) and random.random() < \
            cfg['edge_detect'].get('olasilik', 0):
        effects['edge_detect'] = {
            'threshold': cfg['edge_detect']['threshold'],
            'invert': cfg['edge_detect']['invert'],
        }

    # 🆕 Mirror/Kaleidoscope
    if efekt_kullanilsin_mi('mirror_kaleidoscope') and cfg.get('mirror_kaleidoscope', {}).get('enabled',
                                                                                              False) and random.random() < \
            cfg['mirror_kaleidoscope'].get(
                'olasilik', 0):
        effects['mirror_kaleidoscope'] = {
            'mode': cfg['mirror_kaleidoscope']['mode'],
            'segments': cfg['mirror_kaleidoscope']['segments'],
        }

    # 🆕 Pixelate
    if efekt_kullanilsin_mi('pixelate') and cfg.get('pixelate', {}).get('enabled', False) and random.random() < cfg[
        'pixelate'].get('olasilik', 0):
        effects['pixelate'] = {
            'block_size': cfg['pixelate']['block_size'],
            'animated': cfg['pixelate']['animated'],
        }

    # 🆕 Solarize
    if efekt_kullanilsin_mi('solarize') and cfg.get('solarize', {}).get('enabled', False) and random.random() < cfg[
        'solarize'].get('olasilik', 0):
        effects['solarize'] = {
            'threshold': cfg['solarize']['threshold'],
        }

    # 🆕 Halftone
    if efekt_kullanilsin_mi('halftone') and cfg.get('halftone', {}).get('enabled', False) and random.random() < cfg[
        'halftone'].get('olasilik', 0):
        effects['halftone'] = {
            'dot_size': cfg['halftone']['dot_size'],
            'pattern': cfg['halftone']['pattern'],
            'angle': cfg['halftone']['angle'],
        }

    # 🆕 Shake Advanced
    if efekt_kullanilsin_mi('shake_advanced') and cfg.get('shake_advanced', {}).get('enabled',
                                                                                    False) and random.random() < cfg[
        'shake_advanced'].get('olasilik',
                              0):
        effects['shake_advanced'] = {
            'type': cfg['shake_advanced']['type'],
            'intensity': cfg['shake_advanced']['intensity'],
            'frequency': cfg['shake_advanced']['frequency'],
        }

    # 🆕 Overlay Particles
    if efekt_kullanilsin_mi('overlay_particles') and cfg.get('overlay_particles', {}).get('enabled',
                                                                                          False) and random.random() < \
            cfg['overlay_particles'].get(
                'olasilik', 0):
        effects['overlay_particles'] = {
            'type': cfg['overlay_particles']['type'],
            'density': cfg['overlay_particles']['density'],
            'size': cfg['overlay_particles']['size'],
        }

    # 🆕 Vignette Advanced
    if efekt_kullanilsin_mi('vignette_advanced') and cfg.get('vignette_advanced', {}).get('enabled',
                                                                                          False) and random.random() < \
            cfg['vignette_advanced'].get(
                'olasilik', 0):
        effects['vignette_advanced'] = {
            'intensity': cfg['vignette_advanced']['intensity'],
            'shape': cfg['vignette_advanced']['shape'],
            'feather': cfg['vignette_advanced']['feather'],
        }

    # Camera Shake (eski)
    if efekt_kullanilsin_mi('camera_shake') and cfg['camera_shake']['enabled'] and random.random() < \
            cfg['camera_shake']['olasilik']:
        effects['camera_shake'] = {
            'intensity': round(random.uniform(*cfg['camera_shake']['intensity']), 2),
            'frequency': random.randint(*cfg['camera_shake']['frequency']),
        }

    # Vintage/Retro Styles
    if efekt_kullanilsin_mi('vintage_styles') and cfg['vintage_styles']['enabled'] and random.random() < \
            cfg['vintage_styles']['olasilik']:
        styles = cfg['vintage_styles']['styles']
        style_names = list(styles.keys())
        weights = [styles[s]['weight'] for s in style_names]

        chosen_style = random.choices(style_names, weights=weights, k=1)[0]
        effects['vintage_style'] = {
            'type': chosen_style,
            'params': styles[chosen_style].copy()
        }

    # Chromatic Aberration
    if efekt_kullanilsin_mi('chromatic_aberration') and cfg['chromatic_aberration']['enabled'] and random.random() < \
            cfg['chromatic_aberration']['olasilik']:
        effects['chromatic_aberration'] = {
            'shift': random.randint(*cfg['chromatic_aberration']['shift_amount'])
        }

    # Light Leaks
    if efekt_kullanilsin_mi('light_leaks') and cfg['light_leaks']['enabled'] and random.random() < cfg['light_leaks'][
        'olasilik']:
        effects['light_leak'] = {
            'intensity': round(random.uniform(*cfg['light_leaks']['intensity']), 2),
            'color': random.choice(cfg['light_leaks']['color'])
        }

    # Glitch Effect
    if efekt_kullanilsin_mi('glitch') and cfg['glitch']['enabled'] and random.random() < cfg['glitch']['olasilik']:
        effects['glitch'] = {
            'intensity': round(random.uniform(*cfg['glitch']['intensity']), 2),
            'rgb_split': cfg['glitch']['rgb_split'],
            'scan_lines': cfg['glitch']['scan_lines'],
            'noise': cfg['glitch']['noise'],
        }

    # Motion Blur
    if efekt_kullanilsin_mi('motion_blur') and cfg['motion_blur']['enabled'] and random.random() < cfg['motion_blur'][
        'olasilik']:
        effects['motion_blur'] = {
            'intensity': round(random.uniform(*cfg['motion_blur']['intensity']), 2),
            'angle': cfg['motion_blur']['angle'],
        }

    # Zoom Pulse
    if efekt_kullanilsin_mi('zoom_pulse') and cfg['zoom_pulse']['enabled'] and random.random() < cfg['zoom_pulse'][
        'olasilik']:
        effects['zoom_pulse'] = {
            'type': cfg['zoom_pulse']['type'],
            'intensity': cfg['zoom_pulse']['intensity'],
            'speed': cfg['zoom_pulse']['speed'],
        }

    # Lens Distortion
    if efekt_kullanilsin_mi('lens_distortion') and cfg['lens_distortion']['enabled'] and random.random() < \
            cfg['lens_distortion']['olasilik']:
        effects['lens_distortion'] = {
            'type': cfg['lens_distortion']['type'],
            'strength': cfg['lens_distortion']['strength'],
        }

    # Prism
    if efekt_kullanilsin_mi('prism') and cfg['prism']['enabled'] and random.random() < cfg['prism']['olasilik']:
        effects['prism'] = {
            'intensity': cfg['prism']['intensity'],
            'colors': cfg['prism']['colors'],
        }

    # Color Grading
    if efekt_kullanilsin_mi('color_grading') and cfg['color_grading']['enabled'] and random.random() < \
            cfg['color_grading']['olasilik']:
        presets = cfg['color_grading']['presets']
        preset_names = list(presets.keys())
        weights = [presets[p]['weight'] for p in preset_names]

        chosen_preset = random.choices(preset_names, weights=weights, k=1)[0]
        effects['color_grading'] = {
            'type': chosen_preset,
            'params': presets[chosen_preset].copy()
        }

    # Dream Glow
    if efekt_kullanilsin_mi('dream_glow') and cfg['dream_glow']['enabled'] and random.random() < cfg['dream_glow'][
        'olasilik']:
        effects['dream_glow'] = {
            'intensity': cfg['dream_glow']['intensity'],
            'soft_light': cfg['dream_glow']['soft_light'],
        }

    # RGB Split Advanced
    if efekt_kullanilsin_mi('rgb_split_advanced') and cfg['rgb_split_advanced']['enabled'] and random.random() < \
            cfg['rgb_split_advanced']['olasilik']:
        effects['rgb_split_advanced'] = {
            'offset_x': cfg['rgb_split_advanced']['offset_x'],
            'offset_y': cfg['rgb_split_advanced']['offset_y'],
            'diagonal': cfg['rgb_split_advanced']['diagonal'],
        }

    # Sharpen Boost
    if efekt_kullanilsin_mi('sharpen_boost') and cfg['sharpen_boost']['enabled'] and random.random() < \
            cfg['sharpen_boost']['olasilik']:
        effects['sharpen_boost'] = {
            'intensity': cfg['sharpen_boost']['intensity'],
        }

    # ========== 🔥 VIRAL EFFECTS (Phase 1) ==========

    # Beat Drop Shake
    if efekt_kullanilsin_mi('beat_drop_shake') and cfg.get('beat_drop_shake', {}).get('enabled', False) and random.random() < cfg['beat_drop_shake'].get('olasilik', 0):
        effects['beat_drop_shake'] = {
            'intensity': random.uniform(*cfg['beat_drop_shake']['intensity']),
            'duration': random.uniform(*cfg['beat_drop_shake']['duration']),
            'frequency': random.uniform(*cfg['beat_drop_shake']['frequency']),
        }

    # Beat Drop Zoom
    if efekt_kullanilsin_mi('beat_drop_zoom') and cfg.get('beat_drop_zoom', {}).get('enabled', False) and random.random() < cfg['beat_drop_zoom'].get('olasilik', 0):
        effects['beat_drop_zoom'] = {
            'zoom_in': random.uniform(*cfg['beat_drop_zoom']['zoom_in']),
            'duration': random.uniform(*cfg['beat_drop_zoom']['duration']),
            'snap_back': cfg['beat_drop_zoom']['snap_back'],
        }

    # Beat Drop Flash
    if efekt_kullanilsin_mi('beat_drop_flash') and cfg.get('beat_drop_flash', {}).get('enabled', False) and random.random() < cfg['beat_drop_flash'].get('olasilik', 0):
        effects['beat_drop_flash'] = {
            'color': random.choice(cfg['beat_drop_flash']['colors']),
            'intensity': random.uniform(*cfg['beat_drop_flash']['intensity']),
            'duration': random.uniform(*cfg['beat_drop_flash']['duration']),
            'fade_out': random.uniform(*cfg['beat_drop_flash']['fade_out']),
        }

    # Freeze Frame
    if efekt_kullanilsin_mi('freeze_frame') and cfg.get('freeze_frame', {}).get('enabled', False) and random.random() < cfg['freeze_frame'].get('olasilik', 0):
        effects['freeze_frame'] = {
            'duration': random.uniform(*cfg['freeze_frame']['duration']),
            'zoom': random.uniform(*cfg['freeze_frame']['effects']['zoom_in']['zoom']) if cfg['freeze_frame']['effects']['zoom_in']['enabled'] else 1.0,
            'border_color': random.choice(cfg['freeze_frame']['effects']['border_glow']['color']) if cfg['freeze_frame']['effects']['border_glow']['enabled'] else None,
            'border_thickness': random.randint(*cfg['freeze_frame']['effects']['border_glow']['thickness']) if cfg['freeze_frame']['effects']['border_glow']['enabled'] else 0,
            'saturation_boost': random.randint(*cfg['freeze_frame']['effects']['color_pop']['saturation_boost']) if cfg['freeze_frame']['effects']['color_pop']['enabled'] else 0,
        }

    # Elastic Bounce
    if efekt_kullanilsin_mi('elastic_bounce') and cfg.get('elastic_bounce', {}).get('enabled', False) and random.random() < cfg['elastic_bounce'].get('olasilik', 0):
        effects['elastic_bounce'] = {
            'frequency': random.uniform(*cfg['elastic_bounce']['frequency']),
            'amplitude': random.uniform(*cfg['elastic_bounce']['amplitude']),
            'decay': random.uniform(*cfg['elastic_bounce']['decay']),
            'duration': random.uniform(*cfg['elastic_bounce']['duration']),
            'axis': random.choice(cfg['elastic_bounce']['axis']),
        }

    # Wiggle Shake
    if efekt_kullanilsin_mi('wiggle_shake') and cfg.get('wiggle_shake', {}).get('enabled', False) and random.random() < cfg['wiggle_shake'].get('olasilik', 0):
        # Weighted random type selection
        types = cfg['wiggle_shake']['types']
        type_choice = random.choices(
            list(types.keys()),
            weights=[types[k]['weight'] for k in types.keys()]
        )[0]

        effects['wiggle_shake'] = {
            'type': type_choice,
            'frequency': random.uniform(*types[type_choice]['frequency']),
            'amplitude': random.uniform(*types[type_choice]['amplitude']),
            'duration': random.uniform(*cfg['wiggle_shake']['duration']),
        }

    # Jello Effect
    if efekt_kullanilsin_mi('jello_effect') and cfg.get('jello_effect', {}).get('enabled', False) and random.random() < cfg['jello_effect'].get('olasilik', 0):
        effects['jello_effect'] = {
            'wobble': random.uniform(*cfg['jello_effect']['wobble']),
            'frequency': random.uniform(*cfg['jello_effect']['frequency']),
            'duration': random.uniform(*cfg['jello_effect']['duration']),
            'damping': random.uniform(*cfg['jello_effect']['damping']),
        }

    # ========== 🎥 SUBTITLE-FRIENDLY EFFECTS ==========

    # Ken Burns Effect
    if efekt_kullanilsin_mi('ken_burns') and cfg.get('ken_burns', {}).get('enabled', False) and random.random() < cfg['ken_burns'].get('olasilik', 0):
        types = cfg['ken_burns']['types']
        type_choice = random.choices(
            list(types.keys()),
            weights=[types[k]['weight'] for k in types.keys()]
        )[0]

        if type_choice == 'zoom_in_pan':
            effects['ken_burns'] = {
                'type': 'zoom_in_pan',
                'start_zoom': types[type_choice]['start_zoom'],
                'end_zoom': random.uniform(*types[type_choice]['end_zoom']),
                'pan_direction': random.choice(types[type_choice]['pan_direction']),
            }
        elif type_choice == 'zoom_out_pan':
            effects['ken_burns'] = {
                'type': 'zoom_out_pan',
                'start_zoom': random.uniform(*types[type_choice]['start_zoom']),
                'end_zoom': types[type_choice]['end_zoom'],
                'pan_direction': random.choice(types[type_choice]['pan_direction']),
            }
        else:  # pan_only
            effects['ken_burns'] = {
                'type': 'pan_only',
                'zoom': types[type_choice]['zoom'],
                'pan_distance': random.uniform(*types[type_choice]['pan_distance']),
                'direction': random.choice(types[type_choice]['direction']),
            }

    # Gradient Overlay
    if efekt_kullanilsin_mi('gradient_overlay') and cfg.get('gradient_overlay', {}).get('enabled', False) and random.random() < cfg['gradient_overlay'].get('olasilik', 0):
        types = cfg['gradient_overlay']['types']
        type_choice = random.choices(
            list(types.keys()),
            weights=[types[k]['weight'] for k in types.keys()]
        )[0]

        effects['gradient_overlay'] = {
            'type': type_choice,
            'opacity': random.uniform(*types[type_choice]['opacity']),
            'blend_mode': random.choice(cfg['gradient_overlay']['blend_mode']),
        }

        if type_choice == 'diagonal':
            effects['gradient_overlay']['angle'] = random.uniform(*types[type_choice]['angle'])

    # Soft Focus Background
    if efekt_kullanilsin_mi('soft_focus_background') and cfg.get('soft_focus_background', {}).get('enabled', False) and random.random() < cfg['soft_focus_background'].get('olasilik', 0):
        effects['soft_focus_background'] = {
            'subtitle_area': cfg['soft_focus_background']['subtitle_area'],
            'blur_intensity': random.uniform(*cfg['soft_focus_background']['blur_intensity']),
            'fade_boundary': random.uniform(*cfg['soft_focus_background']['fade_boundary']),
            'brightness_boost': random.uniform(*cfg['soft_focus_background']['brightness_boost']),
        }

    return effects


# ==================== VIDEO/AUDIO FILTER CREATION ====================

def gelismis_varyasyon_uret(video_ad, varyasyon_no):
    """Gelişmiş varyasyon parametreleri + Cinematic Effects"""
    random.seed(hash(f"{video_ad}_{varyasyon_no}"))
    conf = ADVANCED_CONFIG

    return {
        # Basic - SLOW MOTION
        'hiz': round(random.uniform(*conf['hiz_aralik']), 3),
        'parlaklik': random.randint(*conf['parlaklik_aralik']),
        'kontrast': random.randint(*conf['kontrast_aralik']),
        'doygunluk': random.randint(*conf['doygunluk_aralik']),
        'zoom': round(random.uniform(*conf['zoom_aralik']), 3),
        'flip': random.random() < conf['flip_olasilik'],

        # Advanced video
        'rotate': round(random.uniform(*conf['rotate_aralik']), 2),
        'unsharp': round(random.uniform(*conf['unsharp_aralik']), 2),
        'vignette': random.random() < conf['vignette_olasilik'],
        'grain': random.randint(*conf['grain_aralik']),
        'chroma_shift': random.random() < conf['chroma_shift_olasilik'],

        # Audio
        'pitch': round(random.uniform(*conf['pitch_aralik']), 2),
        'volume': round(random.uniform(*conf['volume_aralik']), 2),
        'bass_boost': random.random() < conf['bass_boost_olasilik'],
        'treble_boost': random.random() < conf['treble_boost_olasilik'],
        'stereo_width': round(random.uniform(*conf['stereo_width_aralik']), 2),
        'use_normalization': conf['use_normalization'],
        'use_compression': conf['use_compression'],

        # Other
        'timestamp': False,
        'color_tint': random.choice(conf['color_presets']) if random.random() < conf['color_tint_olasilik'] else None,

        # Cinematic effects
        'cinematic': None,
    }


def gelismis_video_filtre_olustur(varyasyon, subtitle_config=None, cinematic_effects=None, use_gpu_scale=False):
    """🆕 Gelişmiş video filtreleri + TÜM CAPCUT PLUS EFEKTLER

    use_gpu_scale: True ise scale_cuda kullan (NVENC aktifken)
    """
    filtreler = []

    # 1. RESOLUTION NORMALIZATION (1920x1080)
    video_output = VIDEO_OUTPUT
    target_width, target_height = video_output['resolution'].split('x')

    # 🚀 GPU SCALE: scale_cuda varsa kullan (daha hızlı)
    if use_gpu_scale:
        # GPU scale_cuda - hwupload/hwdownload ile
        # Not: scale_cuda force_original_aspect_ratio desteklemiyor, o yüzden
        # önce CPU'da aspect ratio hesapla, sonra GPU'da scale yap
        filtreler.append(
            f"hwupload_cuda,"
            f"scale_cuda={target_width}:{target_height}:interp_algo=lanczos,"
            f"hwdownload,format=nv12"
        )
    else:
        # CPU scale - bicubic + aspect ratio koruma
        filtreler.append(
            f"scale={target_width}:{target_height}:force_original_aspect_ratio=decrease:flags=bicubic,"
            f"pad={target_width}:{target_height}:(ow-iw)/2:(oh-ih)/2"
        )

    # 2. FRAME RATE NORMALIZATION (30fps)
    filtreler.append(f"fps={video_output['fps']}")

    # 3. CINEMATIC EFFECTS
    if cinematic_effects:
        # 🆕 Velocity/Speed Ramping
        if cinematic_effects.get('velocity_ramp'):
            velocity_filters = velocity_ramp_filtre_olustur(cinematic_effects['velocity_ramp'])
            filtreler.extend(velocity_filters)

        # 🆕 Ghost Trail
        if cinematic_effects.get('ghost_trail'):
            ghost_filters = ghost_trail_filtre_olustur(cinematic_effects['ghost_trail'])
            filtreler.extend(ghost_filters)

        # 🆕 Neon Glow
        if cinematic_effects.get('neon_glow'):
            neon_filters = neon_glow_filtre_olustur(cinematic_effects['neon_glow'])
            filtreler.extend(neon_filters)

        # 🆕 VHS Advanced
        if cinematic_effects.get('vhs_advanced'):
            vhs_filters = vhs_advanced_filtre_olustur(cinematic_effects['vhs_advanced'])
            filtreler.extend(vhs_filters)

        # 🆕 Datamosh
        if cinematic_effects.get('datamosh'):
            datamosh_filters = datamosh_filtre_olustur(cinematic_effects['datamosh'])
            filtreler.extend(datamosh_filters)

        # 🆕 Posterize
        if cinematic_effects.get('posterize'):
            posterize_filters = posterize_filtre_olustur(cinematic_effects['posterize'])
            filtreler.extend(posterize_filters)

        # 🆕 Edge Detection
        if cinematic_effects.get('edge_detect'):
            edge_filters = edge_detect_filtre_olustur(cinematic_effects['edge_detect'])
            filtreler.extend(edge_filters)

        # 🆕 Mirror/Kaleidoscope
        if cinematic_effects.get('mirror_kaleidoscope'):
            mirror_filters = mirror_kaleidoscope_filtre_olustur(cinematic_effects['mirror_kaleidoscope'])
            filtreler.extend(mirror_filters)

        # 🆕 Pixelate
        if cinematic_effects.get('pixelate'):
            pixelate_filters = pixelate_filtre_olustur(cinematic_effects['pixelate'])
            filtreler.extend(pixelate_filters)

        # 🆕 Solarize
        if cinematic_effects.get('solarize'):
            solarize_filters = solarize_filtre_olustur(cinematic_effects['solarize'])
            filtreler.extend(solarize_filters)

        # 🆕 Halftone
        if cinematic_effects.get('halftone'):
            halftone_filters = halftone_filtre_olustur(cinematic_effects['halftone'])
            filtreler.extend(halftone_filters)

        # 🆕 Shake Advanced
        if cinematic_effects.get('shake_advanced'):
            shake_adv_filters = shake_advanced_filtre_olustur(cinematic_effects['shake_advanced'])
            filtreler.extend(shake_adv_filters)

        # 🆕 Overlay Particles
        if cinematic_effects.get('overlay_particles'):
            overlay_filters = overlay_particles_filtre_olustur(cinematic_effects['overlay_particles'])
            filtreler.extend(overlay_filters)

        # 🆕 Vignette Advanced
        if cinematic_effects.get('vignette_advanced'):
            vignette_adv_filters = vignette_advanced_filtre_olustur(cinematic_effects['vignette_advanced'])
            filtreler.extend(vignette_adv_filters)

        # Camera Shake (eski)
        if cinematic_effects.get('camera_shake'):
            shake_filters = camera_shake_filtre_olustur(cinematic_effects['camera_shake'])
            filtreler.extend(shake_filters)

        # Glitch Effect
        if cinematic_effects.get('glitch'):
            glitch_filters = glitch_filtre_olustur(cinematic_effects['glitch'])
            filtreler.extend(glitch_filters)

        # Motion Blur
        if cinematic_effects.get('motion_blur'):
            blur_filters = motion_blur_filtre_olustur(cinematic_effects['motion_blur'])
            filtreler.extend(blur_filters)

        # Zoom Pulse
        if cinematic_effects.get('zoom_pulse'):
            zoom_filters = zoom_pulse_filtre_olustur(cinematic_effects['zoom_pulse'])
            filtreler.extend(zoom_filters)

        # Lens Distortion
        if cinematic_effects.get('lens_distortion'):
            dist_filters = lens_distortion_filtre_olustur(cinematic_effects['lens_distortion'])
            filtreler.extend(dist_filters)

        # Vintage Styles
        if cinematic_effects.get('vintage_style'):
            style_type = cinematic_effects['vintage_style']['type']
            style_params = cinematic_effects['vintage_style']['params']

            if style_type == '70s':
                vintage_filters = vintage_70s_filtre_olustur(style_params)
                filtreler.extend(vintage_filters)
            elif style_type == '80s':
                vintage_filters = vintage_80s_filtre_olustur(style_params)
                filtreler.extend(vintage_filters)
            elif style_type == '90s':
                vintage_filters = vintage_90s_filtre_olustur(style_params)
                filtreler.extend(vintage_filters)
            elif style_type == 'film_grain':
                grain_filters = film_grain_filtre_olustur(style_params)
                filtreler.extend(grain_filters)

        # Color Grading Presets
        if cinematic_effects.get('color_grading'):
            grading_filters = color_grading_filtre_olustur(cinematic_effects['color_grading'])
            filtreler.extend(grading_filters)

        # Dream Glow
        if cinematic_effects.get('dream_glow'):
            glow_filters = dream_glow_filtre_olustur(cinematic_effects['dream_glow'])
            filtreler.extend(glow_filters)

        # Prism Effect
        if cinematic_effects.get('prism'):
            prism_filters = prism_filtre_olustur(cinematic_effects['prism'])
            filtreler.extend(prism_filters)

        # Chromatic Aberration (basit)
        if cinematic_effects.get('chromatic_aberration'):
            shift = cinematic_effects['chromatic_aberration']['shift']
            filtreler.append(f"chromashift=crh={shift}:cbh={shift}")

        # RGB Split Advanced
        if cinematic_effects.get('rgb_split_advanced'):
            rgb_filters = rgb_split_advanced_filtre_olustur(cinematic_effects['rgb_split_advanced'])
            filtreler.extend(rgb_filters)

        # Light Leaks
        if cinematic_effects.get('light_leak'):
            leak_filters = light_leak_filtre_olustur(cinematic_effects['light_leak'])
            filtreler.extend(leak_filters)

        # Sharpen Boost
        if cinematic_effects.get('sharpen_boost'):
            sharpen_filters = sharpen_boost_filtre_olustur(cinematic_effects['sharpen_boost'])
            filtreler.extend(sharpen_filters)

        # ========== 🔥 VIRAL EFFECTS (Phase 1) ==========

        # Beat Drop Shake
        if cinematic_effects.get('beat_drop_shake'):
            params = cinematic_effects['beat_drop_shake']
            # DISABLED: geq filter with x/y planes is invalid in FFmpeg
            # geq only supports: lum, cb, cr (YUV) or r, g, b (RGB) planes
            # For shake effects, would need different filter (transform, perspective, etc)
            pass  # Disabled - invalid geq syntax

        # Beat Drop Zoom
        if cinematic_effects.get('beat_drop_zoom'):
            params = cinematic_effects['beat_drop_zoom']
            zoom = params['zoom_in']
            # Hızlı zoom in/out efekti - zoompan filtresi ile
            filtreler.append(f"zoompan=z='if(lte(on,15),{zoom}*on/15,{zoom}*exp(-(on-15)/10))':d=1:s=1920x1080:fps=30")

        # Beat Drop Flash
        if cinematic_effects.get('beat_drop_flash'):
            params = cinematic_effects['beat_drop_flash']
            # Flash efekti - eq ile brightness/gamma boost (FFmpeg-safe)
            intensity = params['intensity']
            color = params.get('color', 'white')

            # FFmpeg eq filter gamma channel mapping
            if color == 'white':
                # White flash: boost all gamma channels
                filtreler.append(f"eq=gamma={1 + intensity}")
            elif color == 'red' or color == 'purple':
                # Red/Purple: boost red gamma
                filtreler.append(f"eq=gamma_r={1 + intensity}")
            elif color == 'blue' or color == 'cyan':
                # Blue/Cyan: boost blue gamma
                filtreler.append(f"eq=gamma_b={1 + intensity}")
            elif color == 'yellow':
                # Yellow: boost red + green gamma
                filtreler.append(f"eq=gamma_r={1 + intensity}:gamma_g={1 + intensity}")
            else:
                # Default: brightness boost
                filtreler.append(f"eq=brightness={intensity * 0.3}")

        # Freeze Frame
        if cinematic_effects.get('freeze_frame'):
            params = cinematic_effects['freeze_frame']
            # Freeze frame - tblend ve setpts kullanarak dondurma efekti
            # Bu FFmpeg'de karmaşık, basit zoom ve saturation boost uygulayalım
            if params['zoom'] > 1.0:
                filtreler.append(f"scale='trunc(iw*{params['zoom']}/2)*2:trunc(ih*{params['zoom']}/2)*2':flags=lanczos")
            if params['saturation_boost'] > 0:
                filtreler.append(f"eq=saturation={1 + params['saturation_boost']/50}")

        # Elastic Bounce
        if cinematic_effects.get('elastic_bounce'):
            params = cinematic_effects['elastic_bounce']
            # DISABLED: geq filter with x/y planes is invalid in FFmpeg
            pass  # Disabled - invalid geq syntax

        # Wiggle Shake
        if cinematic_effects.get('wiggle_shake'):
            params = cinematic_effects['wiggle_shake']
            # DISABLED: geq filter with x/y planes is invalid in FFmpeg
            pass  # Disabled - invalid geq syntax

        # Jello Effect
        if cinematic_effects.get('jello_effect'):
            params = cinematic_effects['jello_effect']
            # Jello - daha karmaşık deformasyon
            pass  # DISABLED: geq filter invalid

        # ========== 🎥 SUBTITLE-FRIENDLY EFFECTS ==========

        # Ken Burns Effect
        if cinematic_effects.get('ken_burns'):
            params = cinematic_effects['ken_burns']
            if params['type'] == 'zoom_in_pan':
                # Yavaş zoom in + pan
                zoom_start = params['start_zoom']
                zoom_end = params['end_zoom']
                filtreler.append(f"zoompan=z='min(zoom+0.0005,{zoom_end})':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080")
            elif params['type'] == 'zoom_out_pan':
                # Yavaş zoom out + pan
                zoom_start = params['start_zoom']
                zoom_end = params['end_zoom']
                filtreler.append(f"zoompan=z='max(zoom-0.0005,{zoom_end})':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080")
            else:  # pan_only
                # Sadece pan hareketi
                direction = params['direction']
                if direction == 'horizontal':
                    filtreler.append(f"crop=iw-{params['pan_distance']}:ih:x=t*{params['pan_distance']/10}:y=0")
                else:  # vertical
                    filtreler.append(f"crop=iw:ih-{params['pan_distance']}:x=0:y=t*{params['pan_distance']/10}")

        # Gradient Overlay
        if cinematic_effects.get('gradient_overlay'):
            params = cinematic_effects['gradient_overlay']
            opacity = params['opacity']
            # Basit gradient overlay - eq filter ile renk ayarı
            if params['type'] == 'vertical':
                filtreler.append(f"eq=brightness={opacity*0.5}:contrast={1+opacity*0.3}")
            elif params['type'] == 'radial':
                filtreler.append(f"vignette=angle=PI/{1/opacity}")

        # Soft Focus Background
        if cinematic_effects.get('soft_focus_background'):
            params = cinematic_effects['soft_focus_background']
            # Alt 1/3'ü net tut, üst 2/3'ü blur
            # Bu FFmpeg'de karmaşık - basit vignette ile benzer etki
            filtreler.append(f"vignette=angle=PI/3:mode=backward")
            filtreler.append(f"eq=brightness={params['brightness_boost']-1.0}")

    # 4. NORMAL VARIATIONS
    # Zoom
    if varyasyon['zoom'] > 1.01:
        zoom = varyasyon['zoom']
        # ✅ FIX: Çift sayı garantisi ekle
        filtreler.append(
            f"scale='trunc(iw*{zoom}/2)*2:trunc(ih*{zoom}/2)*2':flags=lanczos,crop='trunc(iw/{zoom}/2)*2:trunc(ih/{zoom}/2)*2'")

    # Rotate
    if abs(varyasyon['rotate']) > 0.1:
        filtreler.append(f"rotate={varyasyon['rotate']}*PI/180:fillcolor=black:bilinear=1")

    # Flip
    if varyasyon['flip']:
        filtreler.append("hflip")

    # Color adjustments
    eq = []
    if varyasyon['parlaklik'] != 0:
        parlaklik = varyasyon['parlaklik'] * 0.5
        eq.append(f"brightness={parlaklik / 100}")
    if varyasyon['kontrast'] != 0:
        kontrast = varyasyon['kontrast'] * 0.5
        eq.append(f"contrast={(100 + kontrast) / 100}")
    if varyasyon['doygunluk'] != 0:
        doygunluk = varyasyon['doygunluk'] * 0.5
        eq.append(f"saturation={(100 + doygunluk) / 100}")

    if eq:
        filtreler.append(f"eq={':'.join(eq)}")

    # Color tint
    if varyasyon['color_tint'] == 'warm':
        filtreler.append("eq=contrast=1.03:saturation=1.05")
    elif varyasyon['color_tint'] == 'cool':
        filtreler.append("eq=contrast=1.03:saturation=0.97")
    elif varyasyon['color_tint'] == 'vibrant':
        filtreler.append("eq=saturation=1.1")
    elif varyasyon['color_tint'] == 'muted':
        filtreler.append("eq=saturation=0.9")

    # Unsharp - optimize edildi (threshold↑, kernel↓)
    if varyasyon['unsharp'] > 0.7:
        unsharp_val = min(varyasyon['unsharp'] * 0.4, 0.4)
        filtreler.append(f"unsharp=3:3:{unsharp_val}:3:3:0")

    # Vignette
    if varyasyon['vignette']:
        filtreler.append("vignette=PI/6")

    # Film grain - optimize edildi (threshold↑, strength↓)
    if varyasyon['grain'] > 12:
        grain_val = int(varyasyon['grain'] * 0.3)
        if grain_val > 4:
            filtreler.append(f"noise=alls={grain_val}:allf=t")

    # Speed - SLOW MOTION
    if abs(varyasyon['hiz'] - 1.0) > 0.01:
        filtreler.append(f"setpts={1 / varyasyon['hiz']}*PTS")

    # 5. COLOR SPACE (Rec. 709)
    filtreler.append(f"colorspace=bt709:iall=bt601-6-625:fast=1")
    filtreler.append(f"format={video_output['pixel_format']}")

    # 6. ALTYAZI (SUBTITLE)
    if subtitle_config and subtitle_config.get('enabled'):
        if subtitle_config.get('srt_file'):
            srt_path = subtitle_config['srt_file'].replace('\\', '/')

            srt_path_escaped = srt_path.replace("'", "\\'")

            import re
            if re.match(r'^[A-Za-z]:', srt_path_escaped):
                srt_path_escaped = srt_path_escaped.replace(':', '\\:', 1)

            subtitle_filter = f"subtitles='{srt_path_escaped}'"
            logger.info(f"Subtitle filter: {subtitle_filter[:80]}...")
            filtreler.append(subtitle_filter)

    # ✅ FINAL: Kesin 1920x1080 çıkış garantisi
    # Zoom/crop/rotate gibi efektler boyutu değiştirebiliyor
    # Son adımda kesin boyuta scale et
    filtreler.append("scale=1920:1080:force_original_aspect_ratio=disable")

    return ','.join(filtreler) if filtreler else None


def gelismis_audio_filtre_olustur(varyasyon):
    """Gelişmiş audio filtreleri"""
    filtreler = []

    # Audio normalization
    if varyasyon.get('use_normalization', True):
        audio_cfg = AUDIO_SETTINGS
        filtreler.append(
            f"loudnorm=I={audio_cfg['target_loudness']}:"
            f"TP={audio_cfg['true_peak']}:"
            f"LRA={audio_cfg['lra']}"
        )
        # Safety limiter after loudnorm to prevent NaN/Inf
        filtreler.append("alimiter=limit=0.95:attack=5:release=50:level=disabled")

    # Volume boost
    if abs(varyasyon['volume'] - 1.0) > 0.05:
        filtreler.append(f"volume={varyasyon['volume']}")

    # Dynamic range compression
    if varyasyon.get('use_compression', True):
        filtreler.append(
            "compand=attacks=0.3:decays=0.8:points=-90/-90|-70/-70|-60/-20|-20/-5|20/0:soft-knee=6:gain=0:volume=-5"
        )

    # Bass boost
    if varyasyon['bass_boost']:
        filtreler.append("equalizer=f=100:t=h:width=200:g=5")

    # Treble boost
    if varyasyon['treble_boost']:
        filtreler.append("equalizer=f=8000:t=h:width=4000:g=3")

    # Stereo width
    if abs(varyasyon['stereo_width'] - 1.0) > 0.05:
        filtreler.append(f"stereotools=mlev={varyasyon['stereo_width']}")

    # Speed adjustment
    if abs(varyasyon['hiz'] - 1.0) > 0.01:
        tempo = varyasyon['hiz']
        if 0.5 <= tempo <= 2.0:
            filtreler.append(f"atempo={tempo}")

    # Pitch
    if abs(varyasyon['pitch']) > 0.3:
        semitones = varyasyon['pitch']
        rate = 1 + (semitones / 12)
        filtreler.append(f"asetrate=44100*{rate},aresample=44100")

    return ','.join(filtreler) if filtreler else None


# ==================== TRANSITION FUNCTIONS ====================

def transition_sec(transition_index, used_transitions=None):
    """Her klip arası için random transition seç"""
    if not TRANSITION_EFFECTS['enabled']:
        return None

    if used_transitions is None:
        used_transitions = []

    transitions = TRANSITION_EFFECTS['transitions']
    transition_names = list(transitions.keys())
    weights = [transitions[t]['weight'] for t in transition_names]

    # Repetition önleme
    if TRANSITION_EFFECTS['avoid_repetition'] and used_transitions:
        min_gap = TRANSITION_EFFECTS['min_clip_gap']
        recent = used_transitions[-min_gap:] if len(used_transitions) >= min_gap else used_transitions

        adjusted_weights = []
        for i, name in enumerate(transition_names):
            if name in recent:
                adjusted_weights.append(weights[i] * 0.1)
            else:
                adjusted_weights.append(weights[i])
        weights = adjusted_weights

    chosen = random.choices(transition_names, weights=weights, k=1)[0]
    duration = round(random.uniform(*TRANSITION_EFFECTS['default_duration']), 2)

    return {
        'type': chosen,
        'duration': duration,
        'description': transitions[chosen]['description'],
        'index': transition_index,
    }


def xfade_filter_olustur(transition_info, offset):
    """xfade filter string oluştur"""
    if not transition_info:
        return None

    trans_type = transition_info['type']
    duration = transition_info['duration']

    xfade_str = f"xfade=transition={trans_type}:duration={duration}:offset={offset}"

    return xfade_str


def calculate_xfade_offsets(playlist):
    """Her transition için offset hesapla"""
    offsets = []
    cumulative_time = 0

    for i, item in enumerate(playlist):
        if i > 0:
            offset = cumulative_time - TRANSITION_EFFECTS['overlap_duration']
            offsets.append(max(0, offset))

        cumulative_time += item['gercek_sure']

    return offsets


# ==================== UTILITY FUNCTIONS ====================

def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=" * 100)
    print("✅  YOUTUBE ULTRA PRO V4.5 - SEÇİLEBİLİR EFEKT EDITION  ✅".center(100))
    print("=" * 100)
    print("1080p 30fps | Slow Motion | Auto Subs | 30+ EFFECTS | 35+ TRANSITIONS | SEÇİLEBİLİR!".center(100))
    print("=" * 100)
    print()
    print("   🎥 VİDEO KALİTESİ:")
    print("      • 1920x1080 (1080p) | 30fps | 15Mbps 🎬")
    print()
    print("   🆕 YENİ: İSTEDİĞİNİZ EFEKTLERİ SEÇİN!")
    print("      • 🎨 30+ efekti kendiniz seçebilirsiniz")
    print("      • 🎯 Sadece seçtikleriniz kullanılır")
    print("      • 🎲 Veya tümünü random kullanın!")
    print()
    print("   ✨ TRANSİTİON EFFECTS (35+ Geçiş):")
    print("      • 🎭 Fade (Black/White/Color)")
    print("      • ➡️  Wipe (Left/Right/Up/Down)")
    print("      • 🔄 Slide Transitions")
    print("      • ⭕ Circle Open/Close")
    print("      • 💫 Dissolve & Pixelize")
    print("      • 🔍 Zoom & Radial")
    print("      • 📐 Diagonal & Smooth")
    print("      • 🎨 35+ farklı transition!")
    print()
    print("   🎬 CİNEMATİC EFEKTLER (30+ FARKLI):")
    print("      ⭐ CAPCUT POPÜLER EFEKTLER:")
    print("         • 🚀 Velocity/Speed Ramping (CapCut #1)")
    print("         • 👻 Ghost Trail | 💡 Neon Glow | 📼 VHS Advanced")
    print("         • 💥 Datamosh | 🎨 Posterize | 🖼️  Edge Detection")
    print("         • 🪞 Mirror/Kaleidoscope | 🔲 Pixelate | ☀️  Solarize")
    print("         • 🖨️  Halftone | 💥 Shake Advanced | ✨ Particles")
    print()
    print("      📹 KLASİK EFEKTLER:")
    print("         • Camera Shake | 70s/80s/90s Vintage | Film Grain")
    print("         • Chromatic Aberr | Light Leaks | Glitch")
    print("         • Motion Blur | Zoom Pulse | Lens Distortion")
    print("         • Prism | 5 Color Grading | Dream Glow")
    print("         • RGB Split | Sharpen Boost | Vignette")
    print()
    print("   🎬 SLOW MOTION:")
    print("      • %75-90 hız (1.1x-1.3x yavaş) 🐢")
    print()
    print("   🎵 SES: 320kbps AAC + Loudnorm 🔊")
    print()
    print("   📝 ALTYAZI: Otomatik (Whisper AI) 🤖")
    print()
    print("   🎯 KİŞİSELLEŞTİRİLEBİLİR - İSTEDİĞİNİZ EFEKTLERİ SEÇİN!")
    print("=" * 100)
    print()


def ffmpeg_yuklu_mu():
    try:
        subprocess.run([FFMPEG_PATH, '-version'],
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE,
                       check=True,
                       timeout=5)
        return True
    except:
        return False


def video_dosyalarini_bul(klasor_yolu):
    """Video dosyalarını bul - ✅ İYİLEŞTİRİLMİŞ ERROR HANDLING"""
    video_uzantilari = {'.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm', '.m4v'}

    try:
        # Klasör var mı kontrol et
        if not os.path.exists(klasor_yolu):
            logger.error(f"❌ Klasör bulunamadı: {klasor_yolu}")
            return []

        if not os.path.isdir(klasor_yolu):
            logger.error(f"❌ Geçersiz klasör: {klasor_yolu}")
            return []

        # Dosyaları listele
        dosyalar = [f for f in sorted(os.listdir(klasor_yolu))
                    if Path(f).suffix.lower() in video_uzantilari]

        if not dosyalar:
            logger.error(f"❌ Klasörde video dosyası bulunamadı: {klasor_yolu}")
            logger.info(f"   💡 Desteklenen formatlar: {', '.join(video_uzantilari)}")
            return []

        logger.info(f"✅ {len(dosyalar)} video dosyası bulundu")
        return dosyalar

    except PermissionError as e:
        with GracefulErrorHandler(ErrorCategory.PERMISSION_DENIED, continue_on_error=True):
            raise
        return []
    except Exception as e:
        logger.error(f"❌ Video dosyaları aranırken hata: {e}")
        return []


def ses_dosyalarini_bul(klasor_yolu):
    """Ses dosyalarını bul - ✅ İYİLEŞTİRİLMİŞ ERROR HANDLING"""
    ses_uzantilari = {'.mp3', '.wav', '.aac', '.m4a', '.ogg', '.flac', '.wma', '.opus'}

    try:
        # Klasör var mı kontrol et
        if not os.path.exists(klasor_yolu):
            logger.error(f"❌ Klasör bulunamadı: {klasor_yolu}")
            return []

        if not os.path.isdir(klasor_yolu):
            logger.error(f"❌ Geçersiz klasör: {klasor_yolu}")
            return []

        # Dosyaları listele
        dosyalar = [f for f in sorted(os.listdir(klasor_yolu))
                    if Path(f).suffix.lower() in ses_uzantilari]

        if not dosyalar:
            logger.warning(f"⚠️ Klasörde ses dosyası bulunamadı: {klasor_yolu}")
            logger.info(f"   Desteklenen formatlar: {', '.join(ses_uzantilari)}")

        return dosyalar

    except PermissionError as e:
        with GracefulErrorHandler(ErrorCategory.PERMISSION_DENIED, continue_on_error=True):
            raise
        return []
    except Exception as e:
        logger.error(f"❌ Ses dosyaları aranırken hata: {e}")
        return []


def video_bilgisi_al(video_yolu):
    try:
        komut = [
            FFPROBE_PATH, '-v', 'error',
            '-select_streams', 'v:0',
            '-show_entries', 'stream=width,height,duration,bit_rate,codec_name:format=duration',
            '-of', 'json', video_yolu
        ]
        sonuc = subprocess.run(komut,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               text=True,
                               timeout=10)

        if sonuc.returncode == 0:
            veri = json.loads(sonuc.stdout)
            sure = None
            width = 1920
            height = 1080
            bitrate = None
            codec = None

            if 'format' in veri and 'duration' in veri['format']:
                sure = float(veri['format']['duration'])
            elif 'streams' in veri and len(veri['streams']) > 0:
                stream = veri['streams'][0]
                if 'duration' in stream:
                    sure = float(stream['duration'])
                if 'width' in stream:
                    width = int(stream['width'])
                if 'height' in stream:
                    height = int(stream['height'])
                if 'bit_rate' in stream:
                    bitrate = int(stream['bit_rate'])
                if 'codec_name' in stream:
                    codec = stream['codec_name']

            test_komut = [
                FFMPEG_PATH, '-v', 'error',
                '-i', video_yolu,
                '-frames:v', '1',
                '-f', 'null', '-'
            ]
            test_sonuc = subprocess.run(test_komut,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        timeout=10)

            if test_sonuc.returncode != 0:
                logger.warning(f"⚠️  Video decode edilemiyor: {os.path.basename(video_yolu)}")
                return None

            return {
                'sure': sure,
                'width': width,
                'height': height,
                'bitrate': bitrate,
                'codec': codec
            }
        return None
    except Exception as e:
        logger.warning(f"Video bilgisi alınamadı: {e}")
        return None


def ses_bilgisi_al(ses_yolu):
    """Ses dosyasının süresini al - ✅ İYİLEŞTİRİLMİŞ ERROR HANDLING"""
    try:
        # Dosya var mı kontrol et
        if not os.path.exists(ses_yolu):
            logger.error(f"❌ Ses dosyası bulunamadı: {ses_yolu}")
            return None

        komut = [
            FFPROBE_PATH, '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'json', ses_yolu
        ]
        sonuc = subprocess.run(komut,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               text=True,
                               timeout=10)

        if sonuc.returncode == 0:
            veri = json.loads(sonuc.stdout)
            if 'format' in veri and 'duration' in veri['format']:
                duration = float(veri['format']['duration'])
                logger.debug(f"🎵 Ses dosyası süresi: {duration:.1f}s - {os.path.basename(ses_yolu)}")
                return duration
            else:
                logger.warning(f"⚠️ Ses dosyasında süre bilgisi yok: {os.path.basename(ses_yolu)}")
                return None
        else:
            # FFmpeg hatasını kategorize et
            stderr_output = sonuc.stderr if sonuc.stderr else ""
            error_category = parse_ffmpeg_error(stderr_output)

            if error_category == ErrorCategory.CODEC_ERROR:
                logger.error(f"❌ Ses codec hatası: {os.path.basename(ses_yolu)}")
                logger.info(f"   💡 Desteklenen formatlar: MP3, WAV, AAC, M4A, OGG, FLAC")
            elif error_category == ErrorCategory.FILE_NOT_FOUND:
                logger.error(f"❌ Ses dosyası bulunamadı veya hasarlı: {os.path.basename(ses_yolu)}")
            else:
                logger.warning(f"⚠️ Ses bilgisi alınamadı: {error_category.value}")

            return None

    except subprocess.TimeoutExpired:
        logger.error(f"⏱️ Ses dosyası analizi timeout: {os.path.basename(ses_yolu)}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"❌ FFprobe çıktısı parse edilemedi: {e}")
        return None
    except Exception as e:
        logger.warning(f"⚠️ Ses bilgisi alınamadı: {e}")
        return None


def dosya_gecerli_mi(dosya_yolu, min_size_kb=None):
    """Gelişmiş dosya kontrolü - ✅ İYİLEŞTİRİLMİŞ ERROR HANDLING"""
    try:
        # Dosya var mı?
        if not os.path.exists(dosya_yolu):
            logger.debug(f"❌ Dosya bulunamadı: {os.path.basename(dosya_yolu)}")
            return False

        # Dosya boyutu kontrol
        try:
            file_size = os.path.getsize(dosya_yolu)
            min_size = (min_size_kb or QUALITY_CONFIG['min_size_kb']) * 1024

            if file_size < min_size:
                logger.debug(f"❌ Dosya çok küçük: {os.path.basename(dosya_yolu)} ({file_size} bytes < {min_size} bytes)")
                return False
        except OSError as e:
            logger.debug(f"❌ Dosya boyutu okunamadı: {os.path.basename(dosya_yolu)}")
            return False

        # FFprobe ile video stream kontrolü
        try:
            komut = [
                FFPROBE_PATH, '-v', 'error',
                '-select_streams', 'v:0',
                '-show_entries', 'stream=codec_type',
                '-of', 'json', dosya_yolu
            ]
            sonuc = subprocess.run(komut,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   text=True,
                                   timeout=5)

            if sonuc.returncode != 0:
                logger.debug(f"❌ Video stream geçersiz: {os.path.basename(dosya_yolu)}")
                return False

            return True

        except subprocess.TimeoutExpired:
            logger.debug(f"⏱️ Dosya doğrulama timeout: {os.path.basename(dosya_yolu)}")
            return False

    except Exception as e:
        logger.debug(f"❌ Dosya doğrulama hatası: {os.path.basename(dosya_yolu)} - {e}")
        return False


def sure_formatla(saniye):
    if saniye is None:
        return "Bilinmiyor"
    return str(timedelta(seconds=int(saniye)))


def hedef_sure_al(ses_dosyasi_secildi=False, ses_suresi=None):
    """Hedef süreyi belirle"""
    if ses_dosyasi_secildi and ses_suresi:
        print(f"\n⏱️  VİDEO SÜRESİ: {sure_formatla(ses_suresi)} (ses dosyasından)")
        return ses_suresi

    print("\n⏱️  HEDEF VİDEO SÜRESİ:")
    girdi = input("   🎯 Dakika [Enter=30 dk]: ").strip()

    if not girdi:
        return 30 * 60

    try:
        if ':' in girdi:
            h, m = girdi.split(':')
            return (int(h) * 60 + int(m)) * 60
        else:
            return int(girdi) * 60
    except:
        return 30 * 60


def random_dosya_adi_olustur():
    """Timestamp bazlı random dosya adı oluştur"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    random_id = random.randint(1000, 9999)
    return f"youtube_pro_{timestamp}_{random_id}.mp4"


def akilli_video_sec(video_havuzu, hedef_sure, max_varyasyon=10):
    """Ses uzunluğuna göre akıllı video seçimi"""
    import random
    from datetime import datetime

    if not video_havuzu:
        return []

    seed = int(datetime.now().timestamp() * 1000000) % (2 ** 32)
    random.seed(seed)

    # Account for transition overlaps
    # Each transition overlaps clips by overlap_duration (1.0s)
    # Average clip is ~6 seconds, so estimate N clips needed
    ortalama_klip_suresi = sum(v['sure'] for v in video_havuzu) / len(video_havuzu)
    tahmini_klip_sayisi = int(hedef_sure / ortalama_klip_suresi) + 2
    tahmini_transition_sayisi = max(0, tahmini_klip_sayisi - 1)
    transition_kaybi = tahmini_transition_sayisi * TRANSITION_EFFECTS.get('overlap_duration', 1.0)

    # Add extra duration to compensate for transition overlaps + safety margin
    # Safety margin: +5 seconds to ensure video is always longer than audio
    safety_margin = 5.0
    hedef_sure_with_margin = hedef_sure + transition_kaybi + safety_margin

    print(f"\n🎲 AKILLI VIDEO SEÇİMİ (Ultra Random)")
    print(f"   🎯 Hedef süre: {sure_formatla(hedef_sure)} (ses)")
    print(f"   ⚡ Transition kaybı: ~{transition_kaybi:.0f}s ({tahmini_transition_sayisi} geçiş)")
    print(f"   🛡️  Güvenlik marjı: +{safety_margin:.0f}s (video > audio garantisi)")
    print(f"   📊 Ayarlanmış hedef: {sure_formatla(hedef_sure_with_margin)}")
    print(f"   📦 Video havuzu: {len(video_havuzu)} video")
    print(f"   🔀 Randomizasyon seed: {seed}")

    karisik_havuz = video_havuzu.copy()
    random.shuffle(karisik_havuz)

    if len(karisik_havuz) >= max_varyasyon:
        print(f"   ✅ Strateji: MAKSIMUM VARYASYON (her video farklı)")

        secilen_videolar = []
        toplam_sure = 0
        kullanilan_videolar = set()

        while toplam_sure < hedef_sure_with_margin:
            kullanilabilir = [v for v in karisik_havuz if v['ad'] not in kullanilan_videolar]

            if not kullanilabilir:
                kullanilan_videolar.clear()
                kullanilabilir = karisik_havuz.copy()
                random.shuffle(kullanilabilir)
                print(f"   🔄 Tüm videolar kullanıldı, yeniden karıştırılıyor...")

            secilen = kullanilabilir[0]
            secilen_videolar.append(secilen.copy())
            kullanilan_videolar.add(secilen['ad'])
            toplam_sure += secilen['sure']

            kullanim = sum(1 for v in secilen_videolar if v['ad'] == secilen['ad'])
            print(
                f"   {'✓' if kullanim == 1 else '↻'} {secilen['ad'][:50]} ({sure_formatla(secilen['sure'])}) {f'[x{kullanim}]' if kullanim > 1 else ''}")

    else:
        print(f"   ⚠️  Az video ({len(karisik_havuz)} < {max_varyasyon})")
        print(f"   ✅ Strateji: AKILLI TEKRAR (dengeli dağılım)")

        secilen_videolar = []
        toplam_sure = 0

        ortalama_video_suresi = sum(v['sure'] for v in karisik_havuz) / len(karisik_havuz)
        tahmini_video_sayisi = int(hedef_sure_with_margin / ortalama_video_suresi) + 1

        kullanim_sayaci = {v['ad']: 0 for v in karisik_havuz}

        while toplam_sure < hedef_sure_with_margin:
            min_kullanim = min(kullanim_sayaci.values())
            en_az_kullanilanlar = [v for v in karisik_havuz if kullanim_sayaci[v['ad']] == min_kullanim]

            secilen = random.choice(en_az_kullanilanlar)
            secilen_videolar.append(secilen.copy())
            kullanim_sayaci[secilen['ad']] += 1
            toplam_sure += secilen['sure']

            print(f"   ✓ {secilen['ad'][:50]} ({sure_formatla(secilen['sure'])}) [x{kullanim_sayaci[secilen['ad']]}]")

    random.shuffle(secilen_videolar)
    print(f"   🔀 Son karıştırma yapıldı!")

    # Calculate expected duration after transitions
    gercek_transition_sayisi = max(0, len(secilen_videolar) - 1)
    gercek_transition_kaybi = gercek_transition_sayisi * TRANSITION_EFFECTS.get('overlap_duration', 1.0)
    beklenen_final_sure = toplam_sure - gercek_transition_kaybi

    print(f"\n   📊 SONUÇ:")
    print(f"      • {len(secilen_videolar)} video seçildi")
    print(f"      • Ham toplam: {sure_formatla(toplam_sure)}")
    print(f"      • Transition kaybı: -{gercek_transition_kaybi:.0f}s ({gercek_transition_sayisi} geçiş)")
    print(f"      • Beklenen final: {sure_formatla(beklenen_final_sure)} ✅")
    print(f"      • {len(set(v['ad'] for v in secilen_videolar))} farklı video")
    print(f"   🎉 Her çalıştırmada FARKLI kombinasyon garantili!")

    return secilen_videolar


# ==================== WHISPER SUBTITLE ====================

def otomatik_altyazi_olustur(ses_dosyasi, subtitle_config):
    """Whisper AI ile ses dosyasından altyazı oluştur - GPU destekli"""
    if not subtitle_config or subtitle_config.get('mode') != 'auto':
        return subtitle_config

    print(f"\n🤖 Whisper AI ile altyazı oluşturuluyor...")

    try:
        # ✅ Suppress Triton kernel warnings (harmless fallback)
        import warnings
        warnings.filterwarnings("ignore", message="Failed to launch Triton kernels")

        import whisper
        import torch

        # Check CUDA availability AND compatibility
        cuda_available = torch.cuda.is_available()
        device = "cpu"  # Default to CPU

        if cuda_available:
            try:
                # Test if GPU actually works with PyTorch
                gpu_name = torch.cuda.get_device_name(0)
                test_tensor = torch.zeros(1, device="cuda")
                del test_tensor
                device = "cuda"
                print(f"   🚀 GPU tespit edildi! (CUDA)")
                print(f"   🎮 GPU: {gpu_name}")
                print(f"   ⚡ Whisper 10-20x hızlandırılacak!")
            except Exception as e:
                # GPU exists but PyTorch doesn't support its architecture (e.g., RTX 50 series)
                gpu_name = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "Unknown"
                print(f"   ⚠️  GPU tespit edildi: {gpu_name}")
                print(f"   ⚠️  PyTorch bu GPU mimarisini desteklemiyor!")
                print(f"   💻 Whisper CPU modunda çalışacak")
                print(f"   💡 FFmpeg NVENC hala GPU kullanacak (render hızlı olacak)")
                print(f"   💡 RTX 50 serisi için PyTorch 2.7+ gerekli:")
                print(f"      pip install --upgrade torch --index-url https://download.pytorch.org/whl/cu124")
                device = "cpu"

        if device == "cuda":
            compute_type = "float16"
        else:
            # Only show generic CPU message if CUDA wasn't even available
            # (Don't duplicate if we already showed RTX 50 series fallback message)
            if not cuda_available:
                print(f"   💻 CPU kullanılacak (yavaş olabilir)")
                print(f"   ⚠️  PyTorch CUDA desteği bulunamadı!")
                print(f"   💡 GPU için: pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124")
            compute_type = "float32"

            model_name = subtitle_config.get('auto_model', 'base')
            if model_name in ['large', 'medium']:
                print(f"\n   ⚠️  UYARI: '{model_name}' modeli CPU'da çok yavaş!")
                print(f"   💡 Önerilen: 'base' veya 'small' modeli")
                devam = input(f"   📝 Devam edilsin mi? [e/h]: ").strip().lower()
                if devam != 'e':
                    print(f"   ❌ Altyazı iptal edildi")
                    return None

        model_name = subtitle_config.get('auto_model', 'base')
        print(f"   📥 Model yükleniyor: {model_name}... ({device.upper()})")
        model = whisper.load_model(model_name, device=device)

        print(f"   🎤 Ses tanıma yapılıyor...")
        print(f"   ⏳ Bu işlem birkaç dakika sürebilir...")

        language = subtitle_config.get('auto_language')

        result = model.transcribe(
            ses_dosyasi,
            language=language,
            word_timestamps=True,
            verbose=False,
            fp16=(device == "cuda"),
        )

        segments = []
        max_words = subtitle_config.get('max_words_per_line', 8)
        min_duration = subtitle_config.get('min_duration', 1.5)

        current_segment = {
            'start': 0,
            'end': 0,
            'text': '',
            'words': []
        }
        word_count = 0

        for segment in result['segments']:
            if 'words' in segment:
                for word_info in segment['words']:
                    word = word_info['word'].strip()
                    start = word_info['start']
                    end = word_info['end']

                    if word_count == 0:
                        current_segment['start'] = start

                    current_segment['words'].append({
                        'text': word,
                        'start': start,
                        'end': end
                    })
                    current_segment['end'] = end
                    word_count += 1

                    if word_count >= max_words or (end - current_segment['start']) >= 5:
                        current_segment['text'] = ' '.join([w['text'] for w in current_segment['words']])

                        if (current_segment['end'] - current_segment['start']) >= min_duration:
                            segments.append(current_segment.copy())

                        current_segment = {
                            'start': 0,
                            'end': 0,
                            'text': '',
                            'words': []
                        }
                        word_count = 0

        if current_segment['words']:
            current_segment['text'] = ' '.join([w['text'] for w in current_segment['words']])
            if (current_segment['end'] - current_segment['start']) >= min_duration:
                segments.append(current_segment)

        subtitle_config['segments'] = segments

        print(f"   ✅ {len(segments)} altyazı segmenti oluşturuldu!")
        print(f"   📝 Toplam süre: {sure_formatla(result['segments'][-1]['end'] if result['segments'] else 0)}")
        print(f"   📝 İlk segment: '{segments[0]['text'][:60]}...'")

        full_text = ' '.join([seg['text'] for seg in segments])
        subtitle_config['text'] = full_text

        return subtitle_config

    except ImportError as e:
        logger.error("Whisper veya torch kurulu değil!")
        print(f"\n   ❌ Gerekli kütüphaneler kurulu değil!")
        print(f"   💡 Kurulum:")
        print(f"      pip install openai-whisper")
        print(f"      pip install torch")
        return None
    except KeyboardInterrupt:
        print(f"\n\n   ⚠️  İşlem kullanıcı tarafından iptal edildi")
        return None
    except Exception as e:
        logger.error(f"Whisper hatası: {e}")
        print(f"\n   ❌ Altyazı oluşturma hatası: {e}")
        import traceback
        traceback.print_exc()
        return None


def altyazi_srt_olustur(subtitle_config, temp_klasor):
    """Altyazı segmentlerinden ASS dosyası oluştur - 🎨 Hikaye Kanalları Stiller"""
    if not subtitle_config or not subtitle_config.get('segments'):
        return None

    segment_count = len(subtitle_config['segments'])

    # 🎨 NEW: Simple, readable subtitle styles (FFmpeg-safe)
    try:
        from subtitle_styles import generate_ass_subtitle, get_available_styles, get_style_names, get_style_description
        styles_available = True
        available_styles = get_style_names()
        logger.info(f"🎨 Available styles: {', '.join(available_styles)}")
    except ImportError:
        styles_available = False
        logger.warning("⚠️  subtitle_styles.py not found - using fallback")

    if subtitle_config.get('mode') == 'auto':
        # 🎨 NEW SYSTEM: Use subtitle_styles for clean, readable subtitles
        if styles_available:
            # Import interactive selectors
            from subtitle_styles import interactive_style_selector, interactive_highlight_color_selector

            # Let user choose style interactively (or use configured default)
            configured_style = subtitle_config.get('style', 'tiktok')
            configured_color = subtitle_config.get('highlight_color', 'yellow')

            # 🎯 INTERACTIVE MENU: User chooses from 40+ styles
            try:
                chosen_style = interactive_style_selector(default_style=configured_style)
            except Exception as e:
                logger.warning(f"Style selector failed: {e}, using default")
                chosen_style = configured_style

            # Validate style
            if chosen_style not in available_styles:
                print(f"\n   ⚠️  Style '{chosen_style}' bulunamadı, 'tiktok' kullanılıyor")
                chosen_style = 'tiktok'

            # 🎨 INTERACTIVE MENU: User chooses highlight color
            try:
                chosen_color = interactive_highlight_color_selector(default_color=configured_color)
            except Exception as e:
                logger.warning(f"Color selector failed: {e}, using default")
                chosen_color = configured_color

            # Generate ASS file with chosen style and color
            try:
                ass_dosya = generate_ass_subtitle(
                    subtitle_config['segments'],
                    style_name=chosen_style,
                    temp_folder=temp_klasor,
                    highlight_color=chosen_color
                )
                logger.info(f"✅ ASS dosyası oluşturuldu: {segment_count} segment ({chosen_style} style, {chosen_color} color)")
                return ass_dosya
            except Exception as e:
                logger.error(f"ASS generation failed: {e}")
                print(f"   ❌ Yeni stil sistemi hata verdi, fallback'e geçiliyor...")
                # Fall through to legacy system

        # 🔙 FALLBACK: Legacy system (if styles not available or error)
        ass_dosya = os.path.join(temp_klasor, 'subtitles.ass')

        try:
            # FONT FIX: subtitle_config'den seçilen fontu kullan
            fontname = subtitle_config.get('font', 'Arial Black')

            # FFmpeg uyumlu font ismi yap
            fontname = fontname.replace('-', ' ')

            fontsize = subtitle_config.get('fontsize', 72)

            # ✅ FIX: Maksimum font size 75 (80 → 75, ekran taşmasını önler)
            if fontsize < 68:
                fontsize = 68
            elif fontsize > 75:
                fontsize = 75

            outline = subtitle_config.get('outline_width', 3)
            if outline < 4:
                outline = 4

            # Position, Alignment, MarginV sabit
            position = 'bottom'
            alignment = 2
            marginv = 180

            with open(ass_dosya, 'w', encoding='utf-8') as f:
                f.write("[Script Info]\n")
                f.write("ScriptType: v4.00+\n")
                f.write("WrapStyle: 2\n")
                f.write("ScaledBorderAndShadow: yes\n")
                f.write("YCbCr Matrix: TV.709\n")
                f.write("PlayResX: 1920\n")
                f.write("PlayResY: 1080\n")
                f.write("\n")

                f.write("[V4+ Styles]\n")
                f.write(
                    "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n")

                # ✅ FIX: MarginL ve MarginR - Center için de margin ekle (taşma önleme)
                if alignment in [2, 6, 10]:  # Center
                    marginl = 200  # ✅ 0 → 200 (kenarlardan uzak tut)
                    marginr = 200  # ✅ 0 → 200
                elif alignment in [1, 5, 9]:  # Left
                    marginl = 200  # ✅ 150 → 200
                    marginr = 100  # ✅ 50 → 100
                elif alignment in [3, 7, 11]:  # Right
                    marginl = 100  # ✅ 50 → 100
                    marginr = 200  # ✅ 150 → 200
                else:
                    marginl = 200
                    marginr = 200

                f.write(
                    f"Style: Default,{fontname},{fontsize},&H00FFFFFF,&H0000FFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,{outline},3,{alignment},{marginl},{marginr},{marginv},1\n\n")

                f.write("[Events]\n")
                f.write("Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")

                segment_index = 0
                for segment in subtitle_config['segments']:
                    start_time = segment['start']
                    end_time = segment['end']
                    text = segment['text']
                    words = segment.get('words', [])

                    if words and len(words) > 0 and isinstance(words[0], dict):
                        word_list = []
                        # 🔴 FİX: Segment başlangıç zamanını al
                        segment_start = start_time
                        prev_word_end = 0.0  # Önceki kelimenin bitiş zamanı

                        for i, word_info in enumerate(words):
                            word_text = word_info['text'].upper()
                            word_start = word_info['start']
                            word_end = word_info['end']

                            # 🔴 FİX: Kelime zamanlarını segment başlangıcına göre relative yap
                            # Whisper absolute zamanlar veriyor, ASS relative istiyor!
                            relative_start = word_start - segment_start
                            relative_end = word_end - segment_start

                            word_duration = relative_end - relative_start

                            # 🆕 FİX: Kelimeler arası boşluğu (gap) hesapla
                            # ASS karaoke'de \k süresi bir önceki kelimeden bu kelimeye kadar geçen süre
                            if i == 0:
                                # İlk kelime - başlangıç gecikmesi + kelime süresi
                                gap = relative_start  # Segment başından ilk kelimeye kadar
                            else:
                                # Sonraki kelimeler - önceki kelimenin bitişinden bu kelimenin başına kadar
                                gap = relative_start - prev_word_end

                            # Gap negatif olamaz (kelimeler örtüşüyorsa)
                            gap = max(0, gap)

                            # Karaoke timing = gap + kelime süresi
                            total_duration = gap + word_duration
                            duration_cs = int(total_duration * 100)

                            word_list.append({
                                'text': word_text,
                                'duration': max(duration_cs, 10),
                                'start': relative_start,
                                'end': relative_end
                            })

                            prev_word_end = relative_end  # Bu kelimenin bitişini kaydet

                        # 🆕 DİNAMİK: Font'a göre maksimum karakter sayısı hesapla
                        MAX_CHARS_PER_LINE = calculate_max_chars_dynamic(fontname, fontsize, outline)

                        logger.info(f"      🔢 Karaoke limit: {MAX_CHARS_PER_LINE} karakter ({fontname} {fontsize}pt)")

                        # 🔙 LEGACY: Basic karaoke (simple, reliable)
                        if len(word_list) > 8:
                            # Karakter sayısını kontrol ederek en iyi bölme noktasını bul
                            best_split = len(word_list) // 2
                            min_diff = float('inf')

                            for i in range(1, len(word_list)):
                                # Test satırları oluştur
                                line1_test = ' '.join([w['text'] for w in word_list[:i]])
                                line2_test = ' '.join([w['text'] for w in word_list[i:]])

                                len1 = len(line1_test)
                                len2 = len(line2_test)

                                # Her iki satır da limite uyuyorsa ve dengeli ise
                                if len1 <= MAX_CHARS_PER_LINE and len2 <= MAX_CHARS_PER_LINE:
                                    diff = abs(len1 - len2)
                                    if diff < min_diff:
                                        min_diff = diff
                                        best_split = i

                            # Eğer hiçbir split uygun değilse, kelimeleri kısalt
                            if min_diff == float('inf'):
                                # Çok uzun - kelime sayısını azalt
                                target_words = 6  # Her satıra max 3 kelime
                                word_list = word_list[:target_words]
                                best_split = 3

                            line1_words = word_list[:best_split]
                            line2_words = word_list[best_split:]

                            line1_text = ""
                            for word_data in line1_words:
                                line1_text += f"{{\\k{word_data['duration']}}}{word_data['text']} "
                            line1_text = line1_text.strip()

                            line2_text = ""
                            for word_data in line2_words:
                                line2_text += f"{{\\k{word_data['duration']}}}{word_data['text']} "
                            line2_text = line2_text.strip()

                            final_text = f"{line1_text}\\N{line2_text}"
                        else:
                            # 8 veya daha az kelime: tek satır
                            final_text = ""
                            for word_data in word_list:
                                final_text += f"{{\\k{word_data['duration']}}}{word_data['text']} "
                            final_text = final_text.strip()

                            # ✅ FIX: Tek satır da çok uzunsa kes
                            if len(final_text.replace('{\\k', '').replace('}', '')) > MAX_CHARS_PER_LINE * 1.5:
                                # İlk 4-5 kelimeyi al
                                word_list = word_list[:5]
                                final_text = ""
                                for word_data in word_list:
                                    final_text += f"{{\\k{word_data['duration']}}}{word_data['text']} "
                                final_text = final_text.strip()

                    else:
                        # Karaoke yok, basit metin
                        final_text = text.upper()

                        # 🆕 DİNAMİK: Font bilgisi ile akıllı satır kırma
                        final_text = akilli_satir_kir(
                            final_text,
                            max_lines=2,
                            font_name=fontname,
                            font_size=fontsize,
                            outline_width=outline
                        )

                    def format_ass_time(seconds):
                        hours = int(seconds // 3600)
                        minutes = int((seconds % 3600) // 60)
                        secs = int(seconds % 60)
                        centis = int((seconds % 1) * 100)
                        return f"{hours}:{minutes:02d}:{secs:02d}.{centis:02d}"

                    start_str = format_ass_time(start_time)
                    end_str = format_ass_time(end_time)

                    if segment_index < 2 and words:
                        logger.info(f"Segment {segment_index}: {start_str}-{end_str}, {len(words)} words")
                        if len(words) > 0 and isinstance(words[0], dict):
                            logger.info(f"  First word: '{words[0]['text']}' ({words[0]['start']}-{words[0]['end']})")

                    f.write(f"Dialogue: 0,{start_str},{end_str},Default,,0,0,0,,{final_text}\n")

                    segment_index += 1

            logger.info(f"ASS dosyası oluşturuldu: {segment_count} segment (karaoke precise timing 🎤)")
            return ass_dosya

        except Exception as e:
            logger.error(f"ASS dosyası oluşturma hatası: {e}")
            return None

    return None


# ==================== DİNAMİK ALTYAZI SİSTEMİ ====================

def emoji_ekle(text, emoji_config):
    """Metne bağlama uygun emoji ekle"""
    if not emoji_config or not emoji_config.get('enabled'):
        return text

    if not emoji_config.get('auto_detect'):
        return text

    emoji_map = emoji_config.get('emoji_map', {})
    text_lower = text.lower()

    added_emoji = None
    for pattern, emoji in emoji_map.items():
        keywords = pattern.split('|')
        for keyword in keywords:
            if keyword in text_lower:
                added_emoji = emoji
                break
        if added_emoji:
            break

    if added_emoji:
        position = emoji_config.get('position', 'end')
        spacing = ' ' if emoji_config.get('spacing', True) else ''

        if position == 'start':
            return f"{added_emoji}{spacing}{text}"
        elif position == 'end':
            return f"{text}{spacing}{added_emoji}"
        elif position == 'both':
            return f"{added_emoji}{spacing}{text}{spacing}{added_emoji}"

    return text


def akilli_satir_kir(text, max_chars_per_line=30, max_lines=2, font_name=None, font_size=None, outline_width=None):
    """
    Metni akıllıca satırlara böl
    - Maksimum 2 satır (3+ satır = okunmaz)
    - Her satırda dengeli kelime dağılımı
    - Çok uzun metinleri kısalt
    - 🆕 DİNAMİK: Font bilgisi varsa gerçek hesaplama yapar

    Args:
        text: Metin
        max_chars_per_line: Maksimum karakter (varsayılan veya dinamik hesaplanan)
        max_lines: Maksimum satır sayısı
        font_name: Font adı (dinamik hesaplama için)
        font_size: Font boyutu (dinamik hesaplama için)
        outline_width: Outline genişliği (dinamik hesaplama için)
    """
    # 🆕 DİNAMİK HESAPLAMA: Font bilgisi varsa gerçek limit hesapla
    if font_name and font_size and outline_width:
        max_chars_per_line = calculate_max_chars_dynamic(font_name, font_size, outline_width)
        logger.info(f"   🔢 Dinamik limit: {max_chars_per_line} karakter ({font_name} {font_size}pt)")

    # Temiz metni al (tag'ler olmadan)
    clean_text = text

    # Kelime kelime ayır
    words = clean_text.split()

    if not words:
        return text

    # Toplam karakter sayısı
    total_chars = len(clean_text)

    # Tek satıra sığıyorsa direkt döndür
    if total_chars <= max_chars_per_line:
        return text

    # Çok uzunsa kısalt (3+ satır = okunmaz!)
    if total_chars > (max_chars_per_line * max_lines):
        # Kelime sayısını azalt
        target_words = int((max_chars_per_line * max_lines) / (total_chars / len(words)))
        if target_words < len(words):
            words = words[:target_words]
            # Son kelimeye "..." ekle
            if len(words) > 0:
                words[-1] = words[-1] + "..."

    # 2 satıra böl - dengeli dağılım
    if len(words) <= 3:
        # Çok az kelime, tek satır
        return ' '.join(words)

    # En dengeli bölünme noktasını bul
    best_split = len(words) // 2
    min_diff = float('inf')

    for i in range(1, len(words)):
        line1 = ' '.join(words[:i])
        line2 = ' '.join(words[i:])

        # Her satırın karakter sayısı
        len1 = len(line1)
        len2 = len(line2)

        # İki satır arasındaki fark
        diff = abs(len1 - len2)

        # Her iki satır da limite uyuyorsa ve daha dengeli ise
        if len1 <= max_chars_per_line and len2 <= max_chars_per_line:
            if diff < min_diff:
                min_diff = diff
                best_split = i

    # En iyi noktadan böl
    line1 = ' '.join(words[:best_split])
    line2 = ' '.join(words[best_split:])

    return f"{line1}\\N{line2}"


def renk_kodla_kelime(word, color_config):
    """Kelimeye renk kodu uygula (duygu bazlı)"""
    if not color_config or not color_config.get('enabled'):
        return word, '&H00FFFFFF'  # Varsayılan beyaz

    word_lower = word.lower()

    # Emphasis words kontrolü
    emphasis = color_config.get('modes', {}).get('emphasis_words', {})
    if emphasis.get('enabled'):
        keywords = emphasis.get('keywords', [])
        for keyword in keywords:
            if keyword in word_lower:
                color = emphasis.get('highlight_color', '&H0000FFFF')
                if emphasis.get('uppercase'):
                    word = word.upper()
                return word, color

    # Emotion bazlı renklendirme
    emotion_mode = color_config.get('modes', {}).get('emotion_based', {})
    if emotion_mode.get('enabled'):
        sentiment_keywords = emotion_mode.get('sentiment_keywords', {})
        colors = emotion_mode.get('colors', {})

        # Pozitif kelimeler
        for pos_word in sentiment_keywords.get('positive', []):
            if pos_word in word_lower:
                return word, colors.get('positive', '&H0000FF00')

        # Negatif kelimeler
        for neg_word in sentiment_keywords.get('negative', []):
            if neg_word in word_lower:
                return word, colors.get('negative', '&H000000FF')

        # Önemli kelimeler
        for imp_word in sentiment_keywords.get('important', []):
            if imp_word in word_lower:
                return word, colors.get('important', '&H0000FFFF')

        # Soru işareti varsa
        if '?' in word:
            return word, colors.get('question', '&H00FFFF00')

    return word, '&H00FFFFFF'  # Varsayılan beyaz


def animasyon_secimi(animations_config):
    """Rastgele animasyon stili seç"""
    if not animations_config or not animations_config.get('enabled'):
        return None

    styles = animations_config.get('styles', {})
    enabled_styles = []
    probabilities = []

    for style_name, style_data in styles.items():
        if style_data.get('enabled', False):
            enabled_styles.append((style_name, style_data))
            probabilities.append(style_data.get('probability', 0.1))

    if not enabled_styles:
        return None

    # Normalize probabilities
    total = sum(probabilities)
    if total > 0:
        probabilities = [p / total for p in probabilities]

    import random
    chosen_style = random.choices(enabled_styles, weights=probabilities, k=1)[0]

    return chosen_style


def ass_animasyon_tag_olustur(animation_name, animation_data):
    """ASS formatında animasyon tag'i oluştur"""
    tags = []

    if animation_name == 'fade_in':
        duration = int(animation_data.get('duration', 0.3) * 1000)  # ms
        tags.append(f"\\fad({duration},0)")

    elif animation_name == 'slide_up':
        distance = animation_data.get('distance', 30)
        duration = int(animation_data.get('duration', 0.4) * 1000)
        tags.append(f"\\move(0,{distance},0,0,0,{duration})")

    elif animation_name == 'bounce':
        # Bounce efekti için basit move animasyonu
        height = animation_data.get('height', 15)
        duration = int(animation_data.get('duration', 0.5) * 1000)
        tags.append(f"\\t(0,{duration // 2},\\fry360)\\t({duration // 2},{duration},\\fry0)")

    elif animation_name == 'scale_pulse':
        scale = animation_data.get('scale', 1.1)
        duration = int(animation_data.get('duration', 0.3) * 1000)
        scale_percent = int((scale - 1) * 100)
        tags.append(
            f"\\t(0,{duration // 2},\\fscx{100 + scale_percent}\\fscy{100 + scale_percent})\\t({duration // 2},{duration},\\fscx100\\fscy100)")

    return ''.join(tags)


def background_tag_olustur(background_config):
    """ASS formatında arka plan tag'i oluştur"""
    if not background_config or not background_config.get('enabled'):
        return ''

    import random
    styles = background_config.get('styles', {})

    # Olasılıklara göre stil seç
    available_styles = []
    probabilities = []

    for style_name, style_data in styles.items():
        if style_data.get('enabled', False):
            available_styles.append((style_name, style_data))
            probabilities.append(style_data.get('probability', 0.1))

    if not available_styles:
        return ''

    chosen_style = random.choices(available_styles, weights=probabilities, k=1)[0]
    style_name, style_data = chosen_style

    tags = []

    if style_name == 'box':
        # Border ve shadow ile kutu efekti
        padding = style_data.get('padding', 20)
        tags.append(f"\\bord{padding // 4}\\shad{padding // 6}")

    elif style_name == 'highlight_bar':
        # Daha az padding ile bar efekti
        tags.append("\\bord8\\shad4")

    elif style_name == 'outline':
        width = style_data.get('width', 4)
        shadow_offset = style_data.get('shadow_offset', 2) if style_data.get('shadow', True) else 0
        tags.append(f"\\bord{width}\\shad{shadow_offset}")

    return ''.join(tags)


def dinamik_altyazi_ass_olustur(subtitle_config, dynamic_config, temp_klasor, platform='youtube_standard'):
    """
    Gelişmiş dinamik altyazı sistemi
    - Karaoke efekti (kelime kelime vurgulama)
    - Emoji ekleme
    - Renk kodlama
    - Animasyonlar
    - Arka plan efektleri
    """
    if not subtitle_config or not subtitle_config.get('segments'):
        return None

    # Platform preset uygula - ✅ FİX: TÜM AYARLARI UYGULA!
    platform_presets = dynamic_config.get('platform_presets', {})
    preset_position = None
    preset_marginv = None

    if platform in platform_presets:
        preset = platform_presets[platform]
        # Preset ayarlarını uygula
        typography = dynamic_config.get('typography', {})
        typography['font_size'] = preset.get('font_size', typography.get('font_size', 76))

        # Position ve margin_vertical'i preset'ten al
        if 'position' in preset:
            preset_position = preset['position']
        if 'margin_vertical' in preset:
            preset_marginv = preset['margin_vertical']

    segments = subtitle_config['segments']
    ass_dosya = os.path.join(temp_klasor, 'dynamic_subtitles.ass')

    try:
        # Tipografi ayarları
        typography = dynamic_config.get('typography', {})

        # FONT FIX: subtitle_config'den seçilen fontu kullan
        if subtitle_config.get('font'):
            fontname = subtitle_config['font']
        else:
            fontname = typography.get('font_family', 'Arial Black')

        # FFmpeg uyumlu font ismi yap
        fontname = fontname.replace('-', ' ')

        # Font boyutu
        if subtitle_config.get('fontsize'):
            fontsize = subtitle_config['fontsize']
        else:
            fontsize = typography.get('font_size', 76)

        # Positioning - POZİSYON FIX
        positioning = dynamic_config.get('positioning', {})

        # ✅ FİX: Preset varsa onu kullan, yoksa config'den al
        position = preset_position if preset_position else positioning.get('default_position', 'bottom')
        marginv = preset_marginv if preset_marginv is not None else positioning.get('margin', {}).get('vertical', 150)

        # YouTube yatay video için sabit değerler
        position = 'bottom'
        if marginv > 300:
            marginv = 180

        # Alignment - ALT/ÜST FIX
        # 1=sol alt, 2=orta alt, 3=sağ alt
        # 5=sol orta, 6=orta orta, 7=sağ orta
        # 9=sol üst, 10=orta üst, 11=sağ üst
        alignment_base_map = {
            'left': 1,
            'center': 2,
            'right': 3
        }
        base_alignment = alignment_base_map.get(positioning.get('alignment', 'center'), 2)

        # Pozisyona göre alignment ayarla
        if position == 'bottom':
            alignment = base_alignment  # 1, 2, 3 (alt)
        elif position == 'center':
            alignment = base_alignment + 4  # 5, 6, 7 (orta)
        else:  # top
            alignment = base_alignment + 8  # 9, 10, 11 (üst)

        # YouTube yatay için sabit alignment=2 (orta alt)
        alignment = 2

        # Karaoke config
        karaoke_config = dynamic_config.get('karaoke', {})
        karaoke_enabled = karaoke_config.get('enabled', True)
        highlight_color = karaoke_config.get('highlight_color', '&H00FFFF00')  # Sarı
        normal_color = karaoke_config.get('normal_color', '&H00FFFFFF')  # Beyaz

        # Emoji config
        emoji_config = dynamic_config.get('emoji', {})

        # Color coding config
        color_config = dynamic_config.get('color_coding', {})

        # Animation config
        animations_config = dynamic_config.get('animations', {})

        # Background config
        background_config = dynamic_config.get('background', {})

        with open(ass_dosya, 'w', encoding='utf-8') as f:
            # Header
            f.write("[Script Info]\n")
            f.write("Title: Dynamic Subtitles\n")
            f.write("ScriptType: v4.00+\n")
            f.write("WrapStyle: 2\n")
            f.write("ScaledBorderAndShadow: yes\n")
            f.write("YCbCr Matrix: TV.709\n")
            f.write("PlayResX: 1920\n")
            f.write("PlayResY: 1080\n")
            f.write("\n")

            # Styles
            f.write("[V4+ Styles]\n")
            f.write(
                "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n")

            # Default style
            outline_width = 4
            shadow_width = 3
            f.write(
                f"Style: Default,{fontname},{fontsize},{normal_color},&H0000FFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,{outline_width},{shadow_width},{alignment},100,100,{marginv},1\n")

            # Karaoke highlight style
            f.write(
                f"Style: Highlight,{fontname},{fontsize},{highlight_color},&H0000FFFF,&H00000000,&H80000000,-1,0,0,0,110,110,0,0,1,{outline_width},{shadow_width},{alignment},100,100,{marginv},1\n")

            f.write("\n[Events]\n")
            f.write("Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")

            # Segments
            for segment in segments:
                start_time = segment['start']
                end_time = segment['end']
                text = segment['text']
                words = segment.get('words', [])

                # Emoji ekle
                text_with_emoji = emoji_ekle(text, emoji_config)

                # Animasyon seç
                animation = animasyon_secimi(animations_config)
                animation_tags = ''
                if animation:
                    anim_name, anim_data = animation
                    animation_tags = ass_animasyon_tag_olustur(anim_name, anim_data)

                # Background tags
                bg_tags = background_tag_olustur(background_config)

                def format_ass_time(seconds):
                    hours = int(seconds // 3600)
                    minutes = int((seconds % 3600) // 60)
                    secs = int(seconds % 60)
                    centis = int((seconds % 1) * 100)
                    return f"{hours}:{minutes:02d}:{secs:02d}.{centis:02d}"

                start_str = format_ass_time(start_time)
                end_str = format_ass_time(end_time)

                # Karaoke effect oluştur
                if karaoke_enabled and words and len(words) > 0:
                    # 🔴 FİX: Segment başlangıç zamanını al
                    segment_start = start_time
                    prev_word_end = 0.0  # Önceki kelimenin bitiş zamanı

                    # Kelime listesi oluştur
                    word_list = []
                    for i, word_info in enumerate(words):
                        word_text = word_info['text']
                        word_start = word_info['start']
                        word_end = word_info['end']

                        # 🔴 FİX: Kelime zamanlarını segment başlangıcına göre relative yap
                        # Whisper absolute zamanlar veriyor, ASS karaoke relative istiyor!
                        relative_start = word_start - segment_start
                        relative_end = word_end - segment_start

                        # Renk kodlama
                        colored_word, word_color = renk_kodla_kelime(word_text, color_config)

                        # Word duration in centiseconds (relative değerlerle)
                        word_duration = relative_end - relative_start

                        # 🆕 FİX: Kelimeler arası boşluğu (gap) hesapla
                        # ASS karaoke'de \k süresi bir önceki kelimeden bu kelimeye kadar geçen süre
                        if i == 0:
                            # İlk kelime - başlangıç gecikmesi + kelime süresi
                            gap = relative_start
                        else:
                            # Sonraki kelimeler - önceki kelimenin bitişinden bu kelimenin başına kadar
                            gap = relative_start - prev_word_end

                        # Gap negatif olamaz (kelimeler örtüşüyorsa)
                        gap = max(0, gap)

                        # Karaoke timing = gap + kelime süresi
                        total_duration = gap + word_duration
                        duration_cs = int(total_duration * 100)
                        duration_cs = max(duration_cs, 10)  # Minimum 10cs

                        word_list.append({
                            'text': colored_word,
                            'color': word_color,
                            'duration': duration_cs
                        })

                        prev_word_end = relative_end  # Bu kelimenin bitişini kaydet

                    # 🆕 DİNAMİK: Font'a göre maksimum karakter sayısı hesapla
                    MAX_CHARS_PER_LINE = calculate_max_chars_dynamic(fontname, fontsize, outline_width)

                    logger.info(
                        f"      🔢 Dinamik karaoke limit: {MAX_CHARS_PER_LINE} karakter ({fontname} {fontsize}pt)")

                    # Karaoke text başlat
                    karaoke_text = f"{{{animation_tags}{bg_tags}}}"

                    if len(word_list) > 8:
                        # Karakter sayısını kontrol ederek en iyi bölme noktasını bul
                        best_split = len(word_list) // 2
                        min_diff = float('inf')

                        for i in range(1, len(word_list)):
                            # Test satırları oluştur (renk tag'leri olmadan)
                            line1_test = ' '.join([w['text'] for w in word_list[:i]])
                            line2_test = ' '.join([w['text'] for w in word_list[i:]])

                            len1 = len(line1_test)
                            len2 = len(line2_test)

                            # Her iki satır da limite uyuyorsa ve dengeli ise
                            if len1 <= MAX_CHARS_PER_LINE and len2 <= MAX_CHARS_PER_LINE:
                                diff = abs(len1 - len2)
                                if diff < min_diff:
                                    min_diff = diff
                                    best_split = i

                        # Eğer hiçbir split uygun değilse, kelimeleri kısalt
                        if min_diff == float('inf'):
                            # Çok uzun - kelime sayısını azalt
                            target_words = 6  # Her satıra max 3 kelime
                            word_list = word_list[:target_words]
                            best_split = 3

                        line1_words = word_list[:best_split]
                        line2_words = word_list[best_split:]

                        # Satır 1
                        line1_text = ""
                        for word_data in line1_words:
                            if word_data['color'] != normal_color:
                                line1_text += f"{{\\c{word_data['color']}}}{{\\k{word_data['duration']}}}{word_data['text']} "
                            else:
                                line1_text += f"{{\\k{word_data['duration']}}}{word_data['text']} "

                        # Satır 2
                        line2_text = ""
                        for word_data in line2_words:
                            if word_data['color'] != normal_color:
                                line2_text += f"{{\\c{word_data['color']}}}{{\\k{word_data['duration']}}}{word_data['text']} "
                            else:
                                line2_text += f"{{\\k{word_data['duration']}}}{word_data['text']} "

                        karaoke_text += f"{line1_text.strip()}\\N{line2_text.strip()}"
                    else:
                        # 8 veya daha az kelime: tek satır
                        for word_data in word_list:
                            if word_data['color'] != normal_color:
                                karaoke_text += f"{{\\c{word_data['color']}}}{{\\k{word_data['duration']}}}{word_data['text']} "
                            else:
                                karaoke_text += f"{{\\k{word_data['duration']}}}{word_data['text']} "

                        # ✅ FIX: Tek satır da çok uzunsa kes
                        test_text = ' '.join([w['text'] for w in word_list])
                        if len(test_text) > MAX_CHARS_PER_LINE * 1.5:
                            # İlk 4-5 kelimeyi al
                            word_list = word_list[:5]
                            karaoke_text = f"{{{animation_tags}{bg_tags}}}"
                            for word_data in word_list:
                                if word_data['color'] != normal_color:
                                    karaoke_text += f"{{\\c{word_data['color']}}}{{\\k{word_data['duration']}}}{word_data['text']} "
                                else:
                                    karaoke_text += f"{{\\k{word_data['duration']}}}{word_data['text']} "

                    final_text = karaoke_text.strip()

                else:
                    # Karaoke yok, basit metin
                    # 🆕 DİNAMİK: Font bilgisi ile akıllı satır kırma
                    broken_text = akilli_satir_kir(
                        text_with_emoji,
                        max_lines=2,
                        font_name=fontname,
                        font_size=fontsize,
                        outline_width=outline_width
                    )
                    final_text = f"{{{animation_tags}{bg_tags}}}{broken_text}"

                f.write(f"Dialogue: 0,{start_str},{end_str},Default,,0,0,0,,{final_text}\n")

        logger.info(f"✨ Dinamik ASS altyazı oluşturuldu: {len(segments)} segment")
        logger.info(f"   🎨 Karaoke: {'Aktif' if karaoke_enabled else 'Pasif'}")
        logger.info(f"   😊 Emoji: {'Aktif' if emoji_config.get('enabled') else 'Pasif'}")
        logger.info(f"   🎬 Animasyon: {'Aktif' if animations_config.get('enabled') else 'Pasif'}")

        return ass_dosya

    except Exception as e:
        logger.error(f"Dinamik altyazı hatası: {e}")
        import traceback
        traceback.print_exc()
        return None


# ==================== CACHE SYSTEM ====================

def cache_hash_olustur(video_yolu, varyasyon):
    """Video ve varyasyon için benzersiz hash"""
    video_stat = os.stat(video_yolu)
    cache_data = f"{video_yolu}_{video_stat.st_size}_{video_stat.st_mtime}_{json.dumps(varyasyon, sort_keys=True)}"
    return hashlib.md5(cache_data.encode()).hexdigest()


def cache_kontrol(video_yolu, varyasyon):
    """Cache'de işlenmiş versiyon var mı?"""
    if not os.path.exists(CACHE_KLASORU):
        os.makedirs(CACHE_KLASORU, exist_ok=True)

    cache_hash = cache_hash_olustur(video_yolu, varyasyon)
    cache_dosya = os.path.join(CACHE_KLASORU, f"{cache_hash}.mp4")

    if os.path.exists(cache_dosya) and dosya_gecerli_mi(cache_dosya):
        logger.info(f"✅ Cache hit: {os.path.basename(video_yolu)}")
        return cache_dosya

    return None


def cache_kaydet(islenimis_dosya, video_yolu, varyasyon):
    """İşlenmiş dosyayı cache'e kaydet"""
    try:
        if not os.path.exists(CACHE_KLASORU):
            os.makedirs(CACHE_KLASORU, exist_ok=True)

        cache_hash = cache_hash_olustur(video_yolu, varyasyon)
        cache_dosya = os.path.join(CACHE_KLASORU, f"{cache_hash}.mp4")

        shutil.copy2(islenimis_dosya, cache_dosya)
        logger.debug(f"Cache kaydedildi: {cache_hash}")
        return cache_dosya
    except Exception as e:
        logger.warning(f"Cache kayıt hatası: {e}")
        return None


def cache_temizle(max_size_gb=5):
    """Cache boyutunu sınırla"""
    try:
        if not os.path.exists(CACHE_KLASORU):
            return

        total_size = sum(
            os.path.getsize(os.path.join(CACHE_KLASORU, f))
            for f in os.listdir(CACHE_KLASORU)
        )

        max_size = max_size_gb * 1024 * 1024 * 1024

        if total_size > max_size:
            files = []
            for f in os.listdir(CACHE_KLASORU):
                path = os.path.join(CACHE_KLASORU, f)
                files.append((path, os.path.getmtime(path)))

            files.sort(key=lambda x: x[1])

            while total_size > max_size * 0.8 and files:
                oldest = files.pop(0)
                size = os.path.getsize(oldest[0])
                os.remove(oldest[0])
                total_size -= size
    except Exception as e:
        logger.warning(f"Cache temizlik hatası: {e}")


# ==================== PROGRESS TRACKING ====================

def ilerleme_kaydet(playlist_index, toplam, cikti_adi):
    """İlerlemeyi kaydet"""
    try:
        progress_data = {
            'timestamp': datetime.now().isoformat(),
            'playlist_index': playlist_index,
            'toplam': toplam,
            'cikti_adi': cikti_adi,
        }
        with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
            json.dump(progress_data, f, indent=2)
    except Exception as e:
        logger.warning(f"İlerleme kayıt hatası: {e}")


def ilerleme_yukle():
    """Kaydedilmiş ilerlemeyi yükle"""
    try:
        if os.path.exists(PROGRESS_FILE):
            with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except:
        pass
    return None


def ilerleme_temizle():
    """İlerleme dosyasını sil"""
    try:
        if os.path.exists(PROGRESS_FILE):
            os.remove(PROGRESS_FILE)
    except:
        pass


# ==================== SCENE DETECTION ====================

def sahne_tespiti_yap(video_yolu, threshold=None):
    """ffmpeg scene detection ile akıllı segmentasyon"""
    if threshold is None:
        threshold = ADVANCED_CONFIG['min_scene_score']

    logger.info(f"🔍 Sahne tespiti: {os.path.basename(video_yolu)}")

    try:
        komut = [
            FFMPEG_PATH, '-i', video_yolu,
            '-vf', f'select=gt(scene\\,{threshold}),showinfo',
            '-f', 'null', '-'
        ]

        sonuc = subprocess.run(
            komut,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=120
        )

        scene_times = []
        for line in sonuc.stderr.split('\n'):
            if 'pts_time:' in line:
                try:
                    time_str = line.split('pts_time:')[1].split()[0]
                    scene_times.append(float(time_str))
                except:
                    continue

        if scene_times:
            logger.info(f"   ✅ {len(scene_times)} sahne değişimi tespit edildi")
            return sorted(scene_times)

    except Exception as e:
        logger.warning(f"Sahne tespiti hatası: {e}")

    return []


def sahne_bazli_segmentasyon(video_info, temp_klasor, scene_times):
    """Sahne değişimlerine göre segment oluştur"""
    video_yolu = video_info['yol']
    sure = video_info['sure']

    if not scene_times or sure < 10:
        return normal_segmentasyon(video_info, temp_klasor)

    segments = []
    segment_no = 0
    baslangic = 0

    for i, scene_time in enumerate(scene_times):
        if scene_time - baslangic < 4:
            continue

        segment_suresi = min(scene_time - baslangic, 15)

        if segment_suresi > 4:
            segment_dosya = os.path.join(temp_klasor, f"s_{segment_no:04d}.mp4")

            komut = [
                FFMPEG_PATH, '-v', 'error',
                '-i', video_yolu,
                '-ss', str(baslangic),
                '-t', str(segment_suresi),
                '-c', 'copy',
                '-y', segment_dosya
            ]

            subprocess.run(komut, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)

            if dosya_gecerli_mi(segment_dosya):
                segments.append({
                    'dosya': segment_dosya,
                    'sure': segment_suresi,
                    'orijinal_video': video_info['ad']
                })
                segment_no += 1

            baslangic = scene_time

    if sure - baslangic > 4:
        segment_dosya = os.path.join(temp_klasor, f"s_{segment_no:04d}.mp4")
        komut = [
            FFMPEG_PATH, '-v', 'error',
            '-i', video_yolu,
            '-ss', str(baslangic),
            '-c', 'copy',
            '-y', segment_dosya
        ]
        subprocess.run(komut, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)

        if dosya_gecerli_mi(segment_dosya):
            segments.append({
                'dosya': segment_dosya,
                'sure': sure - baslangic,
                'orijinal_video': video_info['ad']
            })

    return segments if segments else normal_segmentasyon(video_info, temp_klasor)


def normal_segmentasyon(video_info, temp_klasor):
    """Normal rastgele segmentasyon"""
    video_yolu = video_info['yol']
    sure = video_info['sure']

    if sure < 10:
        return [{'dosya': video_yolu, 'sure': sure, 'orijinal_video': video_info['ad']}]

    segments = []
    baslangic = 0
    segment_no = 0

    while baslangic < sure:
        segment_suresi = random.uniform(*ADVANCED_CONFIG['segment_duration'])
        segment_suresi = min(segment_suresi, sure - baslangic)

        if segment_suresi < 4:
            break

        segment_dosya = os.path.join(temp_klasor, f"s_{segment_no:04d}.mp4")

        komut = [
            FFMPEG_PATH, '-v', 'error',
            '-i', video_yolu,
            '-ss', str(baslangic),
            '-t', str(segment_suresi),
            '-c', 'copy',
            '-y', segment_dosya
        ]

        subprocess.run(komut, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)

        if dosya_gecerli_mi(segment_dosya):
            segments.append({
                'dosya': segment_dosya,
                'sure': segment_suresi,
                'orijinal_video': video_info['ad']
            })

        baslangic += segment_suresi
        segment_no += 1

    return segments if segments else [{'dosya': video_yolu, 'sure': sure, 'orijinal_video': video_info['ad']}]


def videoyu_segmentlere_bol(video_info, temp_klasor, use_scene_detection=True):
    """Ana segmentasyon fonksiyonu"""
    if use_scene_detection:
        scene_times = sahne_tespiti_yap(video_info['yol'])
        if scene_times:
            return sahne_bazli_segmentasyon(video_info, temp_klasor, scene_times)

    return normal_segmentasyon(video_info, temp_klasor)


# ==================== FINGERPRINT RANDOMIZATION ====================

def fingerprint_parametreleri_olustur(klip_index):
    """Her klip için benzersiz encoding parametreleri"""
    random.seed(hash(f"fingerprint_{klip_index}_{time.time()}"))

    fp_config = FINGERPRINT_CONFIG

    return {
        'gop_size': random.randint(*fp_config['encoding_variance']['gop_size']),
        'keyint': random.randint(*fp_config['encoding_variance']['keyint']),
        'min_keyint': random.randint(*fp_config['encoding_variance']['min_keyint']),
        'bframes': random.randint(*fp_config['encoding_variance']['bframes']),
        'pixel_noise': random.randint(*fp_config['pixel_noise']['strength']) if fp_config['pixel_noise'][
            'enabled'] else 0,
        'micro_pitch': round(random.uniform(*fp_config['audio_fingerprint']['micro_pitch']), 2),
        'use_dither': fp_config['color_space']['dither'],
        'fps_adjust': random.uniform(0.9998, 1.0002) if fp_config['timing']['fps_micro_adjust'] else 1.0,
    }


def fingerprint_video_filtresi(fp_params):
    """Fingerprint video filtreleri"""
    filtreler = []

    try:
        if fp_params['pixel_noise'] > 0:
            filtreler.append(f"noise=alls={fp_params['pixel_noise']}:allf=t")
    except:
        pass

    return filtreler


def fingerprint_audio_filtresi(fp_params):
    """Audio fingerprint filtreleri"""
    filtreler = []

    if abs(fp_params['micro_pitch']) > 0.1:
        semitones = fp_params['micro_pitch']
        rate = 1 + (semitones / 12)
        filtreler.append(f"asetrate=44100*{rate},aresample=44100")

    return filtreler


# ==================== METADATA RANDOMIZATION ====================

def metadata_randomize(video_yolu, cikti_yolu):
    """Gelişmiş metadata randomization"""
    try:
        fake_date = datetime.now() - timedelta(days=random.randint(1, 730))

        encoders = [
            'Lavf60.16.100',
            'Lavf59.27.100',
            'Lavf58.76.100',
            'Lavf61.1.100',
            'HandBrake 1.6.1',
            'HandBrake 1.7.0',
            'FFmpeg 6.0',
            'FFmpeg 5.1.2',
        ]
        fake_encoder = random.choice(encoders)

        import uuid
        fake_uuid = str(uuid.uuid4())

        software_tags = [
            'Adobe Premiere Pro 2023',
            'DaVinci Resolve 18',
            'Final Cut Pro X',
            'Vegas Pro 20',
            '',
        ]
        fake_software = random.choice(software_tags)

        komut = [
            FFMPEG_PATH, '-v', 'error',
            '-i', video_yolu,
            '-map_metadata', '-1',
            '-fflags', '+bitexact',
            '-metadata', f'creation_time={fake_date.isoformat()}Z',
            '-metadata', f'encoder={fake_encoder}',
            '-metadata', 'title=',
            '-metadata', 'artist=',
            '-metadata', 'album=',
            '-metadata', 'comment=',
            '-metadata', 'date=',
            '-metadata', f'handler_name=VideoHandler',
        ]

        if fake_software:
            komut.extend(['-metadata', f'software={fake_software}'])

        komut.extend([
            '-c', 'copy',
            '-y', cikti_yolu
        ])

        subprocess.run(komut, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)

        if dosya_gecerli_mi(cikti_yolu):
            logger.debug(f"Metadata randomized: {fake_encoder}")
            return cikti_yolu

    except Exception as e:
        logger.warning(f"Metadata randomization hatası: {e}")

    return video_yolu


# ==================== PARALLEL PROCESSING ====================

def klip_isle_parallel(args):
    """🆕 Tek bir klibi işle + CAPCUT PLUS EFFECTS + 🌟 STORY FEATURES"""
    item, klip_index, encoder_type, encoder_config, temp_klasor, sessiz_yap, subtitle_config, secilen_efektler, cumulative_time = args

    # ✅ Parallel worker güvenliği: temp klasörü kontrol et ve oluştur
    # ProcessPoolExecutor ile Windows'ta race condition olabiliyor
    if not os.path.exists(temp_klasor):
        try:
            os.makedirs(temp_klasor, exist_ok=True)
        except Exception as e:
            logger.warning(f"⚠️ Temp klasör oluşturma hatası (worker {klip_index}): {e}")

    klip_dosya = os.path.join(temp_klasor, f"c_{klip_index:05d}.mp4")

    fp_params = fingerprint_parametreleri_olustur(klip_index)

    # Cinematic effects oluştur (30+ farklı efekt!)
    cinematic_fx = cinematic_effects_uret(klip_index, secilen_efektler)

    # Cache kontrolü
    cached = cache_kontrol(item['dosya'], item['varyasyon'])
    if cached:
        try:
            shutil.copy2(cached, klip_dosya)
            return (klip_index, True, klip_dosya, "cache")
        except:
            pass

    # ===== 🚀 KORNIA GPU FILTERS: 8-10x Hızlı GPU Filtreleme =====
    # FFmpeg CPU filtreleri yerine PyTorch/Kornia GPU kullan
    use_kornia = (
        KORNIA_GPU_FILTERS and
        KORNIA_GPU_AVAILABLE and
        not TURBO_MODE and
        encoder_type == 'nvidia'  # GPU varsa Kornia kullan
    )

    if use_kornia:
        try:
            # Video filtrelerini oluştur (FFmpeg formatında)
            video_filtre = gelismis_video_filtre_olustur(
                item['varyasyon'],
                subtitle_config=None,
                cinematic_effects=cinematic_fx,
                use_gpu_scale=False
            )
            ses_filtre = gelismis_audio_filtre_olustur(item['varyasyon'])

            # Fingerprint filtreleri
            fp_video_filtre = fingerprint_video_filtresi(fp_params)
            fp_audio_filtre = fingerprint_audio_filtresi(fp_params)

            # Video filtreleri birleştir
            tum_video_filtreler = []
            if video_filtre:
                tum_video_filtreler.append(video_filtre)
            if fp_video_filtre:
                tum_video_filtreler.extend(fp_video_filtre)
            final_video_filtre = ','.join(tum_video_filtreler) if tum_video_filtreler else 'scale=1920:1080,fps=30'

            # Audio filtreleri birleştir
            tum_audio_filtreler = []
            if ses_filtre:
                tum_audio_filtreler.append(ses_filtre)
            if fp_audio_filtre:
                tum_audio_filtreler.extend(fp_audio_filtre)
            final_audio_filtre = ','.join(tum_audio_filtreler) if tum_audio_filtreler else None

            # Kornia pipeline ile işle
            pipeline = KorniaVideoPipeline(use_gpu=True)
            success = pipeline.process_clip_gpu(
                item['dosya'],
                klip_dosya,
                final_video_filtre,
                final_audio_filtre,
                use_nvenc=False  # Kliplar CPU encode (NVENC session limit)
            )

            if success and dosya_gecerli_mi(klip_dosya):
                cache_kaydet(klip_dosya, item['dosya'], item['varyasyon'])
                if klip_index == 1:
                    logger.info("🚀 Kornia GPU: Filtreler GPU'da işlendi (8-10x hızlı)")
                return (klip_index, True, klip_dosya, None)
            else:
                if klip_index <= 3:
                    logger.warning(f"⚠️ Klip {klip_index}: Kornia başarısız, FFmpeg'e geçiliyor")
        except Exception as e:
            if klip_index <= 3:
                logger.warning(f"⚠️ Klip {klip_index}: Kornia hatası: {e}")
            # Kornia başarısız olursa FFmpeg'e devam et

    # Encoder seçimi
    encoders_to_try = []

    if encoder_type != 'cpu':
        encoders_to_try.append((encoder_type, encoder_config))
        encoders_to_try.append(('cpu', {'video': 'libx264'}))
    else:
        encoders_to_try.append(('cpu', {'video': 'libx264'}))

    last_error = None

    for current_encoder_type, current_encoder_config in encoders_to_try:
        for deneme in range(2):
            try:
                # ===== 🚀 TURBO MODE: Minimal filtreler (5-10x hızlı) =====
                if TURBO_MODE:
                    # Sadece scale + fps (efektler atlanır)
                    final_video_filtre = 'scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=30'
                    final_audio_filtre = 'loudnorm=I=-16:TP=-1.5:LRA=11'
                    if klip_index == 1:
                        logger.info("🚀 TURBO MODE: Minimal filtreler (hızlı render)")
                else:
                    # Normal mod - Filtreler + CINEMATIC EFFECTS
                    # GPU scale (scale_cuda) - config.py'den kontrol
                    use_gpu = GPU_SCALE_ENABLED and GPU_OPTIMIZER_AVAILABLE and NVENC_INFO['available'] and current_encoder_type == 'nvidia'
                    video_filtre = gelismis_video_filtre_olustur(
                        item['varyasyon'],
                        subtitle_config=None,
                        cinematic_effects=cinematic_fx,
                        use_gpu_scale=use_gpu
                    )
                    ses_filtre = gelismis_audio_filtre_olustur(item['varyasyon'])
                    if klip_index == 1 and use_gpu:
                        logger.info("🚀 GPU scale_cuda aktif (diğer efektler CPU)")

                    # Fingerprint filtreleri
                    fp_video_filtre = fingerprint_video_filtresi(fp_params)
                    fp_audio_filtre = fingerprint_audio_filtresi(fp_params)

                    # Video filtreleri birleştir
                    tum_video_filtreler = []
                    if video_filtre:
                        tum_video_filtreler.append(video_filtre)
                    if fp_video_filtre:
                        tum_video_filtreler.extend(fp_video_filtre)

                    final_video_filtre = ','.join(tum_video_filtreler) if tum_video_filtreler else None

                    # ✅ FALLBACK: Eğer hiç video filtre yoksa, EN AZINDAN scale ekle!
                    if not final_video_filtre:
                        final_video_filtre = 'scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=30'
                        logger.warning(f"⚠️ Klip {klip_index}: Video filtre yok, fallback scale eklendi")

                    # Audio filtreleri birleştir
                    tum_audio_filtreler = []
                    if ses_filtre:
                        tum_audio_filtreler.append(ses_filtre)
                    if fp_audio_filtre:
                        tum_audio_filtreler.extend(fp_audio_filtre)

                    final_audio_filtre = ','.join(tum_audio_filtreler) if tum_audio_filtreler else None

                # ===== CPU DECODE + GPU ENCODE =====
                # hwaccel cuda KALDIRILDI: Küçük dosyalarda GPU↔CPU transfer overhead
                # CPU decode (hızlı) → CPU filters → GPU encode (hızlı)
                komut = [FFMPEG_PATH, '-v', 'error', '-stats',
                         '-filter_threads', '16',  # ✅ Ryzen 9 5950X (16 core) için optimize
                         '-i', item['dosya']]
                if klip_index == 1 and current_encoder_type == 'nvidia':
                    logger.debug(f"🚀 CPU decode → CPU filters (16 threads) → NVENC encode")

                # ✅ KRİTİK: HER ZAMAN scale filtresi uygula (464x688 gibi boyutları önle)
                if not final_video_filtre:
                    final_video_filtre = 'scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=30'
                    logger.warning(f"⚠️ Klip {klip_index}: Fallback scale eklendi")

                komut.extend(['-vf', final_video_filtre])
                # Detailed logging moved to debug
                if klip_index == 1:
                    logger.debug(f"🎬 Klip {klip_index} video filter: {len(final_video_filtre)} chars")
                    if cinematic_fx:
                        fx_list = [k for k, v in cinematic_fx.items() if v is not None]
                        if fx_list:
                            logger.debug(f"   Effects: {', '.join(fx_list)}")

                if final_audio_filtre:
                    komut.extend(['-af', final_audio_filtre])

                # ===== 🎬 FFMPEG HUMANIZATION V2.0 - 18 FEATURES =====
                use_humanization = False
                if FFMPEG_HUMANIZATION_AVAILABLE:
                    try:
                        # ===== 🚀 GPU OPTIMIZER: Select encoder based on availability =====
                        selected_encoder_type = 'auto'

                        # Force NVIDIA encoder if GPU Optimizer is available and NVENC ready
                        if GPU_OPTIMIZER_AVAILABLE and NVENC_INFO['available'] and current_encoder_type == 'nvidia':
                            selected_encoder_type = 'h264_nvenc'  # Use actual FFmpeg encoder name!
                            # Moved to debug
                            if klip_index == 1:
                                logger.debug(f"🚀 GPU encoding enabled (h264_nvenc)")

                        # Build complete humanized parameters (as libx264 first)
                        humanized_params = build_complete_ffmpeg_params(
                            encoder_type='libx264',  # Build as x264, then translate to NVENC
                            video_path=item['dosya']
                        )

                        # ===== 🚀 GPU OPTIMIZER: Translate x264 → NVENC =====
                        if GPU_OPTIMIZER_AVAILABLE and NVENC_INFO['available'] and current_encoder_type == 'nvidia':
                            try:
                                # Extract x264 parameters for translation
                                # MAXIMUM PERFORMANCE MODE: Use superfast preset (p2)
                                # Bitrate optimized for smaller file size (YouTube 1080p 30fps)
                                x264_params_for_gpu = {
                                    'encoder': 'libx264',
                                    'preset': 'superfast',  # Maps to p2 (~10x faster than x264)
                                    'crf': 20,  # 18→20 (smaller files, still good quality)
                                    'bitrate': '8M',  # 12M→8M (YouTube recommendation)
                                    'maxrate': '12M',  # 15M→12M (peak bitrate)
                                    'keyint': 240,
                                    'bframes': 3,
                                    'refs': 3,
                                    'gpu_id': 0,
                                }

                                # Translate to NVENC (pass cached NVENC_INFO to avoid re-detection)
                                nvenc_params = translate_x264_to_nvenc(x264_params_for_gpu, NVENC_INFO)

                                # Replace encoder and video params with NVENC
                                humanized_params['encoder'] = nvenc_params['encoder']
                                humanized_params['video_params'] = nvenc_params['video_params']
                                humanized_params['x264_params'] = []  # Clear x264-specific params

                                # Moved to debug
                                if klip_index == 1:
                                    logger.debug(f"   → {nvenc_params['encoder']} (preset={nvenc_params['preset']}, cq={nvenc_params['cq_level']})")
                                    logger.debug(f"   → Expected speedup: {nvenc_params['expected_speedup']}x")

                            except Exception as e:
                                logger.warning(f"⚠️ GPU translation failed, using x264: {e}")

                        # Apply encoder selection
                        selected_encoder = humanized_params['encoder']
                        # NOT adding '-c:v' here because video_params already contains it
                        # komut.extend(['-c:v', selected_encoder])  # REMOVED: duplicate

                        # Apply video parameters (all 18 features!)
                        # video_params already includes '-c:v h264_nvenc' or '-c:v libx264'
                        komut.extend(humanized_params['video_params'])

                        # Apply x264-specific parameters (for software encoder)
                        if humanized_params['x264_params']:
                            komut.extend(humanized_params['x264_params'])

                        # Apply audio parameters (humanized audio filters)
                        if humanized_params['audio_params']:
                            # Merge with existing audio filter if present
                            if final_audio_filtre:
                                # Already added above
                                pass
                            else:
                                komut.extend(humanized_params['audio_params'])

                        # Pixel format (always needed)
                        # NOTE: -profile:v and -level already in video_params from GPU optimizer
                        komut.extend([
                            '-pix_fmt', VIDEO_OUTPUT['pixel_format'],
                            # REMOVED: '-profile:v', 'high',  # duplicate - already in video_params
                            # REMOVED: '-level', '4.2',  # duplicate - already in video_params
                        ])

                        # Moved to debug
                        if klip_index == 1:
                            logger.debug(f"✅ Encoder: {selected_encoder}")
                            logger.debug(f"   Rate control: {humanized_params['rate_control_mode']}, Pass: {humanized_params['pass_count']}")

                        use_humanization = True

                    except Exception as e:
                        logger.warning(f"⚠️ Humanization failed, using fallback: {e}")
                        # Fallback to legacy encoding
                        use_humanization = False

                # ===== LEGACY FALLBACK (if humanization unavailable) =====
                if not use_humanization:
                    if current_encoder_type == 'cpu':
                        cpu_settings = QUALITY_SETTINGS['cpu']
                        komut.extend([
                            '-c:v', 'libx264',
                            '-preset', cpu_settings['preset'],
                            '-crf', str(cpu_settings['crf']),
                            '-b:v', cpu_settings['bitrate'],
                            '-maxrate', cpu_settings['maxrate'],
                            '-bufsize', cpu_settings['bufsize'],
                            '-profile:v', 'high',
                            '-level', '4.1',
                            '-pix_fmt', VIDEO_OUTPUT['pixel_format'],

                            '-colorspace', 'bt709',
                            '-color_primaries', 'bt709',
                            '-color_trc', 'bt709',
                            '-color_range', VIDEO_OUTPUT['color_range'],

                            '-g', str(fp_params['gop_size']),
                            '-keyint_min', str(fp_params['min_keyint']),
                            '-bf', str(fp_params['bframes']),
                            '-sc_threshold', str(random.randint(35, 45)),
                        ])
                    elif current_encoder_type == 'nvidia':
                        # ===== 🚀 KLİP ENCODİNG: CPU (NVENC SESSION LİMİT SORUNU) =====
                        # RTX 5060 Ti: Sadece 3-5 eşzamanlı NVENC session destekliyor
                        # 31 worker aynı anda NVENC kullanamaz → CPU encoding kullan
                        # Final encoding'de NVENC kullanılacak (tek session)
                        cpu_settings = QUALITY_SETTINGS.get('cpu', {})
                        komut.extend([
                            '-c:v', 'libx264',
                            '-preset', 'veryfast',  # Hızlı, kliplar küçük (1-5 sn)
                            '-crf', '18',
                            '-pix_fmt', 'yuv420p',
                            '-colorspace', 'bt709',
                            '-color_primaries', 'bt709',
                            '-color_trc', 'bt709',
                            '-color_range', VIDEO_OUTPUT['color_range'],
                            '-g', str(fp_params['gop_size']),
                            '-keyint_min', str(fp_params['min_keyint']),
                            '-bf', str(fp_params['bframes']),
                        ])
                        if klip_index == 1:
                            logger.info(f"🔧 Klip encoding: CPU (libx264 veryfast) - 31 paralel worker")
                            logger.info(f"🚀 Final encoding: NVENC GPU kullanılacak")
                    elif current_encoder_type == 'amd':
                        amd_settings = QUALITY_SETTINGS['amd']
                        komut.extend([
                            '-c:v', 'h264_amf',
                            '-quality', amd_settings['quality'],
                            '-rc', amd_settings['rc'],
                            '-b:v', amd_settings['bitrate'],
                            '-profile:v', 'high',

                            '-colorspace', 'bt709',
                            '-color_primaries', 'bt709',
                            '-color_trc', 'bt709',
                            '-color_range', VIDEO_OUTPUT['color_range'],

                            '-g', str(fp_params['gop_size']),
                        ])
                    elif current_encoder_type == 'intel':
                        qsv_settings = QUALITY_SETTINGS['intel']
                        komut.extend([
                            '-c:v', 'h264_qsv',
                            '-preset', qsv_settings['preset'],
                            '-global_quality', qsv_settings['global_quality'],
                            '-b:v', qsv_settings['bitrate'],
                            '-profile:v', 'high',
                            '-look_ahead', '1',

                            '-colorspace', 'bt709',
                            '-color_primaries', 'bt709',
                            '-color_trc', 'bt709',
                            '-color_range', VIDEO_OUTPUT['color_range'],

                            '-g', str(fp_params['gop_size']),
                            '-bf', str(fp_params['bframes']),
                        ])

                # Audio encoding
                if sessiz_yap:
                    komut.extend([
                        '-an',
                        '-movflags', '+faststart',
                        '-y', klip_dosya
                    ])
                else:
                    audio_cfg = AUDIO_SETTINGS
                    komut.extend([
                        '-c:a', audio_cfg['codec'],
                        '-b:a', audio_cfg['bitrate'],
                        '-ar', audio_cfg['sample_rate'],
                        '-ac', str(audio_cfg['channels']),
                        '-movflags', '+faststart',
                        '-y', klip_dosya
                    ])

                sonuc = subprocess.run(
                    komut,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=180
                )

                if sonuc.returncode == 0 and dosya_gecerli_mi(klip_dosya):
                    cache_kaydet(klip_dosya, item['dosya'], item['varyasyon'])

                    # ✅ İYİLEŞTİRİLMİŞ: GPU→CPU fallback bilgilendirmesi
                    if current_encoder_type == 'cpu' and encoder_type != 'cpu':
                        if klip_index <= 3:
                            logger.info(f"✅ Klip {klip_index}: GPU başarısız oldu, CPU ile tamamlandı")

                    return (klip_index, True, klip_dosya, None)
                else:
                    stderr_output = sonuc.stderr if sonuc.stderr else ""
                    last_error = stderr_output[:200] if stderr_output else "encoding_failed"

                    # 🐛 DEBUG: Log full error for first 3 failing clips
                    if klip_index <= 3:
                        logger.error(f"💥 Klip {klip_index} FULL FFmpeg ERROR:")
                        logger.error(f"   Command: {' '.join(komut[:15])}... (truncated)")
                        logger.error(f"   Stderr (full): {stderr_output}")

                    # ✅ İYİLEŞTİRİLMİŞ: FFmpeg hatasını kategorize et
                    error_category = parse_ffmpeg_error(stderr_output)

                    # GPU hatası tespiti - otomatik CPU fallback
                    if current_encoder_type != 'cpu' and error_category == ErrorCategory.GPU_ERROR:
                        if klip_index <= 3:
                            logger.warning(f"⚠️ Klip {klip_index}: GPU encoding hatası (CPU deneniyor...)")
                        # ✅ FIX: Break inner loop to try CPU encoder immediately
                        break  # Exit deneme loop, outer loop will try CPU
                    else:
                        # Diğer hatalar için detaylı log
                        if klip_index <= 3:
                            logger.warning(f"⚠️ Klip {klip_index} ({current_encoder_type}): {error_category.value}")
                            logger.debug(f"   Detay: {last_error}")

            except subprocess.TimeoutExpired:
                last_error = "timeout"
                if klip_index <= 3:
                    logger.warning(f"⏱️ Klip {klip_index}: Timeout (deneme {deneme + 1}/2)")
            except Exception as e:
                last_error = str(e)[:100]
                if klip_index <= 3:
                    logger.warning(f"❌ Klip {klip_index}: {last_error}")

        if current_encoder_type != 'cpu':
            logger.debug(f"Klip {klip_index}: {current_encoder_type} başarısız, CPU deneniyor...")

    return (klip_index, False, None, f"all_failed: {last_error}")


def parallel_encode(playlist, cikti_adi, temp_klasor, klasor_yolu, encoder_type, encoder_config, ses_dosyasi=None,
                    subtitle_config=None, secilen_efektler=None):
    """Parallel processing ile encode

    Args:
        secilen_efektler: Kullanıcının seçtiği efektler (set) veya None (tüm efektler)
    """
    # ✅ Güvenlik: temp klasörünün var olduğundan emin ol
    if not os.path.exists(temp_klasor):
        os.makedirs(temp_klasor, exist_ok=True)
        logger.info(f"📁 Temp klasör oluşturuldu: {temp_klasor}")

    print(f"\n🚀 Rendering başlıyor...")

    # Encoder info (tek satır)
    if GPU_OPTIMIZER_AVAILABLE and NVENC_INFO['available'] and encoder_type == 'nvidia':
        print(f"   Encoder: GPU ({NVENC_INFO.get('gpu_name', 'NVIDIA')})")
    else:
        print(f"   Encoder: CPU ({encoder_config['video']})")

    # Kornia GPU Filters info
    if KORNIA_GPU_FILTERS and KORNIA_GPU_AVAILABLE and encoder_type == 'nvidia':
        print(f"   Filtreler: Kornia GPU (8-10x hızlı)")
    else:
        print(f"   Filtreler: FFmpeg CPU")

    # Ses durumu
    if ses_dosyasi:
        print(f"   Ses: Final birleştirmede eklenecek")

    # ASS dosyası oluştur
    if subtitle_config and subtitle_config.get('enabled'):
        segment_count = len(subtitle_config.get('segments', []))

        if subtitle_config.get('mode') == 'auto' and segment_count > 0:
            print(f"   Altyazı: {segment_count} segment")

            # Dinamik altyazı kullanımı kontrolü
            use_dynamic = subtitle_config.get('use_dynamic', False)

            if use_dynamic:
                # Sadeleştirilmiş: detaylar kaldırıldı
                platform = subtitle_config.get('platform', 'youtube_standard')
                srt_dosya = dinamik_altyazi_ass_olustur(
                    subtitle_config,
                    DYNAMIC_SUBTITLE_CONFIG,
                    temp_klasor,
                    platform
                )
            else:
                srt_dosya = altyazi_srt_olustur(subtitle_config, temp_klasor)

            if srt_dosya:
                subtitle_config['srt_file'] = srt_dosya
            else:
                logger.warning("ASS dosyası oluşturulamadı")
                subtitle_config = None

    cpu_cores = multiprocessing.cpu_count()  # Ryzen 9 5950X = 32 threads

    # Worker sayısı - MAKSİMUM (render sırasında başka işlem yok)
    if TURBO_MODE:
        max_workers = min(8, cpu_cores)  # Turbo modda da daha fazla worker
        logger.info(f"🚀 TURBO: {max_workers} workers")
    elif GPU_OPTIMIZER_AVAILABLE and NVENC_INFO['available'] and encoder_type == 'nvidia':
        # 🔥 FULL CPU: 32 thread → 31 worker (1 sistem için)
        max_workers = cpu_cores - 1
        logger.info(f"🔥 FULL CPU: {max_workers}/{cpu_cores} workers (Ryzen 9 5950X)")
    else:
        max_workers = cpu_cores - 1

    # Efekt sayısı (sadece manuel seçimde göster)
    if secilen_efektler is not None:
        print(f"   Efektler: {len(secilen_efektler)} seçili")

    toplam = len(playlist)
    tamamlanan = 0
    basarili_klip = []
    basarisiz = []

    sessiz_yap = ses_dosyasi is not None

    # 🌟 Calculate cumulative time for hook optimizer
    cumulative_times = []
    cumulative = 0.0
    for item in playlist:
        cumulative_times.append(cumulative)
        cumulative += item.get('sure', 0.0)

    args_list = [
        (item, i + 1, encoder_type, encoder_config, temp_klasor, sessiz_yap, subtitle_config, secilen_efektler, cumulative_times[i])
        for i, item in enumerate(playlist)
    ]

    import time
    start_time = time.time()

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(klip_isle_parallel, args): args[1] for args in args_list}

        ilk_hata_gosterildi = False

        for future in as_completed(futures):
            klip_index, basarili, klip_dosya, hata = future.result()
            tamamlanan += 1

            # Progress bar with ETA
            yuzde = int((tamamlanan / toplam) * 100)
            bar_len = 40
            filled = int((bar_len * tamamlanan) / toplam)
            bar = '█' * filled + '░' * (bar_len - filled)

            # Calculate ETA
            elapsed = time.time() - start_time
            if tamamlanan > 0:
                avg_time = elapsed / tamamlanan
                remaining = (toplam - tamamlanan) * avg_time
                eta_str = f"ETA: {int(remaining)}s" if remaining > 0 else "Done"
            else:
                eta_str = "Calculating..."

            status = "✅" if basarili else "❌"
            cache_info = " 💾" if hata == "cache" else ""
            print(f"\r   [{bar}] {yuzde:3d}% | {tamamlanan}/{toplam} clips | {eta_str} {status}{cache_info}", end='', flush=True)

            if basarili:
                basarili_klip.append((klip_index, klip_dosya))
            else:
                basarisiz.append(f"Klip {klip_index}: {hata}")

                if not ilk_hata_gosterildi and hata:
                    ilk_hata_gosterildi = True
                    print(f"\n   ⚠️  İLK HATA (Klip {klip_index}): {hata}")

            if tamamlanan % 10 == 0:
                ilerleme_kaydet(tamamlanan, toplam, cikti_adi)

    print()

    # Encoding summary with timing
    total_time = time.time() - start_time
    print(f"\n   Tamamlandı: {total_time:.0f}s ({len(basarili_klip)}/{toplam} klip)")

    if not basarili_klip:
        return False, "Hiçbir klip işlenemedi."

    basarili_klip.sort(key=lambda x: x[0])

    # TRANSİTİON EFFECTS SEÇİMİ
    transitions = []
    if TRANSITION_EFFECTS['enabled'] and len(basarili_klip) > 1:
        used_transitions = []

        for i in range(len(basarili_klip) - 1):
            trans = transition_sec(i, used_transitions)
            if trans:
                transitions.append(trans)
                used_transitions.append(trans['type'])
                if i < 3:
                    logger.debug(f"Transition {i + 1}: {trans['type']} ({trans['duration']}s)")

    print(f"   Birleştirme başladı...")

    concat_liste = os.path.join(temp_klasor, 'list.txt')
    with open(concat_liste, 'w', encoding='utf-8') as f:
        for _, klip in basarili_klip:
            path = klip.replace('\\', '/')
            f.write(f"file '{path}'\n")

    cikti_yolu = os.path.join(klasor_yolu, cikti_adi)

    use_xfade = (TRANSITION_EFFECTS['enabled'] and
                 transitions and
                 len(basarili_klip) <= 15 and
                 not ses_dosyasi)

    if ses_dosyasi:
        print(f"   Ses ekleniyor...")

        # ✅ FIX: Get audio duration to limit video output (video = audio length)
        ses_suresi = ses_bilgisi_al(ses_dosyasi)
        if ses_suresi:
            logger.info(f"🎵 Audio duration: {ses_suresi:.2f}s - Video will be trimmed to match")
        else:
            logger.warning("⚠️ Could not get audio duration, video may be longer than audio")
            ses_suresi = None

        temp_video = os.path.join(temp_klasor, 'merged_nosound.mp4')

        # ✅ FIX: Video freeze sorunu - timestamp ve keyframe düzeltmeleri
        komut = [
            FFMPEG_PATH, '-v', 'warning',
            '-fflags', '+genpts+igndts',  # Timestamp'leri yeniden oluştur
            '-f', 'concat',
            '-safe', '0',
            '-i', concat_liste,
            '-c', 'copy',
            '-avoid_negative_ts', 'make_zero',  # Negatif timestamp'leri düzelt
            '-y', temp_video
        ]
        sonuc = subprocess.run(komut, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if sonuc.returncode != 0 or not dosya_gecerli_mi(temp_video):
            return False, f"Video birleştirme hatası: {sonuc.stderr[:200]}"

        # ✅ OPTİMİZASYON: Scale + Subtitle TEK PASS'ta birleştirildi
        # Eski: Scale pass → Subtitle pass (2x encode, 2x GPU kullanımı)
        # Yeni: Scale+Subtitle tek pass'ta (1x encode, %50 daha hızlı)

        # ✅ PyTorch CUDA cache temizle (Whisper GPU kullandıysa NVENC ile çakışabilir)
        try:
            import torch
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                torch.cuda.synchronize()
                logger.debug("🧹 CUDA cache temizlendi (PyTorch → FFmpeg geçişi)")
        except:
            pass

        nvenc_failed = False

        # ✅ Input video kontrolü
        if not dosya_gecerli_mi(temp_video):
            logger.error(f"❌ Input video geçersiz: {temp_video}")
            return False, "Concat video geçersiz"

        # Input video boyutunu kontrol et - scale gerekli mi?
        probe_cmd = [FFPROBE_PATH, '-v', 'error', '-select_streams', 'v:0',
                     '-show_entries', 'stream=width,height,duration', '-of', 'csv=p=0', temp_video]
        probe_result = subprocess.run(probe_cmd, capture_output=True, text=True)

        needs_scale = True  # Default: scale gerekli
        if probe_result.returncode == 0:
            try:
                parts = probe_result.stdout.strip().split(',')
                width, height = int(parts[0]), int(parts[1])
                duration = float(parts[2]) if len(parts) > 2 else 0
                logger.info(f"📹 Input video: {width}x{height}, {duration:.1f}s")

                # ✅ SADECE TAM 1920x1080 ise scale atla
                if width == 1920 and height == 1080:
                    logger.info(f"✅ Video boyutu TAM 1920x1080 - scale filter atlanacak")
                    needs_scale = False
                else:
                    logger.info(f"⚠️ Video boyutu {width}x{height} != 1920x1080 - scale filter eklenecek")
            except Exception as e:
                logger.warning(f"⚠️ Video boyutu okunamadı: {e}")

        # Scale filter string (tek pass'ta kullanılacak)
        scale_filter = 'scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,format=yuv420p'
        logger.info("⚡ TEK PASS optimizasyonu: Scale + Subtitle birleştirildi")

        audio_cfg = AUDIO_SETTINGS

        audio_filtreler = []

        # 🔧 STEP 1: SAMPLE RATE CONVERSION (ALWAYS FIRST)
        # Convert to target sample rate before any processing to maintain quality
        if audio_cfg['sample_rate'] != '44100':
            audio_filtreler.append(f"aresample={audio_cfg['sample_rate']}")
            logger.info(f"🔧 Sample rate conversion: input → {audio_cfg['sample_rate']}Hz")

        # 🔧 STEP 2: MONO TO STEREO CONVERSION (PROPER UPMIXING)
        # Use pan filter for proper mono→stereo conversion instead of just channel duplication
        # This provides better stereo image and prevents phase issues
        audio_filtreler.append("pan=stereo|FL=FC|FR=FC")
        logger.info("🔧 Mono→Stereo conversion applied (proper upmixing)")

        # 🎙️ STEP 3: AUDIO HUMANIZATION (if enabled)
        use_audio_humanization = False
        if AUDIO_HUMANIZATION_AVAILABLE:
            try:
                humanized_audio = build_humanized_audio_filter()

                if humanized_audio and humanized_audio.get('audio_filters'):
                    # Add humanization filters
                    audio_filtreler.append(humanized_audio['audio_filters'])
                    use_audio_humanization = True
                    logger.info("🎙️ Audio humanization applied (AI → Human voice)")

            except Exception as e:
                logger.warning(f"⚠️ Audio humanization failed, using standard: {e}")
                use_audio_humanization = False

        # 🔧 STEP 4: LOUDNESS NORMALIZATION (always applied)
        if audio_cfg['normalization']:
            audio_filtreler.append(
                f"loudnorm=I={audio_cfg['target_loudness']}:"
                f"TP={audio_cfg['true_peak']}:"
                f"LRA={audio_cfg['lra']}"
            )
            # ✅ İYİLEŞTİRİLDİ: Daha sıkı limiter threshold (clipping'i önlemek için)
            # 0.95 → 0.88 (clipping kesinlikle önlenir)
            audio_filtreler.append("alimiter=limit=0.88:attack=5:release=50:level=disabled")

        # 🔧 STEP 5: VOLUME BOOST (ALWAYS APPLIED)
        # ✅ İYİLEŞTİRİLDİ: Daha düşük volume boost (clipping'i önlemek için)
        # 1.08 → 1.02, 1.12 → 1.04 (Loudnorm zaten yeterli)
        volume_boost = 1.02 if use_audio_humanization else 1.04
        audio_filtreler.append(f"volume={volume_boost}")
        logger.info(f"🔊 Volume boost: {volume_boost}x (clipping-safe)")

        # 🔧 STEP 6: COMPRESSION (only if humanization not active)
        if audio_cfg['compression'] and not use_audio_humanization:
            # Skip standard compression if humanization already added compression
            audio_filtreler.append(
                "compand=attacks=0.3:decays=0.8:points=-90/-90|-70/-70|-60/-20|-20/-5|20/0:soft-knee=6:gain=0:volume=-5"
            )

        audio_filtre_str = ','.join(audio_filtreler)

        # ✅ OPTİMİZASYON: TEK PASS - hwaccel cuda + scale + subtitle birleşik
        # Eski: Scale pass → Subtitle pass (2x encode)
        # Yeni: Tek pass'ta scale+subtitle (1x encode, %50 daha hızlı)

        input_dir = os.path.dirname(temp_video)

        # ✅ HWACCEL CUDA: GPU decode (B optimizasyonu)
        use_hwaccel = GPU_OPTIMIZER_AVAILABLE and NVENC_INFO['available'] and encoder_type == 'nvidia'

        komut = [FFMPEG_PATH, '-v', 'warning']

        if use_hwaccel:
            # GPU hardware decode - input'tan önce gelir
            komut.extend(['-hwaccel', 'cuda', '-hwaccel_output_format', 'cuda'])
            logger.info("⚡ HWACCEL CUDA: GPU decode aktif")

        komut.extend([
            '-i', temp_video,
            '-i', ses_dosyasi,
            '-map', '0:v',
            '-map', '1:a',
        ])

        if subtitle_config and subtitle_config.get('srt_file'):
            ass_file = subtitle_config['srt_file']
            ass_path = ass_file.replace('\\', '/')

            print(f"   📝 Alt yazılar ekleniyor: {os.path.basename(ass_file)}")

            # ✅ FFmpeg subtitles filter - Windows path sorunu çözümü
            import shutil
            temp_ass_name = 'subs_temp.ass'
            temp_ass_path = os.path.join(input_dir, temp_ass_name)
            try:
                shutil.copy2(ass_file, temp_ass_path)
                ass_path_escaped = temp_ass_name
            except Exception as e:
                logger.warning(f"ASS kopyalama hatası: {e}, orijinal path kullanılıyor")
                ass_path_escaped = "'" + ass_path.replace(':', '\\\\:') + "'"

            # ✅ TEK PASS: Scale + Subtitle birleşik filter chain
            # hwaccel cuda kullanıldığında önce hwdownload gerekli (GPU → CPU for subtitle burn)
            if needs_scale:
                if use_hwaccel:
                    # GPU decode → CPU'ya indir → scale + subtitle
                    combined_filter = f'hwdownload,format=nv12,{scale_filter},subtitles={ass_path_escaped}'
                else:
                    combined_filter = f'{scale_filter},subtitles={ass_path_escaped}'
                logger.info(f"⚡ TEK PASS: Scale + Subtitle birleşik")
            else:
                if use_hwaccel:
                    combined_filter = f'hwdownload,format=nv12,subtitles={ass_path_escaped}'
                else:
                    combined_filter = f'subtitles={ass_path_escaped}'
                logger.info(f"⚡ TEK PASS: Sadece Subtitle (scale gerekmez)")

            if use_hwaccel and not nvenc_failed:
                nv_settings = QUALITY_SETTINGS['nvidia']
                print(f"   🚀 NVENC GPU TEK PASS encoding (scale+subtitle)")
                komut.extend([
                    '-vf', combined_filter,
                    '-c:v', 'h264_nvenc',
                    '-preset', nv_settings['preset'],
                    '-rc', nv_settings['rc'],
                    '-b:v', nv_settings['bitrate'],
                    '-maxrate', nv_settings['maxrate'],
                    '-bufsize', nv_settings['bufsize'],
                    '-profile:v', nv_settings['profile'],
                    '-pix_fmt', 'yuv420p',
                ])
            else:
                if nvenc_failed:
                    print(f"   📝 CPU TEK PASS encoding (NVENC fallback)")
                else:
                    print(f"   📝 CPU TEK PASS encoding")
                komut.extend([
                    '-vf', combined_filter,
                    '-c:v', 'libx264',
                    '-preset', 'fast',
                    '-crf', '18',
                    '-pix_fmt', 'yuv420p',
                ])
        else:
            # Subtitle yok - sadece scale gerekirse uygula
            if needs_scale:
                if use_hwaccel:
                    komut.extend(['-vf', f'hwdownload,format=nv12,{scale_filter}'])
                else:
                    komut.extend(['-vf', scale_filter])

                if use_hwaccel and not nvenc_failed:
                    nv_settings = QUALITY_SETTINGS['nvidia']
                    komut.extend([
                        '-c:v', 'h264_nvenc',
                        '-preset', nv_settings['preset'],
                        '-rc', nv_settings['rc'],
                        '-b:v', nv_settings['bitrate'],
                        '-pix_fmt', 'yuv420p',
                    ])
                else:
                    komut.extend([
                        '-c:v', 'libx264',
                        '-preset', 'fast',
                        '-crf', '18',
                        '-pix_fmt', 'yuv420p',
                    ])
            else:
                komut.extend(['-c:v', 'copy'])

        # ✅ FIX: Limit output duration to audio duration (video = audio length)
        # This ensures video doesn't exceed audio duration by more than a few seconds
        if ses_suresi:
            # Add small buffer (2 seconds) to ensure smooth ending
            komut.extend(['-t', str(ses_suresi + 2)])
            logger.info(f"🎬 Output duration limited to {ses_suresi + 2:.2f}s (audio + 2s buffer)")

        komut.extend([
            '-c:a', audio_cfg['codec'],
            '-b:a', audio_cfg['bitrate'],
            '-ar', audio_cfg['sample_rate'],
            '-ac', str(audio_cfg['channels']),
            '-af', audio_filtre_str,
            '-movflags', '+faststart',
            '-y', cikti_yolu
        ])

        # ✅ cwd=input_dir: FFmpeg çalışma dizini subtitle dosyasının olduğu yer
        sonuc = subprocess.run(komut, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=input_dir)

        if sonuc.returncode != 0:
            error_msg = sonuc.stderr[:500] if sonuc.stderr else sonuc.stdout[:500] if sonuc.stdout else "No FFmpeg output"
            logger.error(f"Encoding hatası (code {sonuc.returncode}): {error_msg}")

            # ✅ NVENC crash → CPU fallback retry (TEK PASS - combined filter)
            if sonuc.returncode == 3221225477 and encoder_type == 'nvidia' and not nvenc_failed:
                logger.info("🔄 NVENC crashed during final encode, retrying with CPU (tek pass)...")

                # Rebuild command with CPU encoder - TEK PASS (scale + subtitle birleşik)
                komut_cpu = [
                    FFMPEG_PATH, '-v', 'warning',
                    '-i', temp_video,
                    '-i', ses_dosyasi,
                    '-map', '0:v',
                    '-map', '1:a',
                ]

                if subtitle_config and subtitle_config.get('srt_file'):
                    # CPU fallback - combined filter kullan (hwaccel yok)
                    if needs_scale:
                        cpu_filter = f'{scale_filter},subtitles={ass_path_escaped}'
                    else:
                        cpu_filter = f'subtitles={ass_path_escaped}'
                    komut_cpu.extend([
                        '-vf', cpu_filter,
                        '-c:v', 'libx264',
                        '-preset', 'fast',
                        '-crf', '18',
                        '-pix_fmt', 'yuv420p',
                    ])
                else:
                    if needs_scale:
                        komut_cpu.extend([
                            '-vf', scale_filter,
                            '-c:v', 'libx264',
                            '-preset', 'fast',
                            '-crf', '18',
                            '-pix_fmt', 'yuv420p',
                        ])
                    else:
                        komut_cpu.extend(['-c:v', 'copy'])

                if ses_suresi:
                    komut_cpu.extend(['-t', str(ses_suresi + 2)])

                komut_cpu.extend([
                    '-c:a', audio_cfg['codec'],
                    '-b:a', audio_cfg['bitrate'],
                    '-ar', audio_cfg['sample_rate'],
                    '-ac', str(audio_cfg['channels']),
                    '-af', audio_filtre_str,
                    '-movflags', '+faststart',
                    '-y', cikti_yolu
                ])

                print(f"   🔄 CPU ile tekrar deneniyor...")
                sonuc = subprocess.run(komut_cpu, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=input_dir)

                if sonuc.returncode == 0:
                    logger.info(f"✅ Final encoding başarılı (CPU fallback)")
                else:
                    error_msg = sonuc.stderr[:500] if sonuc.stderr else "No FFmpeg output"
                    logger.error(f"CPU fallback da başarısız (code {sonuc.returncode}): {error_msg}")
                    return False, f"Ses+altyazı birleştirme hatası: {error_msg}"
            else:
                logger.error(f"FFmpeg command: {' '.join(komut[:15])}...")
                return False, f"Ses+altyazı birleştirme hatası: {error_msg}"

        logger.info(f"✅ Final encoding başarılı")

        # Verify output file exists and has audio
        if not dosya_gecerli_mi(cikti_yolu):
            logger.error(f"Output file not created or invalid: {cikti_yolu}")
            return False, "Çıktı dosyası oluşturulamadı"

        try:
            os.remove(temp_video)
        except:
            pass

    else:
        if subtitle_config and subtitle_config.get('srt_file'):
            temp_merged = os.path.join(temp_klasor, 'merged_temp.mp4')

            komut = [
                FFMPEG_PATH, '-v', 'warning',
                '-f', 'concat',
                '-safe', '0',
                '-i', concat_liste,
                '-c', 'copy',
                '-y', temp_merged
            ]
            sonuc = subprocess.run(komut, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            if sonuc.returncode != 0:
                return False, f"Video birleştirme hatası: {sonuc.stderr[:200]}"

            print(f"   📝 Alt yazılar ekleniyor: {os.path.basename(subtitle_config['srt_file'])}")

            ass_file = subtitle_config['srt_file']

            # ✅ FFmpeg subtitles filter - Windows path sorunu çözümü
            import shutil
            temp_ass_name = 'subs_temp.ass'
            input_dir_nosound = os.path.dirname(temp_merged)
            temp_ass_path_nosound = os.path.join(input_dir_nosound, temp_ass_name)
            try:
                shutil.copy2(ass_file, temp_ass_path_nosound)
                ass_path_escaped = temp_ass_name
            except:
                ass_path_escaped = os.path.basename(ass_file)

            komut = [
                FFMPEG_PATH, '-v', 'warning',
                '-i', temp_merged,
                '-vf', f'subtitles={ass_path_escaped}',
                '-c:v', 'libx264',
                '-preset', 'fast',
                '-crf', '18',
                '-c:a', 'copy',
                '-movflags', '+faststart',
                '-y', cikti_yolu
            ]
            sonuc = subprocess.run(komut, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=input_dir_nosound)

            try:
                os.remove(temp_merged)
            except:
                pass
        else:
            komut = [
                FFMPEG_PATH, '-v', 'warning',
                '-f', 'concat',
                '-safe', '0',
                '-i', concat_liste,
                '-c', 'copy',
                '-movflags', '+faststart',
                '-y', cikti_yolu
            ]
            sonuc = subprocess.run(komut, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if sonuc.returncode == 0 and dosya_gecerli_mi(cikti_yolu):
        temp_output = cikti_yolu + ".temp.mp4"
        final_output = metadata_randomize(cikti_yolu, temp_output)

        if final_output != cikti_yolu:
            try:
                os.replace(temp_output, cikti_yolu)
            except:
                pass

        if os.path.exists(temp_output):
            try:
                os.remove(temp_output)
            except:
                pass

        print(f"\n   🧹 Geçici dosyalar temizleniyor...")

        time.sleep(0.5)

        temizlenen_toplam = 0
        try:
            if os.path.exists(temp_klasor):
                for root, dirs, files in os.walk(temp_klasor):
                    temizlenen_toplam += len(files)

                shutil.rmtree(temp_klasor, ignore_errors=False)
                print(f"   ✅ Temp klasör silindi: {temizlenen_toplam} dosya")
                logger.info(f"Temp klasör silindi: {temizlenen_toplam} dosya")
        except PermissionError:
            logger.warning(f"Dosya kilitli, tekrar deneniyor")
            print(f"   ⚠️  Dosyalar kullanımda, 2 saniye bekleniyor...")
            time.sleep(2)

            try:
                shutil.rmtree(temp_klasor, ignore_errors=True)
                print(f"   ✅ Temp klasör silindi (2. deneme)")
            except:
                print(f"   ⚠️  Bazı dosyalar kilitli, tek tek siliniyor...")
                for root, dirs, files in os.walk(temp_klasor, topdown=False):
                    for file in files:
                        try:
                            file_path = os.path.join(root, file)
                            os.chmod(file_path, 0o777)
                            os.remove(file_path)
                        except:
                            pass
                    for dir in dirs:
                        try:
                            os.rmdir(os.path.join(root, dir))
                        except:
                            pass
                try:
                    os.rmdir(temp_klasor)
                    print(f"   ✅ Temp klasör silindi (manuel)")
                except:
                    print(f"   ⚠️  Temp klasör tamamen silinemedi")
        except Exception as e:
            logger.error(f"Temp klasör silinemedi: {e}")

        print(f"   🧹 Downloads klasörü temizleniyor...")
        downloads_temizlik = 0

        gecici_patterns = ['s_*.mp4', 'c_*.mp4', 'list.txt', '*.temp.mp4']

        for pattern in gecici_patterns:
            for dosya in glob.glob(os.path.join(klasor_yolu, pattern)):
                try:
                    if os.path.isfile(dosya) and os.path.basename(dosya) != cikti_adi:
                        os.remove(dosya)
                        downloads_temizlik += 1
                except:
                    pass

        gecici_klasorler = ['temp_safe', 'temp_pro', 'temp_v4']
        for klasor in gecici_klasorler:
            klasor_path = os.path.join(klasor_yolu, klasor)
            if klasor_path != temp_klasor and os.path.exists(klasor_path):
                try:
                    shutil.rmtree(klasor_path, ignore_errors=True)
                except:
                    pass

        if downloads_temizlik > 0:
            print(f"   ✅ Downloads: {downloads_temizlik} geçici dosya silindi")

        # ===== 🆕 YOUTUBE OPTİMİZASYONU: KALİTE KONTROLÜ ve METADATA =====
        if YOUTUBE_OPTIMIZATION_ENABLED:
            try:
                logger.info("\n" + "=" * 100)
                logger.info("🚀 YOUTUBE OPTİMİZASYONLARI UYGULANMAYA BAŞLANIYOR")
                logger.info("=" * 100)

                # 1. Kalite Kontrolü
                if ADVANCED_QUALITY_CHECKS.get('enabled', False):
                    logger.info("\n📊 KALITE KONTROLÜ:")
                    quality_passed, quality_score, quality_details = post_render_quality_check(
                        cikti_yolu,
                        ADVANCED_QUALITY_CHECKS
                    )

                    if not quality_passed:
                        logger.warning("⚠️  Kalite kontrolü başarısız! Video yine de kaydedildi.")
                    else:
                        logger.info(f"✅ Kalite kontrolü başarılı! Skor: {quality_score:.2%}")

                # 2. Metadata Randomizasyonu
                if METADATA_RANDOMIZATION.get('enabled', False):
                    logger.info("\n🏷️  METADATA RANDOMİZASYONU:")
                    temp_output = cikti_yolu + '.metadata_temp.mp4'

                    metadata_success = enhanced_metadata_injection(
                        cikti_yolu,
                        temp_output,
                        METADATA_RANDOMIZATION
                    )

                    if metadata_success and os.path.exists(temp_output):
                        # Orijinali değiştir
                        try:
                            os.remove(cikti_yolu)
                            shutil.move(temp_output, cikti_yolu)
                            logger.info("✅ Metadata başarıyla güncellendi")
                        except Exception as e:
                            logger.warning(f"⚠️  Metadata güncellemesi başarısız: {e}")
                            # Temp dosyayı temizle
                            if os.path.exists(temp_output):
                                try:
                                    os.remove(temp_output)
                                except:
                                    pass

                # 3. Fingerprint Oluştur
                logger.info("\n🔒 VIDEO FİNGERPRİNT:")
                fingerprint = generate_video_fingerprint(cikti_yolu)

                if fingerprint:
                    save_fingerprint_database(fingerprint, klasor_yolu)
                    logger.info(f"✅ Fingerprint: {fingerprint['unique_id'][:16]}...")

                logger.info("\n" + "=" * 100)
                logger.info("✅ TÜM OPTİMİZASYONLAR TAMAMLANDI!")
                logger.info("=" * 100)

            except Exception as e:
                logger.error(f"❌ Optimizasyon hatası: {e}")
                logger.warning("⚠️  Video oluşturuldu ama optimizasyonlar başarısız!")
        # ===== YOUTUBE OPTİMİZASYONU BİTİŞ =====

        return True, cikti_yolu
    else:
        return False, f"Birleştirme hatası: {sonuc.stderr[:200]}"


# ==================== PLAYLIST ====================

def playlist_olustur(video_bilgileri, hedef_sure, temp_klasor):
    print(f"\n🔬 Playlist oluşturuluyor...")

    tum_segmentler = []
    for video_info in video_bilgileri:
        segmentler = videoyu_segmentlere_bol(video_info, temp_klasor, use_scene_detection=True)
        tum_segmentler.extend(segmentler)

    print(f"   ✅ {len(tum_segmentler)} segment")

    playlist = []
    toplam_sure = 0
    kullanim = {}

    segment_havuzu = tum_segmentler.copy()
    random.shuffle(segment_havuzu)

    while toplam_sure < hedef_sure:
        if not segment_havuzu:
            segment_havuzu = tum_segmentler.copy()
            random.shuffle(segment_havuzu)

        segment = segment_havuzu.pop(0)
        key = segment['dosya']

        if key not in kullanim:
            kullanim[key] = 0
        kullanim[key] += 1

        varyasyon = gelismis_varyasyon_uret(key, kullanim[key])
        gercek_sure = segment['sure'] / varyasyon['hiz']

        # ✅ FİX: Son klibi hedef süreye tam olarak fit et (taşmayı önle)
        kalan_sure = hedef_sure - toplam_sure
        if gercek_sure > kalan_sure:
            # Son klip hedeften fazla, trim et
            trim_ratio = kalan_sure / gercek_sure
            segment_trimmed = segment['sure'] * trim_ratio
            gercek_sure_trimmed = kalan_sure

            playlist.append({
                'dosya': segment['dosya'],
                'sure': segment_trimmed,  # Trimmed duration
                'gercek_sure': gercek_sure_trimmed,
                'varyasyon': varyasyon,
            })

            toplam_sure += gercek_sure_trimmed
            # Son klip eklendi, hedef süreye ulaşıldı
            break
        else:
            # Normal klip, tam olarak ekle
            playlist.append({
                'dosya': segment['dosya'],
                'sure': segment['sure'],
                'gercek_sure': gercek_sure,
                'varyasyon': varyasyon,
            })

            toplam_sure += gercek_sure

    print(f"   ✅ {len(playlist)} klip | {sure_formatla(toplam_sure)}")
    return playlist


# ==================== MAIN ====================

def main():
    banner()

    # ===== 🆕 YOUTUBE OPTİMİZASYONU: DURUM BİLGİLENDİRMESİ =====
    if YOUTUBE_OPTIMIZATION_ENABLED:
        print(f"\n" + "=" * 100)
        print("🚀 YOUTUBE ULTRA PRO - ALGORİTMA OPTİMİZASYONU AKTİF".center(100))
        print("=" * 100)
        if TURBO_MODE:
            print(f"   🚀 TURBO MODE: AKTİF (Efektler atlanır, hızlı render)")
        else:
            print(f"   ⚙️  Efekt Modu: {EFFECT_MODE.upper()}")
        print(f"   ✅ Kalite Kontrolü: {'Aktif' if ADVANCED_QUALITY_CHECKS.get('enabled') else 'Devre Dışı'}")
        print(f"   ✅ Metadata Randomizasyonu: {'Aktif' if METADATA_RANDOMIZATION.get('enabled') else 'Devre Dışı'}")
        print(f"   ✅ Efekt Dengeleme: {'Aktif' if EFFECT_BALANCING.get('enabled') else 'Devre Dışı'}")
        print(f"   ✅ Upload Önerileri: {'Aktif' if UPLOAD_STRATEGY.get('enabled') else 'Devre Dışı'}")
        print(f"   💡 Her video benzersiz fingerprint ve metadata ile oluşturulacak")
        print("=" * 100)
    # ===== YOUTUBE OPTİMİZASYONU BİTİŞ =====

    if not ffmpeg_yuklu_mu():
        print("❌ ffmpeg yüklü değil!")
        print("\n💡 Kurulum:")
        print("   Windows: choco install ffmpeg")
        print("   Linux: sudo apt install ffmpeg")
        input("\nDevam...")
        return

    encoder_type, encoder_config = gpu_durumunu_tespit_et()

    # ========== 📖 HİKAYE KANALI - OTOMATİK AYARLAR ==========
    print("\n" + "=" * 100)
    print("📖 HİKAYE KANALI - OTOMATİK AYARLAR".center(100))
    print("=" * 100)
    print(f"\n✅ Tüm ayarlar hikaye kanalları için optimize edildi!")
    print(f"   → Altyazı stili seçince font otomatik gelir")
    print(f"   → Vurgu rengi seçebilirsiniz")
    print(f"   → Efektler akıllı seçim ile otomatik")

    # Otomatik ayarlar
    hikaye_modu = True
    secilen_font = None  # Stilden gelecek
    font_multiplier = 1.0
    outline_width = 5
    shadow = 3
    secilen_efektler = None  # Akıllı seçim

    print(f"\n🚀 Ses seçimi sonrası render otomatik başlayacak!")

    print("\n" + "=" * 80)
    print("📁 RENDER WORKFLOW - KLASÖR YAPISI".center(80))
    print("=" * 80)

    print(f"\n📦 Video Havuzu: {RANDOMS_KLASORU}")
    print(f"🎵 Ses Havuzu:   {SES_KLASORU}")
    print(f"💾 Çıktı:        {RENDER_KLASORU}")

    for klasor_adi, klasor_yolu in [
        ("Video Havuzu", RANDOMS_KLASORU),
        ("Ses Havuzu", SES_KLASORU),
        ("Çıktı", RENDER_KLASORU)
    ]:
        if not os.path.exists(klasor_yolu):
            print(f"\n⚠️  {klasor_adi} bulunamadı: {klasor_yolu}")
            print(f"   📁 Klasör oluşturuluyor...")
            try:
                os.makedirs(klasor_yolu, exist_ok=True)
                print(f"   ✅ Klasör oluşturuldu!")
            except Exception as e:
                print(f"   ❌ Klasör oluşturulamadı: {e}")
                input("\nDevam...")
                return
        else:
            print(f"   ✅ {klasor_adi} mevcut")

    print()

    eski_gecici_dosyalar = []
    for pattern in ['s_*.mp4', 'c_*.mp4', 'list.txt', '*.temp.mp4']:
        eski_gecici_dosyalar.extend(glob.glob(os.path.join(RENDER_KLASORU, pattern)))

    eski_temp_klasorler = []
    for klasor in ['temp_safe', 'temp_pro', 'temp_v4']:
        klasor_path = os.path.join(RENDER_KLASORU, klasor)
        if os.path.exists(klasor_path):
            eski_temp_klasorler.append(klasor_path)

    toplam_eski = len(eski_gecici_dosyalar) + sum(
        sum(len(files) for _, _, files in os.walk(k)) for k in eski_temp_klasorler
    )

    if toplam_eski > 0:
        print(f"⚠️  Önceki çalışmadan {toplam_eski} geçici dosya bulundu")
        print(f"   🗑️  Otomatik temizleniyor...")
        temizlenen = 0

        for dosya in eski_gecici_dosyalar:
            try:
                os.remove(dosya)
                temizlenen += 1
            except:
                pass

        for klasor in eski_temp_klasorler:
            try:
                shutil.rmtree(klasor, ignore_errors=True)
            except:
                pass

        print(f"   ✅ {temizlenen} geçici dosya temizlendi!\n")

    # ===== 🎬 FFMPEG HUMANIZATION V2.0 INITIALIZATION =====
    if FFMPEG_HUMANIZATION_AVAILABLE:
        try:
            init_encoding_log(RENDER_KLASORU)
            logger.info("📝 FFmpeg Humanization encoding log initialized")

            # Show available encoders
            available_encoders = detect_available_encoders()
            print(f"\n🎬 Available Encoders: {', '.join(available_encoders.keys())}")
        except Exception as e:
            logger.warning(f"⚠️ Could not initialize FFmpeg Humanization: {e}")

    video_dosyalari = video_dosyalarini_bul(RANDOMS_KLASORU)
    if not video_dosyalari:
        print(f"❌ {RANDOMS_KLASORU} klasöründe video bulunamadı!")
        print(f"   💡 Lütfen video dosyalarını bu klasöre ekleyin")
        input("\nDevam...")
        return

    print(f"✅ {len(video_dosyalari)} video bulundu\n")

    print("📊 Video bilgileri:")
    video_bilgileri = []
    toplam_sure = 0

    for video in video_dosyalari:
        video_yolu = os.path.join(RANDOMS_KLASORU, video)
        bilgi = video_bilgisi_al(video_yolu)

        if bilgi and bilgi['sure']:
            video_bilgileri.append({
                'ad': video,
                'yol': video_yolu,
                'sure': bilgi['sure']
            })
            toplam_sure += bilgi['sure']
            codec_info = f" [{bilgi.get('codec')}]" if bilgi.get('codec') else ""
            print(f"   ✓ {video[:50]}{codec_info} - {sure_formatla(bilgi['sure'])}")
        else:
            logger.warning(f"Atlandı: {video}")

    if not video_bilgileri:
        print("\n❌ Hiçbir video bilgisi okunamadı!")
        input("\nDevam...")
        return

    print(f"\n   📈 Video havuzu toplam: {sure_formatla(toplam_sure)}")

    print(f"\n" + "=" * 100)
    print("🎵 SES DOSYASI SEÇİMİ".center(100))
    print("=" * 100)
    print(f"📁 Ses klasörü: {SES_KLASORU}\n")

    ses_dosyalari = ses_dosyalarini_bul(SES_KLASORU)

    secilen_ses = None
    ses_suresi = None

    if ses_dosyalari:
        print(f"✅ {len(ses_dosyalari)} ses dosyası bulundu:\n")
        for i, ses in enumerate(ses_dosyalari, 1):
            ses_yolu = os.path.join(SES_KLASORU, ses)
            ses_sure = ses_bilgisi_al(ses_yolu)
            sure_str = sure_formatla(ses_sure) if ses_sure else "Bilinmiyor"
            print(f"   {i}. {ses[:70]} - {sure_str}")

        print(f"\n💡 Ses dosyası kullanmak ister misiniz?")
        print(f"   • Evet: Numarasını girin (1-{len(ses_dosyalari)})")
        print(f"   • Hayır: Enter")

        secim = input(f"\n   🎵 Seçim [Enter=ses yok]: ").strip()

        if secim and secim.isdigit():
            index = int(secim) - 1
            if 0 <= index < len(ses_dosyalari):
                secilen_ses = os.path.join(SES_KLASORU, ses_dosyalari[index])
                ses_suresi = ses_bilgisi_al(secilen_ses)

                if ses_suresi:
                    print(f"\n   ✅ Seçilen ses: {ses_dosyalari[index]}")
                    print(f"   ⏱️  Ses süresi: {sure_formatla(ses_suresi)}")
                else:
                    print(f"\n   ❌ Ses bilgisi okunamadı")
                    secilen_ses = None
            else:
                print(f"\n   ❌ Geçersiz seçim")
        else:
            print(f"\n   ℹ️  Ses kullanılmayacak")
    else:
        print(f"ℹ️  {SES_KLASORU} klasöründe ses dosyası bulunamadı")

    print("=" * 100)

    hedef_sure = hedef_sure_al(secilen_ses is not None, ses_suresi)

    # ========== SUBTITLE CONFIG (Kanal türüne göre) ==========
    subtitle_config = SUBTITLE_CONFIG.copy()

    if hikaye_modu:
        # HİKAYE MODU - Otomatik ayarlar
        from config import STORY_CHANNEL_PRESET
        subtitle_config['font'] = secilen_font
        subtitle_config['fontsize'] = int(72 * font_multiplier)
        subtitle_config['outline_width'] = outline_width
        subtitle_config['shadow'] = shadow
        subtitle_config['position'] = 'bottom'
        subtitle_config['use_dynamic'] = False
        subtitle_config['platform'] = STORY_CHANNEL_PRESET['platform']
        subtitle_config['style'] = 'tiktok'  # 🎨 Otomatik: TikTok Viral

    else:
        # GENEL MOD - Manuel ayarlar
        subtitle_config['font'] = secilen_font
        subtitle_config['fontsize'] = int(72 * font_multiplier)
        subtitle_config['outline_width'] = outline_width
        subtitle_config['shadow'] = shadow
        subtitle_config['position'] = 'bottom'
        subtitle_config['use_dynamic'] = False
        subtitle_config['style'] = 'classic'  # 🎨 Otomatik: Classic Karaoke

    if subtitle_config and subtitle_config.get('mode') == 'auto' and secilen_ses:
        subtitle_config = otomatik_altyazi_olustur(secilen_ses, subtitle_config)
        if not subtitle_config:
            print(f"   ⚠️  Otomatik altyazı başarısız, devam ediliyor...")
        elif subtitle_config.get('use_dynamic'):
            print(f"   🎨 Dinamik altyazı özellikleri uygulanacak!")

    cikti_adi = random_dosya_adi_olustur()
    print(f"\n💾 ÇIKTI:")
    print(f"   📄 Dosya adı: {cikti_adi} (otomatik)")

    print(f"\n" + "=" * 100)
    print("✅ CAPCUT SEÇİLEBİLİR EFEKT EDITION - 30+ EFEKT + 35+ GEÇİŞ".center(100))
    print("=" * 100)
    print(f"   🎯 Hedef süre: {sure_formatla(hedef_sure)}")
    print(f"   💻 Encoder: {encoder_type.upper()}")

    if secilen_efektler is None:
        print(f"\n   🎨 EFEKT MODU: TÜM EFEKTLER (Random)")
        print(f"      • 30+ farklı efekt random kullanılacak")
    else:
        print(f"\n   🎨 EFEKT MODU: SEÇİLİ EFEKTLER ({len(secilen_efektler)} adet)")
        print(f"      • Sadece seçtikleriniz kullanılacak")

    print(f"\n   ✨ YENİ: TRANSITION EFFECTS (35+ Geçiş):")
    print(f"      • Fade, Wipe, Slide, Circle, Dissolve, Zoom...")
    print(f"      • Her klip arası profesyonel geçiş!")
    print(f"\n   🎬 CİNEMATİC EFEKTLER (30+ FARKLI):")
    print(f"      ⭐ CAPCUT POPÜLER (14 YENİ):")
    print(f"         • 🚀 Velocity/Speed Ramping (#1 CapCut efekti!)")
    print(f"         • 👻 Ghost Trail | 💡 Neon Glow | 📼 VHS Advanced")
    print(f"         • 💥 Datamosh | 🎨 Posterize | 🖼️  Edge Detection")
    print(f"         • 🪞 Mirror/Kaleidoscope | 🔲 Pixelate | ☀️  Solarize")
    print(f"         • 🖨️  Halftone | 💥 Shake Advanced | ✨ Particles")
    print(f"\n      📹 KLASİK EFEKTLER (16):")
    print(f"         • Camera Shake, 70s/80s/90s, Film Grain")
    print(f"         • Chromatic, Light Leaks, Glitch, Motion Blur")
    print(f"         • Zoom, Lens, Prism, 5 Color Grading")
    print(f"         • Dream Glow, RGB Split, Sharpen, Vignette")
    print(f"\n   🎬 Slow Motion | 📝 Auto Subs | 🎵 320kbps Audio")
    print("=" * 100)

    print(f"\n🚀 İşlem başlıyor...\n")

    temp_klasor = os.path.join(RENDER_KLASORU, 'temp_pro')
    os.makedirs(temp_klasor, exist_ok=True)

    cache_temizle(max_size_gb=5)

    try:
        baslangic = time.time()
        render_start_datetime = datetime.now()

        if secilen_ses and ses_suresi:
            secilen_videolar = akilli_video_sec(video_bilgileri, ses_suresi, max_varyasyon=10)
        else:
            secilen_videolar = akilli_video_sec(video_bilgileri, hedef_sure, max_varyasyon=10)

        playlist = playlist_olustur(secilen_videolar, hedef_sure, temp_klasor)

        basarili, sonuc = parallel_encode(
            playlist, cikti_adi, temp_klasor, RENDER_KLASORU,
            encoder_type, encoder_config, secilen_ses, subtitle_config, secilen_efektler
        )

        sure = time.time() - baslangic
        render_end_datetime = datetime.now()
        render_elapsed_seconds = sure
        compression_seconds = 0

        if os.path.exists(temp_klasor):
            try:
                shutil.rmtree(temp_klasor, ignore_errors=True)
            except:
                pass

        ilerleme_temizle()

        if basarili:
            dosya_boyutu = os.path.getsize(sonuc) / (1024 * 1024)
            gercek_sure_info = video_bilgisi_al(sonuc)
            gercek_sure = gercek_sure_info['sure'] if gercek_sure_info else 0

            print(f"\n{'='*80}")
            print(f"✅ BAŞARILI")
            print(f"{'='*80}")
            print(f"   Dosya: {sonuc}")
            print(f"   ⏱️  Süre: {sure_formatla(gercek_sure)}")
            print(f"   📊 Boyut: {dosya_boyutu:.1f} MB")
            print(f"   ⚡ İşlem: {int(sure // 60)}:{int(sure % 60):02d}")

            if secilen_efektler is None:
                print(f"\n   🎨 TÜM EFEKTLER KULLANILDI (Random)")
            else:
                print(f"\n   🎨 {len(secilen_efektler)} SEÇİLİ EFEKT KULLANILDI")

            print(f"\n   ✨ 35+ TRANSITION EFFECTS!")
            print(f"      • Fade, Wipe, Slide, Circle, Dissolve...")
            print(f"      • Her klip arası profesyonel geçiş!")
            print(f"\n   🎬 30+ CİNEMATİC EFEKT - SEÇİLEBİLİR:")
            print(f"      ⭐ YENİ CAPCUT POPÜLER (14):")
            print(f"         ✅ Velocity/Speed Ramping (#1 efekt!)")
            print(f"         ✅ Ghost Trail, Neon Glow, VHS Advanced")
            print(f"         ✅ Datamosh, Posterize, Edge Detection")
            print(f"         ✅ Mirror/Kaleidoscope, Pixelate, Solarize")
            print(f"         ✅ Halftone, Shake Advanced, Particles, Vignette")
            print(f"\n      📹 KLASİK EFEKTLER (16):")
            print(f"         ✅ Camera Shake, Vintage 70s/80s/90s, Film Grain")
            print(f"         ✅ Chromatic Aberration, Light Leaks, Glitch")
            print(f"         ✅ Motion Blur, Zoom Pulse, Lens Distortion")
            print(f"         ✅ Prism, 5 Color Grading, Dream Glow")
            print(f"         ✅ RGB Split Advanced, Sharpen Boost")
            print(f"\n   🚀 YOUTUBE'A HAZIR - CAPCUT ULTRA EDITION!")
            print("=" * 100)

            if os.path.exists(CACHE_KLASORU):
                try:
                    shutil.rmtree(CACHE_KLASORU, ignore_errors=True)
                    print(f"\n   ✅ Cache silindi!")
                except:
                    pass

            print(f"\n   ✅ Kaynak videolar korundu")
            print(f"   📄 Çıktı: {os.path.basename(sonuc)}")

            # ===== ⏱️ DETAYLI RENDER İSTATİSTİKLERİ =====
            print(f"\n" + "=" * 70)
            print("📊 DETAYLI RENDER İSTATİSTİKLERİ".center(70))
            print("=" * 70)

            # Zaman bilgileri
            print(f"\n   ⏱️  ZAMAN:")
            print(f"   ├── Başlangıç:     {render_start_datetime.strftime('%H:%M:%S')}")
            print(f"   ├── Bitiş:         {render_end_datetime.strftime('%H:%M:%S')}")
            render_mins = int(render_elapsed_seconds // 60)
            render_secs = int(render_elapsed_seconds % 60)
            print(f"   └── Toplam Süre:   {render_mins}:{render_secs:02d} ({render_elapsed_seconds:.1f}s)")

            # Video bilgileri
            print(f"\n   📹 VİDEO:")
            print(f"   ├── Çıktı Süresi:  {sure_formatla(gercek_sure)}")
            print(f"   ├── Dosya Boyutu:  {dosya_boyutu:.1f} MB")
            if gercek_sure > 0:
                bitrate_mbps = (dosya_boyutu * 8) / gercek_sure
                print(f"   ├── Bitrate:       {bitrate_mbps:.2f} Mbps")
                render_ratio = gercek_sure / render_elapsed_seconds if render_elapsed_seconds > 0 else 0
                print(f"   └── Hız Oranı:     {render_ratio:.1f}x realtime")

            # Klip bilgileri
            print(f"\n   🎬 KLİP:")
            print(f"   ├── Toplam Klip:   {len(playlist)}")
            if render_elapsed_seconds > 0:
                clips_per_min = len(playlist) / (render_elapsed_seconds / 60)
                print(f"   └── Klip/dakika:   {clips_per_min:.1f}")

            # Encoder bilgisi
            print(f"\n   🖥️  ENCODER:")
            print(f"   ├── Tip:           {encoder_type.upper()}")
            if encoder_type == 'nvidia':
                print(f"   └── GPU:           NVENC (RTX 5060 Ti)")
            else:
                print(f"   └── Mode:          Software")

            print(f"\n" + "=" * 70)

        else:
            print(f"\n❌ Hata: {sonuc}")

    except KeyboardInterrupt:
        print(f"\n\n⚠️  İşlem durduruldu.")

    except Exception as e:
        print(f"\n❌ Beklenmeyen hata: {e}")

    # ===== 📊 FFMPEG HUMANIZATION STATISTICS =====
    if FFMPEG_HUMANIZATION_AVAILABLE:
        try:
            print_encoding_dashboard()
        except Exception as e:
            logger.debug(f"Dashboard print error: {e}")

    input("\n\nDevam...")


if __name__ == "__main__":
    main()