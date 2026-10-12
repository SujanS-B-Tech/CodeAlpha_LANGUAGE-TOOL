"""
Unit Test Suite for LinguaBridge Translation Service
Uses unittest.mock to simulate Google Cloud API responses without requiring live API keys.
"""

import json
from unittest.mock import MagicMock, patch

import pytest
import requests

from config import AUTO_DETECT_CODE, MAX_INPUT_CHARACTERS
from translator import (
    ApiError,
    AuthenticationError,
    DetectionResult,
    MissingConfigurationError,
    NetworkError,
    QuotaExceededError,
    TranslationResult,
    TranslationService,
    ValidationError,
)

FAKE_API_KEY = "AIzaSyTestMockKeyForLinguaBridge123456"


@pytest.fixture
def service():
    """Returns a configured TranslationService instance with a mock API key."""
    return TranslationService(api_key=FAKE_API_KEY, timeout=5)


@pytest.fixture
def unconfigured_service():
    """Returns an unconfigured TranslationService instance without an API key."""
    return TranslationService(api_key=None, timeout=5)


# ==============================================================================
# 1. Validation Tests
# ==============================================================================

def test_empty_input_validation(service):
    """Test that translating an empty string raises ValidationError."""
    with pytest.raises(ValidationError, match="Input cannot be empty"):
        service.translate(text="", target_lang="es", source_lang="en")


def test_whitespace_input_validation(service):
    """Test that translating whitespace-only text raises ValidationError."""
    with pytest.raises(ValidationError, match="Input cannot be empty"):
        service.translate(text="   \n\t  ", target_lang="es", source_lang="en")


def test_exceeding_max_characters(service):
    """Test that input exceeding the maximum character limit raises ValidationError."""
    long_text = "A" * (MAX_INPUT_CHARACTERS + 10)
    with pytest.raises(ValidationError, match="exceeds the maximum allowed limit"):
        service.translate(text=long_text, target_lang="es", source_lang="en")


def test_identical_source_and_target_languages(service):
    """Test that setting identical source and target languages raises ValidationError."""
    with pytest.raises(ValidationError, match="Source and target languages are both set to"):
        service.translate(text="Hello world", target_lang="en", source_lang="en")


def test_identical_languages_allowed_if_auto(service):
    """Test that source='auto' does not raise identical language error even if target is English."""
    # Should not raise ValidationError during validation phase
    with patch.object(service.session, "post") as mock_post:
        mock_response = MagicMock(status_code=200)
        mock_response.json.return_value = {
            "data": {
                "translations": [
                    {
                        "translatedText": "Hello world",
                        "detectedSourceLanguage": "fr",
                    }
                ]
            }
        }
        mock_post.return_value = mock_response

        res = service.translate(text="Bonjour le monde", target_lang="en", source_lang=AUTO_DETECT_CODE)
        assert isinstance(res, TranslationResult)
        assert res.translated_text == "Hello world"
        assert res.detected_language == "fr"


def test_unsupported_target_language(service):
    """Test that an invalid target language code raises ValidationError."""
    with pytest.raises(ValidationError, match="Invalid target language"):
        service.translate(text="Hello", target_lang="xyz_invalid", source_lang="en")


def test_unsupported_source_language(service):
    """Test that an invalid source language code raises ValidationError."""
    with pytest.raises(ValidationError, match="Invalid source language"):
        service.translate(text="Hello", target_lang="fr", source_lang="abc_invalid")


# ==============================================================================
# 2. Configuration & Authentication Tests
# ==============================================================================

def test_missing_api_key(unconfigured_service):
    """Test that attempting to translate without API credentials raises MissingConfigurationError."""
    with pytest.raises(MissingConfigurationError, match="Google Cloud Translation API is not configured"):
        unconfigured_service.translate(text="Hello world", target_lang="es", source_lang="en")


def test_auth_error_401(service):
    """Test that HTTP 401 returns an AuthenticationError."""
    with patch.object(service.session, "post") as mock_post:
        mock_response = MagicMock(status_code=401)
        mock_response.json.return_value = {
            "error": {"code": 401, "message": "API key not valid. Please pass a valid API key."}
        }
        mock_post.return_value = mock_response

        with pytest.raises(AuthenticationError, match="Authentication Failed"):
            service.translate(text="Hello", target_lang="es", source_lang="en")


def test_auth_error_400_invalid_key(service):
    """Test that HTTP 400 with 'API key not valid' returns an AuthenticationError."""
    with patch.object(service.session, "post") as mock_post:
        mock_response = MagicMock(status_code=400)
        mock_response.json.return_value = {
            "error": {"code": 400, "message": "API key not valid. Please pass a valid API key."}
        }
        mock_post.return_value = mock_response

        with pytest.raises(AuthenticationError, match="Authentication Failed"):
            service.translate(text="Hello", target_lang="es", source_lang="en")


def test_free_provider_translation_success():
    """Test translation using the alternative Free Google Translate provider."""
    from config import PROVIDER_GOOGLE_FREE
    free_service = TranslationService(provider=PROVIDER_GOOGLE_FREE, timeout=5)
    with patch.object(free_service.session, "get") as mock_get:
        mock_response = MagicMock(status_code=200)
        mock_response.json.return_value = [
            [["Hola mundo", "Hello world", None, None]],
            None,
            "en"
        ]
        mock_get.return_value = mock_response

        res = free_service.translate(text="Hello world", target_lang="es", source_lang="auto")
        assert isinstance(res, TranslationResult)
        assert res.translated_text == "Hola mundo"
        assert res.detected_language == "en"


