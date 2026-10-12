"""
LinguaBridge - Translation Service Module
Encapsulates Google Cloud Translation API communication, validation,
error classification, HTML entity unescaping, and text-to-speech audio generation.
"""

import html
import io
import logging
from dataclasses import dataclass
from typing import Optional

import requests
from config import (
    AUTO_DETECT_CODE,
    DEFAULT_TIMEOUT_SECONDS,
    GOOGLE_DETECT_API_URL,
    GOOGLE_FREE_TRANSLATE_URL,
    GOOGLE_TRANSLATE_API_URL,
    MAX_INPUT_CHARACTERS,
    PROVIDER_GOOGLE_CLOUD,
    PROVIDER_GOOGLE_FREE,
    SUPPORTED_LANGUAGES,
    get_api_key,
    is_supported_language,
)

logger = logging.getLogger("linguabridge.translator")


# ==============================================================================
# Custom Exception Hierarchy
# ==============================================================================

class LinguaBridgeError(Exception):
    """Base exception for all LinguaBridge application errors."""
    pass


class ValidationError(LinguaBridgeError):
    """Raised when user input or language selection fails validation."""
    pass


class MissingConfigurationError(LinguaBridgeError):
    """Raised when the Google Cloud Translation API key or credentials are not found."""
    pass


class AuthenticationError(LinguaBridgeError):
    """Raised when the API key is invalid, unauthorized, or billing is not active."""
    pass


class QuotaExceededError(LinguaBridgeError):
    """Raised when API rate limits or quota boundaries are exceeded."""
    pass


class NetworkError(LinguaBridgeError):
    """Raised when network failures, timeouts, or DNS resolution issues occur."""
    pass


class ApiError(LinguaBridgeError):
    """Raised when Google Cloud Translation API returns an unexpected error."""
    pass


# ==============================================================================
# Data Transfer Objects
# ==============================================================================

@dataclass
class TranslationResult:
    """Represents a successful translation output."""
    translated_text: str
    source_language: str
    target_language: str
    detected_language: Optional[str] = None
    character_count: int = 0


@dataclass
class DetectionResult:
    """Represents a language detection response."""
    language_code: str
    confidence: float


# ==============================================================================
# Translation Service
# ==============================================================================

