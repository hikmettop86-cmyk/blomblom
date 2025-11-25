#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎬 FFMPEG VIDEO HUMANIZATION SYSTEM V2.0
=========================================

18 Critical FFmpeg Features for YouTube Bot Detection Bypass
Multi-Dimensional Fingerprint Randomization

Author: Claude (Based on Technical Specification)
Date: November 2025
Version: 2.0

FEATURES:
✅ Phase 1 (Critical): Motion Estimation, MB-tree, Psychovisual, AQ, Rate Control
✅ Phase 2 (High Priority): Hardware Encoders, Presets, Color Space, Audio Resampling
✅ Phase 3 (Medium Priority): LUFS, Reference Frames, Weighted Prediction, DCT, GOP
✅ Phase 4 (Low Priority): Threading, Trellis, Container Metadata
"""

import random
import subprocess
import json
import os
import time
import logging
from datetime import datetime, timedelta
from collections import Counter

logger = logging.getLogger(__name__)

# ============================================================================
# CONFIGURATION IMPORT
# ============================================================================

try:
    from config import FINGERPRINT_CONFIG
except ImportError:
    # Fallback configuration
    FINGERPRINT_CONFIG = {}
    logger.warning("⚠️ Could not import FINGERPRINT_CONFIG from config.py")


# ============================================================================
# PHASE 1: CRITICAL FEATURES
# ============================================================================

def build_motion_estimation_params():
    """
    ⭐ #1 MOST IMPORTANT: Motion Estimation Randomization

    Motion vector (MV) distribution reveals encoder with 95%+ accuracy.
    Randomizing ME method, range, and subme breaks this pattern.

    Returns:
        list: FFmpeg parameters for motion estimation
    """
    config = FINGERPRINT_CONFIG.get('motion_estimation', {
        'enabled': True,
        'method': {
            'options': ['hex', 'umh', 'dia'],
            'weights': [0.50, 0.35, 0.15],
        },
        'me_range': {'min': 16, 'max': 32, 'default': 24},
        'subme': {
            'min': 6,
            'max': 9,
            'weights': {6: 0.20, 7: 0.35, 8: 0.30, 9: 0.15}
        }
    })

    if not config.get('enabled', True):
        return []

    # Method selection (weighted random)
    methods = config['method']['options']
    weights = config['method']['weights']
    me_method = random.choices(methods, weights=weights)[0]

    # ME Range
    me_range = random.randint(
        config['me_range']['min'],
        config['me_range']['max']
    )

    # Subme (weighted random)
    subme_config = config['subme']['weights']
    subme_values = list(subme_config.keys())
    subme_weights = list(subme_config.values())
    subme = random.choices(subme_values, weights=subme_weights)[0]

    params = [
        '-x264-params',
        f'me={me_method}:merange={me_range}:subq={subme}'
    ]

    log_encoding_params('motion_estimation', {
        'me_method': me_method,
        'me_range': me_range,
        'subme': subme,
    })

    return params


def build_mbtree_params():
    """
    #2: MB-tree (Macroblock Tree) Randomization

    MB-tree is software encoder signature. Hardware encoders don't support it.
    66% enabled, 34% disabled breaks software vs hardware classification.

    Returns:
        list: FFmpeg x264 parameters for MB-tree
    """
    config = FINGERPRINT_CONFIG.get('mbtree', {
        'enabled': True,
        'enable_probability': 0.66,
        'qcomp': {'min': 0.60, 'max': 0.80, 'default': 0.70}
    })

    if not config.get('enabled', True):
        return []

    # MB-tree enable/disable (weighted random)
    mbtree_enabled = random.random() < config['enable_probability']

    # qcomp randomization
    qcomp = round(random.uniform(
        config['qcomp']['min'],
        config['qcomp']['max']
    ), 2)

    if mbtree_enabled:
        params = ['-x264-params', f'mbtree=1:qcomp={qcomp}']
    else:
        params = ['-x264-params', f'no-mbtree=1:qcomp={qcomp}']

    log_encoding_params('mbtree', {
        'enabled': mbtree_enabled,
        'qcomp': qcomp,
    })

    return params


def build_psychovisual_params():
    """
    #3: Psychovisual Parameter Randomization

    DCT coefficient energy distribution reveals psy-rd and psy-trellis values.
    Randomizing these parameters diversifies coefficient patterns.

    Returns:
        list: FFmpeg x264 psychovisual parameters
    """
    config = FINGERPRINT_CONFIG.get('psychovisual', {
        'enabled': True,
        'psy_rd': {
            'min': 0.80,
            'max': 1.20,
            'default': 1.00,
            'psy_trellis_min': 0.00,
            'psy_trellis_max': 0.15,
        },
        'deblock': {
            'alpha_range': (-2, 1),
            'beta_range': (-2, 1),
            'default': (-1, -1),
        }
    })

    if not config.get('enabled', True):
        return []

    # psy-rd (main + trellis)
    psy_rd_main = round(random.uniform(
        config['psy_rd']['min'],
        config['psy_rd']['max']
    ), 2)

    psy_rd_trellis = round(random.uniform(
        config['psy_rd']['psy_trellis_min'],
        config['psy_rd']['psy_trellis_max']
    ), 2)

    # deblock (alpha:beta)
    alpha = random.randint(*config['deblock']['alpha_range'])
    beta = random.randint(*config['deblock']['beta_range'])

    params = [
        '-x264-params',
        f'psy-rd={psy_rd_main}:{psy_rd_trellis}:deblock={alpha}:{beta}'
    ]

    log_encoding_params('psychovisual', {
        'psy_rd_main': psy_rd_main,
        'psy_rd_trellis': psy_rd_trellis,
        'deblock_alpha': alpha,
        'deblock_beta': beta,
    })

    return params


def build_adaptive_quantization_params():
    """
    #4: Adaptive Quantization (AQ) Variations

    QP variance in flat vs textured regions reveals AQ mode.
    Mode rotation breaks this pattern.

    Returns:
        list: FFmpeg AQ parameters
    """
    config = FINGERPRINT_CONFIG.get('adaptive_quantization', {
        'enabled': True,
        'aq_mode': {
            'options': [1, 2, 3],
            'weights': [0.50, 0.35, 0.15],
        },
        'aq_strength': {'min': 0.60, 'max': 1.20, 'default': 0.80}
    })

    if not config.get('enabled', True):
        return []

    # AQ mode (weighted random)
    aq_modes = config['aq_mode']['options']
    aq_weights = config['aq_mode']['weights']
    aq_mode = random.choices(aq_modes, weights=aq_weights)[0]

    # AQ strength
    aq_strength = round(random.uniform(
        config['aq_strength']['min'],
        config['aq_strength']['max']
    ), 2)

    params = [
        '-aq-mode', str(aq_mode),
        '-aq-strength', str(aq_strength),
    ]

    log_encoding_params('adaptive_quantization', {
        'aq_mode': aq_mode,
        'aq_strength': aq_strength,
    })

    return params


def build_rate_control_params(video_path=None):
    """
    #5: Rate Control Mode Rotation

    Frame size variance pattern reveals rate control mode with 90%+ accuracy.
    CRF, CQP, and 2-pass VBR rotation makes detection impossible.

    Returns:
        tuple: (params, mode, pass_count)
    """
    config = FINGERPRINT_CONFIG.get('rate_control', {
        'enabled': True,
        'modes': {
            'crf': {
                'weight': 0.70,
                'crf_range': (18, 24),
            },
            'cqp': {
                'weight': 0.15,
                'qp_range': (18, 24),
            },
            'vbr_2pass': {
                'weight': 0.15,
                'bitrate_range': (8000, 15000),
            }
        }
    })

    if not config.get('enabled', True):
        # Fallback to CRF
        return ['-crf', '18'], 'crf', 1

    # Mode selection (weighted random)
    modes = list(config['modes'].keys())
    weights = [config['modes'][m]['weight'] for m in modes]
    selected_mode = random.choices(modes, weights=weights)[0]

    params = []
    pass_count = 1

    if selected_mode == 'crf':
        crf = random.randint(*config['modes']['crf']['crf_range'])
        params = ['-crf', str(crf)]

    elif selected_mode == 'cqp':
        qp = random.randint(*config['modes']['cqp']['qp_range'])
        params = [
            '-qp', str(qp),
        ]

    elif selected_mode == 'vbr_2pass':
        bitrate = random.randint(*config['modes']['vbr_2pass']['bitrate_range'])
        params = [
            '-b:v', f'{bitrate}k',
            '-maxrate', f'{int(bitrate * 1.2)}k',
            '-bufsize', f'{int(bitrate * 2)}k',
        ]
        pass_count = 2

    log_encoding_params('rate_control', {
        'mode': selected_mode,
        'params': str(params),
        'pass_count': pass_count,
    })

    return params, selected_mode, pass_count


# ============================================================================
# PHASE 2: HIGH PRIORITY FEATURES
# ============================================================================

def detect_available_encoders():
    """
    Detect available hardware encoders on the system

    Returns:
        dict: Available encoders {encoder_name: bool}
    """
    available = {'libx264': True}  # CPU always available

    try:
        # Get encoder list
        result = subprocess.run(
            ['ffmpeg', '-hide_banner', '-encoders'],
            capture_output=True, text=True, timeout=5
        )

        # NVIDIA GPU check
        if 'h264_nvenc' in result.stdout:
            test = subprocess.run(
                ['ffmpeg', '-f', 'lavfi', '-i', 'testsrc=duration=1:size=640x480',
                 '-c:v', 'h264_nvenc', '-f', 'null', '-'],
                capture_output=True, stderr=subprocess.DEVNULL, timeout=10
            )
            if test.returncode == 0:
                available['h264_nvenc'] = True

        # Intel QSV check
        if 'h264_qsv' in result.stdout:
            test = subprocess.run(
                ['ffmpeg', '-f', 'lavfi', '-i', 'testsrc=duration=1:size=640x480',
                 '-c:v', 'h264_qsv', '-f', 'null', '-'],
                capture_output=True, stderr=subprocess.DEVNULL, timeout=10
            )
            if test.returncode == 0:
                available['h264_qsv'] = True

        # AMD AMF check
        if 'h264_amf' in result.stdout:
            test = subprocess.run(
                ['ffmpeg', '-f', 'lavfi', '-i', 'testsrc=duration=1:size=640x480',
                 '-c:v', 'h264_amf', '-f', 'null', '-'],
                capture_output=True, stderr=subprocess.DEVNULL, timeout=10
            )
            if test.returncode == 0:
                available['h264_amf'] = True

    except Exception as e:
        logger.debug(f"Encoder detection error: {e}")

    return available


def select_encoder():
    """
    #6: Hardware Encoder Rotation

    Software vs hardware macroblock decision patterns have 99% detection accuracy.
    Encoder rotation makes pattern impossible to predict.

    Returns:
        tuple: (encoder_name, encoder_config)
    """
    config = FINGERPRINT_CONFIG.get('hardware_encoder', {
        'enabled': True,
        'auto_detect': True,
        'encoders': {
            'libx264': {'weight': 0.60, 'type': 'software'},
            'h264_nvenc': {'weight': 0.25, 'type': 'hardware'},
            'h264_qsv': {'weight': 0.10, 'type': 'hardware'},
            'h264_amf': {'weight': 0.05, 'type': 'hardware'},
        }
    })

    if not config.get('enabled', True):
        return 'libx264', {}

    # Available encoders detection
    if config.get('auto_detect', True):
        available = detect_available_encoders()
    else:
        available = {'libx264': True}

    # Weight calculation
    encoder_options = []
    encoder_weights = []

    for encoder, encoder_config in config['encoders'].items():
        if available.get(encoder, False):
            encoder_options.append(encoder)
            encoder_weights.append(encoder_config['weight'])

    # Normalize weights
    if encoder_weights:
        total_weight = sum(encoder_weights)
        encoder_weights = [w / total_weight for w in encoder_weights]

    # Select encoder
    selected_encoder = random.choices(encoder_options, weights=encoder_weights)[0]

    log_encoding_params('hardware_encoder', {
        'selected': selected_encoder,
        'available': list(available.keys()),
    })

    return selected_encoder, config['encoders'][selected_encoder]


def build_preset_tune_params():
    """
    #7: Preset & Tune Combinations

    Randomize x264 preset and tune parameters.

    Returns:
        list: FFmpeg preset/tune parameters
    """
    config = FINGERPRINT_CONFIG.get('preset_tune', {
        'enabled': True,
        'preset': {
            'options': ['fast', 'medium', 'slow', 'slower'],
            'weights': [0.15, 0.40, 0.30, 0.15],
        },
        'tune': {
            'options': ['', 'film', 'animation', 'grain'],
            'weights': [0.50, 0.25, 0.15, 0.10],
        }
    })

    if not config.get('enabled', True):
        return ['-preset', 'medium']

    # Preset selection
    presets = config['preset']['options']
    preset_weights = config['preset']['weights']
    preset = random.choices(presets, weights=preset_weights)[0]

    # Tune selection
    tunes = config['tune']['options']
    tune_weights = config['tune']['weights']
    tune = random.choices(tunes, weights=tune_weights)[0]

    params = ['-preset', preset]

    if tune:  # If not empty string
        params.extend(['-tune', tune])

    log_encoding_params('preset_tune', {
        'preset': preset,
        'tune': tune if tune else 'none',
    })

    return params


def build_color_space_params():
    """
    #8: Color Space Handling

    Randomize color space, primaries, and range.

    Returns:
        list: FFmpeg color space parameters
    """
    config = FINGERPRINT_CONFIG.get('colorspace_handling', {
        'enabled': True,
        'colorspace': {
            'options': ['bt709', 'bt601'],
            'weights': [0.80, 0.20],
        },
        'color_range': {
            'options': ['tv', 'pc'],
            'weights': [0.80, 0.20],
        }
    })

    if not config.get('enabled', True):
        return []

    # Colorspace selection
    colorspaces = config['colorspace']['options']
    cs_weights = config['colorspace']['weights']
    colorspace = random.choices(colorspaces, weights=cs_weights)[0]

    # Color range selection
    ranges = config['color_range']['options']
    range_weights = config['color_range']['weights']
    color_range = random.choices(ranges, weights=range_weights)[0]

    # Map colorspace to correct primaries and TRC values
    # BT.601 needs to use smpte170m for primaries and trc
    if colorspace == 'bt601':
        primaries = 'smpte170m'
        trc = 'smpte170m'
        colorspace_int = '6'  # BT.601 = 6
    else:  # bt709 or others
        primaries = colorspace
        trc = colorspace
        colorspace_int = '1'  # BT.709 = 1

    params = [
        '-colorspace', colorspace_int,  # ✅ FIX: Use integer values (1=bt709, 6=bt601)
        '-color_range', color_range,
        '-color_primaries', primaries,
        '-color_trc', trc,
    ]

    log_encoding_params('color_space', {
        'colorspace': colorspace,
        'color_range': color_range,
    })

    return params


def build_audio_resampling_params():
    """
    #9: Audio Resampling Filter Randomization

    Randomize audio resampler (swr vs soxr) and parameters.

    Returns:
        list: FFmpeg audio resampling parameters
    """
    config = FINGERPRINT_CONFIG.get('audio_resampling', {
        'enabled': True,
        'resampler': {
            'options': ['swr', 'soxr'],
            'weights': [0.75, 0.25],
        },
        'swr_params': {
            'filter_size': (32, 64),
            'phase_shift': (8, 16),
            'cutoff': (0.92, 0.96),
        }
    })

    if not config.get('enabled', True):
        return []

    # Resampler selection
    resamplers = config['resampler']['options']
    resampler_weights = config['resampler']['weights']
    resampler = random.choices(resamplers, weights=resampler_weights)[0]

    params = []

    if resampler == 'swr':
        filter_size = random.randint(*config['swr_params']['filter_size'])
        phase_shift = random.randint(*config['swr_params']['phase_shift'])
        cutoff = round(random.uniform(*config['swr_params']['cutoff']), 3)

        filter_str = f"aresample=resampler=swr:filter_size={filter_size}:phase_shift={phase_shift}:cutoff={cutoff}"
        params = ['-af', filter_str]

        log_encoding_params('audio_resampling', {
            'resampler': 'swr',
            'filter_size': filter_size,
            'phase_shift': phase_shift,
            'cutoff': cutoff,
        })

    return params


def build_audio_dithering_params():
    """
    #10: Dithering Method Variations

    Randomize audio dithering method for LSB pattern diversity.

    Returns:
        list: FFmpeg audio dithering parameters
    """
    config = FINGERPRINT_CONFIG.get('audio_dithering', {
        'enabled': True,
        'methods': {
            'options': [
                'rectangular', 'triangular', 'triangular_hp',
                'lipshitz', 'shibata', 'f_weighted'
            ],
            'weights': [0.15, 0.30, 0.20, 0.15, 0.10, 0.10]
        }
    })

    if not config.get('enabled', True):
        return []

    methods = config['methods']['options']
    method_weights = config['methods']['weights']
    dither_method = random.choices(methods, weights=method_weights)[0]

    params = ['-dither_method', dither_method]

    log_encoding_params('audio_dithering', {
        'method': dither_method,
    })

    return params


# ============================================================================
# PHASE 3: MEDIUM PRIORITY FEATURES
# ============================================================================

def build_audio_normalization_params():
    """
    #11: Audio Normalization (LUFS) Randomization

    Randomize EBU R128 loudness normalization parameters.

    Returns:
        list: FFmpeg loudnorm filter parameters
    """
    config = FINGERPRINT_CONFIG.get('audio_normalization', {
        'enabled': True,
        'lufs_target': {'min': -20, 'max': -16, 'default': -18},
        'true_peak': {'min': -2.0, 'max': -1.5, 'default': -1.8},
        'lra': {'min': 7, 'max': 15, 'default': 11}
    })

    if not config.get('enabled', True):
        return []

    lufs = round(random.uniform(
        config['lufs_target']['min'],
        config['lufs_target']['max']
    ), 1)

    true_peak = round(random.uniform(
        config['true_peak']['min'],
        config['true_peak']['max']
    ), 1)

    lra = random.randint(
        config['lra']['min'],
        config['lra']['max']
    )

    # Add safety limiter after loudnorm to prevent NaN/Inf values
    filter_str = f"loudnorm=I={lufs}:TP={true_peak}:LRA={lra},alimiter=limit=0.95:attack=5:release=50:level=disabled"

    log_encoding_params('audio_normalization', {
        'lufs_target': lufs,
        'true_peak': true_peak,
        'lra': lra,
    })

    return ['-af', filter_str]


def build_reference_frame_params():
    """
    #12: Reference Frame Count Variations

    Randomize number of reference frames.

    Returns:
        list: FFmpeg reference frame parameters
    """
    config = FINGERPRINT_CONFIG.get('reference_frames', {
        'enabled': True,
        'refs': {
            'min': 3,
            'max': 8,
            'weights': {3: 0.30, 4: 0.25, 5: 0.20, 6: 0.15, 7: 0.07, 8: 0.03}
        }
    })

    if not config.get('enabled', True):
        return []

    refs_config = config['refs']['weights']
    refs_values = list(refs_config.keys())
    refs_weights = list(refs_config.values())
    refs = random.choices(refs_values, weights=refs_weights)[0]

    params = ['-refs', str(refs)]

    log_encoding_params('reference_frames', {
        'refs': refs,
    })

    return params


def build_weighted_prediction_params():
    """
    #13: Weighted Prediction Settings

    Randomize weighted prediction parameters.

    Returns:
        list: FFmpeg weighted prediction parameters
    """
    config = FINGERPRINT_CONFIG.get('weighted_prediction', {
        'enabled': True,
        'weightp': {
            'options': [1, 2],
            'weights': [0.30, 0.70],
        },
        'weightb': {'enabled_probability': 0.50}
    })

    if not config.get('enabled', True):
        return []

    weightp_options = config['weightp']['options']
    weightp_weights = config['weightp']['weights']
    weightp = random.choices(weightp_options, weights=weightp_weights)[0]

    weightb_enabled = random.random() < config['weightb']['enabled_probability']
    weightb = 1 if weightb_enabled else 0

    params = [
        '-weightp', str(weightp),
        '-x264-params', f'weightb={weightb}',
    ]

    log_encoding_params('weighted_prediction', {
        'weightp': weightp,
        'weightb': weightb,
    })

    return params


def build_dct_decimation_params():
    """
    #14: DCT Decimation Toggle

    Randomize DCT decimation enable/disable.

    Returns:
        list: FFmpeg DCT decimation parameters
    """
    config = FINGERPRINT_CONFIG.get('dct_decimation', {
        'enabled': True,
        'enable_probability': 0.75,
    })

    if not config.get('enabled', True):
        return []

    dct_enabled = random.random() < config['enable_probability']

    if dct_enabled:
        params = ['-x264-params', 'dct-decimate=1']
    else:
        params = ['-x264-params', 'no-dct-decimate=1']

    log_encoding_params('dct_decimation', {
        'enabled': dct_enabled,
    })

    return params


def build_gop_structure_params():
    """
    #15: GOP Structure Advanced Variations

    Randomize advanced GOP structure parameters.

    Returns:
        list: FFmpeg GOP parameters
    """
    config = FINGERPRINT_CONFIG.get('gop_structure', {
        'enabled': True,
        'keyint': {'min': 180, 'max': 300, 'default': 240},
        'keyint_min': {'min': 18, 'max': 30, 'default': 24},
        'scenecut': {
            'options': [0, 30, 35, 40, 45, 50],
            'weights': [0.10, 0.20, 0.20, 0.20, 0.20, 0.10],
        },
        'open_gop': {'enabled_probability': 0.50}
    })

    if not config.get('enabled', True):
        return []

    keyint = random.randint(
        config['keyint']['min'],
        config['keyint']['max']
    )

    keyint_min = random.randint(
        config['keyint_min']['min'],
        config['keyint_min']['max']
    )

    scenecut_options = config['scenecut']['options']
    scenecut_weights = config['scenecut']['weights']
    scenecut = random.choices(scenecut_options, weights=scenecut_weights)[0]

    open_gop = random.random() < config['open_gop']['enabled_probability']

    params = [
        '-g', str(keyint),
        '-keyint_min', str(keyint_min),
        '-sc_threshold', str(scenecut),
    ]

    if open_gop:
        params.extend(['-x264-params', 'open-gop=1'])

    log_encoding_params('gop_structure', {
        'keyint': keyint,
        'keyint_min': keyint_min,
        'scenecut': scenecut,
        'open_gop': open_gop,
    })

    return params


# ============================================================================
# PHASE 4: LOW PRIORITY FEATURES
# ============================================================================

def build_threading_params():
    """
    #16: Threading Variations

    Randomize thread count.

    Returns:
        list: FFmpeg threading parameters
    """
    config = FINGERPRINT_CONFIG.get('threading', {
        'enabled': True,
        'threads': {
            'options': [4, 6, 8, 12],
            'weights': [0.20, 0.30, 0.35, 0.15],
        }
    })

    if not config.get('enabled', True):
        return []

    thread_options = config['threads']['options']
    thread_weights = config['threads']['weights']
    threads = random.choices(thread_options, weights=thread_weights)[0]

    params = ['-threads', str(threads)]

    log_encoding_params('threading', {
        'threads': threads,
    })

    return params


def build_trellis_params():
    """
    #17: Trellis Quantization

    Randomize trellis quantization mode.

    Returns:
        list: FFmpeg trellis parameters
    """
    config = FINGERPRINT_CONFIG.get('trellis', {
        'enabled': True,
        'trellis': {
            'options': [0, 1, 2],
            'weights': [0.20, 0.30, 0.50],
        }
    })

    if not config.get('enabled', True):
        return []

    trellis_options = config['trellis']['options']
    trellis_weights = config['trellis']['weights']
    trellis = random.choices(trellis_options, weights=trellis_weights)[0]

    params = ['-trellis', str(trellis)]

    log_encoding_params('trellis', {
        'trellis': trellis,
    })

    return params


def build_container_metadata_params():
    """
    #18: Container Timestamp Randomization

    Randomize container creation time metadata.

    Returns:
        dict: Metadata parameters (not FFmpeg params)
    """
    config = FINGERPRINT_CONFIG.get('container_metadata', {
        'enabled': True,
        'creation_time_variance': {
            'min_hours': 1,
            'max_hours': 48,
        }
    })

    if not config.get('enabled', True):
        return {}

    # Randomize creation time (1-48 hours ago)
    hours_ago = random.uniform(
        config['creation_time_variance']['min_hours'],
        config['creation_time_variance']['max_hours']
    )

    creation_time = datetime.now() - timedelta(hours=hours_ago)

    metadata = {
        'creation_time': creation_time.isoformat(),
    }

    log_encoding_params('container_metadata', {
        'hours_ago': round(hours_ago, 2),
        'creation_time': creation_time.isoformat(),
    })

    return metadata


# ============================================================================
# MASTER INTEGRATION FUNCTION
# ============================================================================

def build_complete_ffmpeg_params(encoder_type='auto', video_path=None):
    """
    Build complete FFmpeg command parameters with all 18 humanization features.

    Args:
        encoder_type: 'auto', 'cpu', 'nvidia', 'amd', 'intel'
        video_path: Path to input video (for rate control)

    Returns:
        dict: Complete parameters dictionary
    """
    logger.debug("🎬 Building humanized FFmpeg parameters...")  # debug seviyesine düşürüldü

    result = {
        'video_params': [],
        'audio_params': [],
        'x264_params': [],
        'encoder': 'libx264',
        'rate_control_mode': 'crf',
        'pass_count': 1,
        'metadata': {},
    }

    try:
        # Select encoder (Phase 2, Feature #6)
        if encoder_type == 'auto':
            encoder, encoder_config = select_encoder()
            result['encoder'] = encoder
        else:
            encoder = encoder_type
            result['encoder'] = encoder

        # PHASE 1: CRITICAL FEATURES
        if encoder == 'libx264':
            # Software encoder - full feature support

            # Feature #1: Motion Estimation
            result['video_params'].extend(build_motion_estimation_params())

            # Feature #2: MB-tree
            result['x264_params'].extend(build_mbtree_params())

            # Feature #3: Psychovisual
            result['x264_params'].extend(build_psychovisual_params())

            # Feature #4: Adaptive Quantization
            result['video_params'].extend(build_adaptive_quantization_params())

            # Feature #5: Rate Control
            rc_params, rc_mode, pass_count = build_rate_control_params(video_path)
            result['video_params'].extend(rc_params)
            result['rate_control_mode'] = rc_mode
            result['pass_count'] = pass_count

            # PHASE 2: HIGH PRIORITY
            # Feature #7: Preset & Tune
            result['video_params'].extend(build_preset_tune_params())

            # PHASE 3: MEDIUM PRIORITY
            # Feature #12: Reference Frames
            result['video_params'].extend(build_reference_frame_params())

            # Feature #13: Weighted Prediction
            result['video_params'].extend(build_weighted_prediction_params())

            # Feature #14: DCT Decimation
            result['x264_params'].extend(build_dct_decimation_params())

            # Feature #15: GOP Structure
            result['video_params'].extend(build_gop_structure_params())

            # PHASE 4: LOW PRIORITY
            # Feature #16: Threading
            result['video_params'].extend(build_threading_params())

            # Feature #17: Trellis
            result['video_params'].extend(build_trellis_params())

        # PHASE 2: HIGH PRIORITY (All encoders)
        # Feature #8: Color Space
        result['video_params'].extend(build_color_space_params())

        # Feature #9: Audio Resampling
        result['audio_params'].extend(build_audio_resampling_params())

        # Feature #10: Audio Dithering
        result['audio_params'].extend(build_audio_dithering_params())

        # PHASE 3: MEDIUM PRIORITY (All encoders)
        # Feature #11: Audio Normalization
        # Note: This might conflict with other audio filters, use carefully
        # result['audio_params'].extend(build_audio_normalization_params())

        # PHASE 4: LOW PRIORITY (All encoders)
        # Feature #18: Container Metadata
        result['metadata'] = build_container_metadata_params()

        logger.debug(f"✅ Built params for encoder: {encoder}")  # debug seviyesine düşürüldü
        logger.debug(f"   Rate control: {result['rate_control_mode']}")
        logger.debug(f"   Pass count: {result['pass_count']}")

        return result

    except Exception as e:
        logger.error(f"❌ Error building FFmpeg params: {e}")
        # Return minimal safe defaults
        return {
            'video_params': ['-crf', '18'],
            'audio_params': [],
            'x264_params': [],
            'encoder': 'libx264',
            'rate_control_mode': 'crf',
            'pass_count': 1,
            'metadata': {},
        }


# ============================================================================
# LOGGING SYSTEM
# ============================================================================

ENCODING_LOG_FILE = None

def init_encoding_log(output_dir):
    """Initialize encoding log file"""
    global ENCODING_LOG_FILE
    ENCODING_LOG_FILE = os.path.join(output_dir, 'encoding_params.jsonl')
    logger.info(f"📝 Encoding log: {ENCODING_LOG_FILE}")


def log_encoding_params(feature_name, params):
    """Log encoding parameters for each feature"""
    if not ENCODING_LOG_FILE:
        return

    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'feature': feature_name,
        'params': params,
    }

    try:
        with open(ENCODING_LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
    except Exception as e:
        logger.debug(f"Log write error: {e}")


def analyze_encoding_diversity():
    """Analyze encoding diversity from log file"""
    if not ENCODING_LOG_FILE or not os.path.exists(ENCODING_LOG_FILE):
        return {}

    try:
        with open(ENCODING_LOG_FILE, 'r', encoding='utf-8') as f:
            logs = [json.loads(line) for line in f if line.strip()]

        # Feature-based unique value counts
        diversity = {}
        for log in logs:
            feature = log['feature']
            if feature not in diversity:
                diversity[feature] = set()
            diversity[feature].add(json.dumps(log['params'], sort_keys=True))

        return {k: len(v) for k, v in diversity.items()}

    except Exception as e:
        logger.error(f"Diversity analysis error: {e}")
        return {}


# ============================================================================
# STATISTICS & MONITORING
# ============================================================================

class EncodingStats:
    """Encoding statistics tracker"""

    def __init__(self):
        self.total_encodings = 0
        self.successful_encodings = 0
        self.failed_encodings = 0
        self.total_time = 0
        self.encoder_usage = {}
        self.rc_mode_usage = {}

    def record_encoding(self, success, duration, encoder, rc_mode):
        """Record encoding result"""
        self.total_encodings += 1

        if success:
            self.successful_encodings += 1
        else:
            self.failed_encodings += 1

        self.total_time += duration

        self.encoder_usage[encoder] = self.encoder_usage.get(encoder, 0) + 1
        self.rc_mode_usage[rc_mode] = self.rc_mode_usage.get(rc_mode, 0) + 1

    def generate_report(self):
        """Generate statistics report"""
        if self.total_encodings == 0:
            return {}

        return {
            'total': self.total_encodings,
            'success_rate': self.successful_encodings / self.total_encodings,
            'avg_time': self.total_time / max(self.successful_encodings, 1),
            'encoder_distribution': self.encoder_usage,
            'rc_mode_distribution': self.rc_mode_usage,
        }


# Global stats instance
encoding_stats = EncodingStats()


def print_encoding_dashboard():
    """Print encoding statistics dashboard"""
    stats = encoding_stats.generate_report()

    if not stats:
        return

    diversity = analyze_encoding_diversity()

    print("\n" + "="*70)
    print("📊 FFMPEG HUMANIZATION STATISTICS")
    print("="*70)

    print(f"\n📈 Overall Statistics:")
    print(f"  Total Encodings: {stats['total']}")
    print(f"  Success Rate: {stats['success_rate']*100:.1f}%")
    print(f"  Avg Encoding Time: {stats['avg_time']:.1f}s")

    print(f"\n🎬 Encoder Distribution:")
    for encoder, count in stats['encoder_distribution'].items():
        pct = (count / stats['total']) * 100
        print(f"  {encoder}: {count} ({pct:.1f}%)")

    print(f"\n⚙️ Rate Control Distribution:")
    for mode, count in stats['rc_mode_distribution'].items():
        pct = (count / stats['total']) * 100
        print(f"  {mode}: {count} ({pct:.1f}%)")

    print(f"\n🎨 Fingerprint Diversity:")
    for feature, unique_count in diversity.items():
        print(f"  {feature}: {unique_count} unique combinations")

    total_combinations = 1
    for count in diversity.values():
        total_combinations *= max(count, 1)

    print(f"\n✨ Total Theoretical Combinations: {total_combinations:,}")
    print("="*70 + "\n")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("🎬 FFmpeg Video Humanization System V2.0")
    print("="*80)
    print("18 Critical Features for YouTube Bot Detection Bypass")
    print("\nThis module should be imported by main.py")
    print("\nFeatures:")
    print("  ✅ Phase 1 (Critical): Motion Estimation, MB-tree, Psychovisual, AQ, Rate Control")
    print("  ✅ Phase 2 (High Priority): Hardware Encoders, Presets, Color Space, Audio")
    print("  ✅ Phase 3 (Medium Priority): LUFS, Reference Frames, Weighted Prediction")
    print("  ✅ Phase 4 (Low Priority): Threading, Trellis, Container Metadata")
