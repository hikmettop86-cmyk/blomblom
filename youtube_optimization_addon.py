#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YOUTUBE ULTRA PRO - ALGORİTMA OPTİMİZASYON MODÃœLÃœ

✅ YouTube Algoritması İçin İyileştirmeler:
   - Video Fingerprint Sistemi (Duplicate detection'dan kaçınma)
   - Gelişmiş Kalite Kontrol (Quality checks)
   - Metadata Randomizasyonu (Her video benzersiz)
   - Efekt Dengeleme (Profesyonel görünüm)
   - Upload Timing Önerileri

Bu modül main.py tarafından import edilir.
"""

import os
import sys
import subprocess
import random
import hashlib
import uuid
import json
import time
import shutil
from datetime import datetime, timedelta
from pathlib import Path
import logging

# ==================== FFMPEG PATH (RTX 50 serisi için güncel FFmpeg) ====================
FFMPEG_PATH = r"C:\ffmpeg\bin\ffmpeg.exe"
FFPROBE_PATH = r"C:\ffmpeg\bin\ffprobe.exe"

if not os.path.exists(FFMPEG_PATH):
    FFMPEG_PATH = shutil.which('ffmpeg') or 'ffmpeg'
    FFPROBE_PATH = shutil.which('ffprobe') or 'ffprobe'

# Logger setup
logger = logging.getLogger(__name__)


# ============================================================================
# 🔒 VIDEO FINGERPRINT SİSTEMİ
# ============================================================================

def generate_video_fingerprint(video_path):
    """
    Her video için benzersiz fingerprint oluştur

    YouTube duplicate detection'dan kaçınmak için her video
    farklı bir dijital parmak izine sahip olmalı.

    Args:
        video_path: Video dosya yolu

    Returns:
        dict: Fingerprint bilgileri
    """
    try:
        # Video hash hesapla (ilk 1MB)
        with open(video_path, 'rb') as f:
            # Sadece ilk 1MB'ı okuyarak hızlı hash
            first_mb = f.read(1024 * 1024)
            video_hash = hashlib.sha256(first_mb).hexdigest()

        # Rastgele salt ekle
        salt = random.randbytes(32).hex()

        # Benzersiz fingerprint
        unique_id = hashlib.sha256(
            (video_hash + salt + str(time.time())).encode()
        ).hexdigest()

        # Timestamp
        timestamp = datetime.now().isoformat()

        fingerprint_data = {
            'unique_id': unique_id,
            'video_hash': video_hash,
            'salt': salt,
            'timestamp': timestamp,
            'file_size': os.path.getsize(video_path),
            'random_seed': random.random(),
        }

        logger.info(f"✅ Video fingerprint oluşturuldu: {unique_id[:16]}...")

        return fingerprint_data

    except Exception as e:
        logger.error(f"❌ Fingerprint oluşturma hatası: {e}")
        return None


def save_fingerprint_database(fingerprint_data, output_dir):
    """
    Fingerprint veritabanına kaydet

    Bu veritabanı sayesinde hangi videoların ne zaman üretildiğini
    takip edebilir ve duplicate upload'ları engelleyebilirsiniz.
    """
    try:
        db_file = os.path.join(output_dir, '.fingerprints.json')

        # Mevcut veritabanını oku
        if os.path.exists(db_file):
            with open(db_file, 'r', encoding='utf-8') as f:
                database = json.load(f)
        else:
            database = {'videos': [], 'created': datetime.now().isoformat()}

        # Yeni fingerprint ekle
        database['videos'].append(fingerprint_data)
        database['last_updated'] = datetime.now().isoformat()

        # Kaydet
        with open(db_file, 'w', encoding='utf-8') as f:
            json.dump(database, f, indent=2, ensure_ascii=False)

        logger.info(f"✅ Fingerprint veritabanına kaydedildi")

    except Exception as e:
        logger.warning(f"⚠️  Fingerprint kaydetme hatası: {e}")


# ============================================================================
# 📊 GELİŞMİŞ KALİTE KONTROL SİSTEMİ
# ============================================================================

def check_video_duration(video_path, expected_duration=None, tolerance=2.0):
    """Video süresini kontrol et"""
    try:
        cmd = [
            FFPROBE_PATH, '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            video_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)

        if result.returncode != 0:
            return False

        actual_duration = float(result.stdout.strip())

        if expected_duration:
            diff = abs(actual_duration - expected_duration)
            if diff > tolerance:
                logger.warning(
                    f"⚠️  Süre farkı: {diff:.2f}s (beklenen: {expected_duration}s, gerçek: {actual_duration}s)")
                return False

        return True

    except Exception as e:
        logger.error(f"❌ Süre kontrolü hatası: {e}")
        return False


def check_video_integrity(video_path):
    """Video bütünlüğünü kontrol et (corrupted frames, errors)"""
    try:
        cmd = [
            FFMPEG_PATH, '-v', 'error',
            '-i', video_path,
            '-f', 'null', '-'
        ]
        # 30 dk video için 10 dk timeout (önceki: 30s)
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)

        # Hata mesajlarını kontrol et
        errors = result.stderr.strip()

        if 'error' in errors.lower() or 'corrupt' in errors.lower():
            logger.error(f"❌ Video bütünlüğü problemi: {errors[:200]}")
            return False

        return True

    except Exception as e:
        logger.error(f"❌ Bütünlük kontrolü hatası: {e}")
        return False


def check_audio_quality(video_path):
    """Ses kalitesini kontrol et (clipping, silence, sync)"""
    try:
        # Ses seviyesi kontrolü
        cmd = [
            FFMPEG_PATH, '-i', video_path,
            '-af', 'volumedetect',
            '-f', 'null', '-'
        ]
        # 30 dk video için 10 dk timeout (önceki: 20s)
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)

        output = result.stderr

        # Ses seviyelerini parse et
        if 'mean_volume' in output and 'max_volume' in output:
            # Çok sessiz veya çok yüksek ses kontrolü
            if 'mean_volume: -91' in output or 'mean_volume: -inf' in output:
                logger.warning("⚠️  Ses çok sessiz veya yok!")
                return False

            # Clipping kontrolü (0 dB üzeri)
            if 'max_volume: 0.0' in output:
                logger.warning("⚠️  Ses clipping tespit edildi!")
                return False

        return True

    except Exception as e:
        logger.error(f"❌ Ses kalitesi kontrolü hatası: {e}")
        return True  # Ses yoksa bile devam et


def check_bitrate_consistency(video_path, min_bitrate='8M'):
    """Video bitrate tutarlılığını kontrol et"""
    try:
        cmd = [
            FFPROBE_PATH, '-v', 'error',
            '-select_streams', 'v:0',
            '-show_entries', 'stream=bit_rate',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            video_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)

        if result.returncode != 0:
            return True  # Kontrol edilemezse geç

        bitrate_str = result.stdout.strip()
        if not bitrate_str or bitrate_str == 'N/A':
            return True

        bitrate = int(bitrate_str)
        min_bitrate_val = int(min_bitrate.replace('M', '000000').replace('k', '000'))

        if bitrate < min_bitrate_val:
            logger.warning(f"⚠️  Düşük bitrate: {bitrate / 1000000:.1f}Mbps (min: {min_bitrate})")
            return False

        return True

    except Exception as e:
        logger.error(f"❌ Bitrate kontrolü hatası: {e}")
        return True


def check_black_frames(video_path, max_duration=2.0):
    """Uzun süreli siyah frame kontrolü - 2 saniyeden uzun siyah bölümleri tespit et"""
    try:
        cmd = [
            FFMPEG_PATH, '-i', video_path,
            '-vf', f'blackdetect=d={max_duration}:pix_th=0.10',
            '-f', 'null', '-'
        ]
        # 30 dk video için 10 dk timeout (önceki: 30s)
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)

        output = result.stderr

        # Siyah frame uyarılarını say
        black_count = output.count('blackdetect')

        if black_count > 5:  # Eşik artırıldı: 3 → 5
            logger.warning(f"⚠️  Çok fazla siyah frame tespit edildi: {black_count}")
            return False

        return True

    except Exception as e:
        logger.error(f"❌ Siyah frame kontrolü hatası: {e}")
        return True


def post_render_quality_check(video_path, quality_config=None):
    """
    Render sonrası kapsamlı kalite kontrolü - PARALEL

    Args:
        video_path: Video dosya yolu
        quality_config: Kalite ayarları (config.py'den)

    Returns:
        tuple: (başarılı mı, kalite skoru, detaylar)
    """
    logger.info("\n🔍 KALİTE KONTROLÜ BAŞLIYOR (Paralel)...")

    if not quality_config:
        # Varsayılan ayarlar
        from config import ADVANCED_QUALITY_CHECKS
        quality_config = ADVANCED_QUALITY_CHECKS

    if not quality_config.get('enabled', True):
        logger.info("⚠️  Kalite kontrolü devre dışı")
        return True, 1.0, {}

    checks = {}

    # ⚡ QUICK MODE: Sadece dosya boyutu kontrolü (en hızlı)
    if quality_config.get('quick_mode', False):
        logger.info("⚡ QUICK MODE: Sadece dosya boyutu kontrolü")
        file_size_mb = os.path.getsize(video_path) / (1024 * 1024)
        checks['file_size'] = file_size_mb > 1.0
        quality_score = 1.0 if checks['file_size'] else 0.0
        logger.info(f"   💾 Dosya boyutu: {file_size_mb:.1f} MB - {'✅' if checks['file_size'] else '❌'}")
        return True, quality_score, checks

    # ✅ PARALEL KONTROLLER - ThreadPoolExecutor ile
    from concurrent.futures import ThreadPoolExecutor, as_completed

    tasks = {}

    with ThreadPoolExecutor(max_workers=4) as executor:
        # 1. Video bütünlüğü
        if quality_config.get('content_safety', {}).get('check_corrupted_frames', True):
            logger.info("   📹 Video bütünlüğü kontrol ediliyor...")
            tasks['integrity'] = executor.submit(check_video_integrity, video_path)
        else:
            checks['integrity'] = True

        # 2. Siyah frame kontrolü
        if quality_config.get('content_safety', {}).get('check_black_frames', True):
            logger.info("   ⬛ Siyah frame kontrolü...")
            max_black = quality_config.get('content_safety', {}).get('max_black_duration', 2.0)
            tasks['black_frames'] = executor.submit(check_black_frames, video_path, max_black)
        else:
            checks['black_frames'] = True

        # 3. Ses kalitesi
        if quality_config.get('audio_quality', {}).get('enabled', True):
            logger.info("   🔊 Ses kalitesi kontrol ediliyor...")
            tasks['audio'] = executor.submit(check_audio_quality, video_path)
        else:
            checks['audio'] = True

        # 4. Bitrate kontrolü
        if quality_config.get('encoding_quality', {}).get('check_bitrate_variance', True):
            logger.info("   📊 Bitrate kontrolü...")
            min_bitrate = quality_config.get('encoding_quality', {}).get('min_avg_bitrate', '8M')
            tasks['bitrate'] = executor.submit(check_bitrate_consistency, video_path, min_bitrate)
        else:
            checks['bitrate'] = True

        # Sonuçları topla
        for check_name, future in tasks.items():
            try:
                checks[check_name] = future.result(timeout=120)  # Max 2 dakika per check
            except Exception as e:
                logger.warning(f"⚠️ {check_name} kontrolü timeout/hata: {e}")
                checks[check_name] = True  # Hata durumunda geç

    # 5. Dosya boyutu kontrolü (anlık, paralel gerekmez)
    file_size_mb = os.path.getsize(video_path) / (1024 * 1024)
    checks['file_size'] = file_size_mb > 1.0  # En az 1MB

    # Kalite skoru hesapla
    passed_checks = sum(1 for v in checks.values() if v)
    total_checks = len(checks)
    quality_score = passed_checks / total_checks if total_checks > 0 else 1.0

    # Minimum kalite skoru kontrolü
    min_score = quality_config.get('overall_quality', {}).get('min_quality_score', 0.95)

    logger.info(f"\n📊 KALİTE RAPORU:")
    logger.info(f"   ✅ Başarılı kontroller: {passed_checks}/{total_checks}")
    logger.info(f"   📈 Kalite skoru: {quality_score:.2%}")
    logger.info(f"   💾 Dosya boyutu: {file_size_mb:.1f} MB")

    for check_name, result in checks.items():
        status = "✅" if result else "❌"
        logger.info(f"   {status} {check_name}: {'BAŞARILI' if result else 'BAŞARISIZ'}")

    # Sonuç
    if quality_score >= min_score:
        logger.info(f"\n✅ KALİTE KONTROLÜ BAŞARILI! (Skor: {quality_score:.2%})")
        success = True
    else:
        logger.warning(f"\n⚠️  KALİTE SKORU DÜŞÜK! (Skor: {quality_score:.2%}, Minimum: {min_score:.2%})")

        fail_on_low = quality_config.get('overall_quality', {}).get('fail_on_low_score', False)
        if fail_on_low:
            logger.error("❌ Video kalite kontrolünden geçemedi!")
            success = False
        else:
            logger.info("   ℹ️  Düşük skora rağmen devam ediliyor...")
            success = True

    return success, quality_score, checks


# ============================================================================
# 🏷️ GELİŞMİŞ METADATA RANDOMİZASYONU
# ============================================================================

def enhanced_metadata_injection(video_path, output_path, metadata_config=None):
    """
    YouTube için optimize edilmiş metadata ekleme

    Her video benzersiz metadata'ya sahip olmalı ki YouTube
    algoritması her videoyu farklı olarak tanısın.

    Args:
        video_path: Kaynak video
        output_path: Hedef video
        metadata_config: Metadata ayarları (config.py'den)

    Returns:
        bool: Başarılı mı
    """
    try:
        if not metadata_config:
            from config import METADATA_RANDOMIZATION
            metadata_config = METADATA_RANDOMIZATION

        if not metadata_config.get('enabled', True):
            # Metadata randomizasyonu kapalıysa, sadece kopyala
            import shutil
            shutil.copy2(video_path, output_path)
            return True

        # Metadata oluştur
        metadata = {}

        # 1. Oluşturma zamanı (1-48 saat önce)
        if metadata_config.get('creation_time', {}).get('enabled', True):
            variance_hours = metadata_config.get('creation_time', {}).get('variance_hours', (1, 48))
            hours_ago = random.randint(*variance_hours)
            creation_time = datetime.now() - timedelta(hours=hours_ago)
            metadata['creation_time'] = creation_time.strftime('%Y-%m-%d %H:%M:%S')

        # 2. Encoder tag (rastgele seç)
        if metadata_config.get('encoder_tags', {}).get('enabled', True):
            encoders = metadata_config.get('encoder_tags', {}).get('options', ['Lavf59.27.100'])
            metadata['encoder'] = random.choice(encoders)

        # 3. Handler name
        if metadata_config.get('handler_name', {}).get('enabled', True):
            handlers = metadata_config.get('handler_name', {}).get('options', ['VideoHandler'])
            metadata['handler_name'] = random.choice(handlers)

        # 4. Comment
        if metadata_config.get('comment', {}).get('enabled', True):
            comments = metadata_config.get('comment', {}).get('options', ['Optimized for platform delivery'])
            metadata['comment'] = random.choice(comments)

        # 5. Benzersiz ID
        if metadata_config.get('additional_metadata', {}).get('include_unique_id', True):
            metadata['unique_id'] = str(uuid.uuid4())

        # FFmpeg komutu oluştur
        cmd = [FFMPEG_PATH, '-i', video_path]

        # Metadata parametrelerini ekle
        for key, value in metadata.items():
            cmd.extend(['-metadata', f'{key}={value}'])

        # Codec kopyalama (re-encode yok)
        cmd.extend([
            '-c', 'copy',
            '-movflags', '+faststart',  # Web için optimize
            '-y',  # Üzerine yaz
            output_path
        ])

        logger.info("🏷️  Metadata enjekte ediliyor...")
        logger.debug(f"   Metadata: {metadata}")

        # Çalıştır
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 dakika
        )

        if result.returncode != 0:
            logger.error(f"❌ Metadata enjeksiyonu başarısız: {result.stderr[:500]}")
            # Hata olursa yine de kopyala
            import shutil
            shutil.copy2(video_path, output_path)
            return False

        logger.info("✅ Metadata başarıyla enjekte edildi!")
        return True

    except Exception as e:
        logger.error(f"❌ Metadata enjeksiyonu hatası: {e}")
        # Hata olursa orijinal dosyayı kopyala
        try:
            import shutil
            shutil.copy2(video_path, output_path)
        except:
            pass
        return False


# ============================================================================
# ⚖️ EFEKT DENGELEME SİSTEMİ
# ============================================================================

def apply_effect_balancing(selected_effects, effect_balancing_config=None):
    """
    Efekt dengeleme uygula

    Çok fazla efekt = YouTube algoritması şüpheli bulabilir
    Bu fonksiyon efektleri dengeler ve profesyonel görünüm sağlar

    Args:
        selected_effects: Seçili efektler listesi
        effect_balancing_config: Dengeleme ayarları

    Returns:
        list: Dengelenmiş efekt listesi
    """
    try:
        if not effect_balancing_config:
            from effects import EFFECT_BALANCING
            effect_balancing_config = EFFECT_BALANCING

        if not effect_balancing_config.get('enabled', True):
            return selected_effects

        logger.info("\n⚖️  EFEKT DENGELEME SİSTEMİ AKTİF")

        # 1. Maksimum efekt sayısı kontrolü
        max_effects = effect_balancing_config.get('max_effects_per_video', 5)
        if len(selected_effects) > max_effects:
            logger.info(f"   📊 Efekt sayısı azaltılıyor: {len(selected_effects)} → {max_effects}")

            # Öncelikli efektleri koru
            priority_effects = effect_balancing_config.get('priority_effects', [])

            # Öncelikli olanları ayır
            prioritized = [e for e in selected_effects if e in priority_effects]
            others = [e for e in selected_effects if e not in priority_effects]

            # Karışık seç
            random.shuffle(others)

            # Birleştir ve maksimuma kırp
            selected_effects = prioritized + others
            selected_effects = selected_effects[:max_effects]

        # 2. Kötü kombinasyonları engelle
        avoid_combos = effect_balancing_config.get('avoid_combinations', [])
        for combo in avoid_combos:
            if len(combo) == 2:
                if combo[0] in selected_effects and combo[1] in selected_effects:
                    # İkinci efekti kaldır
                    selected_effects.remove(combo[1])
                    logger.info(f"   ⚠️  Kötü kombinasyon engellendi: {combo[0]} + {combo[1]}")

        # 3. Efekt cooldown sistemi (aynı kategoriden çok fazla efekt olmasın)
        # Basit kategorizasyon
        heavy_effects = ['datamosh', 'vhs_advanced', 'ghost_trail', 'edge_detect', 'kaleidoscope']
        heavy_count = sum(1 for e in selected_effects if e in heavy_effects)

        if heavy_count > 1:
            logger.info(f"   ⚠️  Ağır efekt sayısı azaltılıyor: {heavy_count} → 1")
            # Sadece birini tut
            heavy_in_list = [e for e in selected_effects if e in heavy_effects]
            for effect in heavy_in_list[1:]:  # İlk hariç hepsini kaldır
                selected_effects.remove(effect)

        logger.info(f"   ✅ Dengelenmiş efekt sayısı: {len(selected_effects)}")
        logger.info(f"   📋 Efektler: {', '.join(selected_effects)}")

        return selected_effects

    except Exception as e:
        logger.error(f"❌ Efekt dengeleme hatası: {e}")
        return selected_effects


# ============================================================================
# 🕒 UPLOAD TIMING ÖNERİLERİ
# ============================================================================

def suggest_upload_time(upload_strategy=None):
    """
    En iyi upload zamanını öner

    YouTube algoritması için tutarlı ve optimize edilmiş
    yükleme zamanları önemlidir.

    Args:
        upload_strategy: Upload ayarları (config.py'den)

    Returns:
        dict: Önerilen upload zamanı bilgileri
    """
    try:
        if not upload_strategy:
            from config import UPLOAD_STRATEGY
            upload_strategy = UPLOAD_STRATEGY

        if not upload_strategy.get('enabled', True):
            return None

        now = datetime.now()

        # En iyi saatler
        best_times = upload_strategy.get('best_upload_times', {}).get('Turkey', ['09:00', '13:00', '18:00', '21:00'])

        # Kaçınılması gereken saatler
        avoid_times = upload_strategy.get('avoid_upload_times', {})
        late_night = avoid_times.get('late_night', ('00:00', '06:00'))

        # Bugün veya yarın?
        current_hour = now.hour

        # Gece saatleri mi?
        if int(late_night[0].split(':')[0]) <= current_hour < int(late_night[1].split(':')[0]):
            # Sabah bekle
            next_time = datetime.combine(now.date(), datetime.strptime(best_times[0], '%H:%M').time())
            if next_time <= now:
                next_time += timedelta(days=1)
        else:
            # En yakın iyi saati bul
            next_time = None
            for time_str in best_times:
                upload_time = datetime.combine(now.date(), datetime.strptime(time_str, '%H:%M').time())

                if upload_time > now:
                    next_time = upload_time
                    break

            if not next_time:
                # Bugün uygun saat yok, yarına bak
                next_time = datetime.combine(now.date() + timedelta(days=1),
                                             datetime.strptime(best_times[0], '%H:%M').time())

        # Hafta içi mi hafta sonu mu?
        weekday_preference = upload_strategy.get('best_upload_times', {}).get('weekday_preference', [])
        while next_time.strftime('%a') not in weekday_preference and weekday_preference:
            next_time += timedelta(days=1)

        wait_time = next_time - now
        hours = int(wait_time.total_seconds() // 3600)
        minutes = int((wait_time.total_seconds() % 3600) // 60)

        suggestion = {
            'suggested_time': next_time.strftime('%Y-%m-%d %H:%M'),
            'wait_hours': hours,
            'wait_minutes': minutes,
            'day_of_week': next_time.strftime('%A'),
            'is_optimal': next_time.strftime('%H:%M') in best_times,
        }

        logger.info(f"\n🕒 UPLOAD ZAMANI ÖNERİSİ:")
        logger.info(f"   📅 Önerilen zaman: {suggestion['suggested_time']}")
        logger.info(f"   ⏰ Bekleme süresi: {hours} saat {minutes} dakika")
        logger.info(f"   📆 Gün: {suggestion['day_of_week']}")
        logger.info(f"   {'✅ Optimal zaman!' if suggestion['is_optimal'] else 'ℹ️  İyi zaman'}")

        return suggestion

    except Exception as e:
        logger.error(f"❌ Upload zamanı önerisi hatası: {e}")
        return None


# ============================================================================
# 📈 TOPLU OPTİMİZASYON FONKSİYONU
# ============================================================================

def apply_youtube_optimizations(video_path, output_dir, config_overrides=None):
    """
    Tüm YouTube optimizasyonlarını uygula

    Bu fonksiyon:
    1. Kalite kontrolü yapar
    2. Metadata randomize eder
    3. Fingerprint oluşturur
    4. Upload zamanı önerir

    Args:
        video_path: Video dosya yolu
        output_dir: Çıktı klasörü
        config_overrides: Ayar overrideleri (opsiyonel)

    Returns:
        dict: Optimizasyon sonuçları
    """
    logger.info("\n" + "=" * 100)
    logger.info("🚀 YOUTUBE ALGORİTMA OPTİMİZASYONLARI BAŞLIYOR")
    logger.info("=" * 100)

    results = {
        'success': True,
        'quality_check': None,
        'fingerprint': None,
        'metadata_injection': None,
        'upload_suggestion': None,
    }

    try:
        # 1. Kalite Kontrolü
        logger.info("\n📊 AŞAMA 1: KALİTE KONTROLÜ")
        quality_passed, quality_score, quality_details = post_render_quality_check(video_path)
        results['quality_check'] = {
            'passed': quality_passed,
            'score': quality_score,
            'details': quality_details
        }

        if not quality_passed:
            logger.error("❌ Kalite kontrolü başarısız! İşlem durduruluyor.")
            results['success'] = False
            return results

        # 2. Metadata Randomizasyonu
        logger.info("\n🏷️  AŞAMA 2: METADATA RANDOMİZASYONU")
        temp_output = video_path + '.optimized.mp4'
        metadata_success = enhanced_metadata_injection(video_path, temp_output)
        results['metadata_injection'] = metadata_success

        if metadata_success and os.path.exists(temp_output):
            # Orijinali değiştir
            import shutil
            shutil.move(temp_output, video_path)
            logger.info("✅ Metadata başarıyla güncellendi")

        # 3. Fingerprint Oluşturma
        logger.info("\n🔒 AŞAMA 3: VIDEO FİNGERPRİNT")
        fingerprint = generate_video_fingerprint(video_path)
        results['fingerprint'] = fingerprint

        if fingerprint:
            save_fingerprint_database(fingerprint, output_dir)

        # 4. Upload Zamanı Önerisi
        logger.info("\n🕒 AŞAMA 4: UPLOAD ZAMANI ÖNERİSİ")
        upload_suggestion = suggest_upload_time()
        results['upload_suggestion'] = upload_suggestion

        logger.info("\n" + "=" * 100)
        logger.info("✅ TÃœM OPTİMİZASYONLAR TAMAMLANDI!")
        logger.info("=" * 100)

        return results

    except Exception as e:
        logger.error(f"❌ Optimizasyon hatası: {e}")
        results['success'] = False
        return results


# ============================================================================
# 📝 OPTİMİZASYON RAPORU
# ============================================================================

def generate_optimization_report(results, output_path):
    """
    Optimizasyon sonuçlarını rapor olarak kaydet
    """
    try:
        report = {
            'timestamp': datetime.now().isoformat(),
            'video_path': output_path,
            'optimizations': results,
            'summary': {
                'quality_passed': results.get('quality_check', {}).get('passed', False),
                'quality_score': results.get('quality_check', {}).get('score', 0),
                'fingerprint_created': results.get('fingerprint') is not None,
                'metadata_injected': results.get('metadata_injection', False),
                'upload_time_suggested': results.get('upload_suggestion') is not None,
            }
        }

        report_file = output_path + '.optimization_report.json'
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        logger.info(f"📝 Optimizasyon raporu kaydedildi: {report_file}")

    except Exception as e:
        logger.warning(f"⚠️  Rapor oluşturma hatası: {e}")


if __name__ == "__main__":
    print("Bu modül doğrudan çalıştırılamaz. main.py tarafından import edilmelidir.")