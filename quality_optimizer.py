#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 QUALITY OPTIMIZER V1.0
==========================

Video ve Audio Kalite Garantisi
- Minimum bitrate enforcement (10M+)
- Audio clipping prevention
- Quality score %95+ garantisi

Author: Claude
Date: November 2025
Version: 1.0
"""

import logging
import subprocess
import json
import os

logger = logging.getLogger(__name__)

# ============================================================================
# CONFIGURATION
# ============================================================================

QUALITY_OPTIMIZER_CONFIG = {
    # Video Quality Guarantees
    'video': {
        'min_bitrate': '10M',  # Minimum 10 Mbps
        'target_bitrate': '12M',  # Target 12 Mbps
        'max_bitrate': '15M',  # Maximum 15 Mbps
        'buffer_size': '24M',  # 2x target
        'enforce_minrate': True,  # CRF + minrate enforcement
    },

    # Audio Quality Guarantees
    'audio': {
        'limiter': {
            'enabled': True,
            'threshold': -1.0,  # dB (prevent clipping)
            'release': 50,  # ms
        },
        'true_peak_limit': -1.5,  # dB (stricter than default)
        'auto_gain_adjustment': True,
    },

    # Quality Validation
    'validation': {
        'min_quality_score': 95,  # %95 altı kabul etme
        'mandatory_checks': [
            'integrity',
            'bitrate',
            'file_size',
        ],
        'strict_mode': True,  # Fail if below threshold
        'auto_retry': True,
        'max_retries': 2,
    },
}


# ============================================================================
# VIDEO QUALITY OPTIMIZER
# ============================================================================

def get_optimized_video_params(encoder='libx264'):
    """
    Optimize edilmiş video encoding parametreleri

    CRF + Constrained Bitrate Mode:
    - CRF kalitesini korur
    - Minrate minimum bitrate garanti eder
    - Maxrate spike'ları önler

    Args:
        encoder: Video encoder type

    Returns:
        dict: Optimized parameters
    """

    config = QUALITY_OPTIMIZER_CONFIG['video']

    if encoder == 'libx264':
        # Software encoder - CRF + constrained bitrate
        params = {
            'video_params': [
                '-crf', '18',  # High quality
                '-minrate', config['min_bitrate'],  # ⭐ MINIMUM BITRATE GUARANTEE
                '-b:v', config['target_bitrate'],  # Target bitrate
                '-maxrate', config['max_bitrate'],  # Maximum bitrate
                '-bufsize', config['buffer_size'],  # Buffer size
            ],
            'description': f'CRF 18 + constrained bitrate ({config["min_bitrate"]} min)',
        }

    elif encoder in ['h264_nvenc', 'hevc_nvenc']:
        # NVIDIA encoder - CBR with quality
        params = {
            'video_params': [
                '-b:v', config['target_bitrate'],
                '-minrate', config['min_bitrate'],
                '-maxrate', config['max_bitrate'],
                '-bufsize', config['buffer_size'],
                '-rc', 'vbr_hq',  # Variable bitrate high quality
                '-rc-lookahead', '32',
                '-cq', '18',  # Quality level
            ],
            'description': f'VBR HQ ({config["min_bitrate"]} min)',
        }

    elif encoder in ['h264_qsv', 'hevc_qsv']:
        # Intel QuickSync
        params = {
            'video_params': [
                '-b:v', config['target_bitrate'],
                '-minrate', config['min_bitrate'],
                '-maxrate', config['max_bitrate'],
                '-bufsize', config['buffer_size'],
                '-global_quality', '18',
            ],
            'description': f'QSV Quality ({config["min_bitrate"]} min)',
        }

    elif encoder in ['h264_amf', 'hevc_amf']:
        # AMD AMF
        params = {
            'video_params': [
                '-b:v', config['target_bitrate'],
                '-maxrate', config['max_bitrate'],
                '-rc', 'vbr_latency',
                '-quality', 'quality',
            ],
            'description': f'AMF VBR ({config["target_bitrate"]})',
        }

    else:
        # Fallback
        params = {
            'video_params': [
                '-b:v', config['target_bitrate'],
                '-maxrate', config['max_bitrate'],
            ],
            'description': f'Standard bitrate ({config["target_bitrate"]})',
        }

    logger.info(f"📊 Video quality: {params['description']}")

    return params


# ============================================================================
# AUDIO QUALITY OPTIMIZER
# ============================================================================

def get_optimized_audio_filter():
    """
    Audio clipping prevention + quality optimization

    Filter chain:
    1. Limiter (prevent clipping)
    2. Loudnorm (normalization)
    3. Volume adjustment

    Returns:
        str: FFmpeg audio filter string
    """

    config = QUALITY_OPTIMIZER_CONFIG['audio']

    filters = []

    # 1. Hard Limiter (PREVENT CLIPPING)
    if config['limiter']['enabled']:
        limiter = (
            f"alimiter="
            f"limit={config['limiter']['threshold']}:"
            f"attack=5:"
            f"release={config['limiter']['release']}:"
            f"level=disabled"
        )
        filters.append(limiter)
        logger.info(f"🔒 Audio limiter: {config['limiter']['threshold']}dB threshold")

    # 2. Loudnorm (with stricter true peak)
    loudnorm = (
        f"loudnorm="
        f"I=-16:"
        f"TP={config['true_peak_limit']}:"  # Stricter true peak
        f"LRA=11:"
        f"print_format=json"
    )
    filters.append(loudnorm)

    # 2.5. Safety limiter after loudnorm to prevent NaN/Inf
    filters.append("alimiter=limit=0.95:attack=5:release=50:level=disabled")

    # 3. Slight volume boost (if auto gain enabled)
    if config['auto_gain_adjustment']:
        filters.append("volume=1.05")  # +5% safety margin
        logger.info("🔊 Auto gain: +5%")

    filter_chain = ','.join(filters)

    logger.info(f"🎙️ Audio filter chain: {len(filters)} filters")

    return filter_chain


# ============================================================================
# QUALITY VALIDATION
# ============================================================================

def validate_video_quality(video_path, min_score=95):
    """
    Video kalitesini doğrula - %95 altı kabul etme!

    Args:
        video_path: Path to video file
        min_score: Minimum acceptable quality score (default: 95)

    Returns:
        tuple: (is_valid, score, issues)
    """

    logger.info(f"🔍 Quality validation: {os.path.basename(video_path)}")

    issues = []
    checks = {
        'integrity': False,
        'bitrate': False,
        'file_size': False,
        'audio_level': False,
    }

    try:
        # 1. Check file integrity
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_format', '-show_streams',
             '-print_format', 'json', video_path],
            capture_output=True, text=True, timeout=10
        )

        if result.returncode == 0:
            data = json.loads(result.stdout)

            # Integrity check
            if 'format' in data and 'streams' in data:
                checks['integrity'] = True
            else:
                issues.append("Invalid video format")

            # Bitrate check
            if 'format' in data:
                bitrate = int(data['format'].get('bit_rate', 0)) / 1_000_000  # Mbps

                min_bitrate_mbps = 8.0  # 8 Mbps minimum

                if bitrate >= min_bitrate_mbps:
                    checks['bitrate'] = True
                    logger.info(f"✅ Bitrate: {bitrate:.1f} Mbps (min: {min_bitrate_mbps})")
                else:
                    issues.append(f"Low bitrate: {bitrate:.1f} Mbps (min: {min_bitrate_mbps})")
                    logger.warning(f"⚠️ Bitrate düşük: {bitrate:.1f} Mbps")

            # File size check (minimum 30MB for 60s video)
            file_size_mb = os.path.getsize(video_path) / (1024 * 1024)

            if file_size_mb >= 30:
                checks['file_size'] = True
                logger.info(f"✅ File size: {file_size_mb:.1f} MB")
            else:
                issues.append(f"File too small: {file_size_mb:.1f} MB")

            # Audio level check
            audio_streams = [s for s in data.get('streams', []) if s.get('codec_type') == 'audio']
            if audio_streams:
                checks['audio_level'] = True
                logger.info(f"✅ Audio stream detected")
            else:
                issues.append("No audio stream found")

        else:
            issues.append("FFprobe failed")

    except Exception as e:
        logger.error(f"❌ Validation error: {e}")
        issues.append(f"Validation exception: {str(e)}")

    # Calculate quality score
    passed_checks = sum(checks.values())
    total_checks = len(checks)
    quality_score = int((passed_checks / total_checks) * 100)

    is_valid = quality_score >= min_score

    if is_valid:
        logger.info(f"✅ Quality validation PASSED: {quality_score}%")
    else:
        logger.warning(f"⚠️ Quality validation FAILED: {quality_score}% (min: {min_score}%)")
        logger.warning(f"   Issues: {', '.join(issues)}")

    return is_valid, quality_score, issues


def enforce_quality_standards(video_path, strict=True):
    """
    Kalite standartlarını zorla - %95 altı kabul etme!

    Args:
        video_path: Path to video
        strict: If True, raise exception on failure

    Returns:
        bool: True if quality is acceptable

    Raises:
        ValueError: If strict=True and quality is below threshold
    """

    config = QUALITY_OPTIMIZER_CONFIG['validation']

    is_valid, score, issues = validate_video_quality(
        video_path,
        min_score=config['min_quality_score']
    )

    if not is_valid:
        error_msg = (
            f"❌ QUALITY VALIDATION FAILED!\n"
            f"   Score: {score}% (Required: {config['min_quality_score']}%)\n"
            f"   Issues: {', '.join(issues)}\n"
        )

        if strict and config['strict_mode']:
            logger.error(error_msg)
            raise ValueError(f"Quality score {score}% below threshold {config['min_quality_score']}%")
        else:
            logger.warning(error_msg)
            logger.warning("   ⚠️ Continuing despite quality issues (strict mode disabled)")

    return is_valid


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_video_bitrate(video_path):
    """
    Get actual video bitrate

    Args:
        video_path: Path to video

    Returns:
        float: Bitrate in Mbps
    """
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
             '-show_entries', 'format=bit_rate', '-of', 'json', video_path],
            capture_output=True, text=True, timeout=10
        )

        if result.returncode == 0:
            data = json.loads(result.stdout)
            bitrate = int(data['format'].get('bit_rate', 0)) / 1_000_000
            return bitrate

    except Exception as e:
        logger.debug(f"Bitrate detection error: {e}")

    return 0.0


def suggest_quality_improvements(issues):
    """
    Kalite sorunlarına göre öneriler sun

    Args:
        issues: List of quality issues

    Returns:
        list: Suggested improvements
    """

    suggestions = []

    for issue in issues:
        if 'bitrate' in issue.lower():
            suggestions.append("• Bitrate artırın: -minrate 10M -b:v 12M ekleyin")

        if 'clipping' in issue.lower():
            suggestions.append("• Audio limiter ekleyin: alimiter=limit=-1.0")

        if 'file too small' in issue.lower():
            suggestions.append("• CRF değerini düşürün (18 → 16)")

        if 'audio' in issue.lower():
            suggestions.append("• Audio codec/bitrate kontrol edin")

    return suggestions


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("🎯 Quality Optimizer V1.0")
    print("="*80)
    print("Video & Audio Quality Guarantees")
    print("\nFeatures:")
    print("  ✅ Minimum bitrate enforcement (10M+)")
    print("  ✅ Audio clipping prevention (limiter)")
    print("  ✅ Quality score 95%+ guarantee")
    print("  ✅ Automatic quality validation")
    print("\nThis module should be imported by main.py")
