#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YOUTUBE ULTRA PRO - SABİT KONFİGÜRASYON
Bu dosyadaki ayarlar sistem düzeyinde sabit ayarlardır.
Genellikle değiştirilmez.

✅ YENİ: YouTube Algoritması Optimizasyonları
   - Gelişmiş Fingerprint Sistemi
   - Metadata Randomizasyonu
   - Kalite Kontrol Metrikleri
   - Upload Timing Optimizasyonu
"""

import os

# Export list - Import sorunlarını önlemek için
__all__ = [
    'RANDOMS_KLASORU', 'SES_KLASORU', 'RENDER_KLASORU',
    'VIDEO_KLASORU', 'CACHE_KLASORU', 'PROGRESS_FILE',
    'QUALITY_SETTINGS', 'VIDEO_OUTPUT', 'AUDIO_SETTINGS', 'QUALITY_OPTIMIZER_CONFIG',
    'GPU_ENCODING_CONFIG',
    'FINGERPRINT_CONFIG', 'AUDIO_HUMANIZATION_CONFIG', 'SUBTITLE_CONFIG', 'QUALITY_CONFIG',
    'SUBTITLE_FONTS', 'STORY_CHANNEL_PRESET',
    'ADVANCED_QUALITY_CHECKS', 'METADATA_RANDOMIZATION',
    'UPLOAD_STRATEGY', 'ENGAGEMENT_OPTIMIZATION'
]

# ============================================================================
# KLASÖR YAPISI
# ============================================================================
RANDOMS_KLASORU = r"C:\randoms"  # Video havuzu
SES_KLASORU = r"C:\ses"  # Ses havuzu
RENDER_KLASORU = r"C:\render"  # Çıktı klasörü
VIDEO_KLASORU = RANDOMS_KLASORU  # Backward compatibility
CACHE_KLASORU = os.path.join(RENDER_KLASORU, ".cache")
PROGRESS_FILE = os.path.join(RENDER_KLASORU, "progress.json")

# ============================================================================
# KALITE AYARLARI - OPTİMİZE (1080p 30fps YouTube)
# ============================================================================
# YouTube önerileri: 1080p 30fps SDR = 8 Mbps, max 12 Mbps
# ✅ DOSYA BOYUTU OPTİMİZE: 30 dk = ~1-1.5 GB (önceki: 3.4 GB)
QUALITY_SETTINGS = {
    'cpu': {
        'preset': 'medium',  # slow→medium (çok daha hızlı, hala iyi kalite)
        'crf': 23,  # 20→23 (daha küçük dosya, YouTube için yeterli kalite)
        'bitrate': '5M',  # 8M→5M (düşük dosya boyutu)
        'maxrate': '8M',  # 12M→8M
        'bufsize': '10M',  # 16M→10M (2x target)
    },
    'nvidia': {
        # ✅ RTX 5060 Ti (Blackwell) için optimize edildi
        'preset': 'p4',  # p1-p7 (p4=balanced speed/quality, RTX 50 için optimal)
        'cq': 23,  # CQ=23 (CRF benzeri, daha küçük dosya)
        'bitrate': '5M',  # 8M→5M
        'maxrate': '8M',  # 12M→8M
        'bufsize': '10M',  # 16M→10M
        'rc': 'vbr',  # Variable Bitrate (RTX 50 için uyumlu)
        'profile': 'high',
        'level': None,  # ✅ None = auto-detect (Invalid Level hatası önlenir)
        # RTX 50 özel ayarlar:
        'spatial_aq': 1,  # Spatial Adaptive Quantization (kalite artışı)
        'temporal_aq': 1,  # Temporal AQ (RTX 50 güçlü, kullan)
        'lookahead': 16,  # Frame lookahead (kalite artışı)
        'b_ref_mode': 'middle',  # B-frame reference mode (kalite)
    },
    'amd': {
        'quality': 'quality',
        'bitrate': '5M',  # 8M→5M
        'rc': 'vbr_latency',
    },
    'intel': {
        'preset': 'veryslow',
        'bitrate': '5M',  # 8M→5M
        'global_quality': '23',  # 20→23
    }
}

# ============================================================================
# VIDEO OUTPUT ÖZELLİKLERİ
# ============================================================================
VIDEO_OUTPUT = {
    'resolution': '1920x1080',
    'fps': 30,
    'color_space': 'rec709',
    'color_range': 'tv',
    'pixel_format': 'yuv420p',
    'aspect_ratio': '16:9',
}

# ============================================================================
# AUDIO QUALITY
# ============================================================================
AUDIO_SETTINGS = {
    'bitrate': '320k',
    'sample_rate': '48000',
    'channels': 2,
    'codec': 'aac',
    'normalization': True,
    'compression': False,  # ⚠️ KAPALI - Boğuk ses sorununa neden oluyordu (loudnorm yeterli)
    'target_loudness': -16,
    'true_peak': -1.5,
    'lra': 11,
}

# ============================================================================
# 🎯 QUALITY OPTIMIZER (Bitrate + Audio Clipping + Quality Guarantee)
# ============================================================================
QUALITY_OPTIMIZER_CONFIG = {
    # Video Quality Guarantees (YouTube 1080p 30fps SDR optimized)
    # ✅ DOSYA BOYUTU OPTİMİZE: 30 dk = ~1-1.5 GB
    'video': {
        'min_bitrate': '4M',  # Minimum 4 Mbps (küçük dosya için)
        'target_bitrate': '5M',  # Target 5 Mbps (düşük dosya boyutu)
        'max_bitrate': '8M',  # Maximum 8 Mbps (peak için)
        'buffer_size': '10M',  # 2x target
        'enforce_minrate': True,  # CRF + minrate enforcement
    },

    # Audio Quality Guarantees
    'audio': {
        'limiter': {
            'enabled': True,  # ⭐ PREVENT CLIPPING (Problem: Audio clipping → Fixed!)
            'threshold': -1.0,  # dB
            'release': 50,  # ms
        },
        'true_peak_limit': -1.5,  # dB (stricter)
        'auto_gain_adjustment': True,  # Slight volume boost
    },

    # Quality Validation
    'validation': {
        'min_quality_score': 95,  # ⭐ %95 MINIMUM (Problem: %60 → Fixed!)
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
# 🚀 GPU OPTIMIZER V1.0 - NVIDIA NVENC Hardware Acceleration
# ============================================================================
#
# GPU encoding ile 5-10x daha hızlı rendering!
# - Rendering süresi: 10 dakika → 1-2 dakika
# - CPU kullanımı: %400 → %50 (-%90 azalma)
# - GPU kullanımı: %0 → %80 (tam kullanım)
# - Kalite: Aynı (CRF 18 = CQ 18)
# - Tüm özellikler: %100 korunuyor
#
# Requires:
# - NVIDIA GPU (GTX 10xx/16xx/RTX 20xx/30xx/40xx/50xx) ✅ RTX 5060 Ti destekleniyor!
# - FFmpeg with NVENC support (güncel sürüm önerilir)
# - NVIDIA drivers installed (RTX 50 için 565+ sürücü gerekli)
#
GPU_ENCODING_CONFIG = {
    # Enable/disable GPU encoding
    # ✅ NVENC artık gerçek test ile doğrulanıyor (SDK uyumluluğu kontrol ediliyor)
    # Eğer test başarısız olursa otomatik CPU'ya geçer
    'enabled': True,  # True = use GPU if available, False = always use CPU

    # ⚠️ RTX 5060 Ti (Blackwell) için önemli:
    # - FFmpeg'in güncel olması gerekiyor (BtbN builds önerilir)
    # - Yeni presetler: p1-p7 (p1=hızlı, p7=kaliteli)
    # - Eski presetler (fast/medium) çalışmayabilir

    # Quality mode: 'speed', 'balanced', 'quality'
    # - speed: ~10-15x faster, good quality (preset p3, cq 23) - RTX 50 ile çok hızlı!
    # - balanced: ~8-10x faster, excellent quality (preset p4, cq 21) ⭐ RECOMMENDED
    # - quality: ~6-8x faster, pristine quality (preset p6, cq 18)
    'quality_mode': 'balanced',

    # GPU selection (0 = first GPU, 1 = second GPU, etc.)
    'gpu_id': 0,

    # CUDA hardware-accelerated filters
    # Speeds up scaling, overlays, etc.
    'cuda_filters': {
        'enabled': True,  # Use CUDA-accelerated filters when possible
        'decode_accel': True,  # Hardware decoding (faster input reading)
    },

    # Fallback behavior
    'fallback_to_cpu': True,  # Auto-fallback to CPU if NVENC fails or unavailable

    # Performance monitoring
    'monitoring': {
        'enabled': True,  # Log GPU usage, encoding speed, temperature
        'detailed': False,  # Detailed per-clip metrics (more verbose)
    },
}

# ============================================================================
# 🎨 ADVANCED FINGERPRINT BREAKING (NEW MODULES)
# ============================================================================
# These features are configured in their own modules:
#
# 1. PERCEPTUAL HASH BREAKER (perceptual_hash_breaker.py)
#    - Pixel dithering, noise injection, color micro-shifts
#    - Config: PERCEPTUAL_HASH_CONFIG (inside module)
#    - Effect: 80-95% different perceptual hash
#
# 2. GOP & SCENE RANDOMIZATION (gop_scene_randomizer.py)
#    - Keyframe placement, GOP structure, B-frame patterns
#    - Config: GOP_SCENE_CONFIG (inside module)
#    - Effect: 60-80% different temporal fingerprint
#
# Import these modules in main.py for advanced fingerprint breaking!

# ============================================================================
# 🆕 GELİŞMİŞ FİNGERPRİNT RANDOMİZATİON (YouTube Duplicate Detection İçin)
# ============================================================================
FINGERPRINT_CONFIG = {
    # ========== LEGACY SETTINGS (Backward Compatibility) ==========
    'pixel_noise': {
        'enabled': True,
        'strength': (1, 3),  # Hafif pixel noise
    },
    'encoding_variance': {
        'gop_size': (24, 72),
        'keyint': (48, 150),
        'min_keyint': (24, 48),
        'bframes': (2, 4),
    },
    'color_space_legacy': {
        'dither': True,
        'matrix_variation': True,
    },
    # Backward compatibility for legacy code
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
        'volume_variance': (-0.5, 0.5),  # 🆕 Ses seviyesi varyasyonu
        'eq_shift': True,  # 🆕 Hafif EQ değişiklikleri
        'dither': False,
        'phase_shift': True,
    },
    'frame_rate_jitter': {
        'enabled': True,
        'variance': (29.97, 30.03),  # 🆕 Mikro FPS değişiklikleri
    },

    # ========== 🚀 FFMPEG HUMANIZATION V2.0 - 18 CRITICAL FEATURES ==========

    # PHASE 1: CRITICAL FEATURES (Week 1)

    # #1: Motion Estimation Randomization ⭐ MOST IMPORTANT
    'motion_estimation': {
        'enabled': True,
        'method': {
            'options': ['hex', 'umh', 'dia'],  # ESA çok yavaş, dikkatli kullan
            'weights': [0.50, 0.35, 0.15],  # hex en yaygın
        },
        'me_range': {
            'min': 16,
            'max': 32,
            'default': 24,
        },
        'subme': {
            'min': 6,  # Fast
            'max': 9,  # Slow, best quality
            'weights': {  # Weighted random distribution
                6: 0.20,  # Fast encoding
                7: 0.35,  # Balanced
                8: 0.30,  # High quality
                9: 0.15,  # Best quality
            }
        }
    },

    # #2: MB-tree (Macroblock Tree) Randomization
    'mbtree': {
        'enabled': True,
        'enable_probability': 0.66,  # %66 enabled, %34 disabled
        'qcomp': {
            'min': 0.60,
            'max': 0.80,
            'default': 0.70,
        }
    },

    # #3: Psychovisual Parameter Randomization
    'psychovisual': {
        'enabled': True,
        'psy_rd': {
            'min': 0.80,
            'max': 1.20,
            'default': 1.00,
            'psy_trellis_min': 0.00,
            'psy_trellis_max': 0.15,
        },
        'deblock': {
            'alpha_range': (-2, 1),  # -2:-2 to 1:1
            'beta_range': (-2, 1),
            'default': (-1, -1),
        }
    },

    # #4: Adaptive Quantization (AQ) Variations
    'adaptive_quantization': {
        'enabled': True,
        'aq_mode': {
            'options': [1, 2, 3],
            'weights': [0.50, 0.35, 0.15],  # Mode 1 en yaygın
        },
        'aq_strength': {
            'min': 0.60,
            'max': 1.20,
            'default': 0.80,
        }
    },

    # #5: Rate Control Mode Rotation
    'rate_control': {
        'enabled': True,
        'modes': {
            'crf': {
                'weight': 0.70,  # %70 CRF kullan
                'crf_range': (22, 26),  # 18-24 → 22-26 (daha küçük dosya)
            },
            'cqp': {
                'weight': 0.15,  # %15 CQP
                'qp_range': (22, 26),  # 18-24 → 22-26
            },
            'vbr_2pass': {
                'weight': 0.15,  # %15 2-pass VBR
                'bitrate_range': (4000, 8000),  # 8000-15000 → 4000-8000 kbps
            }
        }
    },

    # PHASE 2: HIGH PRIORITY FEATURES (Week 2)

    # #6: Hardware Encoder Rotation
    # ⚠️ DÜZELTİLDİ: RTX 5060 Ti için GPU öncelikli (%90 GPU kullanımı)
    'hardware_encoder': {
        'enabled': True,
        'auto_detect': True,  # GPU availability check
        'encoders': {
            'libx264': {
                'weight': 0.10,  # ✅ %60 → %10 (GPU varsa CPU neredeyse hiç kullanılmasın)
                'type': 'software',
            },
            'h264_nvenc': {
                'weight': 0.85,  # ✅ %25 → %85 (RTX 5060 Ti için maksimum GPU kullanımı)
                'type': 'hardware',
            },
            'h264_qsv': {
                'weight': 0.03,  # Intel backup
                'type': 'hardware',
            },
            'h264_amf': {
                'weight': 0.02,  # AMD backup
                'type': 'hardware',
            }
        }
    },

    # #7: Preset & Tune Combinations
    'preset_tune': {
        'enabled': True,
        'preset': {
            'options': ['fast', 'medium', 'slow', 'slower'],
            'weights': [0.15, 0.40, 0.30, 0.15],
        },
        'tune': {
            'options': ['', 'film', 'animation', 'grain'],
            'weights': [0.50, 0.25, 0.15, 0.10],
        }
    },

    # #8: Color Space Handling (FFmpeg Humanization)
    'colorspace_handling': {
        'enabled': True,
        'colorspace': {
            'options': ['bt709', 'bt601'],
            'weights': [0.80, 0.20],  # bt709 modern standart
        },
        'color_range': {
            'options': ['tv', 'pc'],
            'weights': [0.80, 0.20],  # TV range yaygın
        },
    },

    # #9: Audio Resampling Filter Randomization
    'audio_resampling': {
        'enabled': True,
        'resampler': {
            'options': ['swr', 'soxr'],
            'weights': [0.75, 0.25],  # libswresample default
        },
        'swr_params': {
            'filter_size': (32, 64),
            'phase_shift': (8, 16),
            'cutoff': (0.92, 0.96),
        },
    },

    # #10: Dithering Method Variations
    'audio_dithering': {
        'enabled': True,
        'methods': {
            'options': [
                'rectangular',
                'triangular',
                'triangular_hp',
                'lipshitz',
                'shibata',
                'f_weighted',
            ],
            'weights': [
                0.15,  # rectangular
                0.30,  # triangular (common)
                0.20,  # triangular_hp
                0.15,  # lipshitz
                0.10,  # shibata
                0.10,  # f_weighted
            ]
        }
    },

    # PHASE 3: MEDIUM PRIORITY FEATURES (Week 3)

    # #11: Audio Normalization (LUFS) Randomization
    'audio_normalization': {
        'enabled': False,  # DIKKAT: Diğer audio filtreleriyle çakışabilir
        'lufs_target': {
            'min': -20,
            'max': -16,
            'default': -18,
        },
        'true_peak': {
            'min': -2.0,
            'max': -1.5,
            'default': -1.8,
        },
        'lra': {
            'min': 7,
            'max': 15,
            'default': 11,
        }
    },

    # #12: Reference Frame Count Variations
    'reference_frames': {
        'enabled': True,
        'refs': {
            'min': 3,
            'max': 8,
            'weights': {
                3: 0.30,
                4: 0.25,
                5: 0.20,
                6: 0.15,
                7: 0.07,
                8: 0.03,
            }
        }
    },

    # #13: Weighted Prediction Settings
    'weighted_prediction': {
        'enabled': True,
        'weightp': {
            'options': [1, 2],  # 1=simple, 2=smart
            'weights': [0.30, 0.70],  # 2 is default
        },
        'weightb': {
            'enabled_probability': 0.50,  # %50 enabled
        }
    },

    # #14: DCT Decimation Toggle
    'dct_decimation': {
        'enabled': True,
        'enable_probability': 0.75,  # %75 enabled (default)
    },

    # #15: GOP Structure Advanced Variations
    'gop_structure': {
        'enabled': True,
        'keyint': {
            'min': 180,
            'max': 300,
            'default': 240,
        },
        'keyint_min': {
            'min': 18,
            'max': 30,
            'default': 24,
        },
        'scenecut': {
            'options': [0, 30, 35, 40, 45, 50],
            'weights': [0.10, 0.20, 0.20, 0.20, 0.20, 0.10],
        },
        'open_gop': {
            'enabled_probability': 0.50,
        }
    },

    # PHASE 4: LOW PRIORITY FEATURES (Week 4)

    # #16: Threading Variations
    'threading': {
        'enabled': True,
        'threads': {
            'options': [4, 6, 8, 12],
            'weights': [0.20, 0.30, 0.35, 0.15],
        }
    },

    # #17: Trellis Quantization
    'trellis': {
        'enabled': True,
        'trellis': {
            'options': [0, 1, 2],  # 0=off, 1=final, 2=all
            'weights': [0.20, 0.30, 0.50],
        }
    },

    # #18: Container Timestamp Randomization
    'container_metadata': {
        'enabled': True,
        'creation_time_variance': {
            'min_hours': 1,
            'max_hours': 48,
        }
    },
}

# ============================================================================
# 🆕 METADATA RANDOMİZASYON (YouTube Algoritması İçin)
# ============================================================================
METADATA_RANDOMIZATION = {
    'enabled': True,
    'creation_time': {
        'enabled': True,
        'variance_hours': (1, 48),  # 1-48 saat önce oluşturulmuş gibi göster
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
        'include_unique_id': True,  # Her video için benzersiz ID
    }
}

# ============================================================================
# 🆕 GELİŞMİŞ KALİTE KONTROL SİSTEMİ
# ============================================================================
ADVANCED_QUALITY_CHECKS = {
    'enabled': True,  # Master switch

    'frame_analysis': {
        'enabled': True,
        'check_frozen_frames': True,
        'max_duplicate_frames': 3,  # Ardışık aynı frame sayısı
        'scene_change_detection': True,
        'min_scene_duration': 1.0,  # En az 1 saniye
    },

    'audio_quality': {
        'enabled': True,
        'check_clipping': True,  # Ses kırpması kontrolü
        'check_silence': True,  # Uzun sessizlik kontrolü
        'max_silence_duration': 2.0,  # Saniye
        'loudness_normalization': True,  # EBU R128 standardı
        'check_audio_sync': True,  # Audio-video senkronizasyonu
        'sync_threshold_ms': 50,  # Max 50ms sapma
    },

    'encoding_quality': {
        'enabled': True,
        'check_bitrate_variance': True,
        'min_avg_bitrate': '4M',  # Minimum ortalama bitrate (düşük dosya boyutu)
        'max_bitrate_fluctuation': 0.3,  # ±%30 kabul edilir
        'check_keyframe_interval': True,
        'ideal_keyframe_interval': 2.0,  # 2 saniyede bir
    },

    'content_safety': {
        'enabled': True,
        'check_black_frames': True,
        'max_black_duration': 1.0,  # Saniye
        'check_corrupted_frames': True,
        'check_aspect_ratio': True,
        'expected_aspect_ratio': '16:9',
    },

    'overall_quality': {
        'min_quality_score': 0.95,  # %95 başarı oranı gerekli
        'fail_on_low_score': False,  # True ise düşük skor = iptal
        'log_quality_report': True,  # Detaylı rapor oluştur
    }
}

# ============================================================================
# 🆕 UPLOAD TIMING OPTİMİZASYONU
# ============================================================================
UPLOAD_STRATEGY = {
    'enabled': True,

    'best_upload_times': {
        'timezone': 'Europe/Istanbul',
        'Turkey': ['09:00', '13:00', '18:00', '21:00'],
        'weekday_preference': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
    },

    'avoid_upload_times': {
        'late_night': ('00:00', '06:00'),  # Gece yükleme yapma
        'maintenance_hours': ['Tuesday-03:00'],  # YouTube bakım (UTC)
    },

    'upload_spacing': {
        'enabled': True,
        'min_interval_hours': 4,  # Videolar arası min süre
        'max_daily_uploads': 3,  # Günde max yükleme
        'consistent_schedule': True,  # Tutarlı saat diliminde yükle
    },

    'scheduling': {
        'auto_suggest_time': True,  # Otomatik en iyi saati öner
        'consider_audience_timezone': True,
        'peak_hours_priority': True,
    }
}

# ============================================================================
# 🆕 ENGAGEMENT OPTİMİZASYONU
# ============================================================================
ENGAGEMENT_OPTIMIZATION = {
    'enabled': True,

    'video_structure': {
        'hook_duration': 3,  # İlk 3 saniye çok kritik!
        'peak_moment': 0.6,  # Videonun %60'ında climax
        'call_to_action': {
            'enabled': False,  # Manuel eklenmeli
            'position': 'end',
            'duration': 3,
        }
    },

    'retention_optimization': {
        'pattern_breaks': {
            'enabled': True,
            'interval': 15,  # Her 15 saniyede bir değişiklik
            'types': ['zoom', 'transition', 'text'],
        },
        'pacing': {
            'fast_segments': 0.7,  # %70 hızlı
            'slow_segments': 0.3,  # %30 yavaş
        }
    },

    'watch_time_optimization': {
        'target_retention': 0.60,  # %60 ortalama izlenme hedefi
        'loop_potential': True,  # Video tekrar izlenebilir mi?
        'cliffhanger_endings': False,  # Hikaye kanalları için
    }
}

# ============================================================================
# ✨ ALTYAZI FONT KÜTÜPHANESİ - FFmpeg UYUMLU FONTLAR ✨
# ============================================================================
SUBTITLE_FONTS = {
    # ========== 📖 HİKAYE KANALI ÖNERİLERİ (EN İYİLER) ==========
    '📖 HİKAYE KANALLARI': {
        'impact': {
            'name': 'Impact',
            'description': '💥 #1 Hikaye kanalları için (En viral)',
            'best_for': 'Hikaye, viral içerik, TikTok',
            'size_multiplier': 1.0,
            'outline_width': 5,
            'shadow': True,
            'platforms': ['YouTube Shorts', 'TikTok', 'Instagram'],
            'recommended': True,
        },
        'arial_black': {
            'name': 'Arial Black',
            'description': '📌 Güvenli seçim, her hikaye için',
            'best_for': 'Genel hikaye içeriği',
            'size_multiplier': 1.0,
            'outline_width': 4,
            'shadow': True,
            'platforms': ['Tüm platformlar'],
            'recommended': True,
        },
        'verdana_bold': {
            'name': 'Verdana Bold',
            'description': '👓 En okunabilir hikaye fontu',
            'best_for': 'Uzun hikayeler, detaylı anlatım',
            'size_multiplier': 0.95,
            'outline_width': 4,
            'shadow': True,
            'platforms': ['YouTube', 'Instagram'],
            'recommended': True,
        },
        'tahoma_bold': {
            'name': 'Tahoma Bold',
            'description': '✨ Modern hikaye anlatımı',
            'best_for': 'Güncel hikayeler, vloglar',
            'size_multiplier': 0.95,
            'outline_width': 4,
            'shadow': True,
            'platforms': ['YouTube', 'TikTok'],
            'recommended': True,
        },
    },

    # ========== 🎬 SİNEMA & VİRAL FONTLARI (En Popüler) ==========
    '🔥 VIRAL & SİNEMA': {
        'trebuchet_bold': {
            'name': 'Trebuchet MS Bold',
            'description': '📰 Modern, temiz, profesyonel',
            'best_for': 'Haber, blog, genel içerik',
            'size_multiplier': 1.0,
            'outline_width': 3,
            'shadow': True,
            'platforms': ['YouTube', 'Blog'],
        },
    },

    # ========== 📱 MODERN & BOLD FONTLAR ==========
    '📱 MODERN & BOLD': {
        'arial_bold': {
            'name': 'Arial Bold',
            'description': '✨ Güvenilir, her sistemde var',
            'best_for': 'Genel kullanım, evrensel',
            'size_multiplier': 0.95,
            'outline_width': 3,
            'shadow': True,
            'platforms': ['Tüm platformlar'],
        },
        'georgia_bold': {
            'name': 'Georgia Bold',
            'description': '📖 Serif, okunabilir, elegant',
            'best_for': 'Kitap, makale, uzun metin',
            'size_multiplier': 1.0,
            'outline_width': 3,
            'shadow': True,
            'platforms': ['YouTube', 'Eğitim'],
        },
        'courier_bold': {
            'name': 'Courier New Bold',
            'description': '💻 Monospace, kodlama tarzı',
            'best_for': 'Tech, programming, terminal',
            'size_multiplier': 1.05,
            'outline_width': 3,
            'shadow': True,
            'platforms': ['Tech', 'Coding'],
        },
        'times_bold': {
            'name': 'Times New Roman Bold',
            'description': '📜 Klasik serif, resmi',
            'best_for': 'Formal, resmi, klasik',
            'size_multiplier': 1.0,
            'outline_width': 3,
            'shadow': True,
            'platforms': ['Formal', 'Resmi'],
        },
    },

    # ========== 🎨 CAPCUT ALTERNATIF FONTLAR ==========
    '🎨 CAPCUT STIL': {
        'calibri_bold': {
            'name': 'Calibri Bold',
            'description': '🌟 Modern, yumuşak köşeler',
            'best_for': 'Profesyonel, iş, sunum',
            'size_multiplier': 0.95,
            'outline_width': 3,
            'shadow': True,
            'platforms': ['İş', 'Sunum'],
        },
        'segoe_bold': {
            'name': 'Segoe UI Bold',
            'description': '🖥️ Windows modern UI fontu',
            'best_for': 'Tech, modern, temiz',
            'size_multiplier': 0.95,
            'outline_width': 3,
            'shadow': True,
            'platforms': ['Tech', 'Modern'],
        },
        'comic_bold': {
            'name': 'Comic Sans MS Bold',
            'description': '😊 Eğlenceli, casual, samimi',
            'best_for': 'Komedi, çocuk, eğlence',
            'size_multiplier': 1.0,
            'outline_width': 3,
            'shadow': True,
            'platforms': ['Komedi', 'Çocuk'],
        },
    },

    # ========== 💪 GÜÇLÜ WEB FONTLAR ==========
    '💪 WEB SAFE FONTLAR': {
        'helvetica_bold': {
            'name': 'Helvetica Bold',
            'description': '🎯 İsviçre tasarımı, minimal',
            'best_for': 'Minimalist, modern, şık',
            'size_multiplier': 0.95,
            'outline_width': 3,
            'shadow': True,
            'platforms': ['Modern', 'Minimal'],
        },
        'palatino_bold': {
            'name': 'Palatino Bold',
            'description': '✒️ Elegant serif, kitap tarzı',
            'best_for': 'Sanat, edebiyat, kültür',
            'size_multiplier': 1.0,
            'outline_width': 3,
            'shadow': True,
            'platforms': ['Sanat', 'Kültür'],
        },
        'lucida_bold': {
            'name': 'Lucida Sans Bold',
            'description': '🔍 Geometrik, temiz çizgiler',
            'best_for': 'Tech, bilim, modern',
            'size_multiplier': 0.95,
            'outline_width': 3,
            'shadow': True,
            'platforms': ['Tech', 'Bilim'],
        },
        'century_bold': {
            'name': 'Century Gothic Bold',
            'description': '📷 Yuvarlatılmış, modern',
            'best_for': 'Fashion, lifestyle, trend',
            'size_multiplier': 0.95,
            'outline_width': 3,
            'shadow': True,
            'platforms': ['Fashion', 'Lifestyle'],
        },
    },

    # ========== 🎭 YARATICI SISTEM FONTLARI ==========
    '🎭 YARATICI': {
        'consolas_bold': {
            'name': 'Consolas Bold',
            'description': '⌨️ Monospace, kod editör fontu',
            'best_for': 'Coding, hacking, tech',
            'size_multiplier': 1.05,
            'outline_width': 3,
            'shadow': True,
            'platforms': ['Coding', 'Tech'],
        },
        'cambria_bold': {
            'name': 'Cambria Bold',
            'description': '📖 Modern serif, okunabilir',
            'best_for': 'Eğitim, makale, formal',
            'size_multiplier': 1.0,
            'outline_width': 3,
            'shadow': True,
            'platforms': ['Eğitim', 'Formal'],
        },
        'candara_bold': {
            'name': 'Candara Bold',
            'description': '🌊 Yumuşak, modern humanist',
            'best_for': 'Casual, arkadaşça, vlog',
            'size_multiplier': 0.95,
            'outline_width': 3,
            'shadow': True,
            'platforms': ['Vlog', 'Casual'],
        },
        'constantia_bold': {
            'name': 'Constantia Bold',
            'description': '📚 Kitap serif, elegant',
            'best_for': 'Edebiyat, sanat, kültür',
            'size_multiplier': 1.0,
            'outline_width': 3,
            'shadow': True,
            'platforms': ['Sanat', 'Edebiyat'],
        },
    },

    # ========== 👔 PROFESYONEL SİSTEM FONTLARI ==========
    '👔 PROFESYONEL': {
        'franklin_bold': {
            'name': 'Franklin Gothic Bold',
            'description': '💼 Kurumsal, güçlü, net',
            'best_for': 'İş, kurumsal, ciddi',
            'size_multiplier': 1.0,
            'outline_width': 3,
            'shadow': True,
            'platforms': ['İş', 'Kurumsal'],
        },
        'garamond_bold': {
            'name': 'Garamond Bold',
            'description': '🎩 Klasik serif, lüks',
            'best_for': 'Lüks, premium, elegant',
            'size_multiplier': 1.0,
            'outline_width': 3,
            'shadow': True,
            'platforms': ['Lüks', 'Premium'],
        },
        'bookman_bold': {
            'name': 'Bookman Old Style Bold',
            'description': '📕 Kitap tarzı, okunabilir',
            'best_for': 'Kitap, edebiyat, uzun metin',
            'size_multiplier': 1.0,
            'outline_width': 3,
            'shadow': True,
            'platforms': ['Edebiyat', 'Eğitim'],
        },
        'corbel_bold': {
            'name': 'Corbel Bold',
            'description': '✨ Modern humanist, temiz',
            'best_for': 'Genel amaçlı, modern',
            'size_multiplier': 0.95,
            'outline_width': 3,
            'shadow': True,
            'platforms': ['Genel', 'Modern'],
        },
    },
}

# ============================================================================
# 📖 HİKAYE KANALI PRESET (Otomatik Ayarlar)
# ============================================================================
STORY_CHANNEL_PRESET = {
    'name': 'Hikaye Kanalı',
    'description': 'YouTube hikaye kanalları için optimize edilmiş ayarlar (YATAY 16:9)',
    'font': 'Impact',  # En viral font
    'font_size': 72,  # ✅ FIX: 80 → 72 (ekran taşmasını önler)
    'outline_width': 5,  # Kalın outline
    'shadow': True,
    'position': 'bottom',  # ✅ ALTTA (kesin!)
    'dynamic_subtitle': True,
    'platform': 'youtube_standard',  # ✅ FİX: youtube_standard (YATAY video!)
    'karaoke': True,  # Kelime kelime vurgulama
    'emoji': True,  # Otomatik emoji
    'animations': True,  # Fade, slide efektler
    'background': 'box',  # Okunabilirlik için
}

# ============================================================================
# 🎙️ AUDIO HUMANIZATION (ElevenLabs AI → Real Human Voice)
# ============================================================================
AUDIO_HUMANIZATION_CONFIG = {
    'enabled': True,  # Master switch - AI sesini gerçek ses gibi göster

    # Feature 1: Pitch Micro-Variations (Doğal ses titreşimleri)
    # ✅ İYİLEŞTİRİLDİ: Vibrato KAPALI (clipping ve distortion'a sebep oluyor)
    'pitch_variation': {
        'enabled': False,  # ⚠️ KAPALI - Vibrato ses kalitesini bozuyor
        'vibrato_frequency': {'min': 5.0, 'max': 6.0},  # Daha dar aralık
        'vibrato_depth': {'min': 0.05, 'max': 0.12},    # ULTRA HAFIF (0.15-0.35'ten düşürüldü)
        'random_drift': {'min': -0.03, 'max': 0.03},    # Minimal drift (daha da azaltıldı)
    },

    # Feature 2: Background Room Tone (Oda sesi / ambient gürültü)
    'room_tone': {
        'enabled': False,  # ⚠️ KAPALI - Çızırtıya sebep oluyor
        'noise_level': {'min': -70, 'max': -60},  # Çok daha sessiz
        'color': {
            'options': ['pink', 'brown'],  # White noise çıkarıldı (çok sert)
            'weights': [0.60, 0.40],
        },
        'high_pass_freq': {'min': 100, 'max': 200},  # Daha fazla filtre
    },

    # Feature 3: EQ Randomization (Frekans tepkisi varyasyonları)
    'eq_variation': {
        'enabled': True,
        'bass_boost': {'min': -0.3, 'max': 0.3},     # ULTRA HAFIF (daha da azaltıldı)
        'mid_cut': {'min': -0.2, 'max': 0.2},        # ULTRA HAFIF (daha da azaltıldı)
        'presence_boost': {'min': 0, 'max': 0.8},    # Daha hafif boost (1.5'ten düşürüldü)
        'air_boost': {'min': -0.2, 'max': 0.3},      # ULTRA HAFIF
    },

    # Feature 4: Compression Variations (Dinamik aralık)
    'compression': {
        'enabled': False,  # ⚠️ KAPALI - Loudnorm zaten var, çift compression problematik
        'threshold': {'min': -20, 'max': -12},  # Daha yüksek
        'ratio': {
            'options': [1.5, 2.0, 2.5],  # Daha hafif (4.0 çıkarıldı)
            'weights': [0.40, 0.40, 0.20],
        },
        'attack': {'min': 10, 'max': 30},   # Daha yavaş
        'release': {'min': 100, 'max': 300},  # Daha yavaş
        'makeup_gain': {'min': 2, 'max': 8},  # Daha fazla gain compensation
    },

    # Feature 5: Reverb (Oda akustiği)
    'reverb': {
        'enabled': False,  # ⚠️ KAPALI - Çok fazla efekt ses kalitesini düşürüyor
        'room_size': {'min': 5, 'max': 15},    # Daha küçük (önceki: 25)
        'reverberance': {'min': 5, 'max': 15},  # Çok hafif (önceki: 30)
        'wet_gain': {'min': -20, 'max': -12},   # ÇOK HAFIF (önceki: -8)
        'pre_delay': {'min': 5, 'max': 10},    # Kısa
    },

    # Feature 6: De-essing (Sibilance kontrolü - s/ş sesleri)
    'deessing': {
        'enabled': False,  # ⚠️ Complex filter - gerekirse açılabilir
        'frequency': {'min': 5000, 'max': 8000},  # Hz
        'threshold': {'min': -30, 'max': -20},    # dB
        'ratio': {
            'options': [2.0, 3.0, 4.0],
            'weights': [0.40, 0.40, 0.20],
        },
    },

    # Feature 7: Sample Rate Variations
    'sample_rate_variation': {
        'enabled': True,
        'rates': {
            'options': [44100, 48000],
            'weights': [0.30, 0.70],  # 48kHz YouTube için tercih ediliyor
        },
        'dithering': {
            'options': ['rectangular', 'triangular', 'lipshitz'],
            'weights': [0.20, 0.50, 0.30],
        },
    },
}

# ============================================================================
# SUBTITLE SETTINGS (Temel)
# ============================================================================
SUBTITLE_CONFIG = {
    'enabled': True,
    'mode': 'auto',
    'text': '',
    'segments': [],
    'font': 'Impact',  # Varsayılan - en popüler
    'fontsize': 72,
    'fontcolor': 'white',
    'highlight_word': '',
    'highlight_color': 'yellow',
    'position': 'bottom',
    'y_offset': 150,
    'outline': True,
    'outline_color': 'black',
    'outline_width': 3,
    'shadow': True,
    'box': False,
    'box_color': 'black@0.5',
    'animation': None,
    'auto_language': None,
    'auto_model': 'base',
    'max_words_per_line': 8,
    'min_duration': 1.5,
}

# ============================================================================
# KALİTE KONTROL (Basit - Geriye Uyumluluk İçin)
# ============================================================================
QUALITY_CONFIG = {
    'min_size_kb': 50,
    'max_black_frames': 5,
    'min_bitrate': '500k',
}  # !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 GELİŞMİŞ HUMANIZATION CONFIG
================================

Bu dosyayı config.py'nin SONUNA ekleyin!

YouTube algoritması ve bot detection için optimize edilmiş ayarlar.
"""