class TranslationService:
    """
    Production-grade translation service wrapping the official Google Cloud
    Translation v2 REST API with complete lifecycle error handling.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        provider: str = PROVIDER_GOOGLE_CLOUD,
        timeout: int = DEFAULT_TIMEOUT_SECONDS,
        session: Optional[requests.Session] = None,
    ):
        self.api_key = api_key if api_key is not None else get_api_key()
        self.provider = provider
        self.timeout = timeout
        self.session = session or requests.Session()

    def is_configured(self) -> bool:
        """Returns True if the current provider is ready to translate."""
        if self.provider == PROVIDER_GOOGLE_FREE:
            return True
        return bool(self.api_key and self.api_key.strip())

    def validate_request(
        self,
        text: str,
        target_lang: str,
        source_lang: Optional[str] = AUTO_DETECT_CODE,
    ) -> None:
        """
        Validates text length, emptiness, and language compatibility.
        Raises ValidationError if any condition is violated.
        """
        if not text or not text.strip():
            raise ValidationError("Please enter text to translate. Input cannot be empty.")

        if len(text) > MAX_INPUT_CHARACTERS:
            raise ValidationError(
                f"Input text exceeds the maximum allowed limit of {MAX_INPUT_CHARACTERS:,} characters "
                f"(current length: {len(text):,} characters)."
            )

        if not target_lang or not is_supported_language(target_lang) or target_lang == AUTO_DETECT_CODE:
            raise ValidationError(
                f"Invalid target language '{target_lang}'. Please choose a valid target language."
            )

        if source_lang and source_lang != AUTO_DETECT_CODE:
            if not is_supported_language(source_lang):
                raise ValidationError(
                    f"Invalid source language '{source_lang}'. Please choose a supported language."
                )
            if source_lang == target_lang:
                raise ValidationError(
                    f"Source and target languages are both set to '{SUPPORTED_LANGUAGES.get(target_lang, target_lang)}'. "
                    "Please select different languages to translate."
                )

    def translate(
        self,
        text: str,
        target_lang: str,
        source_lang: Optional[str] = AUTO_DETECT_CODE,
    ) -> TranslationResult:
        """
        Executes a real translation via Google Cloud Translation API v2.

        :param text: Text to translate
        :param target_lang: ISO 639-1 code of target language
        :param source_lang: ISO 639-1 code of source language, or 'auto' for auto-detection
        :return: TranslationResult with translated text and metadata
        :raises: ValidationError, MissingConfigurationError, AuthenticationError,
                 QuotaExceededError, NetworkError, ApiError
        """
        self.validate_request(text=text, target_lang=target_lang, source_lang=source_lang)

        if self.provider == PROVIDER_GOOGLE_FREE:
            return self._translate_free(text=text, target_lang=target_lang, source_lang=source_lang)

        if not self.is_configured():
            raise MissingConfigurationError(
                "Google Cloud Translation API is not configured. "
                "Please configure GOOGLE_TRANSLATE_API_KEY in your .env file or Streamlit secrets."
            )

        url = GOOGLE_TRANSLATE_API_URL
        params = {"key": self.api_key}
        payload = {
            "q": text,
            "target": target_lang,
            "format": "text",
        }

        if source_lang and source_lang != AUTO_DETECT_CODE:
            payload["source"] = source_lang

        try:
            response = self.session.post(
                url,
                params=params,
                json=payload,
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout as exc:
            raise NetworkError(
                f"Translation request timed out after {self.timeout}s. "
                "Please check your internet connection and try again."
            ) from exc
        except requests.exceptions.ConnectionError as exc:
            raise NetworkError(
                "Could not establish a connection to Google Cloud Translation API. "
                "Please check your internet connection."
            ) from exc
        except requests.exceptions.RequestException as exc:
            raise NetworkError(f"Network error during translation request: {exc}") from exc

        return self._parse_translation_response(
            response=response,
            original_text=text,
            source_lang=source_lang,
            target_lang=target_lang,
        )

    def detect_language(self, text: str) -> DetectionResult:
        """
        Detects the language of the provided text using Google Cloud Translation API.
        """
        if not text or not text.strip():
            raise ValidationError("Cannot detect language for empty text.")

        if not self.is_configured():
            raise MissingConfigurationError("API key required for language detection.")

        url = GOOGLE_DETECT_API_URL
        params = {"key": self.api_key}
        payload = {"q": text}

        try:
            response = self.session.post(
                url,
                params=params,
                json=payload,
                timeout=self.timeout,
            )
        except requests.exceptions.RequestException as exc:
            raise NetworkError(f"Network error during language detection: {exc}") from exc

        if response.status_code == 200:
            try:
                data = response.json()
                detections = data.get("data", {}).get("detections", [])
                if detections and len(detections[0]) > 0:
                    top_detection = detections[0][0]
                    return DetectionResult(
                        language_code=top_detection.get("language", "unknown"),
                        confidence=float(top_detection.get("confidence", 0.0)),
                    )
            except Exception as exc:
                raise ApiError(f"Failed to parse language detection response: {exc}") from exc

        self._handle_api_error_status(response)
        raise ApiError(f"Language detection failed with status {response.status_code}.")

    def _parse_translation_response(
        self,
        response: requests.Response,
        original_text: str,
        source_lang: Optional[str],
        target_lang: str,
    ) -> TranslationResult:
        """Parses HTTP response from Google Cloud Translation API and returns TranslationResult."""
        if response.status_code == 200:
            try:
                data = response.json()
            except ValueError as exc:
                raise ApiError("Invalid response received from translation API: malformed JSON.") from exc

            translations = data.get("data", {}).get("translations", [])
            if not translations:
                raise ApiError("No translations returned by Google Cloud Translation API.")

            item = translations[0]
            raw_text = item.get("translatedText", "")
            # Ensure any HTML entities (e.g. &quot;, &#39;, &amp;) returned by the API are decoded
            cleaned_text = html.unescape(raw_text)
            detected_lang = item.get("detectedSourceLanguage")

            return TranslationResult(
                translated_text=cleaned_text,
                source_language=source_lang or AUTO_DETECT_CODE,
                target_language=target_lang,
                detected_language=detected_lang,
                character_count=len(original_text),
            )

        self._handle_api_error_status(response)
        raise ApiError(f"API request failed with status code {response.status_code}.")

    def _handle_api_error_status(self, response: requests.Response) -> None:
        """Parses error responses and maps HTTP status codes to custom exceptions."""
        error_message = f"HTTP {response.status_code}"
        try:
            error_json = response.json()
            if "error" in error_json:
                error_message = error_json["error"].get("message", error_message)
        except Exception:
            error_message = response.text or error_message

        if response.status_code in (401, 403) or (response.status_code == 400 and "API key not valid" in error_message):
            raise AuthenticationError(
                f"Google Cloud Translation Authentication Failed ({response.status_code}): {error_message}. "
                "Please verify that your Google Cloud API key is valid and the Cloud Translation API is enabled on your project, "
                "or switch to the Free Translation Engine option."
            )
        elif response.status_code == 429:
            raise QuotaExceededError(
                f"Google Cloud Translation Quota Exceeded ({response.status_code}): {error_message}. "
                "You have exceeded your API usage limit or rate limit. Please try again later."
            )
        else:
            raise ApiError(f"Google Cloud Translation Error ({response.status_code}): {error_message}")

    def _translate_free(
        self,
        text: str,
        target_lang: str,
        source_lang: Optional[str] = AUTO_DETECT_CODE,
    ) -> TranslationResult:
        """
        Translates text via Google Translate public engine (Alternative Provider).
        Requires no API key, performs real-world translation.
        """
        sl = "auto" if not source_lang or source_lang == AUTO_DETECT_CODE else source_lang
        params = {
            "client": "gtx",
            "sl": sl,
            "tl": target_lang,
            "dt": "t",
            "q": text,
        }
        try:
            resp = self.session.get(GOOGLE_FREE_TRANSLATE_URL, params=params, timeout=self.timeout)
            if resp.status_code != 200:
                raise ApiError(f"Alternative translation provider returned HTTP {resp.status_code}.")
            data = resp.json()
            translated_segments = []
            if isinstance(data, list) and len(data) > 0 and isinstance(data[0], list):
                for segment in data[0]:
                    if segment and len(segment) > 0 and segment[0]:
                        translated_segments.append(segment[0])
            translated_text = "".join(translated_segments)
            detected_lang = None
            if len(data) > 2 and isinstance(data[2], str):
                detected_lang = data[2]

            return TranslationResult(
                translated_text=html.unescape(translated_text),
                source_language=source_lang or AUTO_DETECT_CODE,
                target_language=target_lang,
                detected_language=detected_lang,
                character_count=len(text),
            )
        except requests.exceptions.Timeout as exc:
            raise NetworkError(f"Translation request timed out after {self.timeout}s.") from exc
        except requests.exceptions.RequestException as exc:
            raise NetworkError(f"Network error during free translation: {exc}") from exc
        except Exception as exc:
            raise ApiError(f"Failed to process translation response: {exc}") from exc

    @staticmethod
    def generate_speech(text: str, lang: str) -> Optional[bytes]:
        """
        Generates text-to-speech audio bytes using gTTS.
        Returns audio/mp3 bytes if successful, or None if gTTS fails or language is unsupported.
        """
        if not text or not text.strip():
            return None

        # Clean simple code (e.g. 'zh-CN' -> 'zh-CN', 'en' -> 'en')
        tts_lang = lang.split("-")[0] if "-" in lang and lang not in ("zh-CN", "zh-TW") else lang

        try:
            from gtts import gTTS
            tts = gTTS(text=text.strip(), lang=tts_lang, slow=False)
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            return fp.read()
        except Exception as exc:
            logger.warning(f"Text-to-speech generation failed for lang '{lang}': {exc}")
            return None
