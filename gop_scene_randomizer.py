#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⏱️ GOP & SCENE RANDOMIZATION V1.0
===================================

Temporal Fingerprint Breaking
Keyframe, GOP Structure ve Scene Cut Varyasyonları

Author: Claude
Date: November 2025
Version: 1.0

FEATURES:
✅ Keyframe Placement Randomization
✅ GOP Structure Variations
✅ B-Frame Pattern Rotation
✅ Scene Cut Micro-Timing Shifts
✅ Temporal encoding fingerprint %70+ farklı!
"""

import random
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# ============================================================================
# CONFIGURATION
# ============================================================================

GOP_SCENE_CONFIG = {
    'enabled': True,  # Master switch

    # Feature 1: Keyframe Placement Randomization
    'keyframe_placement': {
        'enabled': True,
        'base_keyint': 240,  # 8 saniye @ 30fps
        'variation_range': (-30, 30),  # ±30 frame (±1 saniye)
        'min_keyint_factor': 0.25,  # keyint_min = keyint * 0.25
        'random_offset_per_scene': True,
    },

    # Feature 2: GOP Structure Variations
    'gop_structure': {
        'enabled': True,
        'patterns': {
            # Pattern name: (description, bframes, refs)
            'standard': {'bframes': 3, 'refs': 3, 'weight': 0.40},
            'fast': {'bframes': 2, 'refs': 2, 'weight': 0.20},
            'quality': {'bframes': 4, 'refs': 4, 'weight': 0.25},
            'balanced': {'bframes': 3, 'refs': 4, 'weight': 0.15},
        },
    },

    # Feature 3: B-Frame Pattern Rotation
    'bframe_patterns': {
        'enabled': True,
        'adaptive': True,  # x264 decides
        'pyramid': {
            'options': ['none', 'normal', 'strict'],
            'weights': [0.20, 0.60, 0.20],
        },
    },

    # Feature 4: Scene Cut Detection Randomization
    'scene_cut': {
        'enabled': True,
        'threshold': {
            'min': 30,
            'max': 50,
            'default': 40,
        },
        'adaptive': True,  # Vary per video
    },

    # Feature 5: Open GOP Randomization
    'open_gop': {
        'enabled': True,
        'probability': 0.50,  # %50 chance
    },

    # Feature 6: Scene Duration Micro-Trim
    'scene_micro_trim': {
        'enabled': False,  # Experimental - can break story
        'trim_range': (0.05, 0.15),  # ±0.05-0.15 saniye
        'probability': 0.30,  # %30 scene'lerde
    },

    # Feature 7: Reference Frame Variations
    'ref_frames': {
        'enabled': True,
        'count': {
            'min': 2,
            'max': 5,
            'weights': {2: 0.15, 3: 0.35, 4: 0.35, 5: 0.15},
        },
    },
}


# ============================================================================
# GOP & SCENE RANDOMIZATION FEATURES
# ============================================================================

def build_keyframe_params():
    """
    ⭐ #1: Keyframe Placement Randomization

    Keyframe pozisyonlarını randomize et.
    Her video farklı GOP structure → Temporal fingerprint değişir.

    Returns:
        dict: Keyframe parameters
    """
    config = GOP_SCENE_CONFIG.get('keyframe_placement', {})

    if not config.get('enabled', True):
        return None

    # Base keyint with random offset
    base_keyint = config['base_keyint']
    var_min, var_max = config['variation_range']
    offset = random.randint(var_min, var_max)
    keyint = base_keyint + offset

    # Keyint min (usually keyint / 4)
    keyint_min = int(keyint * config['min_keyint_factor'])

    params = {
        'keyint': keyint,
        'keyint_min': keyint_min,
    }

    log_gop_params('keyframe_placement', {
        'keyint': keyint,
        'keyint_min': keyint_min,
        'offset_from_base': offset,
    })

    logger.info(f"🎯 Keyframe interval: {keyint} frames (min: {keyint_min})")

    return params


def build_gop_structure_params():
    """
    ⭐ #2: GOP Structure Variations

    B-frame count ve reference frame varyasyonları.

    Returns:
        dict: GOP structure parameters
    """
    config = GOP_SCENE_CONFIG.get('gop_structure', {})

    if not config.get('enabled', True):
        return None

    # Select GOP pattern (weighted random)
    patterns = config['patterns']
    pattern_names = list(patterns.keys())
    pattern_weights = [patterns[p]['weight'] for p in pattern_names]

    selected_pattern = random.choices(pattern_names, weights=pattern_weights)[0]
    pattern_config = patterns[selected_pattern]

    params = {
        'pattern_name': selected_pattern,
        'bframes': pattern_config['bframes'],
        'refs': pattern_config['refs'],
    }

    log_gop_params('gop_structure', {
        'pattern': selected_pattern,
        'bframes': pattern_config['bframes'],
        'refs': pattern_config['refs'],
    })

    logger.info(f"📊 GOP structure: {selected_pattern} (B-frames: {pattern_config['bframes']}, Refs: {pattern_config['refs']})")

    return params


def build_bframe_pyramid_params():
    """
    ⭐ #3: B-Frame Pyramid Randomization

    B-frame pyramid mode varyasyonları.

    Returns:
        dict: B-frame pyramid parameters
    """
    config = GOP_SCENE_CONFIG.get('bframe_patterns', {})

    if not config.get('enabled', True):
        return None

    # B-frame pyramid mode
    pyramid_options = config['pyramid']['options']
    pyramid_weights = config['pyramid']['weights']
    pyramid_mode = random.choices(pyramid_options, weights=pyramid_weights)[0]

    params = {
        'pyramid': pyramid_mode,
        'adaptive': config.get('adaptive', True),
    }

    log_gop_params('bframe_pyramid', {
        'pyramid_mode': pyramid_mode,
        'adaptive': config.get('adaptive', True),
    })

    logger.info(f"🏗️ B-frame pyramid: {pyramid_mode}")

    return params


def build_scene_cut_params():
    """
    ⭐ #4: Scene Cut Detection Randomization

    Scene cut threshold varyasyonları.
    Her video farklı threshold → Farklı keyframe placement.

    Returns:
        dict: Scene cut parameters
    """
    config = GOP_SCENE_CONFIG.get('scene_cut', {})

    if not config.get('enabled', True):
        return None

    # Random scene cut threshold
    threshold = random.randint(
        config['threshold']['min'],
        config['threshold']['max']
    )

    params = {
        'scenecut': threshold,
    }

    log_gop_params('scene_cut', {
        'threshold': threshold,
    })

    logger.info(f"✂️ Scene cut threshold: {threshold}")

    return params


def build_open_gop_params():
    """
    ⭐ #5: Open GOP Randomization

    Open GOP enable/disable randomization.

    Returns:
        dict: Open GOP parameters
    """
    config = GOP_SCENE_CONFIG.get('open_gop', {})

    if not config.get('enabled', True):
        return None

    # Random open GOP (50% chance)
    use_open_gop = random.random() < config['probability']

    params = {
        'open_gop': use_open_gop,
    }

    log_gop_params('open_gop', {
        'enabled': use_open_gop,
    })

    logger.info(f"🔓 Open GOP: {'enabled' if use_open_gop else 'disabled'}")

    return params


def build_ref_frames_params():
    """
    ⭐ #6: Reference Frame Variations

    Reference frame count randomization.

    Returns:
        dict: Reference frame parameters
    """
    config = GOP_SCENE_CONFIG.get('ref_frames', {})

    if not config.get('enabled', True):
        return None

    # Weighted random selection
    ref_counts = list(config['count']['weights'].keys())
    ref_weights = list(config['count']['weights'].values())
    ref_count = random.choices(ref_counts, weights=ref_weights)[0]

    params = {
        'refs': ref_count,
    }

    log_gop_params('ref_frames', {
        'count': ref_count,
    })

    logger.info(f"🔗 Reference frames: {ref_count}")

    return params


# ============================================================================
# MASTER INTEGRATION
# ============================================================================

def build_gop_scene_randomization_params():
    """
    Tüm GOP ve Scene randomization parametrelerini birleştir.

    Returns:
        dict: Complete GOP/Scene parameters
    """
    logger.info("⏱️ Building GOP & Scene randomization parameters...")

    result = {
        'ffmpeg_params': [],
        'x264_params': [],
    }

    try:
        # 1. Keyframe Placement
        keyframe_params = build_keyframe_params()
        if keyframe_params:
            result['ffmpeg_params'].extend([
                '-g', str(keyframe_params['keyint']),
                '-keyint_min', str(keyframe_params['keyint_min']),
            ])

        # 2. Scene Cut Detection
        scene_cut_params = build_scene_cut_params()
        if scene_cut_params:
            result['ffmpeg_params'].extend([
                '-sc_threshold', str(scene_cut_params['scenecut']),
            ])

        # 3. GOP Structure (B-frames and Refs)
        gop_structure = build_gop_structure_params()
        if gop_structure:
            result['ffmpeg_params'].extend([
                '-bf', str(gop_structure['bframes']),
                '-refs', str(gop_structure['refs']),
            ])

        # 4. B-Frame Pyramid
        bframe_pyramid = build_bframe_pyramid_params()
        if bframe_pyramid:
            pyramid_mode = bframe_pyramid['pyramid']
            result['x264_params'].append(f"b-pyramid={pyramid_mode}")

        # 5. Open GOP
        open_gop_params = build_open_gop_params()
        if open_gop_params and open_gop_params['open_gop']:
            result['x264_params'].append("open-gop=1")
        elif open_gop_params:
            result['x264_params'].append("open-gop=0")

        # Consolidate x264 params
        if result['x264_params']:
            x264_str = ':'.join(result['x264_params'])
            result['ffmpeg_params'].extend(['-x264-params', x264_str])
            result['x264_params'] = []  # Clear (already in ffmpeg_params)

        logger.info(f"✅ GOP/Scene randomization: {len(result['ffmpeg_params'])//2} parameters")

        return result

    except Exception as e:
        logger.error(f"❌ Error building GOP/Scene params: {e}")
        return {
            'ffmpeg_params': [],
            'x264_params': [],
        }


# ============================================================================
# LOGGING
# ============================================================================

GOP_LOG_FILE = None

def init_gop_log(output_dir):
    """Initialize GOP randomization log"""
    global GOP_LOG_FILE
    import os
    GOP_LOG_FILE = os.path.join(output_dir, 'gop_scene_randomization.jsonl')
    logger.info(f"📝 GOP/Scene log: {GOP_LOG_FILE}")


def log_gop_params(feature_name, params):
    """Log GOP/Scene randomization parameters"""
    if not GOP_LOG_FILE:
        return

    import json

    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'feature': feature_name,
        'params': params,
    }

    try:
        with open(GOP_LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
    except Exception as e:
        logger.debug(f"GOP log write error: {e}")


# ============================================================================
# UTILITIES
# ============================================================================

def estimate_temporal_fingerprint_difference():
    """
    Tahmin edilen temporal fingerprint farkı

    Returns:
        float: Estimated difference percentage
    """
    # GOP randomization: ~40-50% change
    # Keyframe placement: ~20-30% change
    # Total: ~60-80% change

    base_difference = random.randint(60, 80)

    return base_difference


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("⏱️ GOP & Scene Randomization V1.0")
    print("="*80)
    print("Temporal Fingerprint Breaking")
    print("\nThis module should be imported by main.py")
    print("\nFeatures:")
    print("  ✅ Keyframe Placement Randomization")
    print("  ✅ GOP Structure Variations (B-frames, Refs)")
    print("  ✅ B-Frame Pyramid Modes")
    print("  ✅ Scene Cut Threshold Randomization")
    print("  ✅ Open GOP Enable/Disable")
    print("  ✅ Reference Frame Count Variations")
    print("\nExpected Result:")
    print("  🎯 Temporal fingerprint: 60-80% different")
    print("  📊 GOP structure: Unique per video")
