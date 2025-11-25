#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YOUTUBE ULTRA PRO - EFEKT KONFİGÜRASYONU
Bu dosyadaki ayarlar kolayca güncellenebilir.
Cinematic efektler, transition'lar ve varyasyon ayarları burada.

✅ YENİ: YouTube Algoritması Optimizasyonları
   - Efekt Dengelemesi (EFFECT_BALANCING)
   - EFFECT_MODE = 'light' (Varsayılan)
   - Efekt Cooldown Sistemi
   - Profesyonel Efekt Kombinasyonları
"""

# Export list - Import sorunlarını önlemek için
__all__ = [
    'CINEMATIC_EFFECTS', 'TRANSITION_EFFECTS', 'ADVANCED_CONFIG',
    'DYNAMIC_SUBTITLE_CONFIG', 'EFFECT_MODE', 'EFFECT_BALANCING'
]

# ============================================================================
# ⚠️ EFEKT MODU AYARLARI - YOUTUBE ALGORİTMASI İÇİN
# ============================================================================
# 'light': Hafif, profesyonel (✅ ÖNERİLEN - YouTube algoritması için ideal)
# 'medium': Orta şiddet (Dikkatli kullanın)
# 'heavy': Ağır efektler (Sadece özel içerik için)

EFFECT_MODE = 'light'  # 👈 ✅ YouTube için 'light' önerilir

# ============================================================================
# 🆕 EFEKT DENGELEME SİSTEMİ (YouTube Algoritması İçin)
# ============================================================================
EFFECT_BALANCING = {
    'enabled': True,  # Master switch

    # Video başına maksimum efekt sayısı
    'max_effects_per_video': 5,  # Toplam 5 farklı efekt (daha profesyonel)

    # Efektsiz segment minimumu (doğal görünüm)
    'min_clean_segments': 3,  # En az 3 segment tamamen efektsiz

    # Efektler arası bekleme süresi (cooldown)
    'effect_cooldown': 5.0,  # Aynı efekt için min 5 saniye bekle

    # Öncelikli efektler (HİKAYE VİDEOLARI İÇİN OPTİMİZE)
    'priority_effects': [
        'color_grading',  # #1 Hikaye atmosferi - story_warm, story_dramatic, cinematic_teal
        'vignette_advanced',  # #2 Merkeze odak - hikaye anlatımı güçlendirir
        'light_leaks',  # #3 Atmosfer oluşturur - warm_memory, sunset_romance
        'soft_focus_background',  # #4 Anlatıcıya/altyazıya odak
        'dream_glow',  # #5 Duygusal sahneler - romantic, dreamy, emotional
        'sharpen_boost',  # #6 Altyazı netliği - subtitle_focus
        'gradient_overlay',  # #7 Duygu renkleri - tension, hope, mystery, calm
        'vintage_styles',  # #8 Nostaljik hikayeler - story_classic, story_flashback
    ],

    # Kaçınılması gereken efekt kombinasyonları
    'avoid_combinations': [
        ['datamosh', 'vhs_advanced'],  # İkisi birden çok bozucu
        ['ghost_trail', 'edge_detect'],  # Çok ağır birlikte
        ['mirror_kaleidoscope', 'kaleidoscope'],  # Aynı tür
        ['pixelate', 'posterize'],  # Görüntüyü çok bozar
        ['glitch', 'datamosh'],  # İkisi de bozucu
    ],

    # Efekt yoğunluğu kontrolü (segment başına)
    'effects_per_segment': {
        'min': 0,  # Bazı segmentler efektsiz olabilir
        'max': 1,  # Bir segmente max 1 efekt (daha temiz)
        'probability': 0.40,  # %40 segment efekt alır (%60 efektsiz)
    },

    # Efekt süre sınırları
    'effect_duration_limits': {
        'min': 2.0,  # Min 2 saniye efekt
        'max': 8.0,  # Max 8 saniye efekt (çok uzun olmasın)
        'ideal': 4.0,  # İdeal 4 saniye
    },

    # Transition dengelemesi
    'transition_balance': {
        'enabled': True,
        'smooth_transitions_ratio': 0.70,  # %70 yumuşak geçiş (fade, dissolve)
        'dynamic_transitions_ratio': 0.30,  # %30 dinamik geçiş (wipe, slide)
    }
}

# ============================================================================
# 🎬 CİNEMATİK EFEKTLER - OPTİMİZE EDİLMİŞ VERSIYON (LIGHT MODE)
# ============================================================================

CINEMATIC_EFFECTS = {
    # ========== ✅ HAFIF EFEKTLER (Her zaman güvenli) ==========

    # Velocity/Speed Ramping - KAPATILDI (donma sorununa sebep oluyordu)
    'velocity_ramp': {
        'enabled': False,  # ⚠️ KAPALI - Video donma sorununa sebep oluyordu
        'olasilik': 0.0,
        'type': ['slow_to_fast', 'fast_to_slow'],
        'speed_range': (0.95, 1.05),  # Minimum hız değişimi (kullanılmıyor)
        'transition_duration': (0.8, 1.2),
    },

    # ========== ⚠️ AĞIR EFEKTLER (Kapatıldı/Azaltıldı) ==========

    # Ghost Trail - KAPATILDI (çok ağır)
    'ghost_trail': {
        'enabled': False,  # ❌ Kapalı
        'olasilik': 0.05,
        'trail_count': (2, 3),
        'opacity': (0.15, 0.25),
        'offset': (2, 4),
    },

    # Neon Glow - Çok hafif versiyon
    'neon_glow': {
        'enabled': True,
        'olasilik': 0.08,  # %8 (nadir)
        'intensity': (0.3, 0.6),  # Çok hafif
        'color': ['cyan', 'magenta'],
        'blur_radius': (3, 8),
    },

    # VHS Advanced - KAPATILDI (çok bozucu)
    'vhs_advanced': {
        'enabled': False,  # ❌ Kapalı
        'olasilik': 0.03,
        'tracking_lines': False,
        'color_bleeding': (0.1, 0.2),
        'tape_crease': False,
        'timestamp': False,
    },

    # Datamosh - KAPATILDI (görüntüyü bozuyor)
    'datamosh': {
        'enabled': False,  # ❌ Kapalı
        'olasilik': 0.02,
        'intensity': (0.1, 0.3),
        'block_size': (16, 24),
        'direction': ['horizontal'],
    },

    # Posterize - KAPATILDI (altyazı okunabilirliğini bozuyor)
    'posterize': {
        'enabled': False,  # ❌ Kapalı - text okunabilirliği için
        'olasilik': 0.06,  # %6
        'levels': (6, 10),  # Daha fazla renk = daha az bozulma
        'dithering': False,
    },

    # Edge Detection - KAPATILDI (çok ağır)
    'edge_detect': {
        'enabled': False,  # ❌ Kapalı
        'olasilik': 0.02,
        'threshold': (0.2, 0.5),
        'invert': False,
    },

    # Mirror/Kaleidoscope - KAPATILDI (çok bozucu)
    'mirror_kaleidoscope': {
        'enabled': False,  # ❌ Kapalı
        'olasilik': 0.02,
        'mode': ['horizontal'],
        'segments': (4, 6),
    },

    # Pixelate - KAPATILDI (görüntüyü bozuyor)
    'pixelate': {
        'enabled': False,  # ❌ Kapalı
        'olasilik': 0.03,
        'block_size': (16, 24),
        'animated': False,
    },

    # Solarize - KAPATILDI (renkleri bozuyor)
    'solarize': {
        'enabled': False,  # ❌ Kapalı
        'olasilik': 0.02,
        'threshold': (0.4, 0.6),
    },

    # Halftone - KAPATILDI (çok ağır)
    'halftone': {
        'enabled': False,  # ❌ Kapalı
        'olasilik': 0.02,
        'dot_size': (4, 5),
        'pattern': ['circle'],
        'angle': (0, 15),
    },

    # Shake Advanced - Çok hafif versiyon
    'shake_advanced': {
        'enabled': True,
        'olasilik': 0.08,  # %8
        'type': ['handheld'],  # Sadece el kamerası
        'intensity': (0.2, 0.4),  # Çok hafif
        'frequency': (8, 12),
    },

    # Overlay Particles - ✨ ULTRA HAFİF
    'overlay_particles': {
        'enabled': True,
        'olasilik': 0.04,  # %4 (çok nadir)
        'type': ['dust', 'bokeh'],
        'density': (0.05, 0.15),  # Çok az yoğunluk
        'size': (1, 3),
    },

    # Vignette Advanced - HİKAYE İÇİN OPTİMİZE (merkeze odak)
    'vignette_advanced': {
        'enabled': True,
        'olasilik': 0.12,  # %12 (azaltıldı - daha doğal)
        'intensity': (0.10, 0.20),  # Daha hafif
        'shape': ['circle'],
        'feather': (0.5, 0.7),
    },

    # ========== ✅ HAFIF EFEKTLER (Güvenli) ==========

    # Kamera Sallama - Çok hafif
    'camera_shake': {
        'enabled': False,  # ⚠️ KAPALI - Akıcılık sorununa sebep oluyordu
        'olasilik': 0.0,
        'intensity': (0.2, 0.4),
        'frequency': (10, 13),
    },

    # ========== Vintage/Retro Styles - Hafif ==========
    'vintage_styles': {
        'enabled': True,
        'olasilik': 0.08,  # %8 (azaltıldı)
        'styles': {
            '70s': {
                'weight': 0.35,
                'warm_tone': 5,
                'saturation': -3,
                'grain': 3,
                'soft_focus': 0.1,
                'vignette': True,
            },
            '80s': {
                'weight': 0.35,
                'saturation': 6,
                'contrast': 5,
                'neon_glow': False,
                'scan_lines': False,
                'color_bleed': 0.08,
                'vhs_noise': 2,
            },
            'film_grain': {
                'weight': 0.30,
                'grain_strength': (2, 5),
                'keep_colors': True,
            }
        }
    },

    # ========== Chromatic Aberration - Hafif ==========
    'chromatic_aberration': {
        'enabled': True,
        'olasilik': 0.10,  # %10
        'shift_amount': (1, 2),
    },

    # ========== Light Leaks - HİKAYE İÇİN OPTİMİZE (atmosfer) ==========
    'light_leaks': {
        'enabled': True,
        'olasilik': 0.10,  # %10 (azaltıldı - daha doğal)
        'intensity': (0.08, 0.15),  # Daha hafif
        'color': ['warm', 'cool'],
    },

    # ========== Glitch Effect - Çok hafif ==========
    'glitch': {
        'enabled': True,
        'olasilik': 0.05,  # %5 (azaltıldı)
        'intensity': (0.08, 0.15),  # Daha hafif
        'rgb_split': False,
        'scan_lines': False,
        'noise': (1, 3),
    },

    # ========== Motion Blur - Hafif ==========
    'motion_blur': {
        'enabled': False,  # ⚠️ KAPALI - Akıcılık sorununa sebep oluyordu
        'olasilik': 0.0,
        'intensity': (0.2, 0.4),
        'angle': (0, 360),
    },

    # ========== Zoom Pulse - KAPATILDI (akıcılık sorunu) ==========
    'zoom_pulse': {
        'enabled': False,  # ⚠️ KAPALI - Akıcılık sorununa sebep oluyordu
        'olasilik': 0.0,
        'type': ['in', 'out'],
        'intensity': (1.02, 1.08),
        'speed': (1, 2),
    },

    # ========== Lens Distortion - Hafif ==========
    'lens_distortion': {
        'enabled': True,
        'olasilik': 0.08,  # %8
        'type': ['barrel'],
        'strength': (0.05, 0.15),
    },

    # ========== Prism Effect - Hafif ==========
    'prism': {
        'enabled': True,
        'olasilik': 0.08,  # %8
        'intensity': (0.1, 0.3),
        'colors': 2,
    },

    # ========== Advanced Color Grading - HİKAYE VİDEOLARI İÇİN OPTİMİZE ==========
    'color_grading': {
        'enabled': True,
        'olasilik': 0.15,  # %15 (azaltıldı - daha doğal görünüm)
        'presets': {
            # 🎬 HİKAYE/DRAMA PRESET'LERİ (Altyazı uyumlu, profesyonel)
            'story_warm': {
                'weight': 0.25,  # Sıcak, samimi hikayeler için
                'warm_boost': 8,
                'saturation': 5,
                'contrast': 5,
                'vignette': True,
            },
            'story_dramatic': {
                'weight': 0.20,  # Gerilim, dram hikayeleri için
                'shadows': -8,
                'contrast': 12,
                'saturation': -5,
                'blue_tint': 3,
            },
            'story_nostalgic': {
                'weight': 0.20,  # Nostaljik hikayeler için
                'warm_boost': 10,
                'saturation': -8,
                'soft_light': True,
                'grain': 2,
            },
            'golden_hour': {
                'weight': 0.20,  # Romantik/duygusal hikayeler için
                'warm_boost': 12,
                'soft_light': True,
                'saturation': 8,
            },
            'cinematic_teal': {
                'weight': 0.15,  # Modern sinema görünümü
                'teal_shadows': True,
                'orange_highlights': True,
                'contrast': 8,
            }
        }
    },

    # ========== Dream Glow - Hafif ==========
    'dream_glow': {
        'enabled': True,
        'olasilik': 0.08,  # %8 (azaltıldı)
        'intensity': (0.10, 0.20),  # Daha hafif
        'soft_light': True,
    },

    # ========== RGB Split - Hafif ==========
    'rgb_split_advanced': {
        'enabled': True,
        'olasilik': 0.08,  # %8
        'offset_x': (1, 3),
        'offset_y': (1, 2),
        'diagonal': False,
    },

    # ========== Sharpen - Hafif ==========
    'sharpen_boost': {
        'enabled': True,
        'olasilik': 0.10,  # %10 (azaltıldı)
        'intensity': (0.3, 0.5),  # Daha hafif
    },

    # ========== Auto Velocity - ✨ ULTRA HAFİF ==========
    'auto_velocity': {
        'enabled': True,
        'olasilik': 0.05,  # %5 (çok nadir)
        'patterns': {
            'speed_ramp': {
                'weight': 1.0,
                'start_speed': (0.90, 0.95),
                'peak_speed': (1.05, 1.10),
                'end_speed': (0.95, 1.0),
            },
            'bounce': {'weight': 0.0},  # Kapalı
            'stutter': {'weight': 0.0},  # Kapalı
        }
    },

    # ========== Flash/Strobe - Hafif ==========
    'flash_effect': {
        'enabled': True,
        'olasilik': 0.08,  # %8
        'types': {
            'white_flash': {
                'weight': 0.80,
                'duration': (0.05, 0.1),
                'intensity': (0.2, 0.4),
            },
            'color_flash': {
                'weight': 0.20,
                'duration': (0.08, 0.15),
                'colors': ['cyan', 'purple'],
            },
            'strobe': {'weight': 0.00},  # Kapalı (rahatsız edici)
        }
    },

    # ========== 3D Tilt - ✨ ULTRA HAFİF ==========
    '3d_tilt': {
        'enabled': True,
        'olasilik': 0.03,  # %3 (çok nadir)
        'axis': ['x'],
        'angle': (1, 3),
        'zoom_compensation': True,
    },

    # ========== Echo Trail - ✨ ULTRA HAFİF ==========
    'echo_trail': {
        'enabled': True,
        'olasilik': 0.03,  # %3 (çok nadir)
        'trail_count': (2, 2),
        'spacing': (0.08, 0.12),
        'opacity': (0.10, 0.20),
    },

    # ========== Glow/Bloom - ✨ ULTRA HAFİF ==========
    'glow_bloom': {
        'enabled': True,
        'olasilik': 0.04,  # %4 (çok nadir)
        'types': {
            'soft_glow': {
                'weight': 1.0,
                'intensity': (0.1, 0.2),
                'radius': (5, 10),
            },
            'bloom': {'weight': 0.0},  # Kapalı
            'edge_glow': {'weight': 0.0},  # Kapalı
        }
    },

    # ========== Edge Detection - KAPATILDI ==========
    'edge_detection': {
        'enabled': False,  # ❌ Kapalı
        'olasilik': 0.02,
        'types': {
            'cartoon_outline': {
                'weight': 0.60,
                'thickness': (1, 2),
                'color': 'black',
            },
            'neon_edges': {
                'weight': 0.30,
                'color': ['cyan'],
                'glow': False,
            },
            'sketch': {
                'weight': 0.10,
                'intensity': (0.2, 0.4),
                'invert': False,
            }
        }
    },

    # ========== Parallax - KAPATILDI ==========
    'parallax_offset': {
        'enabled': False,  # ❌ Kapalı
        'olasilik': 0.02,
        'direction': ['horizontal'],
        'offset': (5, 10),
        'layers': (2, 2),
    },

    # ========== Kaleidoscope - KAPATILDI ==========
    'kaleidoscope': {
        'enabled': False,  # ❌ Kapalı
        'olasilik': 0.01,
        'segments': (4, 6),
        'rotation': (0, 180),
        'center_x': (0.45, 0.55),
        'center_y': (0.45, 0.55),
    },

    # ========== Mirror/Symmetry - KAPATILDI ==========
    'mirror_symmetry': {
        'enabled': False,  # ❌ Kapalı
        'olasilik': 0.02,
        'axis': ['vertical'],
        'position': (0.4, 0.6),
    },

    # ========== Posterize/Cartoon - KAPATILDI ==========
    'posterize_cartoon': {
        'enabled': False,  # ❌ Kapalı
        'olasilik': 0.02,
        'types': {
            'posterize': {
                'weight': 0.60,
                'levels': (6, 10),
            },
            'cartoon': {
                'weight': 0.30,
                'edge_thickness': (1, 2),
                'color_levels': (8, 12),
            },
            'cel_shading': {
                'weight': 0.10,
                'threshold': (0.4, 0.6),
            }
        }
    },

    # ========== Speed Ripple - ✨ ULTRA HAFİF ==========
    'speed_ripple': {
        'enabled': True,
        'olasilik': 0.03,  # %3 (çok nadir)
        'wave_frequency': (1.2, 1.4),
        'amplitude': (0.03, 0.08),
        'base_speed': (0.98, 1.02),
    },

    # ========== Time Displacement - KAPATILDI ==========
    'time_displacement': {
        'enabled': False,  # ❌ Kapalı
        'olasilik': 0.01,
        'offset': (0.1, 0.3),
        'direction': ['forward'],
        'blend_mode': ['overlay'],
    },

    # ========== 🔥 BEAT DROP EFFECTS - KAPATILDI (akıcılık sorunu) ==========
    'beat_drop_shake': {
        'enabled': False,  # ⚠️ KAPALI - Akıcılık sorununa sebep oluyordu
        'olasilik': 0.0,
        'intensity': (0.5, 1.5),
        'duration': (0.1, 0.2),
        'frequency': (15, 25),  # Titreşim frekansı
        'description': 'Beat drop camera shake - TikTok viral effect'
    },

    'beat_drop_zoom': {
        'enabled': False,  # ⚠️ KAPALI - Akıcılık sorununa sebep oluyordu
        'olasilik': 0.0,
        'zoom_in': (1.05, 1.15),
        'duration': (0.15, 0.25),
        'snap_back': True,  # Hemen geri döner
        'ease': 'cubic',  # Sert geçiş
        'description': 'Beat drop zoom punch - CapCut favorite'
    },

    'beat_drop_flash': {
        'enabled': False,  # ⚠️ KAPALI - Akıcılık sorununa sebep oluyordu
        'olasilik': 0.0,
        'colors': ['white', 'cyan', 'purple', 'yellow'],
        'intensity': (0.6, 0.9),
        'duration': (0.05, 0.15),  # Flash süresi
        'fade_out': (0.1, 0.2),  # Sönme süresi
        'description': 'Beat drop flash bang - High energy'
    },

    # ========== 🎬 FREEZE FRAME - KAPATILDI (donma sorununa sebep oluyordu) ==========
    'freeze_frame': {
        'enabled': False,  # ⚠️ KAPALI - Video donma sorununa sebep oluyordu
        'olasilik': 0.0,
        'duration': (0.5, 1.5),  # Donma süresi
        'effects': {
            'zoom_in': {
                'enabled': True,
                'zoom': (1.05, 1.15),  # Hafif yakınlaşma
                'smooth': True,
            },
            'border_glow': {
                'enabled': True,
                'color': ['white', 'cyan', 'purple'],
                'thickness': (3, 6),  # Çerçeve kalınlığı
                'glow_radius': (8, 15),  # Parlama yarıçapı
            },
            'color_pop': {
                'enabled': True,
                'saturation_boost': (15, 25),  # Renk vurgusu
                'contrast_boost': (5, 10),
            },
            'desaturate_background': {
                'enabled': False,  # Arka planı gri yap (opsiyonel)
                'amount': (0.5, 0.8),
            }
        },
        'description': 'Freeze frame with effects - CapCut 50M+ uses'
    },

    # ========== 🎪 BOUNCE/WIGGLE - KAPATILDI (akıcılık sorunu) ==========
    'elastic_bounce': {
        'enabled': False,  # ⚠️ KAPALI - Akıcılık sorununa sebep oluyordu
        'olasilik': 0.0,
        'frequency': (3, 6),
        'amplitude': (0.05, 0.15),
        'decay': (0.7, 0.9),
        'duration': (0.5, 1.0),
        'axis': ['y', 'both'],
        'description': 'Elastic bounce - DISABLED'
    },

    'wiggle_shake': {
        'enabled': False,  # ⚠️ KAPALI - Akıcılık sorununa sebep oluyordu
        'olasilik': 0.0,
        'types': {
            'horizontal': {
                'weight': 0.40,
                'frequency': (5, 10),
                'amplitude': (5, 15),
            },
            'vertical': {
                'weight': 0.30,
                'frequency': (5, 10),
                'amplitude': (5, 15),
            },
            'both': {
                'weight': 0.30,
                'frequency': (5, 10),
                'amplitude': (5, 15),
            }
        },
        'duration': (0.3, 0.8),
        'description': 'Wiggle shake - DISABLED'
    },

    'jello_effect': {
        'enabled': False,  # ⚠️ KAPALI - Akıcılık sorununa sebep oluyordu
        'olasilik': 0.0,
        'wobble': (0.1, 0.3),
        'frequency': (4, 8),
        'duration': (0.4, 0.9),
        'damping': (0.6, 0.8),
        'description': 'Jello wobble - DISABLED'
    },

    # ========== 🎥 KEN BURNS EFFECT - KAPATILDI (akıcılık sorunu) ==========
    'ken_burns': {
        'enabled': False,  # ⚠️ KAPALI - Zoom/pan akıcılık sorununa sebep oluyordu
        'olasilik': 0.0,
        'types': {
            'zoom_in_pan': {
                'weight': 0.40,  # En popüler
                'start_zoom': 1.0,
                'end_zoom': (1.15, 1.30),
                'pan_direction': ['left', 'right', 'up', 'down'],
            },
            'zoom_out_pan': {
                'weight': 0.30,
                'start_zoom': (1.20, 1.35),
                'end_zoom': 1.0,
                'pan_direction': ['left', 'right', 'up', 'down'],
            },
            'pan_only': {
                'weight': 0.30,
                'zoom': 1.0,
                'pan_distance': (50, 100),  # pixels
                'direction': ['horizontal', 'vertical'],
            }
        },
        'smooth_curve': 'ease_in_out',  # Yumuşak geçiş
        'description': 'Ken Burns pan & zoom - Perfect for story channels'
    },

    # ========== 🌈 GRADIENT OVERLAY - Hafif ==========
    'gradient_overlay': {
        'enabled': True,
        'olasilik': 0.08,  # %8 (azaltıldı)
        'types': {
            'vertical': {
                'weight': 0.50,
                'start_color': ['top_dark', 'top_light'],
                'end_color': ['bottom_dark', 'bottom_light'],
                'opacity': (0.08, 0.15),  # Daha hafif
            },
            'radial': {
                'weight': 0.30,
                'center': 'center',
                'inner_color': 'light',
                'outer_color': 'dark',
                'opacity': (0.08, 0.15),
            },
            'diagonal': {
                'weight': 0.20,
                'angle': (30, 60),
                'opacity': (0.08, 0.12),
            },
        },
        'blend_mode': ['overlay', 'soft_light'],
    },

    # ========== 🔍 SOFT FOCUS BACKGROUND - Hafif ==========
    'soft_focus_background': {
        'enabled': True,
        'olasilik': 0.06,  # %6 (azaltıldı)
        'subtitle_area': 'bottom_third',
        'blur_intensity': (2, 4),  # Daha hafif
        'fade_boundary': (0.2, 0.4),
        'brightness_boost': (1.02, 1.08),
    },
}

# ============================================================================
# 🎬 TRANSİTİON EFFECTS - 35+ GEÇİŞ EFEKTİ (YouTube İçin Optimize)
# ============================================================================
TRANSITION_EFFECTS = {
    'enabled': True,
    'default_duration': (0.5, 1.5),  # Geçiş süresi (saniye)
    'overlap_duration': 1.0,  # Klip overlap süresi

    # Transition tipleri ve ağırlıkları
    'transitions': {
        # ===== FADE TRANSITIONS (En popüler - %70 yumuşak geçiş) =====
        'fade': {
            'weight': 0.20,  # %20 olasılık (en popüler)
            'description': 'Smooth fade transition',
        },
        'fadeblack': {
            'weight': 0.12,  # Artırıldı
            'description': 'Fade through black',
        },
        'fadewhite': {
            'weight': 0.08,
            'description': 'Fade through white',
        },
        'dissolve': {
            'weight': 0.10,  # Artırıldı
            'description': 'Dissolve/cross-fade',
        },

        # ===== WIPE TRANSITIONS (Orta popülerlik) =====
        'wipeleft': {
            'weight': 0.06,
            'description': 'Wipe from right to left',
        },
        'wiperight': {
            'weight': 0.06,
            'description': 'Wipe from left to right',
        },
        'wipeup': {
            'weight': 0.04,
            'description': 'Wipe from bottom to top',
        },
        'wipedown': {
            'weight': 0.04,
            'description': 'Wipe from top to bottom',
        },

        # ===== SLIDE TRANSITIONS =====
        'slideleft': {
            'weight': 0.05,
            'description': 'Slide from right to left',
        },
        'slideright': {
            'weight': 0.05,
            'description': 'Slide from left to right',
        },
        'slideup': {
            'weight': 0.03,
            'description': 'Slide from bottom to top',
        },
        'slidedown': {
            'weight': 0.03,
            'description': 'Slide from top to bottom',
        },

        # ===== SMOOTH TRANSITIONS =====
        'smoothleft': {
            'weight': 0.04,
            'description': 'Smooth slide left',
        },
        'smoothright': {
            'weight': 0.04,
            'description': 'Smooth slide right',
        },
        'smoothup': {
            'weight': 0.02,
            'description': 'Smooth slide up',
        },
        'smoothdown': {
            'weight': 0.02,
            'description': 'Smooth slide down',
        },

        # ===== CIRCLE TRANSITIONS (Azaltıldı) =====
        'circleopen': {
            'weight': 0.02,  # Azaltıldı
            'description': 'Circle expand',
        },
        'circleclose': {
            'weight': 0.02,  # Azaltıldı
            'description': 'Circle shrink',
        },

        # ===== SPECIAL TRANSITIONS (Azaltıldı) =====
        'pixelize': {
            'weight': 0.01,  # Azaltıldı
            'description': 'Pixelate transition',
        },
        'radial': {
            'weight': 0.02,
            'description': 'Radial wipe',
        },
        'distance': {
            'weight': 0.01,
            'description': 'Distance based',
        },

        # ===== DIAGONAL TRANSITIONS (Minimal) =====
        'diagtl': {
            'weight': 0.005,
            'description': 'Diagonal top-left',
        },
        'diagtr': {
            'weight': 0.005,
            'description': 'Diagonal top-right',
        },
        'diagbl': {
            'weight': 0.005,
            'description': 'Diagonal bottom-left',
        },
        'diagbr': {
            'weight': 0.005,
            'description': 'Diagonal bottom-right',
        },
    },

    # Transition uygulama stratejisi
    'strategy': 'random',  # 'random', 'sequential', 'beat_sync'
    'avoid_repetition': True,  # Ardışık aynı transition'ı engelle
    'min_clip_gap': 2,  # Minimum klip sayısı (aynı transition tekrarı için)
}

# ============================================================================
# GELİŞMİŞ VARYASYON CONFIG - NORMAL SPEED (Slow motion kapalı)
# ============================================================================
ADVANCED_CONFIG = {
    # ========== Video effects - NORMAL SPEED ==========
    # ⚠️ SLOW MOTION KAPATILDI - Video donma sorununa sebep oluyordu
    'hiz_aralik': (1.0, 1.0),  # ✅ Normal hız (donma sorunu düzeltildi)
    'parlaklik_aralik': (-5, 5),  # Daha hafif (-8,8 → -5,5)
    'kontrast_aralik': (-3, 3),  # Daha hafif (-5,5 → -3,3)
    'doygunluk_aralik': (-4, 4),  # Daha hafif (-6,6 → -4,4)
    'zoom_aralik': (1.0, 1.03),  # Daha hafif zoom (1.06 → 1.03)
    'flip_olasilik': 0.05,  # Daha az flip (0.10 → 0.05)
    'rotate_aralik': (-0.3, 0.3),  # Daha az döndürme (-0.8,0.8 → -0.3,0.3)

    # ========== Advanced effects ==========
    'unsharp_aralik': (0.2, 0.4),  # Daha hafif keskinlik
    'vignette_olasilik': 0.10,  # Daha az vignette (0.15 → 0.10)
    'grain_aralik': (0, 4),  # Daha az grain (8 → 4)
    'chroma_shift_olasilik': 0.0,

    # ========== Audio effects ==========
    'pitch_aralik': (-0.2, 0.2),  # Daha az pitch değişimi (-0.5,0.5 → -0.2,0.2)
    'volume_aralik': (1.0, 1.10),  # Daha az volume boost (1.20,1.40 → 1.0,1.10)
    'bass_boost_olasilik': 0.15,  # Daha az (0.30 → 0.15)
    'treble_boost_olasilik': 0.10,  # Daha az (0.25 → 0.10)
    'stereo_width_aralik': (0.98, 1.02),  # Daha dar aralık
    'use_normalization': True,
    'use_compression': False,  # ⚠️ KAPALI - Boğuk ses sorununu önler

    # ========== Other ==========
    'timestamp_olasilik': 0.15,
    'color_tint_olasilik': 0.20,
    'color_presets': ['warm', 'cool', 'vibrant', 'muted'],

    # ========== Segment settings ==========
    'segment_duration': (7, 11),
    'min_scene_score': 0.35,
}

# ============================================================================
# 🎨 DİNAMİK ALTYAZI SİSTEMİ - ENGAGEMENT BOOSTER
# ============================================================================
DYNAMIC_SUBTITLE_CONFIG = {
    # ========== Temel Ayarlar ==========
    'enabled': True,
    'mode': 'dynamic',  # 'basic', 'dynamic', 'karaoke'

    # ========== Karaoke Stil (Kelime Kelime Vurgulama) ==========
    'karaoke': {
        'enabled': True,
        'highlight_style': 'color_change',  # 'color_change', 'scale', 'glow', 'bounce'
        'highlight_color': '&H00FFFF00',  # Sarı (ASS formatı: &HBBGGRR)
        'normal_color': '&H00FFFFFF',  # Beyaz
        'transition_smooth': True,  # Yumuşak geçiş
        'word_by_word': True,  # Her kelime ayrı vurgulanır
    },

    # ========== Emoji Ekleme (Bağlama Uygun) ==========
    'emoji': {
        'enabled': True,
        'auto_detect': True,  # Kelimelere göre otomatik emoji
        'emoji_map': {
            # Duygular
            'happy|güzel|harika|mükemmel|muhteşem|süper|çok iyi|bravo|tebrikler': '😊',
            'love|aşk|sevgi|seviyorum|kalp': '❤️',
            'sad|üzgün|kötü|berbat|mutsuz': '😢',
            'angry|kızgın|sinirli|öfkeli': '😠',
            'surprised|şaşırdım|vay|wow': '😮',
            'laugh|gülme|komik|haha|lol': '😂',
            'think|düşün|hmm': '🤔',
            'cool|havalı|süper': '😎',

            # Nesneler
            'money|para|dolar|zengin': '💰',
            'fire|ateş|yanıyor|hot': '🔥',
            'star|yıldız': '⭐',
            'trophy|kupa|başarı|kazanmak': '🏆',
            'rocket|roket|hızlı': '🚀',
            'light|ışık|ampul|fikir': '💡',
            'check|tamam|oldu|başarılı': '✅',
            'warning|uyarı|dikkat': '⚠️',
            'stop|dur|stop': '🛑',
            'music|müzik|şarkı': '🎵',
            'video|film|kamera': '🎥',
            'book|kitap|okuma': '📚',
            'phone|telefon': '📱',
            'computer|bilgisayar|pc': '💻',
            'game|oyun': '🎮',

            # Sayılar ve işaretler
            'one|bir|1': '1️⃣',
            'two|iki|2': '2️⃣',
            'three|üç|3': '3️⃣',
            'four|dört|4': '4️⃣',
            'five|beş|5': '5️⃣',
            'hundred|yüz|100': '💯',

            # Doğa
            'sun|güneş': '☀️',
            'moon|ay': '🌙',
            'rain|yağmur': '🌧️',
            'snow|kar': '❄️',
            'tree|ağaç': '🌳',
            'flower|çiçek': '🌸',
        },
        'position': 'end',  # 'end', 'start', 'both'
        'spacing': True,  # Emoji öncesi/sonrası boşluk
    },

    # ========== Animasyonlu Stiller ==========
    'animations': {
        'enabled': True,
        'styles': {
            'fade_in': {
                'enabled': True,
                'duration': 0.3,  # Saniye
                'probability': 0.25,
            },
            'slide_up': {
                'enabled': True,
                'distance': 30,  # Piksel
                'duration': 0.4,
                'probability': 0.20,
            },
            'bounce': {
                'enabled': True,
                'height': 15,
                'duration': 0.5,
                'probability': 0.15,
            },
            'scale_pulse': {
                'enabled': True,
                'scale': 1.1,  # 1.1x büyüme
                'duration': 0.3,
                'probability': 0.20,
            },
            'typewriter': {
                'enabled': True,
                'speed': 0.05,  # Saniye/karakter
                'probability': 0.10,
            },
            'wave': {
                'enabled': True,
                'amplitude': 10,
                'frequency': 0.5,
                'probability': 0.10,
            }
        }
    },

    # ========== Renk Kodlama ==========
    'color_coding': {
        'enabled': True,
        'modes': {
            'emotion_based': {
                'enabled': True,
                'colors': {
                    'positive': '&H0000FF00',  # Yeşil (mutlu, pozitif)
                    'negative': '&H000000FF',  # Kırmızı (üzgün, negatif)
                    'neutral': '&H00FFFFFF',  # Beyaz (nötr)
                    'question': '&H00FFFF00',  # Sarı (soru)
                    'important': '&H0000FFFF',  # Turuncu (önemli)
                },
                'sentiment_keywords': {
                    'positive': ['güzel', 'harika', 'mükemmel', 'iyi', 'süper', 'başarılı', 'kazandık'],
                    'negative': ['kötü', 'berbat', 'üzgün', 'başarısız', 'kaybettik', 'yanlış'],
                    'important': ['dikkat', 'önemli', 'uyarı', 'not', 'unutma', 'kritik'],
                }
            },
            'speaker_based': {
                'enabled': False,  # Birden fazla konuşmacı için
                'speaker_colors': {
                    'speaker1': '&H00FFFFFF',  # Beyaz
                    'speaker2': '&H0000FFFF',  # Sarı
                    'speaker3': '&H00FF00FF',  # Magenta
                },
            },
            'emphasis_words': {
                'enabled': True,
                'highlight_color': '&H0000FFFF',  # Turuncu
                'keywords': ['çok', 'en', 'muhteşem', 'inanılmaz', 'gerçekten', 'kesinlikle'],
                'uppercase': True,  # Vurgulanan kelimeleri büyük harfle yaz
            }
        }
    },

    # ========== Arka Plan Şekilleri ==========
    'background': {
        'enabled': True,
        'styles': {
            'box': {
                'enabled': True,
                'color': '&H80000000',  # Yarı saydam siyah (AABBGGRR formatı)
                'padding': 20,  # Piksel
                'border_radius': 15,
                'probability': 0.40,
            },
            'highlight_bar': {
                'enabled': True,
                'color': '&H60000000',  # Daha saydam
                'height': 'auto',
                'full_width': False,
                'probability': 0.30,
            },
            'gradient': {
                'enabled': True,
                'start_color': '&H00000000',  # Saydam
                'end_color': '&H80000000',  # Yarı saydam siyah
                'direction': 'bottom_to_top',
                'probability': 0.20,
            },
            'outline': {
                'enabled': True,
                'color': '&H00000000',  # Siyah
                'width': 4,  # Piksel
                'shadow': True,
                'shadow_offset': 2,
                'probability': 0.10,  # Diğerleri yoksa kullan
            }
        }
    },

    # ========== Pozisyon ve Görünüm ==========
    'positioning': {
        'default_position': 'bottom',  # 'top', 'center', 'bottom'
        'auto_adjust': True,  # Yüz/nesne varsa kaydır
        'safe_area': {
            'top': 10,  # % cinsinden güvenli alan
            'bottom': 15,
            'left': 10,
            'right': 10,
        },
        'alignment': 'center',  # 'left', 'center', 'right'
        'margin': {
            'vertical': 150,  # Piksel
            'horizontal': 100,
        }
    },

    # ========== Tipografi ==========
    'typography': {
        'font_family': 'Arial Black',  # Bold font daha okunabilir
        'font_size': 76,  # 1080p için optimize
        'font_weight': 'bold',
        'letter_spacing': 0,  # Piksel
        'line_height': 1.2,
        'uppercase': False,  # Tüm metni büyük harf
        'max_chars_per_line': 40,  # Maksimum karakter
        'max_lines': 2,  # Maksimum satır
    },

    # ========== Gelişmiş Efektler ==========
    'advanced_effects': {
        'word_pop': {
            'enabled': True,
            'trigger_words': ['wow', 'amazing', 'incredible', 'vay', 'inanılmaz', 'muhteşem'],
            'scale': 1.3,
            'duration': 0.2,
            'color': '&H0000FFFF',  # Turuncu
            'shake': True,
        },
        'slow_motion_sync': {
            'enabled': True,
            'sync_with_video': True,  # Video yavaşladığında altyazı da yavaşlar
            'stretch_duration': 1.2,  # Video yavaşlığı kadar
        },
        'beat_sync': {
            'enabled': False,  # Müzik beat'ine senkron (gelişmiş)
            'pulse_on_beat': True,
            'color_flash': True,
        },
        'progressive_reveal': {
            'enabled': True,
            'style': 'word_by_word',  # 'char_by_char', 'word_by_word', 'line_by_line'
            'speed': 0.08,  # Saniye/kelime
            'probability': 0.15,
        }
    },

    # ========== Optimizasyon ==========
    'optimization': {
        'auto_timing': True,  # Konuşma hızına göre timing ayarla
        'min_duration': 1.5,  # Minimum görünme süresi (saniye)
        'max_duration': 6.0,  # Maksimum görünme süresi
        'gap_threshold': 0.3,  # Kelimeler arası maksimum boşluk
        'reading_speed': 180,  # Kelime/dakika (ortala 150-200)
        'overlap_prevention': True,  # Altyazıların üst üste gelmesini engelle
    },

    # ========== Platform Optimizasyonları ==========
    'platform_presets': {
        'youtube_standard': {
            'font_size': 76,
            'position': 'bottom',
            'margin_vertical': 150,
            'max_chars': 40,
            'background': 'box',
        },
        'youtube_shorts': {
            'font_size': 84,  # Daha büyük (mobil için)
            'position': 'bottom',
            'margin_vertical': 200,
            'max_chars': 30,
            'background': 'outline',
            'uppercase': True,  # Daha dikkat çekici
        },
        'tiktok': {
            'font_size': 88,
            'position': 'bottom',
            'margin_vertical': 180,
            'max_chars': 25,
            'karaoke': True,
            'emoji': True,
            'background': 'none',  # TikTok için minimal
        },
        'instagram_reels': {
            'font_size': 80,
            'position': 'bottom',
            'margin_vertical': 190,
            'max_chars': 28,
            'background': 'gradient',
        }
    },

    # ========== A/B Test Varyasyonları ==========
    'variants': {
        'enabled': False,  # A/B test için farklı stiller üret
        'count': 3,  # Kaç varyasyon
        'randomize': ['colors', 'animations', 'background'],
    }
}