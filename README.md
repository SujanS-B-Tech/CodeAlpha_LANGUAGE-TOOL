# LinguaBridge — Language Translation Tool

[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B.svg)](https://streamlit.io/)
[![Google Cloud Translation API](https://img.shields.io/badge/Google%20Cloud-Translation%20v2-4285F4.svg)](https://cloud.google.com/translate)
[![Tests Passing](https://img.shields.io/badge/Tests-100%25%20Passing-success.svg)](https://docs.pytest.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**LinguaBridge** is a professional, full-featured language translation web application built with Python and Streamlit, connecting directly to the official **Google Cloud Translation API (v2 REST API)**. Engineered for high reliability, clean architecture, and intuitive user experience, LinguaBridge bridges linguistic gaps across 30+ languages, including major Indian regional languages and global tongues.

---

## 🌟 Key Features

1. **Official Google Cloud Integration**: Real-time translation powered by Google Cloud's neural machine translation service.
2. **30+ Supported Languages**:
   - **Indian Regional**: Tamil (`ta`), Hindi (`hi`), Telugu (`te`), Kannada (`kn`), Malayalam (`ml`), Marathi (`mr`), Bengali (`bn`), Gujarati (`gu`), Punjabi (`pa`), Urdu (`ur`).
   - **Global Languages**: English (`en`), French (`fr`), German (`de`), Spanish (`es`), Japanese (`ja`), Chinese Simplified (`zh-CN`), Chinese Traditional (`zh-TW`), Arabic (`ar`), Russian (`ru`), Portuguese (`pt`), Italian (`it`), Korean (`ko`), and more.
3. **Automatic Language Detection**: Detects source language automatically when "Detect Language (Auto)" is selected.
4. **Side-by-Side Dual-Panel Layout**: Modern side-by-side interface for intuitive reading, comparison, and review.
5. **Language & Content Swap (`⇄`)**: One-click swap button that reverses source/target languages and shifts translated output back into the input field for reverse translation checks.
6. **Live Character & Word Counters**: Real-time character counter (with 5,000 character limit enforcement) and word counter.
7. **One-Click Clipboard Copy**: Built-in copy mechanism for fast text export.
8. **Text-to-Speech (TTS) Audio**: Pronunciation playback powered by Google Text-to-Speech (`gTTS`) directly inside the UI.
9. **Zero Data Loss on Failure**: Preserves user input text intact if an API error, rate limit, or network disconnection occurs.
10. **Defensive Error Handling**: Clear, user-friendly alert callouts for:
    - Empty or whitespace input
    - Identical source and target language selection
    - Missing API credentials with step-by-step setup assistance
    - Invalid API keys (HTTP 401/403)
    - Quota and rate limit exhaustion (HTTP 429)
    - Network connectivity timeouts
11. **HTML Entity Decoding**: Automatically unescapes HTML entities returned by the API (such as `&#39;` and `&quot;`) into clean punctuation.
12. **Comprehensive Automated Test Suite**: Mocked pytest test suite covering 100% of failure modes and validations without incurring API costs.

---

## 🏗 Project Architecture

```
language-translation-tool/
│
├── .env.example             # Configuration and API key template
├── .gitignore               # Strict exclusion of virtualenvs, secrets, caches
├── requirements.txt         # Production and testing dependencies
├── config.py                # Environment loader, constants, and language mappings
├── translator.py            # Translation engine, validation, API requests, and TTS
├── app.py                   # Streamlit frontend with modern UI components
│
├── tests/
│   ├── __init__.py
│   └── test_translator.py   # Unit test suite with mocked Google Cloud API responses
│
└── README.md                # Complete documentation and setup guide
```

### Module Responsibilities

| File | Purpose |
|---|---|
| `config.py` | Securely reads environment variables and Streamlit secrets. Maintains supported language mapping dictionaries and constants. |
| `translator.py` | Encapsulates the `TranslationService` class, custom exception hierarchy (`ValidationError`, `AuthenticationError`, `QuotaExceededError`, `NetworkError`), Google Cloud REST calls, payload validation, and `gTTS` audio synthesis. |
| `app.py` | Implements the responsive Streamlit frontend, interactive sidebar/expander setup, dual-panel layout, character counter, swap logic, and audio playback. |
| `tests/test_translator.py` | Pytest suite validating input constraints, language detection, error classification, and HTML decoding with zero live API calls. |

---

## 🚀 Quick Start Guide

### Method 1: One-Click Launch (Easiest)
Simply double-click **`start.bat`** in the project folder, or run:
```cmd
start.bat
```
This script automatically:
1. Checks for Python 3.9+.
2. Creates the virtual environment (`.venv`) if not present.
3. Activates the environment and installs all dependencies from `requirements.txt`.
4. Initializes `.env` from `.env.example` if needed.
5. Launches the LinguaBridge Streamlit application in your default browser.

---

### Method 2: Manual PowerShell Setup
Follow these exact steps if you prefer running manually:

#### Step 1: Open PowerShell and Navigate to the Directory
```powershell
cd "d:\PROJECTS\Projects\CODEALPHAINTERN\LANGUAGE TOOL"
```

### Step 2: Create a Virtual Environment
```powershell
python -m venv .venv
```

### Step 3: Activate the Virtual Environment
```powershell
.venv\Scripts\Activate.ps1
```
*(If PowerShell execution policies block script activation, run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` and try again).*

### Step 4: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 5: Run Automated Unit Tests
Verify all validation rules and mocked API error handlers pass:
```powershell
pytest -v tests/
```

### Step 6: Launch the Streamlit Web Application
```powershell
streamlit run app.py
```
Streamlit will start local server hosting the application at:
```
http://localhost:8501
```

---

## 🌐 Translation Engines & Providers

LinguaBridge supports two operational modes:

1. **⚡ Google Translate Engine (Free Alternative — No API Key Required)**
   - Enabled by default when no Google Cloud credentials are configured.
   - Dispatches real-time translations through Google Translate's neural models without requiring an API key or credit card.
   - Ideal for instant testing, internship evaluation, and demonstrations.

2. **🏢 Google Cloud Translation API v2 (Official Enterprise — Requires API Key)**
   - Uses the official Google Cloud Translation API v2 endpoint.
   - Enterprise security and quota controls with Google Cloud projects.

---

## 🔑 Google Cloud Translation API Configuration

When using the **Official Enterprise** provider, configure credentials via either:

### Option A: Via `.env` File (Recommended)
1. In the project root, copy `.env.example` to `.env`:
   ```powershell
   Copy-Item .env.example .env
   ```
2. Open `.env` and paste your Google Cloud API Key:
   ```env
   GOOGLE_TRANSLATE_API_KEY=AIzaSyYourActualGoogleCloudApiKeyHere
   ```

### Option B: Direct In-App Session Key
If you do not wish to edit files, you can launch the app, select **Google Cloud Translation API**, and paste your API key directly into the configuration input box inside the web UI.

### Option C: Streamlit Secrets (For Streamlit Community Cloud)
Create `.streamlit/secrets.toml`:
```toml
GOOGLE_TRANSLATE_API_KEY = "AIzaSyYourActualGoogleCloudApiKeyHere"
```

---

## 🛠 How to Obtain a Google Cloud Translation API Key

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (e.g., `linguabridge-translator`).
3. Ensure **Billing** is enabled for your Google Cloud account (Google provides a free tier with 500,000 free translation characters per month).
4. Navigate to **APIs & Services > Library**.
5. Search for **Cloud Translation API** and click **Enable**.
6. Navigate to **APIs & Services > Credentials**.
7. Click **+ Create Credentials > API Key**.
8. Copy your new API key and paste it into `.env`.
9. *(Optional but Recommended)* Click **Edit API Key** and restrict usage strictly to the **Cloud Translation API**.

---

## 🧪 Automated Testing Details

LinguaBridge includes a unit test suite built with `pytest` and `unittest.mock`. **No real API requests are dispatched during testing**, preventing any charges or quota consumption.

To execute tests:
```powershell
pytest -v tests/
```

### Test Scenarios Covered
- `test_empty_input_validation`: Verifies empty input raises `ValidationError`.
- `test_whitespace_input_validation`: Verifies whitespace input raises `ValidationError`.
- `test_exceeding_max_characters`: Verifies inputs > 5,000 characters are rejected.
- `test_identical_source_and_target_languages`: Ensures selecting the same source and target produces an alert.
- `test_identical_languages_allowed_if_auto`: Ensures "Auto-detect" works even if detected language matches target.
- `test_unsupported_target_language`: Verifies non-existent target language codes are rejected.
- `test_unsupported_source_language`: Verifies non-existent source language codes are rejected.
- `test_missing_api_key`: Verifies that translation without credentials raises `MissingConfigurationError`.
- `test_auth_error_401`: Verifies HTTP 401 raises `AuthenticationError`.
- `test_auth_error_403_billing`: Verifies HTTP 403 API disabled/billing error raises `AuthenticationError`.
- `test_successful_translation_explicit_source`: Validates complete translation flow and payload integrity.
- `test_html_entity_unescaping`: Verifies HTML entities like `&#39;` and `&quot;` are properly decoded.
- `test_quota_exceeded_429`: Verifies HTTP 429 quota exhaustion raises `QuotaExceededError`.
- `test_network_timeout`: Verifies request timeouts raise `NetworkError`.
- `test_network_connection_error`: Verifies connection drops raise `NetworkError`.
- `test_malformed_json_response`: Verifies invalid JSON payloads raise `ApiError`.
- `test_empty_translations_data`: Verifies missing translation lists raise `ApiError`.
- `test_detect_language_success`: Validates language detection endpoint and confidence score.
- `test_detect_language_empty_input`: Validates detection rejects empty text.
- `test_text_to_speech_generation`: Validates text-to-speech audio byte stream synthesis.

---

## 🛡 Security and Best Practices

- **Zero Hardcoded Secrets**: No API keys or tokens are stored in source code.
- **Strict `.gitignore`**: Protects `.env`, credentials JSON files, virtual environments, and caches from being committed to Git.
- **Fail-Safe Preserved State**: User input text is retained across failed requests, preventing accidental work loss.
- **Clean REST Abstraction**: Direct REST integration through `requests` allows complete transparency, precise status code checking, and lightweight execution without bulky dependencies.

---

## 📄 License
This project is open-source under the [MIT License](LICENSE).
