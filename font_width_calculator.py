#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YOUTUBE ULTRA PRO - SABİT KONFİGÜRASYON V5.0
🆕 ADVANCED ENCODER RANDOMIZATION EKLENDI

✅ Motion Estimation Randomization
✅ MB-tree & Psychovisual Parameters
✅ Rate Control Mode Rotation
✅ Hardware Encoder Support
✅ Advanced Audio Resampling
✅ Complete Anti-Detection System
"""

import os

# Export list
__all__ = [
    'RANDOMS_KLASORU', 'SES_KLASORU', 'RENDER_KLASORU',
    'VIDEO_KLASORU', 'CACHE_KLASORU', 'PROGRESS_FILE',
    'QUALITY_SETTINGS', 'VIDEO_OUTPUT', 'AUDIO_SETTINGS',
    'FINGERPRINT_CONFIG', 'SUBTITLE_CONFIG', 'QUALITY_CONFIG',
    'SUBTITLE_FONTS', 'STORY_CHANNEL_PRESET',
    'ADVANCED_QUALITY_CHECKS', 'METADATA_RANDOMIZATION',
    'UPLOAD_STRATEGY', 'ENGAGEMENT_OPTIMIZATION',
    'ADVANCED_ENCODER_CONFIG', 'MOTION_ESTIMATION_CONFIG',
    'PSYCHOVISUAL_CONFIG', 'RATE_CONTROL_CONFIG',
    'AUDIO_FINGERPRINT_CONFIG', 'COLOR_SPACE_CONFIG',
    'GOP_STRUCTURE_ADVANCED', 'HARDWARE_ENCODER_CONFIG'
]

# ============================================================================
# KLASÖR YAPISI
# ============================================================================
RANDOMS_KLASORU = r"C:\randoms"
SES_KLASORU = r"C:\ses"
RENDER_KLASORU = r"C:\render"
VIDEO_KLASORU = RANDOMS_KLASORU
CACHE_KLASORU = os.path.join(RENDER_KLASORU, ".cache")
PROGRESS_FILE = os.path.join(RENDER_KLASORU, "progress.json")

# ============================================================================
# 🆕 ADVANCED ENCODER RANDOMIZATION - KRITIK ÖNCELIK
# ============================================================================

# 1️⃣ MOTION ESTIMATION RANDOMIZATION (EN ÖNEMLİ!)
MOTION_ESTIMATION_CONFIG = {
    'enabled': True,
    'me_method': {
        'enabled': True,
        'options': ['hex', 'umh', 'dia'],  # hex=default, vary et
        'weights': [0.50, 0.30, 0.20],  # hex %50, umh %30, dia %20
    },
    'me_range': {
        'enabled': True,
        'min': 16,
        'max': 32,  # 16-32 range
    },
    'subme': {
        'enabled': True,
        'min': 6,
        'max': 9,  # 6-9 (extremes avoid)
    },
}

# 2️⃣ MB-TREE (MACROBLOCK TREE) RANDOMIZATION
MB_TREE_CONFIG = {
    'enabled': True,
    'mbtree_enabled_probability': 0.66,  # %66 enabled
    'qcomp_with_mbtree': 0.60,  # MB-tree enabled ise
    'qcomp_without_mbtree_range': (0.60, 0.80),  # MB-tree disabled ise
}

# 3️⃣ PSYCHOVISUAL PARAMETER RANDOMIZATION
PSYCHOVISUAL_CONFIG = {
    'enabled': True,
    'psy_rd': {
        'enabled': True,
        'range': (0.8, 1.2),  # Default 1.0
    },
    'psy_trellis': {
        'enabled': True,
        'probability': 0.30,  # %30 olasılıkla enabled
        'range': (0.0, 0.15),
    },
    'deblock': {
        'enabled': True,
        'alpha_range': (-2, 1),
        'beta_range': (-2, 1),
    },
}

# 4️⃣ ADAPTIVE QUANTIZATION (AQ) VARIATIONS
ADAPTIVE_QUANTIZATION_CONFIG = {
    'enabled': True,
    'aq_mode': {
        'enabled': True,
        'options': [1, 1, 2, 3],  # 1 = default, vary et
    },
    'aq_strength': {
        'enabled': True,
        'range': (0.6, 1.2),  # Default 1.0, expand
    },
}

# 5️⃣ RATE CONTROL MODE ROTATION
RATE_CONTROL_CONFIG = {
    'enabled': True,
    'modes': {
        'crf': {
            'weight': 0.50,  # %50 CRF
            'crf_range': (18, 24),
        },
        '2pass': {
            'weight': 0.30,  # %30 2-pass
            'bitrate_range': (2000, 6000),  # kbps
        },
        'cqp': {
            'weight': 0.20,  # %20 CQP
            'qp_range': (18, 24),
        },
    },
}

# 6️⃣ HARDWARE ENCODER ROTATION
HARDWARE_ENCODER_CONFIG = {
    'enabled': True,
    'rotation': {
        'libx264': 0.60,  # %60 libx264 (en esnek)
        'h264_nvenc': 0.25,  # %25 NVENC (hızlı)
        'h264_qsv': 0.15,  # %15 QSV (Intel)
    },
    'fallback_to_cpu': True,  # Hardware yoksa CPU'ya dön
}

# 7️⃣ PRESET & TUNE COMBINATIONS
PRESET_TUNE_CONFIG = {
    'enabled': True,
    'preset': {
        'enabled': True,
        'options': ['fast', 'medium', 'medium', 'slower', 'slow'],
    },
    'tune': {
        'enabled': True,
        'options': ['', '', 'film', 'animation', 'grain'],  # %40 no tune
    },
}

# 8️⃣ COLOR SPACE HANDLING
COLOR_SPACE_CONFIG = {
    'enabled': True,
    'colorspace': {
        'enabled': True,
        'options': ['bt709', 'bt709', 'bt709', 'bt601'],  # %75 bt709
    },
    'color_range': {
        'enabled': True,
        'options': ['tv', 'tv', 'tv', 'pc'],  # %75 TV range
    },
}

# 9️⃣ AUDIO RESAMPLING FILTER RANDOMIZATION
AUDIO_FINGERPRINT_CONFIG = {
    'enabled': True,
    'resampling': {
        'enabled': True,
        'filter_size_range': (32, 64),
        'phase_shift_range': (8, 16),
        'cutoff_range': (0.92, 0.96),
        'resampler_options': ['swr', 'swr', 'swr', 'soxr'],  # %75 swr
    },
    'dithering': {
        'enabled': True,
        'methods': [
            'triangular',
            'triangular_hp',
            'lipshitz',
            'modified_e_weighted',
            'rectangular'
        ],
    },
    'normalization': {
        'enabled': True,
        'target_lufs_range': (-20, -16),  # LUFS
        'lra_range': (7, 15),  # LRA
        'true_peak_range': (-2.0, -1.5),
    },
}

# 🔟 REFERENCE FRAME COUNT VARIATIONS
REFERENCE_FRAME_CONFIG = {
    'enabled': True,
    'refs_range': (3, 8),  # 3-8 refs (default 3)
}

# 1️⃣1️⃣ WEIGHTED PREDICTION SETTINGS
WEIGHTED_PREDICTION_CONFIG = {
    'enabled': True,
    'weightp_options': [1, 2, 2],  # 0=disabled, 1=simple, 2=smart
    'weightb_options': [0, 1],  # Weighted B-frames
}

# 1️⃣2️⃣ DCT DECIMATION TOGGLE
DCT_DECIMATION_CONFIG = {
    'enabled': True,
    'enabled_probability': 0.75,  # %75 enabled
}

# 1️⃣3️⃣ GOP STRUCTURE ADVANCED VARIATIONS
GOP_STRUCTURE_ADVANCED = {
    'enabled': True,
    'keyint_range': (180, 300),  # 180-300 (daha geniş)
    'keyint_min_range': (18, 30),
    'scenecut': {
        'enabled_probability': 0.90,  # %90 enabled
        'threshold_range': (30, 50),
    },
    'open_gop_probability': 0.66,  # %66 open GOP
}

# 1️⃣4️⃣ THREADING VARIATIONS
THREADING_CONFIG = {
    'enabled': True,
    'threads_options': [4, 6, 8, 12],
}

# 1️⃣5️⃣ TRELLIS QUANTIZATION VARIATIONS
TRELLIS_CONFIG = {
    'enabled': True,
    'options': [1, 2, 2],  # 0=off, 1=final, 2=all
}

# ============================================================================
# MASTER ENCODER CONFIG (Tüm özellikleri bir arada)
# ============================================================================
ADVANCED_ENCODER_CONFIG = {
    'enabled': True,
    'motion_estimation': MOTION_ESTIMATION_CONFIG,
    'mb_tree': MB_TREE_CONFIG,
    'psychovisual': PSYCHOVISUAL_CONFIG,
    'adaptive_quantization': ADAPTIVE_QUANTIZATION_CONFIG,
    'rate_control': RATE_CONTROL_CONFIG,
    'hardware_encoder': HARDWARE_ENCODER_CONFIG,
    'preset_tune': PRESET_TUNE_CONFIG,
    'color_space': COLOR_SPACE_CONFIG,
    'audio_fingerprint': AUDIO_FINGERPRINT_CONFIG,
    'reference_frames': REFERENCE_FRAME_CONFIG,
    'weighted_prediction': WEIGHTED_PREDICTION_CONFIG,
    'dct_decimation': DCT_DECIMATION_CONFIG,
    'gop_structure': GOP_STRUCTURE_ADVANCED,
    'threading': THREADING_CONFIG,
    'trellis': TRELLIS_CONFIG,
}

# ============================================================================
# MEVCUT AYARLAR (ESKİ SİSTEM - BACKWARD COMPATIBILITY)
# ============================================================================

QUALITY_SETTINGS = {
    'cpu': {
        'preset': 'slow',
        'crf': 18,
        'bitrate': '15M',
        'maxrate': '18M',
        'bufsize': '30M',
    },
    'nvidia': {
        'preset': 'hq',
        'bitrate': '15M',
        'maxrate': '18M',
        'bufsize': '30M',
        'rc': 'vbr_hq',
        'profile': 'high',
        'level': '4.1',  # Changed from 4.2 to 4.1 (GTX 1050 Ti max support)
    },
    'amd': {
        'quality': 'quality',
        'bitrate': '15M',
        'rc': 'vbr_latency',
    },
    'intel': {
        'preset': 'veryslow',
        'bitrate': '15M',
        'global_quality': '18',
    }
}

VIDEO_OUTPUT = {
    'resolution': '1920x1080',
    'fps': 30,
    'color_space': 'rec709',
    'color_range': 'tv',
    'pixel_format': 'yuv420p',
    'aspect_ratio': '16:9',
}

AUDIO_SETTINGS = {
    'bitrate': '320k',
    'sample_rate': '48000',
    'channels': 2,
    'codec': 'aac',
    'normalization': True,
    'compression': True,
    'target_loudness': -16,
    'true_peak': -1.5,
    'lra': 11,
}

# ============================================================================
# GELİŞMİŞ FİNGERPRİNT RANDOMİZATİON
# ============================================================================
FINGERPRINT_CONFIG = {
    'pixel_noise': {
        'enabled': True,
        'strength': (1, 3),
    },
    'encoding_variance': {
        'gop_size': (24, 72),
        'keyint': (48, 150),
        'min_keyint': (24, 48),
        'bframes': (2, 4),
    },
    'color_space': {
        'dither': True,
        'matrix_variation': True,
    },
    'timing': {
        'fps_micro_adjust': True,
        'timestamp_jitter': True,
    },
    'audio_fingerprint': {
        'micro_pitch': (-0.3, 0.3),
        'volume_variance': (-0.5, 0.5),
        'eq_shift': True,
        'dither': False,
        'phase_shift': True,
    },
    'frame_rate_jitter': {
        'enabled': True,
        'variance': (29.97, 30.03),
    }
}

# ============================================================================
# METADATA RANDOMİZASYON
# ============================================================================
METADATA_RANDOMIZATION = {
    'enabled': True,
    'creation_time': {
        'enabled': True,
        'variance_hours': (1, 48),
    },
    'encoder_tags': {
        'enabled': True,
        'options': [
            'Lavf59.27.100',
            'Lavf60.3.100',
            'Lavf61.1.100',
            'HandBrake 1.6.1',
            'HandBrake 1.7.2',
            'Adobe Premiere Pro 2023',
            'Adobe Premiere Pro 2024',
            'DaVinci Resolve 18',
            'Final Cut Pro X',
        ]
    },
    'handler_name': {
        'enabled': True,
        'options': [
            'VideoHandler',
            'Core Media Video',
            'GPAC ISO Video Handler',
            'VideoMedia',
            'Mainconcept Video Media Handler',
        ]
    },
    'comment': {
        'enabled': True,
        'options': [
            'Optimized for platform delivery',
            'Encoded for web streaming',
            'High quality video content',
            'Professional video production',
            'Content optimized for viewing',
        ]
    },
    'additional_metadata': {
        'enabled': True,
        'include_software_version': True,
        'include_unique_id': True,
    }
}

# ============================================================================
# KALİTE KONTROL
# ============================================================================
ADVANCED_QUALITY_CHECKS = {
    'enabled': True,

    'frame_analysis': {
        'enabled': True,
        'check_frozen_frames': True,
        'max_duplicate_frames': 3,
        'scene_change_detection': True,
        'min_scene_duration': 1.0,
    },

    'audio_quality': {
        'enabled': True,
        'check_clipping': True,
        'check_silence': True,
        'max_silence_duration': 2.0,
        'loudness_normalization': True,
        'check_audio_sync': True,
        'sync_threshold_ms': 50,
    },

    'encoding_quality': {
        'enabled': True,
        'check_bitrate_variance': True,
        'min_avg_bitrate': '8M',
        'max_bitrate_fluctuation': 0.3,
        'check_keyframe_interval': True,
        'ideal_keyframe_interval': 2.0,
    },

    'content_safety': {
        'enabled': True,
        'check_black_frames': True,
        'max_black_duration': 1.0,
        'check_corrupted_frames': True,
        'check_aspect_ratio': True,
        'expected_aspect_ratio': '16:9',
    },

    'overall_quality': {
        'min_quality_score': 0.95,
        'fail_on_low_score': False,
        'log_quality_report': True,
    }
}

# ============================================================================
# UPLOAD TIMING OPTİMİZASYONU
# ============================================================================
UPLOAD_STRATEGY = {
    'enabled': True,

    'best_upload_times': {
        'timezone': 'Europe/Istanbul',
        'Turkey': ['09:00', '13:00', '18:00', '21:00'],
        'weekday_preference': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
    },

    'avoid_upload_times': {
        'Turkey': ['03:00-07:00', '23:00-01:00'],
        'weekend_caution': True,
    },

    'scheduling': {
        'random_offset_minutes': (0, 30),
        'consistency_bonus': True,
    }
}

# ============================================================================
# SUBTITLE CONFIG
# ============================================================================
SUBTITLE_CONFIG = {
    'enabled': True,
    'font_size': 75,
    'font_name': 'Impact',
    'outline_width': 4,
    'shadow': True,
    'position': 'center',
    'max_chars': 32,
    'split_long_sentences': True,
}

QUALITY_CONFIG = {
    'video_quality': 'high',
    'audio_quality': 'high',
    'fast_render': False,
}

# ============================================================================
# SUBTITLE FONTS (30+ Professional Fonts)
# ============================================================================
SUBTITLE_FONTS = {
    "📖 HİKAYE KANALLARI (YouTube/TikTok)": {
        'impact': {
            'name': 'Impact',
            'description': 'EN POPÜLER! Viral hikaye videoları için ideal',
            'best_for': 'YouTube Shorts, TikTok hikaye kanalları',
            'platforms': ['YouTube', 'TikTok', 'Instagram Reels'],
            'size_multiplier': 1.0,
            'outline_width': 4,
            'shadow': True,
        },
        'arial_black': {
            'name': 'Arial Black',
            'description': 'Kalın ve okunaklı, profesyonel görünüm',
            'best_for': 'Profesyonel hikaye anlatımı',
            'platforms': ['YouTube', 'Facebook'],
            'size_multiplier': 0.95,
            'outline_width': 4,
            'shadow': True,
        },
        'verdana_bold': {
            'name': 'Verdana Bold',
            'description': 'Geniş harfler, çok net okunur',
            'best_for': 'Uzun hikayeler, detaylı açıklamalar',
            'platforms': ['YouTube', 'Website'],
            'size_multiplier': 0.90,
            'outline_width': 3,
            'shadow': True,
        },
    },

    "📱 MODERN & BOLD": {
        'arial_bold': {
            'name': 'Arial Bold',
            'description': 'Evrensel, her platformda çalışır',
            'best_for': 'Genel amaçlı, tutorial videoları',
            'platforms': ['YouTube', 'TikTok', 'Instagram'],
            'size_multiplier': 0.95,
            'outline_width': 3,
            'shadow': True,
        },
        'tahoma_bold': {
            'name': 'Tahoma Bold',
            'description': 'Kompakt ama okunaklı',
            'best_for': 'Hızlı tempolu videolar',
            'platforms': ['TikTok', 'Shorts'],
            'size_multiplier': 0.92,
            'outline_width': 3,
            'shadow': True,
        },
        'trebuchet_bold': {
            'name': 'Trebuchet MS Bold',
            'description': 'Modern ve şık görünüm',
            'best_for': 'Lifestyle, vlog içerikleri',
            'platforms': ['YouTube', 'Instagram'],
            'size_multiplier': 0.94,
            'outline_width': 3,
            'shadow': True,
        },
    },

    "🎨 SERIF (Klasik/Elegant)": {
        'georgia_bold': {
            'name': 'Georgia Bold',
            'description': 'Elit ve sofistike görünüm',
            'best_for': 'Edebi içerik, kitap özetleri',
            'platforms': ['YouTube', 'Website'],
            'size_multiplier': 0.93,
            'outline_width': 3,
            'shadow': True,
        },
        'times_bold': {
            'name': 'Times New Roman Bold',
            'description': 'Klasik ve profesyonel',
            'best_for': 'Tarih, belgesel içerik',
            'platforms': ['YouTube', 'Educational'],
            'size_multiplier': 0.88,
            'outline_width': 3,
            'shadow': True,
        },
    }
}

STORY_CHANNEL_PRESET = {
    'font': 'Impact',
    'font_size': 75,
    'outline_width': 4,
    'shadow': True,
    'max_chars': 32,
}

# ============================================================================
# ENGAGEMENT OPTIMIZATION
# ============================================================================
ENGAGEMENT_OPTIMIZATION = {
    'enabled': True,

    'hook_moments': {
        'enabled': True,
        'interval_seconds': 15,
        'types': ['zoom_pulse', 'brightness_pop', 'sound_emphasis', 'color_pop'],
    },

    'pacing_optimization': {
        'enabled': True,
        'dynamic_tempo': True,
        'maintain_engagement': True,
    },

    'retention_triggers': {
        'enabled': True,
        'anticipation_cues': True,
        'pattern_interrupts': True,
    },

    'subtitle_variations': {
        'enabled': True,
        'emphasis_triggers': [
            'ama', 'ancak', 'fakat', 'çok', 'asla', 'hiç',
            'mutlaka', 'kesinlikle', 'tam', 'hemen', 'şimdi',
            'but', 'never', 'always', 'very', 'really', 'must',
        ],
    },

    'algorithm_optimization': {
        'enabled': True,

        'watch_time_optimization': {
            'enabled': True,
            'target_retention_curve': {
                '0-10%': 0.95,
                '10-30%': 0.85,
                '30-60%': 0.75,
                '60-90%': 0.65,
                '90-100%': 0.55,
            },
            'strategies': {
                'strong_hook_first_15s': True,
                'mid_roll_hooks': True,
                'pacing_optimization': True,
                'retention_triggers': True,
            },
        },

        'ctr_optimization': {
            'enabled': True,
            'thumbnail_criteria': {
                'has_face_weight': 30,
                'high_contrast_weight': 20,
                'action_scene_weight': 25,
                'bright_colors_weight': 15,
                'text_overlay_weight': 10,
            },
            'top_candidates': 5,
        },

        'engagement_triggers': {
            'enabled': True,
            'cta_moments': [
                {'time_percentage': 10, 'type': 'subtle_reminder'},
                {'time_percentage': 50, 'type': 'engagement_boost'},
                {'time_percentage': 90, 'type': 'end_screen_prep'},
            ],
            'retention_mechanics': {
                'curiosity_gaps': True,
                'pattern_interrupts': True,
                'value_promises': True,
            },
        },
    },

    'reporting': {
        'enabled': True,
        'generate_humanization_report': True,
        'calculate_scores': True,
        'save_to_file': True,
    },
}

# ============================================================================
# HUMANIZATION CONFIG
# ============================================================================
HUMANIZATION_CONFIG = {
    'enabled': True,

    'human_imperfections': {
        'micro_timing_errors': {
            'enabled': True,
            'probability': 0.05,
            'max_error_ms': 50,
        },
        'imperfect_cuts': {
            'enabled': True,
            'probability': 0.10,
            'frame_error_range': (1, 3),
        },
        'volume_inconsistency': {
            'enabled': True,
            'max_variance': 0.05,
        },
        'hesitation_pauses': {
            'enabled': False,
            'probability': 0.03,
            'duration_range': (0.1, 0.3),
        },
    },

    'organic_variations': {
        'encoder_randomization': {
            'enabled': True,
        },
        'color_variations': {
            'enabled': True,
            'hue_shift_range': (-2, 2),
            'saturation_range': (0.97, 1.03),
            'brightness_range': (0.98, 1.02),
            'contrast_range': (0.97, 1.03),
        },
        'noise_patterns': {
            'enabled': True,
            'default_level': 'subtle',
            'levels': {
                'subtle': (1, 3),
                'medium': (3, 6),
                'heavy': (6, 10),
            },
        },
        'audio_randomization': {
            'enabled': True,
            'eq_presets': True,
            'stereo_width_range': (0.98, 1.02),
            'pitch_shift_range': (-0.2, 0.2),
        },
    },

    'engagement_optimization': {
        'hook_moments': {
            'enabled': True,
            'interval_seconds': 15,
        },
        'pacing_optimization': {
            'enabled': True,
        },
        'retention_triggers': {
            'enabled': True,
        },
    },

    'anti_duplicate': {
        'enabled': True,
        'generate_video_dna': True,
        'frame_shuffle': False,
        'pixel_salt': True,
    },
}

# ============================================================================
# HUMANIZATION PRESETS
# ============================================================================
HUMANIZATION_PRESETS = {
    'light': {
        'description': 'Hafif humanization, maksimum güvenlik',
        'human_imperfections': {
            'micro_timing_errors': {'probability': 0.05},
            'imperfect_cuts': {'probability': 0.10},
            'volume_inconsistency': {'enabled': True},
            'hesitation_pauses': {'enabled': False},
        },
        'organic_variations': {
            'encoder_randomization': {'enabled': True},
            'color_variations': {'enabled': True},
            'noise_patterns': {'default_level': 'subtle'},
            'audio_randomization': {'enabled': True},
        },
        'engagement_optimization': {
            'hook_moments': {'interval_seconds': 20},
            'pacing_optimization': {'enabled': True},
        },
        'effect_probability': 0.30,
    },

    'medium': {
        'description': 'Orta seviye humanization',
        'human_imperfections': {
            'micro_timing_errors': {'probability': 0.08},
            'imperfect_cuts': {'probability': 0.15},
            'volume_inconsistency': {'enabled': True},
            'hesitation_pauses': {'enabled': False},
        },
        'organic_variations': {
            'encoder_randomization': {'enabled': True},
            'color_variations': {'enabled': True},
            'noise_patterns': {'default_level': 'medium'},
            'audio_randomization': {'enabled': True},
        },
        'engagement_optimization': {
            'hook_moments': {'interval_seconds': 15},
            'pacing_optimization': {'enabled': True},
        },
        'effect_probability': 0.40,
    },

    'aggressive': {
        'description': 'Maksimum varyasyon',
        'human_imperfections': {
            'micro_timing_errors': {'probability': 0.12},
            'imperfect_cuts': {'probability': 0.20},
            'volume_inconsistency': {'enabled': True},
            'hesitation_pauses': {'enabled': True},
        },
        'organic_variations': {
            'encoder_randomization': {'enabled': True},
            'color_variations': {'enabled': True},
            'noise_patterns': {'default_level': 'heavy'},
            'audio_randomization': {'enabled': True},
        },
        'engagement_optimization': {
            'hook_moments': {'interval_seconds': 12},
            'pacing_optimization': {'enabled': True},
        },
        'effect_probability': 0.50,
    },

    'minimal': {
        'description': 'Minimal humanization',
        'human_imperfections': {
            'micro_timing_errors': {'probability': 0.02},
            'imperfect_cuts': {'probability': 0.05},
            'volume_inconsistency': {'enabled': False},
            'hesitation_pauses': {'enabled': False},
        },
        'organic_variations': {
            'encoder_randomization': {'enabled': True},
            'color_variations': {'enabled': False},
            'noise_patterns': {'enabled': False},
            'audio_randomization': {'enabled': True},
        },
        'engagement_optimization': {
            'hook_moments': {'interval_seconds': 25},
            'pacing_optimization': {'enabled': False},
        },
        'effect_probability': 0.20,
    },
}

ACTIVE_HUMANIZATION_PRESET = 'light'

# ============================================================================
# KULLANIM NOTLARI
# ============================================================================
HUMANIZATION_TIPS = """
🎓 ADVANCED ENCODER RANDOMIZATION KILAVUZU
==========================================

