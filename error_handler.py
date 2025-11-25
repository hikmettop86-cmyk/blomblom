#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ERROR HANDLING UTILITY MODULE
==============================

Centralized error handling for render workflow
Provides retry logic, fallbacks, and graceful degradation

Author: Claude
Date: November 2025
Version: 1.0

FEATURES:
✅ Retry decorator with exponential backoff
✅ Fallback mechanisms
✅ User-friendly error messages
✅ Partial success tracking
✅ Recovery suggestions
✅ Error categorization
"""

import functools
import logging
import time
import traceback
from typing import Callable, Any, Optional, Dict, List
from enum import Enum

logger = logging.getLogger(__name__)


# ============================================================================
# ERROR CATEGORIES
# ============================================================================

class ErrorCategory(Enum):
    """Error categorization for better handling"""
    GPU_ERROR = "gpu_error"
    FILE_NOT_FOUND = "file_not_found"
    PERMISSION_DENIED = "permission_denied"
    FFMPEG_ERROR = "ffmpeg_error"
    AUDIO_ERROR = "audio_error"
    MEMORY_ERROR = "memory_error"
    NETWORK_ERROR = "network_error"
    CODEC_ERROR = "codec_error"
    TIMEOUT_ERROR = "timeout_error"
    UNKNOWN_ERROR = "unknown_error"


class ErrorSeverity(Enum):
    """Error severity levels"""
    CRITICAL = "critical"  # Stop everything
    HIGH = "high"  # Try fallback, then stop
    MEDIUM = "medium"  # Retry, then fallback
    LOW = "low"  # Log and continue


# ============================================================================
# USER-FRIENDLY ERROR MESSAGES
# ============================================================================

ERROR_MESSAGES = {
    ErrorCategory.GPU_ERROR: {
        'message': '🎮 GPU encoding başarısız, CPU encoding ile devam ediliyor...',
        'suggestion': '💡 GPU sürücülerinizi güncelleyin veya FFmpeg NVENC desteğini kontrol edin.',
        'recoverable': True,
    },
    ErrorCategory.FILE_NOT_FOUND: {
        'message': '📁 Dosya bulunamadı',
        'suggestion': '💡 Dosya yolunu kontrol edin ve dosyanın var olduğundan emin olun.',
        'recoverable': False,
    },
    ErrorCategory.PERMISSION_DENIED: {
        'message': '🔒 İzin hatası',
        'suggestion': '💡 Dosya/klasör izinlerini kontrol edin veya yönetici olarak çalıştırın.',
        'recoverable': False,
    },
    ErrorCategory.FFMPEG_ERROR: {
        'message': '🎬 FFmpeg komutu başarısız',
        'suggestion': '💡 FFmpeg kurulumunu kontrol edin. Komut: ffmpeg -version',
        'recoverable': True,
    },
    ErrorCategory.AUDIO_ERROR: {
        'message': '🎵 Ses işleme hatası',
        'suggestion': '💡 Ses dosyası formatını kontrol edin (MP3/WAV/AAC desteklenir).',
        'recoverable': True,
    },
    ErrorCategory.MEMORY_ERROR: {
        'message': '💾 Bellek yetersiz',
        'suggestion': '💡 Daha az video kullanın veya daha düşük çözünürük seçin.',
        'recoverable': True,
    },
    ErrorCategory.CODEC_ERROR: {
        'message': '🎞️ Codec hatası',
        'suggestion': '💡 Video/audio codec desteğini kontrol edin.',
        'recoverable': True,
    },
    ErrorCategory.TIMEOUT_ERROR: {
        'message': '⏱️ İşlem zaman aşımına uğradı',
        'suggestion': '💡 Daha küçük dosyalar kullanın veya timeout süresini artırın.',
        'recoverable': True,
    },
}


# ============================================================================
# RETRY DECORATOR
# ============================================================================

def retry_on_failure(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple = (Exception,),
    on_retry: Optional[Callable] = None
):
    """
    Retry decorator with exponential backoff

    Args:
        max_attempts: Maximum retry attempts
        delay: Initial delay in seconds
        backoff: Multiplier for delay (exponential backoff)
        exceptions: Tuple of exceptions to catch
        on_retry: Callback function on retry (receives attempt number)

    Example:
        @retry_on_failure(max_attempts=3, delay=2.0)
        def risky_operation():
            # code that might fail
            pass
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            last_exception = None

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e

                    if attempt == max_attempts:
                        logger.error(f"❌ {func.__name__} failed after {max_attempts} attempts")
                        logger.error(f"   Last error: {str(e)}")
                        raise

                    logger.warning(f"⚠️ {func.__name__} failed (attempt {attempt}/{max_attempts})")
                    logger.warning(f"   Error: {str(e)}")
                    logger.warning(f"   Retrying in {current_delay}s...")

                    if on_retry:
                        on_retry(attempt)

                    time.sleep(current_delay)
                    current_delay *= backoff

            raise last_exception

        return wrapper
    return decorator


