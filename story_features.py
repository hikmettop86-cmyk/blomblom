#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
STORY FEATURES - Hikaye Kanalları İçin Özel Özellikler
Hook optimization, climax detection, pacing control
"""

import random
import subprocess
import json
from typing import Dict, List, Tuple, Optional

# ============================================================================
# 🎣 HOOK OPTIMIZER - İlk 3 Saniye Viral Efektler
# ============================================================================

HOOK_DURATION = 3.0  # İlk 3 saniye = hook


def generate_hook_effects(clip_duration: float, base_effects: str = "") -> str:
    """
    İlk 3 saniye için agresif viral efektler oluştur

    Hook Stratejisi:
    - Daha agresif zoom/shake
    - Yüksek kontrast/brightness
    - Hızlı pulse efektleri
    - TikTok/Reels optimize

    Args:
        clip_duration: Clip süresi (saniye)
        base_effects: Mevcut efektler (varsa)

    Returns:
        FFmpeg filter string
    """
    hook_filters = []

    # 1. 🔥 AGGRESSIVE ZOOM - Basit zoom in effect
    # Constant zoom 1.12x (smooth, no expression errors)
    hook_filters.append(
        "zoompan=z='1.12':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080"
    )

    # 2. 🌈 BRIGHT COLORS - Kontrast & Saturation boost
    # İlk 3 saniyede daha canlı renkler
    contrast = 1.25  # %25 daha fazla kontrast
    saturation = 1.3  # %30 daha fazla doygunluk
    brightness = 0.05  # Hafif brightness boost

    hook_filters.append(
        f"eq=contrast={contrast}:saturation={saturation}:brightness={brightness}"
    )

    # 3. 📳 SHAKE EFFECT - Basitleştirilmiş (expression karmaşıklığını önle)
    # Static crop + scale (shake yerine slight zoom/crop)
    hook_filters.append(
        "crop=in_w-16:in_h-16:8:8"  # Slight crop from edges
    )
    hook_filters.append(
        "scale=1920:1080:flags=lanczos"  # Scale back to 1920x1080
    )

    # 4. ⚡ VIGNETTE - Merkeze odaklanma (text için ideal)
    # Güçlü vignette
    hook_filters.append(
        "vignette=angle=PI/3.5:mode=forward"
    )

    # 5. ✨ SHARPNESS BOOST - Glow yerine keskinlik (basit ve güvenli)
    # Unsharp mask for sharpness (no complex filter syntax)
    hook_filters.append(
        "unsharp=5:5:0.8:5:5:0.0"  # Sharpen (luma only)
    )

    return ','.join(hook_filters)


def should_apply_hook_effects(clip_index: int, clip_start_time: float) -> bool:
    """
    Bu clip'e hook effects uygulanmalı mı?

    Args:
        clip_index: Clip index (0-based)
        clip_start_time: Clip'in video içindeki başlangıç zamanı (saniye)

    Returns:
        True if hook effects should be applied
    """
    # İlk 3 saniyeye denk gelen tüm clipler hook alır
    return clip_start_time < HOOK_DURATION


def get_hook_intensity(clip_start_time: float, clip_duration: float) -> float:
    """
    Hook efektlerinin yoğunluğunu hesapla (0.0-1.0)

    Args:
        clip_start_time: Clip başlangıç zamanı
        clip_duration: Clip süresi

    Returns:
        Intensity factor (1.0 = full, 0.0 = none)
    """
    if clip_start_time >= HOOK_DURATION:
        return 0.0

    # Clip'in hook zone içinde ne kadarı var?
    clip_end_time = clip_start_time + clip_duration
    hook_overlap = min(HOOK_DURATION, clip_end_time) - clip_start_time

    # Intensity = overlap / clip_duration
    intensity = hook_overlap / clip_duration

    return max(0.0, min(1.0, intensity))


# ============================================================================
# 🎭 CLIMAX DETECTION - Audio Energy Analizi
# ============================================================================

def analyze_audio_energy(audio_file: str, segment_duration: float = 0.5) -> List[Dict]:
    """
    Audio dosyasını analiz et, her segment için enerji seviyesi hesapla

    Args:
        audio_file: Audio dosya yolu
        segment_duration: Her segment süresi (saniye)

    Returns:
        List of segments with energy levels:
        [
            {'start': 0.0, 'end': 0.5, 'energy': 0.85, 'is_climax': True},
            {'start': 0.5, 'end': 1.0, 'energy': 0.42, 'is_climax': False},
            ...
        ]
    """
    try:
        # FFmpeg ile audio stats al
        cmd = [
            'ffmpeg', '-i', audio_file,
            '-af', f'astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level:file=-',
            '-f', 'null', '-'
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, stderr=subprocess.PIPE)

        # RMS level'ları parse et
        rms_values = []
        for line in result.stderr.split('\n'):
            if 'lavfi.astats.Overall.RMS_level' in line:
                try:
                    value = float(line.split('=')[-1].strip())
                    rms_values.append(value)
                except ValueError:
                    pass

        if not rms_values:
            return []

        # Segment'lere böl
        segments = []
        for i, rms in enumerate(rms_values):
            start_time = i * segment_duration
            end_time = (i + 1) * segment_duration

            # RMS'i 0-1 range'e normalize et (-60dB to 0dB)
            normalized_energy = max(0.0, min(1.0, (rms + 60) / 60))

            segments.append({
                'start': start_time,
                'end': end_time,
                'energy': normalized_energy,
                'rms': rms
            })

        # Climax detection - enerji threshold
        if segments:
            energies = [s['energy'] for s in segments]
            mean_energy = sum(energies) / len(energies)
            std_energy = (sum((e - mean_energy) ** 2 for e in energies) / len(energies)) ** 0.5

            climax_threshold = mean_energy + (std_energy * 1.5)  # 1.5 std above mean

            for segment in segments:
                segment['is_climax'] = segment['energy'] > climax_threshold

        return segments

    except Exception as e:
        print(f"   ⚠️  Audio energy analysis failed: {e}")
        return []


def generate_climax_effects(intensity: float = 1.0) -> str:
    """
    Climax anları için özel efektler

    Args:
        intensity: Efekt yoğunluğu (0.0-1.0)

    Returns:
        FFmpeg filter string
    """
    if intensity < 0.3:
        return ""

    climax_filters = []

    # 1. 🔍 ZOOM PULSE - Dramatic zoom (basit, sabit zoom)
    zoom_amount = 1.0 + (0.15 * intensity)  # Max 1.15x zoom
    climax_filters.append(
        f"zoompan=z='{zoom_amount:.2f}':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080"
    )

    # 2. 📳 CROP - Static crop (shake expressions kaldırıldı)
    crop_amount = int(15 * intensity)  # Max 15 pixels
    climax_filters.append(
        f"crop=in_w-{crop_amount*2}:in_h-{crop_amount*2}:{crop_amount}:{crop_amount}"
    )
    climax_filters.append(
        "scale=1920:1080:flags=lanczos"
    )

    # 3. 🌟 HIGH CONTRAST - Dramatic look
    contrast = 1.0 + (0.3 * intensity)  # Max 1.3x
    saturation = 1.0 + (0.4 * intensity)  # Max 1.4x
    climax_filters.append(
        f"eq=contrast={contrast:.2f}:saturation={saturation:.2f}"
    )

    # 4. ✨ SHARPNESS - Keskinlik boost (complex filter yerine)
    if intensity > 0.6:
        climax_filters.append(
            "unsharp=5:5:1.0:5:5:0.0"  # Stronger sharpness
        )

    return ','.join(climax_filters)


def detect_climax_moments(audio_file: str, min_duration: float = 2.0) -> List[Tuple[float, float]]:
    """
    Audio'dan climax anlarını tespit et

    Args:
        audio_file: Audio dosya yolu
        min_duration: Minimum climax süresi (saniye)

    Returns:
        List of (start_time, end_time) tuples for climax moments
    """
    segments = analyze_audio_energy(audio_file)

    if not segments:
        return []

    # Ardışık climax segment'lerini birleştir
    climax_moments = []
    current_start = None
    current_end = None

    for segment in segments:
        if segment['is_climax']:
            if current_start is None:
                current_start = segment['start']
            current_end = segment['end']
        else:
            if current_start is not None:
                duration = current_end - current_start
                if duration >= min_duration:
                    climax_moments.append((current_start, current_end))
                current_start = None
                current_end = None

    # Son climax'i ekle
    if current_start is not None:
        duration = current_end - current_start
        if duration >= min_duration:
            climax_moments.append((current_start, current_end))

    return climax_moments


# ============================================================================
# ⏱️ PACING CONTROL - Hız Ayarı (Boring/Dramatic)
# ============================================================================

def calculate_pacing_factor(energy: float, mean_energy: float) -> float:
    """
    Audio energy'ye göre pacing factor hesapla

    Args:
        energy: Segment energy (0.0-1.0)
        mean_energy: Ortalama energy

    Returns:
        Speed factor (0.9-1.2)
        < 1.0: slow down (dramatic)
        > 1.0: speed up (boring)
    """
    if energy > mean_energy * 1.3:
        # Dramatic - yavaşlat (%90-95)
        factor = random.uniform(0.90, 0.95)
    elif energy < mean_energy * 0.7:
        # Boring - hızlandır (%110-120)
        factor = random.uniform(1.10, 1.20)
    else:
        # Normal - hafif ayar
        factor = random.uniform(0.98, 1.02)

    return factor


def apply_pacing_control(segments: List[Dict], target_duration: float) -> List[Dict]:
    """
    Segment'lere pacing control uygula

    Args:
        segments: Audio energy segments
        target_duration: Hedef video süresi

    Returns:
        Updated segments with pacing factors
    """
    if not segments:
        return segments

    # Mean energy hesapla
    energies = [s['energy'] for s in segments]
    mean_energy = sum(energies) / len(energies)

    # Her segment için pacing factor hesapla
    for segment in segments:
        segment['pacing_factor'] = calculate_pacing_factor(segment['energy'], mean_energy)

    # Toplam süreyi kontrol et
    total_duration = sum((s['end'] - s['start']) / s['pacing_factor'] for s in segments)

    # Duration'ı hedef süreye scale et
    scale = target_duration / total_duration if total_duration > 0 else 1.0

    for segment in segments:
        segment['pacing_factor'] *= scale
        # Limit: 0.85-1.25
        segment['pacing_factor'] = max(0.85, min(1.25, segment['pacing_factor']))

    return segments


def generate_pacing_filter(pacing_factor: float) -> str:
    """
    Pacing factor için FFmpeg filter oluştur

    Args:
        pacing_factor: Speed factor (0.85-1.25)

    Returns:
        FFmpeg filter string
    """
    if 0.98 <= pacing_factor <= 1.02:
        # Minimal değişiklik - filter gereksiz
        return ""

    # setpts filter - video speed adjustment
    pts_factor = 1.0 / pacing_factor

    # atempo filter - audio speed adjustment (0.5-2.0 range)
    atempo_factor = pacing_factor

    # atempo 0.5-2.0 arasında olmalı, multiple atempo ile chain yapılabilir
    if 0.5 <= atempo_factor <= 2.0:
        return f"setpts={pts_factor}*PTS,atempo={atempo_factor}"
    else:
        # Out of range - clamp
        atempo_factor = max(0.5, min(2.0, atempo_factor))
        return f"setpts={pts_factor}*PTS,atempo={atempo_factor}"


# ============================================================================
# 🎬 STORY FEATURES CONFIG
# ============================================================================

STORY_FEATURES_CONFIG = {
    'enabled': True,

    # Hook Optimizer
    'hook': {
        'enabled': True,
        'duration': 3.0,  # İlk 3 saniye
        'aggressive_effects': True,
        'effects': {
            'zoom': True,
            'shake': True,
            'bright_colors': True,
            'vignette': True,
            'glow': True,
        }
    },

    # Climax Detection
    'climax': {
        'enabled': True,
        'min_duration': 2.0,  # Min 2 saniye climax
        'threshold_std': 1.5,  # 1.5 std above mean
        'effects': {
            'zoom': True,
            'shake': True,
            'freeze_frame': False,  # Experimental
            'slow_motion': False,    # Experimental
            'glow': True,
        }
    },

    # Pacing Control
    'pacing': {
        'enabled': True,
        'boring_speedup': (1.10, 1.20),    # %110-120
        'dramatic_slowdown': (0.90, 0.95),  # %90-95
        'normal_variance': (0.98, 1.02),    # Minimal değişiklik
    }
}


def get_story_features_config():
    """Story features config'i döndür"""
    return STORY_FEATURES_CONFIG