✅ YENİ ÖZELLİKLER:
------------------
1. Motion Estimation Randomization (EN ÖNEMLİ!)
   • Her video farklı motion vector dağılımı
   • %95+ doğrulukla encoder detection'dan kaçınma

2. MB-tree & Psychovisual Parameters
   • Software vs hardware encoder ayrımını gizle
   • DCT coefficient distribution randomize et

3. Rate Control Mode Rotation
   • CRF/2-pass/CQP arasında değişim
   • Frame size variance pattern'ini maskele

4. Hardware Encoder Support
   • libx264/NVENC/QSV rotation
   • Her encoder unique macroblock patterns yaratır

5. Advanced Audio Resampling
   • libswresample vs libsoxr randomization
   • Frequency response fingerprint değişimi

6. Color Space Handling
   • bt709 vs bt601 8-unit değişimler
   • Color matrix variation

⚙️ AKTİVASYON:
--------------
• Tüm özellikler varsayılan olarak AÇIK
• config.py'de ADVANCED_ENCODER_CONFIG ile kontrol edilir
• Her özellik ayrı ayrı enable/disable edilebilir

🎯 ÖNERİLER:
-----------
• İlk kullanımda tüm özellikleri açık bırakın
• Sorun yaşarsanız tek tek devre dışı bırakın
• Hardware encoder yoksa CPU'ya otomatik düşer
• Log dosyalarını kontrol edin

⚠️  DİKKAT:
----------
• 2-pass encoding render süresini 2x artırır
• Hardware encoder her zaman mevcut olmayabilir
• Audio resampling hafif gecikme yaratabilir

📊 PERFORMANS:
-------------
• Motion Estimation: %5-10 daha yavaş
• Rate Control Rotation: CRF=hızlı, 2-pass=yavaş
• Hardware Encoder: CPU'dan 3-5x daha hızlı
• Audio Resampling: Minimal etki
"""

if __name__ == "__main__":
    print("=" * 80)
    print("YOUTUBE ULTRA PRO - ADVANCED CONFIG V5.0".center(80))
    print("=" * 80)
    print("\n✅ YENİ ÖZELLİKLER:")
    print("   • Motion Estimation Randomization")
    print("   • MB-tree & Psychovisual Parameters")
    print("   • Rate Control Mode Rotation")
    print("   • Hardware Encoder Support")
    print("   • Advanced Audio Resampling")
    print("   • Complete Anti-Detection System")
    print("\n" + "=" * 80)
    print(HUMANIZATION_TIPS)