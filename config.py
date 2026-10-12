"""
LinguaBridge - Configuration Module
Handles environment variables, secrets, API constants, and supported language mappings.
"""

import os
from typing import Dict, Optional
from dotenv import load_dotenv

# Load local .env if present
load_dotenv()


def get_api_key() -> Optional[str]:
    """
    Retrieve Google Cloud Translation API key from environment variables
    or Streamlit secrets (if running in a Streamlit context).
    """
    # 1. Check direct environment variable
    api_key = os.getenv("GOOGLE_TRANSLATE_API_KEY")
    if api_key and api_key.strip():
        return api_key.strip()

    # 2. Check Streamlit secrets if available
    try:
        import streamlit as st
        if hasattr(st, "secrets") and "GOOGLE_TRANSLATE_API_KEY" in st.secrets:
            key = st.secrets["GOOGLE_TRANSLATE_API_KEY"]
            if key and key.strip():
                return key.strip()
    except Exception:
        pass

    return None


def get_service_account_path() -> Optional[str]:
    """Retrieve Google Cloud Service Account credentials JSON path if configured."""
    creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if creds_path and os.path.exists(creds_path.strip()):
        return creds_path.strip()
    return None


# Google Cloud Translation v2 REST Endpoint
GOOGLE_TRANSLATE_API_URL = "https://translation.googleapis.com/language/translate/v2"
GOOGLE_DETECT_API_URL = "https://translation.googleapis.com/language/translate/v2/detect"
GOOGLE_FREE_TRANSLATE_URL = "https://translate.googleapis.com/translate_a/single"

# Provider options
PROVIDER_GOOGLE_CLOUD = "google_cloud"
PROVIDER_GOOGLE_FREE = "google_free"
DEFAULT_PROVIDER = os.getenv("TRANSLATION_PROVIDER", PROVIDER_GOOGLE_CLOUD)

# Network & input constraints
DEFAULT_TIMEOUT_SECONDS = int(os.getenv("TRANSLATION_TIMEOUT_SECONDS", "10"))
MAX_INPUT_CHARACTERS = 5000
AUTO_DETECT_CODE = "auto"
AUTO_DETECT_LABEL = "Detect Language (Auto)"

# Comprehensive list of languages supported by Google Cloud Translation API
# Includes all explicitly requested languages (Tamil, Hindi, Telugu, Kannada, Malayalam, etc.)
SUPPORTED_LANGUAGES: Dict[str, str] = {
    "en": "English",
    "ta": "Tamil (தமிழ்)",
    "hi": "Hindi (हिन्दी)",
    "te": "Telugu (తెలుగు)",
    "kn": "Kannada (ಕನ್ನಡ)",
    "ml": "Malayalam (മലയാളം)",
    "mr": "Marathi (मराठी)",
    "bn": "Bengali (বাংলা)",
    "gu": "Gujarati (ગુજરાતી)",
    "pa": "Punjabi (ਪੰਜਾਬੀ)",
    "ur": "Urdu (اردو)",
    "fr": "French (Français)",
    "de": "German (Deutsch)",
    "es": "Spanish (Español)",
    "ja": "Japanese (日本語)",
    "zh-CN": "Chinese Simplified (简体中文)",
    "zh-TW": "Chinese Traditional (繁體中文)",
    "ar": "Arabic (العربية)",
    "ru": "Russian (Русский)",
    "pt": "Portuguese (Português)",
    "it": "Italian (Italiano)",
    "ko": "Korean (한국어)",
    "nl": "Dutch (Nederlands)",
    "tr": "Turkish (Türkçe)",
    "pl": "Polish (Polski)",
    "vi": "Vietnamese (Tiếng Việt)",
    "th": "Thai (ไทย)",
    "id": "Indonesian (Bahasa Indonesia)",
    "el": "Greek (Ελληνικά)",
    "he": "Hebrew (עברית)",
    "sv": "Swedish (Svenska)",
    "da": "Danish (Dansk)",
    "fi": "Finnish (Suomi)",
    "no": "Norwegian (Norsk)",
}


def get_language_name(code: str) -> str:
    """Return the human-readable display name for a given language code."""
    if code == AUTO_DETECT_CODE:
        return AUTO_DETECT_LABEL
    return SUPPORTED_LANGUAGES.get(code, f"Unknown ({code})")


def is_supported_language(code: str) -> bool:
    """Check if a language code is in the supported languages dictionary."""
    if code == AUTO_DETECT_CODE:
        return True
    return code in SUPPORTED_LANGUAGES
