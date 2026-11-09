# LinguaBridge — Language Translation Tool

[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B.svg)](https://streamlit.io/)
[![Google Cloud Translation API](https://img.shields.io/badge/Google%20Cloud-Translation%20v2-4285F4.svg)](https://cloud.google.com/translate)
[![Tests Passing](https://img.shields.io/badge/Tests-22%2F22%20Passing%20(100%25)-success.svg)](https://docs.pytest.org/)
[![Internship](https://img.shields.io/badge/CodeAlpha-Internship%20Task-orange.svg)](https://codealpha.tech/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**LinguaBridge** is a professional, full-featured language translation web application built with Python and Streamlit. Developed as part of the **CodeAlpha Internship**, LinguaBridge bridges linguistic gaps across **34+ languages**—with dedicated support for **10 major Indian regional languages** and top global tongues.

The application features a **dual translation architecture**: it works completely **out of the box with zero API key setup** using its Free Translation Engine, and seamlessly connects to the official enterprise **Google Cloud Translation API (v2 REST API)** whenever high-volume enterprise credentials are provided.

---

## 🌟 Key Features

1. **Dual Translation Engine Architecture**:
   - ⚡ **Google Translate Engine (Free Alternative)**: Active out-of-the-box with **no API key or billing required**. Ideal for demonstrations, development, and testing.
   - 🏢 **Google Cloud Translation API v2 (Official Enterprise)**: Enterprise-grade neural machine translation powered by Google Cloud when an API key is supplied.
2. **34+ Supported Languages**:
   - **10 Indian Regional Languages**: Tamil (`ta`), Hindi (`hi`), Telugu (`te`), Kannada (`kn`), Malayalam (`ml`), Marathi (`mr`), Bengali (`bn`), Gujarati (`gu`), Punjabi (`pa`), Urdu (`ur`).
   - **24 Global Languages**: English (`en`), French (`fr`), German (`de`), Spanish (`es`), Japanese (`ja`), Chinese Simplified (`zh-CN`), Chinese Traditional (`zh-TW`), Arabic (`ar`), Russian (`ru`), Portuguese (`pt`), Italian (`it`), Korean (`ko`), Dutch (`nl`), Turkish (`tr`), Polish (`pl`), Vietnamese (`vi`), Thai (`th`), Indonesian (`id`), Greek (`el`), Hebrew (`he`), Swedish (`sv`), Danish (`da`), Finnish (`fi`), Norwegian (`no`).
3. **Automatic Language Detection**:
   - Select **Detect Language (Auto)** (`auto`) to automatically identify the source text language with high confidence.
4. **Side-by-Side Dual-Panel Interface**:
   - Modern, responsive card layout with dedicated source and target panels for intuitive side-by-side reading and editing.
5. **Language & Content Swap (`⇄`)**:
   - One-click swap button reverses source and target languages and rotates the translated output back into the input box for effortless back-translation verification.
6. **Live Character & Word Counters**:
   - Real-time word counter and character counter with a strict **5,000-character ceiling** and visual warning styling.
7. **One-Click Clipboard Copy**:
   - Streamlit popover integration with one-click code-block copy functionality for rapid text export.
8. **Text-to-Speech (TTS) Pronunciation**:
   - Built-in audio playback powered by Google Text-to-Speech (`gTTS`), enabling users to listen to the translated pronunciation directly inside the UI.
9. **Zero Data Loss on Failure**:
   - Preserves user input text intact if an API error, rate limit, or network disconnection occurs.
10. **Defensive Error Handling & HTML Entity Decoding**:
    - Automatically decodes escaped HTML entities (such as `&#39;`, `&quot;`, `&amp;`) into clean human-readable punctuation.
    - Custom exception hierarchy with clear, actionable user alerts for validation errors, authentication failures, quota limits, and timeouts.
11. **Comprehensive Automated Test Suite**:
    - 22 mocked `pytest` unit tests covering 100% of failure modes, validation constraints, and audio synthesis without consuming API credits.

---

## 🏗 Project Architecture

```
CodeAlpha_LANGUAGE-TOOL/
│
├── .env.example             # Configuration and API key template
├── .gitignore               # Strict exclusion of virtualenvs, secrets, caches
├── LICENSE                  # MIT License
├── requirements.txt         # Production and testing dependencies
├── config.py                # Environment loader, constants, and language mappings
├── translator.py            # Translation engine, validation, API requests, and TTS
├── app.py                   # Streamlit frontend with modern dual-panel UI
├── start.bat                # Windows Command Prompt one-click launcher
├── start.ps1                # Windows PowerShell one-click launcher
│
├── tests/
│   ├── __init__.py
│   └── test_translator.py   # Complete 22-test unit test suite
│
└── README.md                # Complete documentation and setup guide
```

### Module Responsibilities

| File | Purpose |
|---|---|
| [`config.py`](config.py) | Securely loads environment variables and Streamlit secrets. Ignores template placeholder keys and defines the 34 supported language mappings and limits. |
| [`translator.py`](translator.py) | Core engine implementing the `TranslationService` class, custom exception hierarchy (`ValidationError`, `AuthenticationError`, `QuotaExceededError`, `NetworkError`, `ApiError`), Google Cloud v2 REST calls, free fallback engine, and `gTTS` speech generation. |
| [`app.py`](app.py) | Streamlit web application with modern CSS styling, dual-panel layout, character counter, swap logic, TTS player, copy popover, and engine switchers. |
| [`tests/test_translator.py`](tests/test_translator.py) | Unit test suite validating input rules, error classifications, free provider, HTML decoding, and TTS generation with zero live API calls. |
| [`start.bat`](start.bat) | Windows batch file to bootstrap `.venv`, install requirements, and run the app. |
| [`start.ps1`](start.ps1) | PowerShell script to bootstrap `.venv`, install dependencies, and launch Streamlit. |

---

## 🚀 Quick Start Guide

### Method 1: One-Click Batch Launcher (Windows CMD / File Explorer)
Double-click **`start.bat`** in the project folder, or run:
```cmd
start.bat
```
This script automatically:
1. Verifies Python 3.9+ is installed.
2. Creates the virtual environment (`.venv`) if not present.
3. Installs dependencies from `requirements.txt`.
4. Initializes `.env` from `.env.example` if needed.
5. Launches LinguaBridge in your default web browser at `http://localhost:8501`.

---

### Method 2: One-Click PowerShell Launcher
Right-click **`start.ps1`** and select **Run with PowerShell**, or execute:
```powershell
.\start.ps1
```

---

### Method 3: Manual Terminal Setup

#### Step 1: Open Terminal and Navigate to Directory
```powershell
cd "d:\PROJECTS\Projects\CODEALPHAINTERN\LANGUAGE TOOL"
```

#### Step 2: Create a Virtual Environment
```powershell
python -m venv .venv
```

#### Step 3: Activate the Virtual Environment
- **Windows (PowerShell)**:
  ```powershell
  .venv\Scripts\Activate.ps1
  ```
  *(If execution policies block script activation, run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`)*
- **Windows (Command Prompt)**:
  ```cmd
  .venv\Scripts\activate.bat
  ```
- **macOS / Linux**:
  ```bash
  source .venv/bin/activate
  ```

#### Step 4: Install Dependencies
```powershell
pip install -r requirements.txt
```

#### Step 5: Run Automated Unit Tests
```powershell
pytest -v
```

#### Step 6: Launch the Web Application
```powershell
streamlit run app.py
```
Open your browser at **`http://localhost:8501`**.

---

## 🌐 Translation Engines & Providers

LinguaBridge features two operational modes selectable via the UI radio button:

1. **⚡ Google Translate Engine (Free Alternative — No API Key Required)**
   - **Active by default** when no Google Cloud API key is configured.
   - Sends real-time translations via Google's neural models without requiring an API key, billing account, or credit card.
   - Ideal for internship demonstrations, student reviews, and quick testing.

2. **🏢 Google Cloud Translation API v2 (Official Enterprise — Requires API Key)**
   - Connects to Google Cloud's official `https://translation.googleapis.com/language/translate/v2` REST API.
   - Built for enterprise rate limits, strict uptime SLAs, and project quotas.

---

## 🔑 Google Cloud API Key Configuration (Optional)

If you wish to test with an official Google Cloud Translation API key:

### Option A: Via `.env` File (Recommended)
1. Copy `.env.example` to `.env`:
   ```powershell
   Copy-Item .env.example .env
   ```
2. Open `.env` and set your key:
   ```env
   GOOGLE_TRANSLATE_API_KEY=AIzaSyYourActualGoogleCloudApiKeyHere
   ```

### Option B: Direct In-App Input
Switch the provider to **Google Cloud Translation API** in the web app UI, expand the configuration drawer, and paste your API key directly for that session.

### Option C: Streamlit Secrets (For Cloud Deployment)
Create `.streamlit/secrets.toml`:
```toml
GOOGLE_TRANSLATE_API_KEY = "AIzaSyYourActualGoogleCloudApiKeyHere"
```

---

## 🧪 Automated Testing Details

LinguaBridge includes a unit test suite built with `pytest` and `unittest.mock`. **No real API requests are dispatched during testing**, preventing unintended charges, network reliance, or quota consumption.

To run all 22 tests:
```powershell
pytest -v
```

### Complete Test Catalog (22 / 22 Tests)

| # | Test Function | Purpose / Scenario Covered |
|---|---|---|
| 1 | `test_empty_input_validation` | Verifies empty string input raises `ValidationError`. |
| 2 | `test_whitespace_input_validation` | Verifies whitespace-only text raises `ValidationError`. |
| 3 | `test_exceeding_max_characters` | Verifies inputs > 5,000 characters raise `ValidationError`. |
| 4 | `test_identical_source_and_target_languages` | Verifies selecting identical source and target raises `ValidationError`. |
| 5 | `test_identical_languages_allowed_if_auto` | Verifies `auto` does not raise identical language error even if detected matches target. |
| 6 | `test_unsupported_target_language` | Verifies invalid target language codes are rejected. |
| 7 | `test_unsupported_source_language` | Verifies invalid source language codes are rejected. |
| 8 | `test_missing_api_key` | Verifies unconfigured cloud service raises `MissingConfigurationError`. |
| 9 | `test_auth_error_401` | Verifies HTTP 401 raises `AuthenticationError`. |
| 10 | `test_auth_error_400_invalid_key` | Verifies HTTP 400 with invalid key message raises `AuthenticationError`. |
| 11 | `test_free_provider_translation_success` | Validates complete translation flow using the free alternative provider. |
| 12 | `test_successful_translation_explicit_source` | Validates successful translation, payload structure, and metadata mapping. |
| 13 | `test_html_entity_unescaping` | Verifies HTML entities (`&#39;`, `&quot;`, `&amp;`) are properly unescaped. |
| 14 | `test_quota_exceeded_429` | Verifies HTTP 429 quota exhaustion raises `QuotaExceededError`. |
| 15 | `test_network_timeout` | Verifies network request timeouts raise `NetworkError`. |
| 16 | `test_network_connection_error` | Verifies connection drops raise `NetworkError`. |
| 17 | `test_malformed_json_response` | Verifies non-JSON responses from API raise `ApiError`. |
| 18 | `test_empty_translations_data` | Verifies empty translation arrays raise `ApiError`. |
| 19 | `test_detect_language_success` | Validates language detection endpoint and confidence score parsing. |
| 20 | `test_detect_language_empty_input` | Validates detection rejects empty text. |
| 21 | `test_text_to_speech_empty_text` | Verifies TTS gracefully returns `None` for empty inputs. |
| 22 | `test_text_to_speech_generation` | Validates TTS synthesis and binary MP3 byte generation. |

---

## 🗺 Supported Languages Reference

| Code | Language | Native / Script | Group |
|---|---|---|---|
| `auto` | Auto-Detection | ✨ Auto-Detect | System |
| `ta` | Tamil | தமிழ் | Indian Regional |
| `hi` | Hindi | हिन्दी | Indian Regional |
| `te` | Telugu | తెలుగు | Indian Regional |
| `kn` | Kannada | ಕನ್ನಡ | Indian Regional |
| `ml` | Malayalam | മലയാളം | Indian Regional |
| `mr` | Marathi | मराठी | Indian Regional |
| `bn` | Bengali | বাংলা | Indian Regional |
| `gu` | Gujarati | ગુજરાતી | Indian Regional |
| `pa` | Punjabi | ਪੰਜਾਬੀ | Indian Regional |
| `ur` | Urdu | اردو | Indian Regional |
| `en` | English | English | Global |
| `es` | Spanish | Español | Global |
| `fr` | French | Français | Global |
| `de` | German | Deutsch | Global |
| `ja` | Japanese | 日本語 | Global |
| `zh-CN` | Chinese (Simplified) | 简体中文 | Global |
| `zh-TW` | Chinese (Traditional) | 繁體中文 | Global |
| `ar` | Arabic | العربية | Global |
| `ru` | Russian | Русский | Global |
| `pt` | Portuguese | Português | Global |
| `it` | Italian | Italiano | Global |
| `ko` | Korean | 한국어 | Global |
| `nl` | Dutch | Nederlands | Global |
| `tr` | Turkish | Türkçe | Global |
| `pl` | Polish | Polski | Global |
| `vi` | Vietnamese | Tiếng Việt | Global |
| `th` | Thai | ไทย | Global |
| `id` | Indonesian | Bahasa Indonesia | Global |
| `el` | Greek | Ελληνικά | Global |
| `he` | Hebrew | עברית | Global |
| `sv` | Swedish | Svenska | Global |
| `da` | Danish | Dansk | Global |
| `fi` | Finnish | Suomi | Global |
| `no` | Norwegian | Norsk | Global |

---

## 🛡 Security & Best Practices

- **Zero Secret Leakage**: No API keys or credentials are hardcoded into source files.
- **Placeholder Key Detection**: Automatically identifies unconfigured placeholder values (`your_google_cloud_api_key_here`) and gracefully falls back to the Free Engine.
- **Comprehensive `.gitignore`**: Protects `.env`, `.venv`, credentials files, and cache directories from being committed to version control.
- **Preserved User State**: Any network or API failure leaves the user's source text untouched in session state to prevent lost work.

---

## 👨‍💻 Author & Acknowledgements

- **Developer**: Sujan S
- **Repository**: [CodeAlpha_LANGUAGE-TOOL](https://github.com/SujanS-B-Tech/CodeAlpha_LANGUAGE-TOOL)
- **Program**: CodeAlpha Internship Program

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