# ============================================================================
# 🤖 ADVANCED HUMANIZATION SETTINGS
# ============================================================================

HUMANIZATION_CONFIG = {
    'enabled': True,  # Master switch - TÜM sistemi açar/kapar

    # ========== 1. İNSAN DAVRANIŞI SİMÜLASYONU ==========
    'human_imperfections': {
        'enabled': True,

        'micro_timing_errors': {
            'enabled': True,
            'probability': 0.05,  # %5 segmentlerde timing hatası
            'max_variance_ms': 50,  # ±50ms varyasyon
        },

        'imperfect_cuts': {
            'enabled': True,
            'probability': 0.10,  # %10 kesim noktalarında hata
            'frame_variance': (1, 3),  # 1-3 frame kadar hata
        },

        'volume_inconsistency': {
            'enabled': True,
            'max_variance': 0.05,  # ±%5 ses seviyesi farkı
        },

        'hesitation_pauses': {
            'enabled': False,  # İHTİYATLI: Sync sorunlarına neden olabilir
            'probability': 0.03,  # %3 duraksama şansı
            'duration_range': (0.1, 0.3),  # 100-300ms
        },
    },

    # ========== 2. ORGANİK VARYASYON MOTORU ==========
    'organic_variations': {
        'enabled': True,

        'encoder_randomization': {
            'enabled': True,
            'gop_range': (24, 72),  # GOP size varyasyonu
            'keyint_range': (48, 150),  # Keyframe interval
            'bframe_range': (2, 4),  # B-frame sayısı
            'bitrate_variance': 0.10,  # ±%10 bitrate
            'me_methods': ['hex', 'umh', 'esa'],  # Motion estimation
            'subq_range': (7, 10),  # Subpixel refinement
        },

        'color_variations': {
            'enabled': True,
            'hue_shift_range': (-2, 2),  # ±2 derece (fark edilmez)
            'saturation_range': (0.97, 1.03),  # ±%3
            'brightness_range': (0.98, 1.02),  # ±%2
            'contrast_range': (0.97, 1.03),  # ±%3
        },

        'noise_patterns': {
            'enabled': True,
            'strength_levels': {
                'subtle': (1, 3),
                'medium': (3, 6),
                'heavy': (6, 10),
            },
            'default_level': 'subtle',  # 👈 Subtle önerilir
            'grain_size_range': (1.0, 2.0),
            'temporal_variation': True,  # Zamana bağlı değişim
        },

        'audio_randomization': {
            'enabled': True,

            # EQ presets (insan kulakla fark edemez)
            'eq_presets': [
                {'bass': 1.02, 'mid': 1.00, 'treble': 0.98},
                {'bass': 0.98, 'mid': 1.02, 'treble': 1.00},
                {'bass': 1.00, 'mid': 0.98, 'treble': 1.02},
                {'bass': 0.99, 'mid': 1.01, 'treble': 0.99},
            ],

            'stereo_width_range': (0.98, 1.02),  # ±%2
            'pitch_shift_range': (-0.2, 0.2),  # ±0.2% (fark edilmez)
        },
    },

    # ========== 3. ENGAGEMENT OPTİMİZATION ==========
    'engagement_optimization': {
        'enabled': True,

        'hook_moments': {
            'enabled': True,
            'interval_seconds': 15,  # Her 15 saniyede bir hook
            'interval_variance': 2,  # ±2 saniye varyasyon
            'types': [
                'zoom_pulse',  # Hafif zoom
                'brightness_pop',  # Parlaklık artışı
                'sound_emphasis',  # Ses vurgusu
                'color_pop',  # Renk patlaması
                'transition_hook',  # Geçiş efekti
            ],
        },

        'pacing_optimization': {
            'enabled': True,
            'first_segments_speedup': (0.9, 1.0),  # İlk segmentler hafif hızlı
            'middle_variation': (0.95, 1.05),  # Ortalar normal
            'final_speedup': (0.95, 1.0),  # Son hafif hızlı
        },

        'retention_triggers': {
            'enabled': True,
            'trigger_interval': 5,  # Her 5 altyazıda bir trigger
            'types': [
                'anticipation',  # "Ama şimdi..."
                'question',  # "Peki ya...?"
                'surprise',  # "İnanmayacaksınız ama..."
            ],
        },

        'optimal_length': {
            'story': (60, 180),  # 1-3 dakika (hikaye kanalları)
            'entertainment': (180, 480),  # 3-8 dakika
            'tutorial': (300, 900),  # 5-15 dakika
            'vlog': (480, 720),  # 8-12 dakika
        },
    },

    # ========== 4. ANTI-DUPLICATE SİSTEM ==========
    'anti_duplicate': {
        'enabled': True,

        'unique_dna': {
            'enabled': True,
            'include_timestamp': True,
            'include_random_salt': True,
            'include_session_id': True,
            'frame_shuffle_seed': True,  # Frame order'a hafif varyasyon
        },

        'invisible_watermark': {
            'enabled': True,
            'positions': ['topleft', 'topright', 'bottomleft', 'bottomright'],
            'alpha_range': (0.01, 0.02),  # Çok şeffaf (görünmez)
            'pattern_id_range': (10000, 99999),
        },

        'frame_order_variation': {
            'enabled': False,  # ⚠️ İHTİYATLI: Sync bozulabilir!
            'probability': 0.05,  # %5 B-frame'lerde
            'frame_types': ['B'],  # Sadece B-frame'ler
        },

        'unique_metadata': {
            'enabled': True,
            'creation_time_variance_hours': (1, 48),  # 1-48 saat önce
            'software_versions': [
                "FFmpeg 6.0.1-full_build",
                "FFmpeg 6.1-full_build",
                "FFmpeg 5.1.4",
                "Lavf59.27.100",
                "Lavf60.3.100",
                "HandBrake 1.6.1 2023011000",
                "HandBrake 1.7.2 2024010700",
            ],
            'encoders': [
                "Lavf59.27.100",
                "Lavf60.3.100",
                "x264 core 164",
                "x264 core 163",
            ],
        },
    },

    # ========== 5. ALTYAZI VARYASYONLARI ==========
    'subtitle_variations': {
        'enabled': True,

        'timing_randomization': {
            'enabled': True,
            'max_variance_ms': 50,  # ±50ms varyasyon
        },

        'style_variations': {
            'enabled': True,
            'fontsize_variance': 0.05,  # ±%5
            'outline_width_variance': 1,  # ±1px
            'y_position_variance': 20,  # ±20px
            'shadow_angles': [0, 45, 90, 135, 180, 225, 270, 315],
        },

        'word_emphasis': {
            'enabled': True,
            'emphasis_triggers': [
                # Türkçe
                'ama', 'ancak', 'fakat', 'çok', 'asla', 'hiç',
                'mutlaka', 'kesinlikle', 'tam', 'hemen', 'şimdi',
                # İngilizce
                'but', 'never', 'always', 'very', 'really', 'must',
            ],
        },
    },

    # ========== 6. ALGORİTMA SKORU OPTİMİZASYONU ==========
    'algorithm_optimization': {
        'enabled': True,

        'watch_time_optimization': {
            'enabled': True,

            # İdeal retention curve (YouTube'un sevdiği)
            'target_retention_curve': {
                '0-10%': 0.95,  # İlk %10: %95 retention (kritik!)
                '10-30%': 0.85,  # %10-30: %85 retention
                '30-60%': 0.75,  # %30-60: %75 retention
                '60-90%': 0.65,  # %60-90: %65 retention
                '90-100%': 0.55,  # Son %10: %55 retention
            },

            'strategies': {
                'strong_hook_first_15s': True,  # İlk 15 saniye kritik
                'mid_roll_hooks': True,  # Ortada hook'lar
                'pacing_optimization': True,  # Tempo optimizasyonu
                'retention_triggers': True,  # Tutma mekanizmaları
            },
        },

        'ctr_optimization': {
            'enabled': True,

            # Thumbnail için en iyi frame'leri bul
            'thumbnail_criteria': {
                'has_face_weight': 30,
                'high_contrast_weight': 20,
                'action_scene_weight': 25,
                'bright_colors_weight': 15,
                'text_overlay_weight': 10,
            },
            'top_candidates': 5,  # En iyi 5 anı öner
        },

        'engagement_triggers': {
            'enabled': True,

            'cta_moments': [
                {'time_percentage': 10, 'type': 'subtle_reminder'},
                {'time_percentage': 50, 'type': 'engagement_boost'},
                {'time_percentage': 90, 'type': 'end_screen_prep'},
            ],

            'retention_mechanics': {
                'curiosity_gaps': True,  # Merak boşlukları
                'pattern_interrupts': True,  # Tempo değişiklikleri
                'value_promises': True,  # "Az sonra göreceksiniz..."
            },
        },
    },

    # ========== 7. RAPORLAMA & ANALİZ ==========
    'reporting': {
        'enabled': True,
        'generate_humanization_report': True,
        'calculate_scores': True,
        'save_to_file': True,
    },
}