# ==============================================================================
# 3. Successful Translation & Data Integrity Tests
# ==============================================================================

def test_successful_translation_explicit_source(service):
    """Test a successful translation response with explicit source language."""
    with patch.object(service.session, "post") as mock_post:
        mock_response = MagicMock(status_code=200)
        mock_response.json.return_value = {
            "data": {
                "translations": [
                    {
                        "translatedText": "வணக்கம் உலகம்",
                    }
                ]
            }
        }
        mock_post.return_value = mock_response

        result = service.translate(text="Hello world", target_lang="ta", source_lang="en")

        assert isinstance(result, TranslationResult)
        assert result.translated_text == "வணக்கம் உலகம்"
        assert result.source_language == "en"
        assert result.target_language == "ta"
        assert result.character_count == len("Hello world")

        # Verify call payload
        call_kwargs = mock_post.call_args[1]
        assert call_kwargs["params"]["key"] == FAKE_API_KEY
        assert call_kwargs["json"]["q"] == "Hello world"
        assert call_kwargs["json"]["source"] == "en"
        assert call_kwargs["json"]["target"] == "ta"


def test_html_entity_unescaping(service):
    """Test that HTML escaped characters returned by Google API are decoded properly."""
    with patch.object(service.session, "post") as mock_post:
        mock_response = MagicMock(status_code=200)
        mock_response.json.return_value = {
            "data": {
                "translations": [
                    {
                        "translatedText": "Don&#39;t worry &amp; &quot;smile&quot;!",
                    }
                ]
            }
        }
        mock_post.return_value = mock_response

        result = service.translate(text="Don't worry & 'smile'!", target_lang="es", source_lang="en")

        # Google Cloud returns &#39; and &quot; which must be decoded
        assert result.translated_text == "Don't worry & \"smile\"!"


# ==============================================================================
# 4. Rate Limits & Network Error Tests
# ==============================================================================

def test_quota_exceeded_429(service):
    """Test that HTTP 429 returns QuotaExceededError."""
    with patch.object(service.session, "post") as mock_post:
        mock_response = MagicMock(status_code=429)
        mock_response.json.return_value = {
            "error": {"code": 429, "message": "Resource has been exhausted (e.g. check quota)."}
        }
        mock_post.return_value = mock_response

        with pytest.raises(QuotaExceededError, match="Quota Exceeded"):
            service.translate(text="Hello", target_lang="es", source_lang="en")


def test_network_timeout(service):
    """Test that network timeout raises NetworkError."""
    with patch.object(service.session, "post", side_effect=requests.exceptions.Timeout("Connection timed out")):
        with pytest.raises(NetworkError, match="timed out"):
            service.translate(text="Hello", target_lang="es", source_lang="en")


def test_network_connection_error(service):
    """Test that connection failure raises NetworkError."""
    with patch.object(service.session, "post", side_effect=requests.exceptions.ConnectionError("Failed to connect")):
        with pytest.raises(NetworkError, match="Could not establish a connection"):
            service.translate(text="Hello", target_lang="es", source_lang="en")


def test_malformed_json_response(service):
    """Test that non-JSON response from API raises ApiError."""
    with patch.object(service.session, "post") as mock_post:
        mock_response = MagicMock(status_code=200)
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_post.return_value = mock_response

        with pytest.raises(ApiError, match="malformed JSON"):
            service.translate(text="Hello", target_lang="es", source_lang="en")


def test_empty_translations_data(service):
    """Test that an empty translations list in API response raises ApiError."""
    with patch.object(service.session, "post") as mock_post:
        mock_response = MagicMock(status_code=200)
        mock_response.json.return_value = {"data": {"translations": []}}
        mock_post.return_value = mock_response

        with pytest.raises(ApiError, match="No translations returned"):
            service.translate(text="Hello", target_lang="es", source_lang="en")


# ==============================================================================
# 5. Language Detection Endpoint Tests
# ==============================================================================

def test_detect_language_success(service):
    """Test successful detection through the detect_language method."""
    with patch.object(service.session, "post") as mock_post:
        mock_response = MagicMock(status_code=200)
        mock_response.json.return_value = {
            "data": {
                "detections": [
                    [
                        {"language": "hi", "confidence": 0.98}
                    ]
                ]
            }
        }
        mock_post.return_value = mock_response

        res = service.detect_language("नमस्ते")
        assert isinstance(res, DetectionResult)
        assert res.language_code == "hi"
        assert res.confidence == 0.98


def test_detect_language_empty_input(service):
    """Test that detecting language on empty text raises ValidationError."""
    with pytest.raises(ValidationError, match="Cannot detect language for empty text"):
        service.detect_language("")


# ==============================================================================
# 6. Text-to-Speech Helper Tests
# ==============================================================================

def test_text_to_speech_empty_text():
    """Test that TTS returns None when provided empty text."""
    res = TranslationService.generate_speech("", lang="en")
    assert res is None


def test_text_to_speech_generation():
    """Test that TTS audio bytes are generated successfully."""
    dummy_bytes = b"ID3\x03\x00\x00\x00mock_audio_stream"
    with patch("gtts.gTTS") as mock_gtts_cls:
        mock_instance = MagicMock()
        def write_fake(fp):
            fp.write(dummy_bytes)
        mock_instance.write_to_fp.side_effect = write_fake
        mock_gtts_cls.return_value = mock_instance

        audio = TranslationService.generate_speech("Hello world", lang="en")
        assert audio == dummy_bytes
