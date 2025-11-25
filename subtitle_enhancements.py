#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SUBTITLE ENHANCEMENTS - Hikaye Kanalları İçin Gelişmiş Altyazı Sistemi
Story-focused subtitle features: karaoke glow, dramatic words, dynamic sizing
"""

import re
import random
from typing import Dict, List, Tuple

# ============================================================================
# 🎯 DRAMATIC WORD DETECTION - Önemli Kelimeleri Tespit Et
# ============================================================================

# Dramatic word patterns - duygusal/vurgulu kelimeler
DRAMATIC_PATTERNS = {
    # Pozitif/Heyecan
    'positive': {
        'keywords': ['aşk', 'mutlu', 'harika', 'muhteşem', 'mükemmel', 'süper', 'güzel',
                     'love', 'amazing', 'perfect', 'great', 'wonderful', 'wow'],
        'color': '00FFAA',  # Yeşil-mavi
        'size_mult': 1.15,   # %15 büyüt
    },
    # Negatif/Korku
    'negative': {
        'keywords': ['korku', 'dehşet', 'tehlike', 'ölüm', 'kan', 'acı', 'üzgün', 'kötü',
                     'fear', 'death', 'danger', 'terrible', 'horror', 'bad', 'evil'],
        'color': 'FF3333',  # Kırmızı
        'size_mult': 1.20,   # %20 büyüt
    },
    # Şaşırma/Vurgu
    'surprise': {
        'keywords': ['ne', 'nasıl', 'inanamıyorum', 'şok', 'vay', 'aman', 'allah',
                     'what', 'how', 'omg', 'wow', 'god', 'unbelievable'],
        'color': 'FFFF00',  # Sarı
        'size_mult': 1.25,   # %25 büyüt
    },
    # Aksiyon/Hız
    'action': {
        'keywords': ['hızlı', 'koş', 'kaç', 'dur', 'gel', 'git', 'çabuk', 'acele',
                     'run', 'fast', 'quick', 'stop', 'go', 'hurry', 'now'],
        'color': 'FF8800',  # Turuncu
        'size_mult': 1.18,   # %18 büyüt
    },
}

# Ünlem işaretli kelimeler - her zaman dramatic
EXCLAMATION_MULT = 1.30  # %30 büyüt

def is_dramatic_word(word: str) -> Tuple[bool, str, float]:
    """
    Kelimenin dramatic olup olmadığını kontrol et

    Returns:
        (is_dramatic, color_hex, size_multiplier)
    """
    word_clean = word.strip().lower()
    word_clean = re.sub(r'[^\w\s]', '', word_clean)  # Noktalama işaretlerini temizle

    # Ünlem işareti kontrolü
    has_exclamation = '!' in word

    # Pattern matching
    for category, config in DRAMATIC_PATTERNS.items():
        if word_clean in config['keywords']:
            size_mult = config['size_mult']
            if has_exclamation:
                size_mult = max(size_mult, EXCLAMATION_MULT)
            return True, config['color'], size_mult

    # BÜYÜK HARFLER kontrolü (ALL CAPS)
    if word_clean and len(word_clean) > 2 and word.isupper():
        return True, 'FFFFFF', 1.20  # Beyaz, %20 büyüt

    # Ünlem işareti varsa
    if has_exclamation:
        return True, 'FFAA00', EXCLAMATION_MULT  # Turuncu-sarı

    return False, 'FFFFFF', 1.0


def detect_word_length_category(word: str) -> str:
    """Kelime uzunluğuna göre kategori belirle"""
    length = len(word.strip())

    if length <= 3:
        return 'very_short'  # "İLE", "VE", "DA"
    elif length <= 6:
        return 'short'       # Normal kelimeler
    elif length <= 10:
        return 'medium'      # Uzunca kelimeler
    else:
        return 'long'        # Çok uzun kelimeler


def calculate_dynamic_size(word: str, base_size: int, is_dramatic: bool, dramatic_mult: float) -> int:
    """
    Kelime için dinamik font size hesapla

    Args:
        word: Kelime
        base_size: Temel font boyutu
        is_dramatic: Dramatic word mi?
        dramatic_mult: Dramatic çarpanı

    Returns:
        Hesaplanan font size
    """
    length_category = detect_word_length_category(word)

    # Uzunluk bazlı çarpan
    length_multipliers = {
        'very_short': 0.95,   # Çok kısa kelimeler biraz küçük
        'short': 1.0,         # Normal
        'medium': 0.95,       # Uzun kelimeler küçült
        'long': 0.85,         # Çok uzun kelimeler daha da küçült
    }

    length_mult = length_multipliers.get(length_category, 1.0)

    # Dramatic ise dramatic_mult uygula
    if is_dramatic:
        final_mult = dramatic_mult
    else:
        final_mult = length_mult

    calculated_size = int(base_size * final_mult)

    # Limit kontrolü (minimum 60, maksimum 90)
    calculated_size = max(60, min(90, calculated_size))

    return calculated_size


# ============================================================================
# 🌟 KARAOKE GLOW & PULSE EFFECTS - ASS Override Tags
# ============================================================================

def generate_karaoke_glow_effect(word: str, duration_cs: int, color: str = 'FFFFFF',
                                   glow_strength: int = 3) -> str:
    """
    Kelime için karaoke + glow effect oluştur

    ASS Override Tags:
        \\k{duration} - Karaoke timing
        \\blur{strength} - Glow effect (blur ile glow simülasyonu)
        \\bord{width} - Border width (glow için)
        \\3c&H{color}& - Border color
        \\t(start,end,tags) - Transform animation

    Args:
        word: Kelime
        duration_cs: Süre (centiseconds)
        color: Hex renk (RRGGBB format)
        glow_strength: Glow yoğunluğu (1-5)

    Returns:
        ASS formatted karaoke text
    """
    # Karaoke timing
    karaoke_tag = f"\\k{duration_cs}"

    # Glow efekti - başlangıç (opacity düşük)
    glow_start = f"\\blur{glow_strength}\\3c&H{color}&\\alpha&H40&"

    # Glow efekti - zirve (opacity yüksek, kelime aktif olunca)
    glow_peak = f"\\blur{glow_strength + 2}\\3c&H{color}&\\alpha&H00&"

    # Transform animation - kelime aktif olunca glow parlar
    # \t(accel,start_time,end_time,style_mods)
    transform_in = f"\\t(0,{duration_cs // 4},{glow_peak})"
    transform_out = f"\\t({duration_cs * 3 // 4},{duration_cs},{glow_start})"

    # Final tag
    effect_tag = f"{{{karaoke_tag}{transform_in}{transform_out}}}"

    return f"{effect_tag}{word}"


def generate_pulse_effect(word: str, duration_cs: int, size_mult: float = 1.15) -> str:
    """
    Kelime için pulse (nabız) efekti oluştur

    ASS Override Tags:
        \\fscx, \\fscy - Font scale X/Y (pulse için)
        \\t() - Transform animation

    Args:
        word: Kelime
        duration_cs: Süre (centiseconds)
        size_mult: Boyut çarpanı (1.15 = %15 büyüme)

    Returns:
        ASS formatted text with pulse
    """
    karaoke_tag = f"\\k{duration_cs}"

    # Normal boyut
    scale_normal = 100

    # Büyüme boyutu
    scale_pulse = int(100 * size_mult)

    # Pulse animasyonu - büyü, sonra küçült
    # İlk yarısı: normal → büyük
    pulse_in = f"\\t(0,{duration_cs // 2},\\fscx{scale_pulse}\\fscy{scale_pulse})"

    # İkinci yarısı: büyük → normal
    pulse_out = f"\\t({duration_cs // 2},{duration_cs},\\fscx{scale_normal}\\fscy{scale_normal})"

    effect_tag = f"{{{karaoke_tag}{pulse_in}{pulse_out}}}"

    return f"{effect_tag}{word}"


def generate_dramatic_word_effect(word: str, duration_cs: int, color: str,
                                   size: int, base_size: int) -> str:
    """
    Dramatic words için özel efekt - glow + pulse + color + size

    Args:
        word: Kelime
        duration_cs: Süre (centiseconds)
        color: Hex renk
        size: Hedef font size
        base_size: Temel font size

    Returns:
        ASS formatted dramatic word
    """
    karaoke_tag = f"\\k{duration_cs}"

    # Font size override
    size_diff = size - base_size
    size_tag = f"\\fs{size}" if size_diff != 0 else ""

    # Color override (primary color)
    color_tag = f"\\c&H{color}&"

    # Glow efekti
    glow_strength = 4  # Dramatic words için daha güçlü glow
    glow_tag = f"\\blur{glow_strength}\\3c&HFF{color[2:]}FF&"  # Border color lighter

    # Pulse animation
    scale_pulse = 115  # %15 büyüme
    pulse_in = f"\\t(0,{duration_cs // 3},\\fscx{scale_pulse}\\fscy{scale_pulse})"
    pulse_out = f"\\t({duration_cs * 2 // 3},{duration_cs},\\fscx100\\fscy100)"

    # Alpha animation (fade in)
    alpha_in = f"\\alpha&HFF&\\t(0,{duration_cs // 4},\\alpha&H00&)"

    # Combine all
    effect_tag = f"{{{karaoke_tag}{size_tag}{color_tag}{glow_tag}{pulse_in}{pulse_out}{alpha_in}}}"

    return f"{effect_tag}{word}"


# ============================================================================
# 🎨 MAIN ENHANCEMENT FUNCTION
# ============================================================================

def enhance_subtitle_segment(words: List[Dict], base_fontsize: int = 72,
                             enable_glow: bool = True, enable_pulse: bool = True,
                             enable_dramatic: bool = True) -> str:
    """
    Segment içindeki tüm kelimeler için gelişmiş efektler uygula

    Args:
        words: Kelime listesi [{'text': 'kelime', 'start': 0.0, 'end': 0.5, 'duration': 50}, ...]
        base_fontsize: Temel font boyutu
        enable_glow: Glow efekti aktif mi?
        enable_pulse: Pulse efekti aktif mi?
        enable_dramatic: Dramatic word detection aktif mi?

    Returns:
        ASS formatted subtitle text
    """
    enhanced_words = []

    for word_data in words:
        word = word_data['text']
        duration = word_data['duration']

        # Dramatic word detection
        is_dramatic, color, size_mult = False, 'FFFFFF', 1.0
        if enable_dramatic:
            is_dramatic, color, size_mult = is_dramatic_word(word)

        # Dynamic sizing
        word_size = calculate_dynamic_size(word, base_fontsize, is_dramatic, size_mult)

        # Efekt seçimi
        if is_dramatic and enable_dramatic:
            # Dramatic word - full effects
            enhanced_word = generate_dramatic_word_effect(
                word, duration, color, word_size, base_fontsize
            )
        elif enable_glow and enable_pulse:
            # Normal word - glow + pulse
            # Rastgele glow veya pulse seç
            if random.random() < 0.5:
                enhanced_word = generate_karaoke_glow_effect(word, duration, color='FFFFFF', glow_strength=2)
            else:
                enhanced_word = generate_pulse_effect(word, duration, size_mult=1.08)
        elif enable_glow:
            # Sadece glow
            enhanced_word = generate_karaoke_glow_effect(word, duration, color='FFFFFF', glow_strength=2)
        elif enable_pulse:
            # Sadece pulse
            enhanced_word = generate_pulse_effect(word, duration, size_mult=1.08)
        else:
            # Basit karaoke
            enhanced_word = f"{{\\k{duration}}}{word}"

        enhanced_words.append(enhanced_word)

    return ' '.join(enhanced_words)


# ============================================================================
# 📐 DYNAMIC LINE BREAKING - Per-Word Analysis
# ============================================================================

def smart_line_break_with_sizing(words: List[Dict], max_chars_per_line: int = 35,
                                  base_fontsize: int = 72) -> Tuple[str, str]:
    """
    Kelime uzunluklarını ve dramatic statuslerini hesaba katarak akıllıca satır kır

    Args:
        words: Kelime listesi
        max_chars_per_line: Maksimum karakter (yaklaşık - dynamic sizing ile değişir)
        base_fontsize: Temel font boyutu

    Returns:
        (line1_text, line2_text) - Her biri enhanced ASS formatted
    """
    if len(words) <= 4:
        # Tek satır yeterli
        line1 = enhance_subtitle_segment(words, base_fontsize)
        return line1, ""

    # En iyi bölme noktasını bul
    total_words = len(words)
    best_split = total_words // 2
    min_imbalance = float('inf')

    for i in range(1, total_words):
        line1_words = words[:i]
        line2_words = words[i:]

        # Her satırın tahmini pixel genişliğini hesapla
        line1_width = sum(len(w['text']) * calculate_dynamic_size(w['text'], base_fontsize, *is_dramatic_word(w['text'])[:2])
                          for w in line1_words)
        line2_width = sum(len(w['text']) * calculate_dynamic_size(w['text'], base_fontsize, *is_dramatic_word(w['text'])[:2])
                          for w in line2_words)

        imbalance = abs(line1_width - line2_width)

        if imbalance < min_imbalance:
            min_imbalance = imbalance
            best_split = i

    # Satırları oluştur
    line1_words = words[:best_split]
    line2_words = words[best_split:]

    line1_text = enhance_subtitle_segment(line1_words, base_fontsize)
    line2_text = enhance_subtitle_segment(line2_words, base_fontsize)

    return line1_text, line2_text


# ============================================================================
# 🔧 CONFIGURATION
# ============================================================================

SUBTITLE_ENHANCEMENT_CONFIG = {
    'enabled': True,

    # Feature toggles
    'features': {
        'glow_effect': True,          # Kelime kelime glow
        'pulse_effect': True,         # Pulse animasyonu
        'dramatic_detection': True,   # Dramatic word detection
        'dynamic_sizing': True,       # Uzunluğa göre boyutlandırma
        'color_changes': True,        # Duygu bazlı renk değişimi
    },

    # Intensity settings
    'intensity': {
        'glow_strength': 3,           # 1-5 (3 = optimal)
        'pulse_multiplier': 1.15,     # 1.10-1.25
        'dramatic_size_boost': 1.25,  # Dramatic words %25 daha büyük
    },

    # Performance
    'max_words_per_segment': 10,     # Çok fazla kelime olursa kısalt
}


def get_enhancement_config():
    """Enhancement config'i döndür"""
    return SUBTITLE_ENHANCEMENT_CONFIG