# ============================================================================
# 🎯 PRESET MODLARI (Hızlı Kullanım)
# ============================================================================

HUMANIZATION_PRESETS = {
    # 🟢 LIGHT MODE - Güvenli ve Profesyonel (ÖNERİLEN)
    'light': {
        'description': 'Hafif humanization, maksimum güvenlik, profesyonel görünüm',
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
            'hook_moments': {'interval_seconds': 20},  # Daha az sıklıkta
            'pacing_optimization': {'enabled': True},
        },
        'effect_probability': 0.30,  # %30 segment efekt alır
    },

    # 🟡 MEDIUM MODE - Dengeli
    'medium': {
        'description': 'Orta seviye humanization, dengeli ayarlar',
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
        'effect_probability': 0.40,  # %40 segment efekt alır
    },

    # 🔴 AGGRESSIVE MODE - Maksimum Varyasyon
    'aggressive': {
        'description': 'Agresif humanization, maksimum benzersizlik (dikkatli kullan!)',
        'human_imperfections': {
            'micro_timing_errors': {'probability': 0.12},
            'imperfect_cuts': {'probability': 0.20},
            'volume_inconsistency': {'enabled': True},
            'hesitation_pauses': {'enabled': True},  # ⚠️ Riskli
        },
        'organic_variations': {
            'encoder_randomization': {'enabled': True},
            'color_variations': {'enabled': True},
            'noise_patterns': {'default_level': 'heavy'},
            'audio_randomization': {'enabled': True},
        },
        'engagement_optimization': {
            'hook_moments': {'interval_seconds': 12},  # Daha sık
            'pacing_optimization': {'enabled': True},
        },
        'effect_probability': 0.50,  # %50 segment efekt alır
    },

    # 🔵 MINIMAL MODE - En Az Müdahale
    'minimal': {
        'description': 'Minimal humanization, maksimum doğallık',
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
        'effect_probability': 0.20,  # %20 segment efekt alır
    },
}

