#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SUBTITLE STYLES - 40+ Profesyonel Altyazı Stili
YouTube Hikaye Kanalları İçin Optimize Edilmiş
"""

from typing import Dict, List, Optional

# ============================================================================
# 🎨 HIGHLIGHT COLOR PRESETS - Vurgu Renkleri
# ============================================================================
# ASS format: &HAABBGGRR (Alpha, Blue, Green, Red)

HIGHLIGHT_COLORS = {
    'yellow': {
        'name': 'Sarı',
        'description': '💛 En popüler - Dikkat çekici',
        'color': '&H0000FFFF',  # Yellow (BGR: 00FFFF)
    },
    'white': {
        'name': 'Beyaz',
        'description': '⚪ Klasik - Her arka plana uygun',
        'color': '&H00FFFFFF',  # White
    },
    'cyan': {
        'name': 'Cyan/Turkuaz',
        'description': '💎 Modern - Parlak mavi',
        'color': '&H00FFFF00',  # Cyan (BGR: FFFF00)
    },
    'green': {
        'name': 'Yeşil',
        'description': '💚 Canlı - Enerji dolu',
        'color': '&H0000FF00',  # Green
    },
    'orange': {
        'name': 'Turuncu',
        'description': '🧡 Sıcak - Dikkat çekici',
        'color': '&H0000A5FF',  # Orange (BGR: 00A5FF)
    },
    'pink': {
        'name': 'Pembe',
        'description': '💗 Eğlenceli - Enerjik',
        'color': '&H00FF00FF',  # Magenta/Pink
    },
    'red': {
        'name': 'Kırmızı',
        'description': '❤️ Güçlü - Dramatik',
        'color': '&H000000FF',  # Red
    },
    'gold': {
        'name': 'Altın',
        'description': '✨ Lüks - Premium his',
        'color': '&H0000D7FF',  # Gold (BGR: 00D7FF)
    },
    'lime': {
        'name': 'Lime/Açık Yeşil',
        'description': '💚 Neon - Çok parlak',
        'color': '&H0000FF7F',  # Lime
    },
    'purple': {
        'name': 'Mor',
        'description': '💜 Gizemli - Yaratıcı',
        'color': '&H00FF0080',  # Purple
    },
}

# Default highlight color
DEFAULT_HIGHLIGHT_COLOR = 'yellow'

# ============================================================================
# 🎨 SUBTITLE STYLE PRESETS - 40+ Stil
# ============================================================================

SUBTITLE_STYLES = {
    # ══════════════════════════════════════════════════════════════════════════
    # ⭐ VİRAL / TREND STİLLERİ (En Popüler YouTube Stilleri)
    # ══════════════════════════════════════════════════════════════════════════

    'mrbeast': {
        'name': 'MrBeast',
        'description': '🔥 En popüler YouTube stili - Büyük, net',
        'category': 'Viral',
        'fontname': 'Impact',
        'fontsize': 82,
        'primary_color': '&H00FFFFFF',
        'secondary_color': '&H0000FFFF',
        'outline_color': '&H00000000',
        'back_color': '&H00000000',
        'bold': -1,
        'italic': 0,
        'underline': 0,
        'outline': 6,
        'shadow': 2,
        'alignment': 2,
        'margin_v': 150,
        'karaoke_mode': 'sentence',
    },

    'reddit': {
        'name': 'Reddit Stories',
        'description': '🔥 Hikaye kanalları favorisi',
        'category': 'Viral',
        'fontname': 'Arial Black',
        'fontsize': 76,
        'primary_color': '&H00FFFFFF',
        'secondary_color': '&H0000BFFF',
        'outline_color': '&H00000000',
        'back_color': '&H00000000',
        'bold': -1,
        'italic': 0,
        'underline': 0,
        'outline': 5,
        'shadow': 3,
        'alignment': 2,
        'margin_v': 160,
        'karaoke_mode': 'sentence',
    },

    'storytime': {
        'name': 'Storytime',
        'description': '🔥 Hikaye anlatımı için mükemmel',
        'category': 'Viral',
        'fontname': 'Arial Black',
        'fontsize': 78,
        'primary_color': '&H00FFFFFF',
        'secondary_color': '&H0000FFFF',
        'outline_color': '&H00000000',
        'back_color': '&H00000000',
        'bold': -1,
        'italic': 0,
        'underline': 0,
        'outline': 5,
        'shadow': 3,
        'alignment': 2,
        'margin_v': 155,
        'karaoke_mode': 'sentence',
    },

    'tiktok': {
        'name': 'TikTok Viral',
        'description': '🔥 Modern TikTok/Reels stili',
        'category': 'Viral',
        'fontname': 'Arial Black',
        'fontsize': 80,
        'primary_color': '&H00FFFFFF',
        'secondary_color': '&H00FF00FF',
        'outline_color': '&H00000000',
        'back_color': '&H00000000',
        'bold': -1,
        'italic': 0,
        'underline': 0,
        'outline': 5,
        'shadow': 3,
        'alignment': 2,
        'margin_v': 160,
        'karaoke_mode': 'sentence',
    },

    'hormozi': {
        'name': 'Hormozi Style',
        'description': '🔥 İş/Motivasyon - Profesyonel',
        'category': 'Viral',
        'fontname': 'Arial Black',
        'fontsize': 74,
        'primary_color': '&H00FFFFFF',
        'secondary_color': '&H0000D4FF',
        'outline_color': '&H00000000',
        'back_color': '&H00000000',
        'bold': -1,
        'italic': 0,
        'underline': 0,
        'outline': 4,
        'shadow': 2,
        'alignment': 2,
        'margin_v': 165,
        'karaoke_mode': 'sentence',
    },

    'shorts': {
        'name': 'YouTube Shorts',
        'description': '🔥 Shorts için optimize',
        'category': 'Viral',
        'fontname': 'Impact',
        'fontsize': 84,
        'primary_color': '&H00FFFFFF',
        'secondary_color': '&H000000FF',
        'outline_color': '&H00000000',
        'back_color': '&H00000000',
        'bold': -1,
        'italic': 0,
        'underline': 0,
        'outline': 6,
        'shadow': 2,
        'alignment': 2,
        'margin_v': 140,
        'karaoke_mode': 'sentence',
    },

    'captivate': {
        'name': 'Captivate',
        'description': '🔥 Dikkat çekici - Parlak sarı',
        'category': 'Viral',
        'fontname': 'Arial Black',
        'fontsize': 80,
        'primary_color': '&H0000FFFF',
        'secondary_color': '&H00FFFFFF',
        'outline_color': '&H00000000',
        'back_color': '&H00000000',
        'bold': -1,
        'italic': 0,
        'underline': 0,
        'outline': 6,
        'shadow': 3,
        'alignment': 2,
        'margin_v': 150,
        'karaoke_mode': 'sentence',
    },

    'viral_white': {
        'name': 'Viral White',
        'description': '🔥 Sade beyaz - Her arka plana uygun',
        'category': 'Viral',
        'fontname': 'Impact',
        'fontsize': 78,
        'primary_color': '&H00FFFFFF',
        'secondary_color': '&H00FFFFFF',
        'outline_color': '&H00000000',
        'back_color': '&H00000000',
        'bold': -1,
        'italic': 0,
        'underline': 0,
        'outline': 5,
        'shadow': 3,
        'alignment': 2,
        'margin_v': 155,
        'karaoke_mode': 'sentence',
    },

    # ══════════════════════════════════════════════════════════════════════════
    # 🎭 HİKAYE TÜRLERİ (Genre-Specific)
    # ══════════════════════════════════════════════════════════════════════════

    'horror': {
        'name': 'Horror/Korku',
        'description': '👻 Korku hikayeleri - Kırmızı kan',
        'category': 'Tür',
        'fontname': 'Impact',
        'fontsize': 76,
        'primary_color': '&H000000FF',
        'secondary_color': '&H00FFFFFF',
        'outline_color': '&H00000000',
        'back_color': '&H00000000',
        'bold': -1,
        'italic': 0,
        'underline': 0,
        'outline': 5,
        'shadow': 4,
        'alignment': 2,
        'margin_v': 160,
        'karaoke_mode': 'sentence',
    },

    'creepy': {
        'name': 'Creepy/Ürkütücü',
        'description': '👻 Paranormal hikayeler - Koyu',
        'category': 'Tür',
        'fontname': 'Impact',
        'fontsize': 74,
        'primary_color': '&H00AAAAAA',
        'secondary_color': '&H00FF0000',
        'outline_color': '&H00000000',
        'back_color': '&H00000000',
        'bold': -1,
        'italic': 0,
        'underline': 0,
        'outline': 4,
        'shadow': 6,
        'alignment': 2,
        'margin_v': 165,
        'karaoke_mode': 'sentence',
    },

    'thriller': {
        'name': 'Thriller/Gerilim',
        'description': '🔪 Gerilim hikayeleri - Keskin',
        'category': 'Tür',
        'fontname': 'Impact',
        'fontsize': 76,
        'primary_color': '&H00FFFFFF',
        'secondary_color': '&H000000FF',
        'outline_color': '&H00000000',
        'back_color': '&H00000000',
        'bold': -1,
        'italic': 0,
        'underline': 0,
        'outline': 5,
        'shadow': 5,
        'alignment': 2,
        'margin_v': 158,
        'karaoke_mode': 'sentence',
    },

    'romance': {
        'name': 'Romance/Aşk',
        'description': '💕 Romantik hikayeler - Pembe',
        'category': 'Tür',
        'fontname': 'Arial',
        'fontsize': 72,
        'primary_color': '&H00FF69B4',
        'secondary_color': '&H00FFFFFF',
        'outline_color': '&H00000000',
        'back_color': '&H00000000',
        'bold': -1,
        'italic': 0,
        'underline': 0,
        'outline': 4,
        'shadow': 3,
        'alignment': 2,
        'margin_v': 165,
        'karaoke_mode': 'sentence',
    },

    'drama': {
        'name': 'Drama/Dram',
        'description': '🎭 Dramatik hikayeler - Duygusal',
        'category': 'Tür',
        'fontname': 'Arial Black',
        'fontsize': 74,
        'primary_color': '&H00FFFFFF',
        'secondary_color': '&H00FFD700',
        'outline_color': '&H00000000',
        'back_color': '&H00000000',
        'bold': -1,
        'italic': 0,
        'underline': 0,
        'outline': 4,
        'shadow': 3,
        'alignment': 2,
        'margin_v': 162,
        'karaoke_mode': 'sentence',
    },

    'comedy': {
        'name': 'Comedy/Komedi',
        'description': '😂 Komik hikayeler - Renkli',
        'category': 'Tür',
        'fontname': 'Impact',
        'fontsize': 78,
        'primary_color': '&H0000FFFF',
        'secondary_color': '&H0000FF00',
        'outline_color': '&H00000000',
        'back_color': '&H00000000',
        'bold': -1,
        'italic': 0,
        'underline': 0,
        'outline': 5,
        'shadow': 3,
        'alignment': 2,
        'margin_v': 155,
        'karaoke_mode': 'sentence',
    },

    'action': {
        'name': 'Action/Aksiyon',
        'description': '💥 Aksiyon hikayeleri - Güçlü',
        'category': 'Tür',
        'fontname': 'Impact',
        'fontsize': 80,
        'primary_color': '&H00FFFFFF',
        'secondary_color': '&H000080FF',
        'outline_color': '&H00000000',
        'back_color': '&H00000000',
        'bold': -1,
        'italic': 0,
        'underline': 0,
        'outline': 6,
        'shadow': 4,
        'alignment': 2,
        'margin_v': 150,
        'karaoke_mode': 'sentence',
    },

    'mystery': {
        'name': 'Mystery/Gizem',
        'description': '🔮 Gizem hikayeleri - Mor',
        'category': 'Tür',
        'fontname': 'Impact',
        'fontsize': 74,
        'primary_color': '&H00FF00FF',
        'secondary_color': '&H00FFFFFF',
        'outline_color': '&H00000000',
        'back_color': '&H00000000',
        'bold': -1,
        'italic': 0,
        'underline': 0,
        'outline': 5,
        'shadow': 5,
        'alignment': 2,
        'margin_v': 160,
        'karaoke_mode': 'sentence',
    },

    'truecrime': {
        'name': 'True Crime',
        'description': '🔍 Gerçek suç hikayeleri',
        'category': 'Tür',
        'fontname': 'Impact',
        'fontsize': 76,
        'primary_color': '&H00FFFFFF',
        'secondary_color': '&H000000FF',
        'outline_color': '&H00000000',
        'back_color': '&H00000000',
        'bold': -1,
        'italic': 0,
        'underline': 0,
        'outline': 5,
        'shadow': 4,
        'alignment': 2,
        'margin_v': 158,
        'karaoke_mode': 'sentence',
    },

    'scifi': {
        'name': 'Sci-Fi/Bilim Kurgu',
        'description': '🚀 Bilim kurgu hikayeleri - Cyan',
        'category': 'Tür',
        'fontname': 'Arial Black',
        'fontsize': 74,
        'primary_color': '&H00FFFF00',
        'secondary_color': '&H00FF00FF',
        'outline_color': '&H00000000',
        'back_color': '&H00000000',
        'bold': -1,
        'italic': 0,
        'underline': 0,
        'outline': 4,
        'shadow': 4,
        'alignment': 2,
        'margin_v': 162,
        'karaoke_mode': 'sentence',
    },

    'fantasy': {
        'name': 'Fantasy/Fantezi',
        'description': '🧙 Fantezi hikayeleri - Altın',
        'category': 'Tür',
        'fontname': 'Georgia',
        'fontsize': 72,
        'primary_color': '&H0000D4FF',
        'secondary_color': '&H00FFFFFF',
        'outline_color': '&H00000000',
        'back_color': '&H00000000',
        'bold': -1,
        'italic': 0,
        'underline': 0,
        'outline': 4,
        'shadow': 3,
        'alignment': 2,
        'margin_v': 165,
        'karaoke_mode': 'sentence',
    },

    # ══════════════════════════════════════════════════════════════════════════
    # ✨ EFEKT STİLLERİ (Özel Görsel Efektler)
    # ══════════════════════════════════════════════════════════════════════════

    'neon_pink': {
        'name': 'Neon Pink',
        'description': '💗 Parlak pembe neon',
        'category': 'Efekt',
        'fontname': 'Impact',
        'fontsize': 76,
        'primary_color': '&H00FF00FF',
        'secondary_color': '&H00FFFFFF',
        'outline_color': '&H00FF00FF',
        'back_color': '&H00000000',
        'bold': -1,
        'italic': 0,
        'underline': 0,
        'outline': 4,
        'shadow': 8,
        'alignment': 2,
        'margin_v': 160,
        'karaoke_mode': 'sentence',
    },

    'neon_blue': {
        'name': 'Neon Blue',
        'description': '💙 Parlak mavi neon',
        'category': 'Efekt',
        'fontname': 'Impact',
        'fontsize': 76,
        'primary_color': '&H00FF7700',
        'secondary_color': '&H00FFFFFF',
        'outline_color': '&H00FF7700',
        'back_color': '&H00000000',
        'bold': -1,
        'italic': 0,
        'underline': 0,
        'outline': 4,
        'shadow': 8,
        'alignment': 2,
        'margin_v': 160,
        'karaoke_mode': 'sentence',
    },

    'neon_green': {
        'name': 'Neon Green',
        'description': '💚 Parlak yeşil neon',
        'category': 'Efekt',
        'fontname': 'Impact',
        'fontsize': 76,
        'primary_color': '&H0000FF00',
        'secondary_color': '&H00FFFFFF',
        'outline_color': '&H0000FF00',
        'back_color': '&H00000000',
        'bold': -1,
        'italic': 0,
        'underline': 0,
        'outline': 4,
        'shadow': 8,
        'alignment': 2,
        'margin_v': 160,
        'karaoke_mode': 'sentence',
    },

    'fire': {
        'name': 'Fire/Ateş',
        'description': '🔥 Ateş efekti - Turuncu/Kırmızı',
        'category': 'Efekt',
        'fontname': 'Impact',
        'fontsize': 80,
        'primary_color': '&H000080FF',
        'secondary_color': '&H000000FF',
        'outline_color': '&H00000000',
        'back_color': '&H00000000',
        'bold': -1,
        'italic': 0,
        'underline': 0,
        'outline': 5,
        'shadow': 4,
        'alignment': 2,
        'margin_v': 155,
        'karaoke_mode': 'sentence',
    },

    'ice': {
        'name': 'Ice/Buz',
        'description': '❄️ Buz efekti - Soğuk mavi',
        'category': 'Efekt',
        'fontname': 'Impact',
        'fontsize': 76,
        'primary_color': '&H00FFFF00',
        'secondary_color': '&H00FFFFFF',
        'outline_color': '&H00FFAA00',
        'back_color': '&H00000000',
        'bold': -1,
        'italic': 0,
        'underline': 0,
        'outline': 5,
        'shadow': 5,
        'alignment': 2,
        'margin_v': 160,
        'karaoke_mode': 'sentence',
    },

    'gold': {
        'name': 'Gold/Altın',
        'description': '✨ Lüks altın efekti',
        'category': 'Efekt',
        'fontname': 'Arial Black',
        'fontsize': 76,
        'primary_color': '&H0000D4FF',
        'secondary_color': '&H00FFFFFF',
        'outline_color': '&H00004080',
        'back_color': '&H00000000',
        'bold': -1,
        'italic': 0,
        'underline': 0,
        'outline': 4,
        'shadow': 3,
        'alignment': 2,
        'margin_v': 158,
        'karaoke_mode': 'sentence',
    },

    'silver': {
        'name': 'Silver/Gümüş',
        'description': '🪙 Zarif gümüş efekti',
        'category': 'Efekt',
        'fontname': 'Arial Black',
        'fontsize': 76,
        'primary_color': '&H00C0C0C0',
        'secondary_color': '&H00FFFFFF',
        'outline_color': '&H00404040',
        'back_color': '&H00000000',
        'bold': -1,
        'italic': 0,
        'underline': 0,
        'outline': 4,
        'shadow': 3,
        'alignment': 2,
        'margin_v': 158,
        'karaoke_mode': 'sentence',
    },

    'rainbow': {
        'name': 'Rainbow/Gökkuşağı',
        'description': '🌈 Renkli gökkuşağı',
        'category': 'Efekt',
        'fontname': 'Impact',
        'fontsize': 78,
        'primary_color': '&H00FF00FF',
        'secondary_color': '&H0000FFFF',
        'outline_color': '&H00000000',
        'back_color': '&H00000000',
        'bold': -1,
        'italic': 0,
        'underline': 0,
        'outline': 5,
        'shadow': 3,
        'alignment': 2,
        'margin_v': 155,
        'karaoke_mode': 'sentence',
    },

    'glow': {
        'name': 'Glow/Işıltı',
        'description': '💫 Hafif beyaz ışıltı',
        'category': 'Efekt',
        'fontname': 'Impact',
        'fontsize': 74,
        'primary_color': '&H00FFFFFF',
        'secondary_color': '&H0000FFFF',
        'outline_color': '&H00FFFFFF',
        'back_color': '&H00000000',
        'bold': -1,
        'italic': 0,
        'underline': 0,
        'outline': 3,
        'shadow': 7,
        'alignment': 2,
        'margin_v': 162,
        'karaoke_mode': 'sentence',
    },

    'shadow_deep': {
        'name': 'Deep Shadow',
        'description': '🌑 Derin gölge efekti',
        'category': 'Efekt',
        'fontname': 'Impact',
        'fontsize': 76,
        'primary_color': '&H00FFFFFF',
        'secondary_color': '&H00FFFFFF',
        'outline_color': '&H00000000',
        'back_color': '&H00000000',
        'bold': -1,
        'italic': 0,
        'underline': 0,
        'outline': 4,
        'shadow': 10,
        'alignment': 2,
        'margin_v': 160,
        'karaoke_mode': 'sentence',
    },

    # ══════════════════════════════════════════════════════════════════════════
    # 📺 PROFESYONEL STİLLER (TV/Film Tarzı)
    # ══════════════════════════════════════════════════════════════════════════

    'netflix': {
        'name': 'Netflix Style',
        'description': '📺 Netflix belgesel tarzı',
        'category': 'Profesyonel',
        'fontname': 'Arial',
        'fontsize': 70,
        'primary_color': '&H00FFFFFF',
        'secondary_color': '&H0000FFFF',
        'outline_color': '&H00000000',
        'back_color': '&H80000000',
        'bold': -1,
        'italic': 0,
        'underline': 0,
        'outline': 2,
        'shadow': 0,
        'alignment': 2,
        'margin_v': 80,
        'karaoke_mode': 'sentence',
    },

    'documentary': {
        'name': 'Documentary',
        'description': '📺 Belgesel - Ciddi ton',
        'category': 'Profesyonel',
        'fontname': 'Arial',
        'fontsize': 68,
        'primary_color': '&H00FFFFFF',
        'secondary_color': '&H00FFFFFF',
        'outline_color': '&H00000000',
        'back_color': '&HA0000000',
        'bold': 0,
        'italic': 0,
        'underline': 0,
        'outline': 1,
        'shadow': 0,
        'alignment': 2,
        'margin_v': 60,
        'karaoke_mode': 'sentence',
    },

    'cinematic': {
        'name': 'Cinematic',
        'description': '🎬 Sinematik film tarzı',
        'category': 'Profesyonel',
        'fontname': 'Arial',
        'fontsize': 66,
        'primary_color': '&H00FFFFFF',
        'secondary_color': '&H0080FFFF',
        'outline_color': '&H00000000',
        'back_color': '&H00000000',
        'bold': 0,
        'italic': 0,
        'underline': 0,
        'outline': 3,
        'shadow': 2,
        'alignment': 2,
        'margin_v': 100,
        'karaoke_mode': 'sentence',
    },

    'news': {
        'name': 'News/Haber',
        'description': '📰 Haber kanalı tarzı',
        'category': 'Profesyonel',
        'fontname': 'Arial',
        'fontsize': 68,
        'primary_color': '&H00FFFFFF',
        'secondary_color': '&H000000FF',
        'outline_color': '&H00000000',
        'back_color': '&H90000000',
        'bold': -1,
        'italic': 0,
        'underline': 0,
        'outline': 2,
        'shadow': 0,
        'alignment': 2,
        'margin_v': 70,
        'karaoke_mode': 'sentence',
    },

    'podcast': {
        'name': 'Podcast Style',
        'description': '🎙️ Podcast/Röportaj',
        'category': 'Profesyonel',
        'fontname': 'Arial',
        'fontsize': 72,
        'primary_color': '&H00FFFFFF',
        'secondary_color': '&H0000FFFF',
        'outline_color': '&H00000000',
        'back_color': '&H90000000',
        'bold': -1,
        'italic': 0,
        'underline': 0,
        'outline': 2,
        'shadow': 0,
        'alignment': 2,
        'margin_v': 70,
        'karaoke_mode': 'sentence',
    },

    'interview': {
        'name': 'Interview',
        'description': '🎤 Röportaj tarzı - Alt bar',
        'category': 'Profesyonel',
        'fontname': 'Arial',
        'fontsize': 64,
        'primary_color': '&H00FFFFFF',
        'secondary_color': '&H00FFFFFF',
        'outline_color': '&H00000000',
        'back_color': '&HCC000000',
        'bold': 0,
        'italic': 0,
        'underline': 0,
        'outline': 0,
        'shadow': 0,
        'alignment': 2,
        'margin_v': 50,
        'karaoke_mode': 'sentence',
    },

    # ══════════════════════════════════════════════════════════════════════════
    # 🎮 ÖZEL AMAÇ STİLLERİ
    # ══════════════════════════════════════════════════════════════════════════

    'gaming': {
        'name': 'Gaming/Oyun',
        'description': '🎮 Oyun videoları - Yeşil',
        'category': 'Özel',
        'fontname': 'Impact',
        'fontsize': 78,
        'primary_color': '&H0000FF00',
        'secondary_color': '&H00FFFFFF',
        'outline_color': '&H00000000',
        'back_color': '&H00000000',
        'bold': -1,
        'italic': 0,
        'underline': 0,
        'outline': 5,
        'shadow': 3,
        'alignment': 2,
        'margin_v': 155,
        'karaoke_mode': 'sentence',
    },

    'anime': {
        'name': 'Anime/Manga',
        'description': '🎌 Anime tarzı - Renkli',
        'category': 'Özel',
        'fontname': 'Arial Black',
        'fontsize': 74,
        'primary_color': '&H00FFFFFF',
        'secondary_color': '&H00FF1493',
        'outline_color': '&H00000000',
        'back_color': '&H00000000',
        'bold': -1,
        'italic': 0,
        'underline': 0,
        'outline': 4,
        'shadow': 3,
        'alignment': 2,
        'margin_v': 160,
        'karaoke_mode': 'sentence',
    },

    'motivational': {
        'name': 'Motivational',
        'description': '💪 Motivasyon videoları',
        'category': 'Özel',
        'fontname': 'Arial Black',
        'fontsize': 82,
        'primary_color': '&H00FFFFFF',
        'secondary_color': '&H0000D4FF',
        'outline_color': '&H00000000',
        'back_color': '&H00000000',
        'bold': -1,
        'italic': 0,
        'underline': 0,
        'outline': 6,
        'shadow': 2,
        'alignment': 2,
        'margin_v': 145,
        'karaoke_mode': 'sentence',
    },

    'educational': {
        'name': 'Educational',
        'description': '📚 Eğitim videoları - Temiz',
        'category': 'Özel',
        'fontname': 'Arial',
        'fontsize': 70,
        'primary_color': '&H00FFFFFF',
        'secondary_color': '&H000099FF',
        'outline_color': '&H00000000',
        'back_color': '&H80000000',
        'bold': -1,
        'italic': 0,
        'underline': 0,
        'outline': 2,
        'shadow': 0,
        'alignment': 2,
        'margin_v': 80,
        'karaoke_mode': 'sentence',
    },

    'tech': {
        'name': 'Tech/Teknoloji',
        'description': '💻 Teknoloji videoları',
        'category': 'Özel',
        'fontname': 'Arial',
        'fontsize': 72,
        'primary_color': '&H00FFFFFF',
        'secondary_color': '&H00FF7700',
        'outline_color': '&H00000000',
        'back_color': '&H00000000',
        'bold': -1,
        'italic': 0,
        'underline': 0,
        'outline': 4,
        'shadow': 2,
        'alignment': 2,
        'margin_v': 165,
        'karaoke_mode': 'sentence',
    },

    'travel': {
        'name': 'Travel/Seyahat',
        'description': '✈️ Seyahat videoları',
        'category': 'Özel',
        'fontname': 'Arial Black',
        'fontsize': 74,
        'primary_color': '&H00FFFFFF',
        'secondary_color': '&H00FFD700',
        'outline_color': '&H00000000',
        'back_color': '&H00000000',
        'bold': -1,
        'italic': 0,
        'underline': 0,
        'outline': 4,
        'shadow': 3,
        'alignment': 2,
        'margin_v': 162,
        'karaoke_mode': 'sentence',
    },

    'cooking': {
        'name': 'Cooking/Yemek',
        'description': '🍳 Yemek videoları - Sıcak',
        'category': 'Özel',
        'fontname': 'Arial Black',
        'fontsize': 74,
        'primary_color': '&H00FFFFFF',
        'secondary_color': '&H000080FF',
        'outline_color': '&H00000000',
        'back_color': '&H00000000',
        'bold': -1,
        'italic': 0,
        'underline': 0,
        'outline': 4,
        'shadow': 3,
        'alignment': 2,
        'margin_v': 162,
        'karaoke_mode': 'sentence',
    },

    # ══════════════════════════════════════════════════════════════════════════
    # 🎨 KLASİK / MİNİMAL STİLLER
    # ══════════════════════════════════════════════════════════════════════════

    'minimal': {
        'name': 'Minimal Clean',
        'description': '⚪ Temiz, sade, profesyonel',
        'category': 'Klasik',
        'fontname': 'Arial',
        'fontsize': 72,
        'primary_color': '&H00FFFFFF',
        'secondary_color': '&H00FFFFFF',
        'outline_color': '&H00000000',
        'back_color': '&H00000000',
        'bold': -1,
        'italic': 0,
        'underline': 0,
        'outline': 4,
        'shadow': 2,
        'alignment': 2,
        'margin_v': 170,
        'karaoke_mode': 'sentence',
    },

    'elegant': {
        'name': 'Elegant',
        'description': '✨ Zarif, sofistike',
        'category': 'Klasik',
        'fontname': 'Georgia',
        'fontsize': 68,
        'primary_color': '&H00FFFFFF',
        'secondary_color': '&H0080FFFF',
        'outline_color': '&H00000000',
        'back_color': '&H00000000',
        'bold': 0,
        'italic': -1,
        'underline': 0,
        'outline': 3,
        'shadow': 2,
        'alignment': 2,
        'margin_v': 170,
        'karaoke_mode': 'sentence',
    },

    'classic': {
        'name': 'Classic White',
        'description': '⚪ Klasik beyaz - Evrensel',
        'category': 'Klasik',
        'fontname': 'Arial',
        'fontsize': 70,
        'primary_color': '&H00FFFFFF',
        'secondary_color': '&H00FFFFFF',
        'outline_color': '&H00000000',
        'back_color': '&H00000000',
        'bold': -1,
        'italic': 0,
        'underline': 0,
        'outline': 3,
        'shadow': 2,
        'alignment': 2,
        'margin_v': 175,
        'karaoke_mode': 'sentence',
    },

    'retro': {
        'name': 'Retro/Vintage',
        'description': '📼 Eski film efekti',
        'category': 'Klasik',
        'fontname': 'Arial',
        'fontsize': 70,
        'primary_color': '&H00FFCC99',
        'secondary_color': '&H00FFFFFF',
        'outline_color': '&H00000000',
        'back_color': '&H00000000',
        'bold': -1,
        'italic': 0,
        'underline': 0,
        'outline': 3,
        'shadow': 3,
        'alignment': 2,
        'margin_v': 170,
        'karaoke_mode': 'sentence',
    },

    'typewriter': {
        'name': 'Typewriter',
        'description': '⌨️ Daktilo tarzı',
        'category': 'Klasik',
        'fontname': 'Courier New',
        'fontsize': 66,
        'primary_color': '&H00FFFFFF',
        'secondary_color': '&H00FFFFFF',
        'outline_color': '&H00000000',
        'back_color': '&H00000000',
        'bold': -1,
        'italic': 0,
        'underline': 0,
        'outline': 3,
        'shadow': 2,
        'alignment': 2,
        'margin_v': 175,
        'karaoke_mode': 'sentence',
    },
}


# ============================================================================
# 🎬 ASS SUBTITLE GENERATOR
# ============================================================================

def generate_ass_subtitle(segments: List[Dict], style_name: str = 'storytime',
                          temp_folder: str = '/tmp', highlight_color: Optional[str] = None) -> str:
    """
    Verilen style ile ASS subtitle dosyası oluştur - KARAOKE DESTEKLİ

    Args:
        segments: Altyazı segmentleri listesi
        style_name: Kullanılacak stil adı
        temp_folder: Geçici dosya klasörü
        highlight_color: Vurgu rengi ('yellow', 'cyan', vb.) - None ise stil varsayılanı

    Karaoke Efekti:
        - SecondaryColour: Henüz söylenmemiş metin (beyaz)
        - PrimaryColour: Söylenen metin (seçilen vurgu rengi)
        - \\kf tag'i ile dolum efekti
    """
    import os

    if style_name not in SUBTITLE_STYLES:
        style_name = 'storytime'  # Fallback

    style = SUBTITLE_STYLES[style_name]
    ass_file = os.path.join(temp_folder, f'subtitles_{style_name}.ass')

    # Vurgu rengini belirle (söylenen metin rengi)
    if highlight_color and highlight_color in HIGHLIGHT_COLORS:
        primary_color = HIGHLIGHT_COLORS[highlight_color]['color']
        color_name = HIGHLIGHT_COLORS[highlight_color]['name']
    else:
        # Varsayılan: Sarı (en popüler)
        primary_color = HIGHLIGHT_COLORS[DEFAULT_HIGHLIGHT_COLOR]['color']
        color_name = HIGHLIGHT_COLORS[DEFAULT_HIGHLIGHT_COLOR]['name']

    # Henüz söylenmemiş metin rengi (beyaz)
    secondary_color = '&H00FFFFFF'  # Beyaz

    with open(ass_file, 'w', encoding='utf-8') as f:
        # Header
        f.write("[Script Info]\n")
        f.write("ScriptType: v4.00+\n")
        f.write("WrapStyle: 2\n")
        f.write("ScaledBorderAndShadow: yes\n")
        f.write("YCbCr Matrix: TV.709\n")
        f.write("PlayResX: 1920\n")
        f.write("PlayResY: 1080\n")
        f.write(f"; Style: {style['name']}\n")
        f.write(f"; Highlight Color: {color_name}\n")
        f.write(f"; Karaoke: Spoken={color_name}, Unspoken=White\n")
        f.write("\n")

        # Style definition
        # PrimaryColour = Söylenen metin (vurgu rengi)
        # SecondaryColour = Söylenmemiş metin (beyaz) - karaoke için
        f.write("[V4+ Styles]\n")
        f.write("Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, "
                "Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
                "Alignment, MarginL, MarginR, MarginV, Encoding\n")

        f.write(f"Style: Default,"
                f"{style['fontname']},"
                f"{style['fontsize']},"
                f"{primary_color},"  # Söylenen metin (vurgu rengi)
                f"{secondary_color},"  # Söylenmemiş metin (beyaz)
                f"{style['outline_color']},"
                f"{style['back_color']},"
                f"{style['bold']},"
                f"{style['italic']},"
                f"{style['underline']},"
                f"0,"  # StrikeOut
                f"100,"  # ScaleX
                f"100,"  # ScaleY
                f"0,"  # Spacing
                f"0,"  # Angle
                f"1,"  # BorderStyle
                f"{style['outline']},"
                f"{style['shadow']},"
                f"{style['alignment']},"
                f"350,"  # MarginL
                f"350,"  # MarginR
                f"{style['margin_v']},"
                f"1\n")  # Encoding
        f.write("\n")

        # Events
        f.write("[Events]\n")
        f.write("Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")

        for segment in segments:
            start_time = segment['start']
            end_time = segment['end']
            text = segment['text'].upper()
            words = segment.get('words', [])

            def format_ass_time(seconds):
                hours = int(seconds // 3600)
                minutes = int((seconds % 3600) // 60)
                secs = int(seconds % 60)
                centis = int((seconds % 1) * 100)
                return f"{hours}:{minutes:02d}:{secs:02d}.{centis:02d}"

            start_str = format_ass_time(start_time)
            end_str = format_ass_time(end_time)

            # 🎤 KARAOKE: Kelime söylendiğinde ANINDA renklenir
            # \k = instant highlight (kelime anında renklenir, harf harf değil)
            if words and len(words) > 0:
                karaoke_text = ""
                for word_info in words:
                    word_text = word_info['text'].upper()
                    word_end = word_info.get('end', 0)
                    word_start = word_info.get('start', 0)

                    # Kelime süresi (centiseconds)
                    relative_duration = (word_end - word_start)
                    duration_cs = int(relative_duration * 100)
                    duration_cs = max(duration_cs, 10)  # Minimum 0.1 saniye

                    # \k = instant karaoke (kelime ANINDA renklenir)
                    karaoke_text += f"{{\\k{duration_cs}}}{word_text} "

                final_text = "{\\q3}" + karaoke_text.strip()
            else:
                # Kelime zamanlaması yoksa düz metin
                final_text = "{\\q3}" + text

            f.write(f"Dialogue: 0,{start_str},{end_str},Default,,0,0,0,,{final_text}\n")

    return ass_file


def get_available_styles() -> Dict[str, Dict]:
    """Mevcut subtitle stillerini döndür"""
    return SUBTITLE_STYLES


def get_style_names() -> List[str]:
    """Style isimlerini liste olarak döndür"""
    return list(SUBTITLE_STYLES.keys())


def get_style_description(style_name: str) -> str:
    """Style açıklamasını döndür"""
    if style_name in SUBTITLE_STYLES:
        style = SUBTITLE_STYLES[style_name]
        return f"{style['name']}: {style['description']}"
    return "Unknown style"


def get_styles_by_category() -> Dict[str, List[str]]:
    """Stilleri kategoriye göre grupla"""
    categories = {}
    for style_name, style in SUBTITLE_STYLES.items():
        category = style.get('category', 'Diğer')
        if category not in categories:
            categories[category] = []
        categories[category].append(style_name)
    return categories


def interactive_style_selector(default_style: str = 'storytime') -> str:
    """
    Kullanıcıya interaktif stil seçim menüsü göster
    """
    print("\n" + "═"*80)
    print("🎨 ALTYAZI STİLİ SEÇİMİ".center(80))
    print(f"📊 {len(SUBTITLE_STYLES)} Farklı Stil".center(80))
    print("═"*80)

    # Kategorilere göre grupla
    categories = get_styles_by_category()
    category_order = ['Viral', 'Tür', 'Efekt', 'Profesyonel', 'Özel', 'Klasik']
    category_icons = {
        'Viral': '🔥',
        'Tür': '🎭',
        'Efekt': '✨',
        'Profesyonel': '📺',
        'Özel': '🎯',
        'Klasik': '⚪'
    }

    style_index = 1
    style_map = {}

    for category in category_order:
        if category in categories:
            icon = category_icons.get(category, '📁')
            print(f"\n{icon} {category.upper()} ({len(categories[category])} stil)")
            print("─" * 80)

            # 2 sütun halinde göster
            styles = categories[category]
            for i in range(0, len(styles), 2):
                left_style = styles[i]
                left_info = SUBTITLE_STYLES[left_style]
                left_marker = "▸" if left_style == default_style else " "
                left_text = f"{left_marker}{style_index:2d}. {left_info['name']:<18} {left_info['description'][:25]}"
                style_map[style_index] = left_style
                style_index += 1

                if i + 1 < len(styles):
                    right_style = styles[i + 1]
                    right_info = SUBTITLE_STYLES[right_style]
                    right_marker = "▸" if right_style == default_style else " "
                    right_text = f"{right_marker}{style_index:2d}. {right_info['name']:<18} {right_info['description'][:25]}"
                    style_map[style_index] = right_style
                    style_index += 1
                    print(f"  {left_text:<38} │ {right_text}")
                else:
                    print(f"  {left_text}")

    print("\n" + "═"*80)
    default_info = SUBTITLE_STYLES.get(default_style, SUBTITLE_STYLES['storytime'])
    print(f"💡 Varsayılan: {default_info['name']} (Enter ile devam)")
    print("═"*80)

    while True:
        try:
            secim = input(f"\n🎯 Stil seçin (1-{len(style_map)}) veya Enter: ").strip()

            if secim == "":
                print(f"✅ Seçilen: {default_info['name']}")
                return default_style

            secim_num = int(secim)

            if secim_num in style_map:
                chosen_style = style_map[secim_num]
                chosen_info = SUBTITLE_STYLES[chosen_style]
                print(f"✅ Seçilen: {chosen_info['name']} - {chosen_info['description']}")
                return chosen_style
            else:
                print(f"❌ Geçersiz! 1-{len(style_map)} arası bir sayı girin.")

        except ValueError:
            print("❌ Geçersiz giriş! Sayı girin veya Enter basın.")
        except KeyboardInterrupt:
            print(f"\n⚠️ İptal - Varsayılan: {default_info['name']}")
            return default_style


def interactive_highlight_color_selector(default_color: str = 'yellow') -> str:
    """
    Kullanıcıya interaktif vurgu rengi seçim menüsü göster
    """
    print("\n" + "═"*60)
    print("🎨 VURGU RENGİ SEÇİMİ".center(60))
    print("Altyazı metni bu renkte görünecek".center(60))
    print("═"*60)

    color_map = {}
    color_index = 1

    # Renkleri listele
    for color_key, color_info in HIGHLIGHT_COLORS.items():
        marker = "▸" if color_key == default_color else " "
        print(f"  {marker}{color_index:2d}. {color_info['name']:<15} {color_info['description']}")
        color_map[color_index] = color_key
        color_index += 1

    print("\n" + "═"*60)
    default_info = HIGHLIGHT_COLORS.get(default_color, HIGHLIGHT_COLORS['yellow'])
    print(f"💡 Varsayılan: {default_info['name']} (Enter ile devam)")
    print("═"*60)

    while True:
        try:
            secim = input(f"\n🎨 Renk seçin (1-{len(color_map)}) veya Enter: ").strip()

            if secim == "":
                print(f"✅ Seçilen Renk: {default_info['name']}")
                return default_color

            secim_num = int(secim)

            if secim_num in color_map:
                chosen_color = color_map[secim_num]
                chosen_info = HIGHLIGHT_COLORS[chosen_color]
                print(f"✅ Seçilen Renk: {chosen_info['name']} - {chosen_info['description']}")
                return chosen_color
            else:
                print(f"❌ Geçersiz! 1-{len(color_map)} arası bir sayı girin.")

        except ValueError:
            print("❌ Geçersiz giriş! Sayı girin veya Enter basın.")
        except KeyboardInterrupt:
            print(f"\n⚠️ İptal - Varsayılan: {default_info['name']}")
            return default_color


def get_highlight_colors() -> Dict[str, Dict]:
    """Mevcut vurgu renklerini döndür"""
    return HIGHLIGHT_COLORS


def get_highlight_color_names() -> List[str]:
    """Vurgu rengi isimlerini liste olarak döndür"""
    return list(HIGHLIGHT_COLORS.keys())