# ============================================================================
# FALLBACK DECORATOR
# ============================================================================

def fallback_on_error(
    fallback_func: Callable,
    exceptions: tuple = (Exception,),
    log_fallback: bool = True
):
    """
    Fallback decorator - calls fallback function if main function fails

    Args:
        fallback_func: Function to call if main function fails
        exceptions: Tuple of exceptions to catch
        log_fallback: Whether to log fallback execution

    Example:
        def cpu_encode():
            # CPU encoding
            pass

        @fallback_on_error(fallback_func=cpu_encode)
        def gpu_encode():
            # GPU encoding (might fail)
            pass
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exceptions as e:
                if log_fallback:
                    logger.warning(f"⚠️ {func.__name__} failed, falling back to {fallback_func.__name__}")
                    logger.warning(f"   Error: {str(e)}")

                return fallback_func(*args, **kwargs)

        return wrapper
    return decorator


# ============================================================================
# GRACEFUL ERROR HANDLER
# ============================================================================

class GracefulErrorHandler:
    """
    Context manager for graceful error handling with user-friendly messages

    Example:
        with GracefulErrorHandler(ErrorCategory.GPU_ERROR, continue_on_error=True):
            # risky GPU operation
            pass
    """

    def __init__(
        self,
        category: ErrorCategory,
        continue_on_error: bool = False,
        context: Optional[str] = None
    ):
        self.category = category
        self.continue_on_error = continue_on_error
        self.context = context
        self.error_occurred = False
        self.error_message = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            return True

        self.error_occurred = True
        self.error_message = str(exc_val)

        # Get user-friendly message
        error_info = ERROR_MESSAGES.get(
            self.category,
            {
                'message': '❌ Bilinmeyen hata',
                'suggestion': '💡 Hata loglarını kontrol edin.',
                'recoverable': False,
            }
        )

        # Log error with context
        context_str = f" [{self.context}]" if self.context else ""
        logger.error(f"\n{'='*70}")
        logger.error(f"❌ HATA{context_str}: {error_info['message']}")
        logger.error(f"   Detay: {exc_val}")
        if error_info.get('suggestion'):
            logger.error(f"   {error_info['suggestion']}")
        logger.error(f"{'='*70}\n")

        # Print user-friendly message
        print(f"\n{'='*70}")
        print(f"❌ {error_info['message']}{context_str}")
        print(f"   Detay: {exc_val}")
        if error_info.get('suggestion'):
            print(f"\n{error_info['suggestion']}")
        print(f"{'='*70}\n")

        # Decide whether to continue
        if self.continue_on_error and error_info.get('recoverable', False):
            logger.info("ℹ️ Hata atlanıyor, işleme devam ediliyor...")
            return True  # Suppress exception

        return False  # Re-raise exception


# ============================================================================
# PARTIAL SUCCESS TRACKER
# ============================================================================

class PartialSuccessTracker:
    """
    Track partial success in batch operations

    Example:
        tracker = PartialSuccessTracker("Video Encoding")
        for video in videos:
            with tracker.track_item(video):
                encode_video(video)

        tracker.print_summary()
    """

    def __init__(self, operation_name: str):
        self.operation_name = operation_name
        self.total = 0
        self.successful = 0
        self.failed = 0
        self.failed_items: List[Dict[str, str]] = []

    def track_item(self, item_name: str):
        """Context manager for tracking individual items"""
        class ItemTracker:
            def __init__(self, parent, name):
                self.parent = parent
                self.name = name

            def __enter__(self):
                self.parent.total += 1
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                if exc_type is None:
                    self.parent.successful += 1
                    return True
                else:
                    self.parent.failed += 1
                    self.parent.failed_items.append({
                        'name': self.name,
                        'error': str(exc_val),
                    })
                    logger.warning(f"⚠️ {self.name} başarısız: {exc_val}")
                    return True  # Suppress exception, continue with next item

        return ItemTracker(self, item_name)

    def print_summary(self):
        """Print operation summary"""
        success_rate = (self.successful / self.total * 100) if self.total > 0 else 0

        print(f"\n{'='*70}")
        print(f"📊 {self.operation_name} ÖZET:")
        print(f"   ✅ Başarılı: {self.successful}/{self.total} ({success_rate:.1f}%)")
        print(f"   ❌ Başarısız: {self.failed}/{self.total}")

        if self.failed_items:
            print(f"\n   Başarısız öğeler:")
            for item in self.failed_items[:5]:  # Show first 5
                print(f"   - {item['name']}: {item['error'][:60]}...")

            if len(self.failed_items) > 5:
                print(f"   ... ve {len(self.failed_items) - 5} tane daha")

        print(f"{'='*70}\n")

        logger.info(f"📊 {self.operation_name}: {self.successful}/{self.total} başarılı")


# ============================================================================
# ERROR RECOVERY
# ============================================================================

def safe_file_operation(operation: Callable, error_category: ErrorCategory = ErrorCategory.FILE_NOT_FOUND):
    """
    Wrapper for safe file operations with better error messages

    Args:
        operation: File operation function
        error_category: Category of error to expect

    Returns:
        Result of operation or None if failed
    """
    try:
        return operation()
    except FileNotFoundError as e:
        with GracefulErrorHandler(ErrorCategory.FILE_NOT_FOUND, continue_on_error=True, context=str(e)):
            raise
        return None
    except PermissionError as e:
        with GracefulErrorHandler(ErrorCategory.PERMISSION_DENIED, continue_on_error=False, context=str(e)):
            raise
        return None
    except Exception as e:
        with GracefulErrorHandler(error_category, continue_on_error=True, context=str(e)):
            raise
        return None


# ============================================================================
# FFMPEG ERROR PARSER
# ============================================================================

def parse_ffmpeg_error(stderr: str) -> ErrorCategory:
    """
    Parse FFmpeg error output and categorize

    Args:
        stderr: FFmpeg stderr output

    Returns:
        ErrorCategory based on error message
    """
    stderr_lower = stderr.lower()

    # GPU/NVENC errors (including Invalid Level, InitializeEncoder failed, etc.)
    gpu_error_keywords = [
        'nvenc', 'cuda', 'gpu', 'invalid level', 'initializeencoder failed',
        'invalid param', 'h264_nvenc', 'hevc_nvenc', 'hardware encoder'
    ]
    if any(keyword in stderr_lower for keyword in gpu_error_keywords):
        return ErrorCategory.GPU_ERROR
    elif 'no such file' in stderr_lower or 'cannot find' in stderr_lower:
        return ErrorCategory.FILE_NOT_FOUND
    elif 'permission denied' in stderr_lower:
        return ErrorCategory.PERMISSION_DENIED
    elif 'codec' in stderr_lower or 'encoder' in stderr_lower:
        return ErrorCategory.CODEC_ERROR
    elif 'memory' in stderr_lower or 'out of memory' in stderr_lower:
        return ErrorCategory.MEMORY_ERROR
    elif 'timeout' in stderr_lower or 'timed out' in stderr_lower:
        return ErrorCategory.TIMEOUT_ERROR
    else:
        return ErrorCategory.FFMPEG_ERROR


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("🛡️ Error Handler Utility Module")
    print("="*70)
    print("This module should be imported by main.py")
    print("\nFeatures:")
    print("  ✅ Retry decorator with exponential backoff")
    print("  ✅ Fallback mechanisms")
    print("  ✅ Graceful error handling")
    print("  ✅ User-friendly error messages")
    print("  ✅ Partial success tracking")
    print("  ✅ FFmpeg error parsing")