# Aktif preset (config.py'de değiştirilebilir)
ACTIVE_HUMANIZATION_PRESET = 'light'  # 👈 ÖNERİLEN: 'light'

# ============================================================================
# 🎓 KULLANIM NOTLARI VE İPUÇLARI
# ============================================================================

HUMANIZATION_TIPS = """
🎓 HUMANIZATION KULLANIM KILAVUZU
================================

1. 🟢 LIGHT MODE (ÖNERİLEN)
   - Çoğu kullanım senaryosu için ideal
   - Profesyonel görünüm korur
   - Bot tespiti riski minimum
   - Algoritma dostu

2. 🟡 MEDIUM MODE
   - Daha fazla varyasyon gerektiğinde
   - Günlük birden fazla video yüklerken
   - Orta risk seviyesi

3. 🔴 AGGRESSIVE MODE
   - Sadece deneysel kullanım için
   - Çok fazla video üretiyorsanız
   - Yüksek risk - dikkatli kullanın!

4. 🔵 MINIMAL MODE
   - Test amaçlı
   - Minimum müdahale
   - Doğal görünüm öncelik

⚠️  ÖNEMLİ UYARILAR:
--------------------
• 'hesitation_pauses' özelliği sync sorunlarına neden olabilir
• 'frame_order_variation' çok riskli - kapalı bırakın
• Her preset için test yapın
• Aynı anda farklı presetler deneyin
• Algoritma tepkilerini izleyin

💡 İPUÇLARI:
-----------
• İlk videolarda 'light' kullanın
• Başarılı olduktan sonra 'medium' deneyin
• Günde 1-2 videodan fazla yüklüyorsanız humanization şart
• Fingerprint database'i saklayın (duplicate kontrolü için)
• Upload timing önerilerine uyun
• Tutarlı yükleme saatleri kullanın

📊 BAŞARI METRİKLERİ:
--------------------
• Humanization Score: >90% hedefleyin
• Uniqueness Score: >85% olmalı
• Engagement Score: >75% ideal
• Watch Time Retention: >60% ortalama

🔧 SORUN GİDERME:
----------------
• Video sync sorunları → hesitation_pauses'u kapat
• Görüntü bozulması → noise_patterns'i azalt
• Ses problemleri → audio_randomization'ı kapat
• Render süresi uzun → light preset'e dön

📞 DESTEK:
---------
Sorunlarınız için log dosyasını inceleyin:
  • video_process.log
  • *.humanization_report.json
  • *.optimization_report.json
"""

# Bu string'i istediğiniz zaman yazdırabilirsiniz
if __name__ == "__main__":
    print(HUMANIZATION_TIPS)