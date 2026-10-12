"""
LinguaBridge — Language Translation Tool
A professional, modern web application for real-time multilingual translation
powered by Python, Streamlit, and Google Cloud Translation API.
"""

import streamlit as st
import streamlit.components.v1 as components
from config import (
    AUTO_DETECT_CODE,
    AUTO_DETECT_LABEL,
    MAX_INPUT_CHARACTERS,
    PROVIDER_GOOGLE_CLOUD,
    PROVIDER_GOOGLE_FREE,
    SUPPORTED_LANGUAGES,
    get_api_key,
    get_language_name,
)
from translator import (
    AuthenticationError,
    LinguaBridgeError,
    MissingConfigurationError,
    NetworkError,
    QuotaExceededError,
    TranslationService,
    ValidationError,
)

# ==============================================================================
# Page Configuration & Styling
# ==============================================================================

st.set_page_config(
    page_title="LinguaBridge — Language Translation Tool",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom Styling for a polished corporate / modern interface
CUSTOM_CSS = """
<style>
    /* Global font & smooth transitions */
    html, body, [class*="css"] {
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    }
    
    /* Header Card */
    .header-container {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        padding: 28px 32px;
        border-radius: 14px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(30, 58, 138, 0.15);
    }
    .header-title {
        font-size: 2.1rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .header-subtitle {
        font-size: 1.05rem;
        opacity: 0.92;
        margin-top: 6px;
        font-weight: 400;
    }
    .badge-status {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 10px;
    }
    .badge-configured {
        background-color: #10b981;
        color: white;
    }
    .badge-warning {
        background-color: #f59e0b;
        color: #111827;
    }

    /* Panel Card Styling */
    .card-panel {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        margin-bottom: 16px;
    }
    
    /* Dark mode support */
    @media (prefers-color-scheme: dark) {
        .card-panel {
            background: #1f2937;
            border-color: #374151;
        }
    }
    
    .panel-label {
        font-size: 0.95rem;
        font-weight: 600;
        color: #4b5563;
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    @media (prefers-color-scheme: dark) {
        .panel-label {
            color: #9ca3af;
        }
    }

    /* Translated output container */
    .output-box {
        background-color: #f8fafc;
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        padding: 16px;
        min-height: 180px;
        max-height: 380px;
        overflow-y: auto;
        font-size: 1.05rem;
        line-height: 1.6;
        white-space: pre-wrap;
        word-break: break-word;
        color: #0f172a;
    }
    @media (prefers-color-scheme: dark) {
        .output-box {
            background-color: #111827;
            border-color: #374151;
            color: #f3f4f6;
        }
    }
    
    .output-placeholder {
        color: #94a3b8;
        font-style: italic;
    }

    /* Meta badge */
    .meta-tag {
        display: inline-block;
        background: #e0e7ff;
        color: #3730a3;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    @media (prefers-color-scheme: dark) {
        .meta-tag {
            background: #312e81;
            color: #c7d2fe;
        }
    }

    /* Character counter */
    .char-counter {
        font-size: 0.85rem;
        color: #6b7280;
        text-align: right;
        margin-top: 4px;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ==============================================================================
# Session State Initialization
# ==============================================================================

if "input_text" not in st.session_state:
    st.session_state.input_text = ""
if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""
if "source_lang" not in st.session_state:
    st.session_state.source_lang = AUTO_DETECT_CODE
if "target_lang" not in st.session_state:
    st.session_state.target_lang = "ta"  # Default target to Tamil as requested
if "detected_lang" not in st.session_state:
    st.session_state.detected_lang = None
if "tts_audio" not in st.session_state:
    st.session_state.tts_audio = None
if "runtime_api_key" not in st.session_state:
    st.session_state.runtime_api_key = ""
if "provider" not in st.session_state:
    raw_key = get_api_key()
    has_valid_key = bool(raw_key and not raw_key.startswith("your_") and not raw_key.startswith("AIzaSy_your_"))
    st.session_state.provider = PROVIDER_GOOGLE_CLOUD if has_valid_key else PROVIDER_GOOGLE_FREE


# Determine active API Key (runtime override or environment / secrets)
active_api_key = st.session_state.runtime_api_key.strip() or get_api_key()
service = TranslationService(api_key=active_api_key, provider=st.session_state.provider)


# ==============================================================================
# Header Section
# ==============================================================================

if st.session_state.provider == PROVIDER_GOOGLE_FREE:
    status_badge = '<span class="badge-status badge-configured">● Free Translation Engine Active</span>'
elif service.is_configured():
    status_badge = '<span class="badge-status badge-configured">● Cloud API Connected</span>'
else:
    status_badge = '<span class="badge-status badge-warning">⚠ Cloud API Key Required</span>'

st.markdown(
    f"""
    <div class="header-container">
        <div class="header-title">
            <span>🌐</span> LinguaBridge — Language Translation Tool
        </div>
        <div class="header-subtitle">
            Multilingual translation tool supporting Indian regional and international languages.
        </div>
        {status_badge}
    </div>
    """,
    unsafe_allow_html=True,
)


# ==============================================================================
# Provider Engine Selector
# ==============================================================================

provider_names = {
    PROVIDER_GOOGLE_FREE: "⚡ Google Translate Engine (Free Alternative — No API Key Required)",
    PROVIDER_GOOGLE_CLOUD: "🏢 Google Cloud Translation API (Official Enterprise — Requires API Key)",
}

selected_prov = st.radio(
    "Translation Engine / Provider:",
    options=[PROVIDER_GOOGLE_FREE, PROVIDER_GOOGLE_CLOUD],
    index=0 if st.session_state.provider == PROVIDER_GOOGLE_FREE else 1,
    format_func=lambda x: provider_names[x],
    horizontal=True,
    help="Select between the free translation engine and official Google Cloud Translation API.",
)
if selected_prov != st.session_state.provider:
    st.session_state.provider = selected_prov
    st.rerun()


# ==============================================================================
# Setup Notice (If Google Cloud is chosen but not configured)
# ==============================================================================

if st.session_state.provider == PROVIDER_GOOGLE_CLOUD and not service.is_configured():
    with st.expander("🔑 Google Cloud Translation API Configuration (Required for Official Mode)", expanded=True):
        st.warning(
            "You selected the **Official Google Cloud Translation API**, which requires a valid Google Cloud API key. "
            "Please provide your API key below, configure it in your `.env` file, or select the **Free Alternative** above."
        )
        col_key_input, col_key_btn = st.columns([4, 1])
        with col_key_input:
            temp_key = st.text_input(
                "Enter Google Cloud API Key for this session:",
                type="password",
                placeholder="AIzaSy...",
                help="Your API key will remain active for this session only.",
                label_visibility="collapsed",
            )
        with col_key_btn:
            if st.button("Apply Key", use_container_width=True, type="primary"):
                if temp_key.strip():
                    st.session_state.runtime_api_key = temp_key.strip()
                    st.success("API Key applied! Reloading...")
                    st.rerun()
                else:
                    st.error("Please enter a valid key.")

        st.markdown(
            """
            ---
            **Quick Setup Instructions:**
            1. Visit the [Google Cloud Console](https://console.cloud.google.com/).
            2. Enable the **Cloud Translation API** for your project.
            3. Navigate to **APIs & Services > Credentials > Create Credentials > API Key**.
            4. Add the key to a `.env` file in the project root:
               ```env
               GOOGLE_TRANSLATE_API_KEY=AIzaSyYourActualKeyHere
               ```
            5. Or paste it directly in the input box above for instant testing!
            """
        )


# ==============================================================================
# Language Selector Bar (Side-by-Side with Swap Control)
# ==============================================================================

# Construct language options
source_options = [AUTO_DETECT_CODE] + list(SUPPORTED_LANGUAGES.keys())
target_options = list(SUPPORTED_LANGUAGES.keys())

def get_source_label(code: str) -> str:
    if code == AUTO_DETECT_CODE:
        return f"✨ {AUTO_DETECT_LABEL}"
    return f"{SUPPORTED_LANGUAGES.get(code, code)} ({code})"

def get_target_label(code: str) -> str:
    return f"{SUPPORTED_LANGUAGES.get(code, code)} ({code})"

col_src_select, col_swap, col_tgt_select = st.columns([5, 1, 5], vertical_alignment="bottom")

with col_src_select:
    # Ensure session language is valid
    if st.session_state.source_lang not in source_options:
        st.session_state.source_lang = AUTO_DETECT_CODE
    
    src_idx = source_options.index(st.session_state.source_lang)
    selected_source = st.selectbox(
        "Source Language",
        options=source_options,
        index=src_idx,
        format_func=get_source_label,
        key="src_dropdown",
        help="Select original language or enable auto-detection.",
    )
    if selected_source != st.session_state.source_lang:
        st.session_state.source_lang = selected_source

with col_swap:
    # Swap button between dropdowns
    swap_disabled = st.session_state.source_lang == AUTO_DETECT_CODE
    if st.button("⇄", help="Swap Source and Target Languages", disabled=swap_disabled, use_container_width=True):
        # Swap languages
        old_src = st.session_state.source_lang
        old_tgt = st.session_state.target_lang
        st.session_state.source_lang = old_tgt
        st.session_state.target_lang = old_src
        
        # Also swap content if translation is present
        if st.session_state.translated_text:
            st.session_state.input_text = st.session_state.translated_text
            st.session_state.translated_text = ""
            st.session_state.tts_audio = None
        st.rerun()

with col_tgt_select:
    if st.session_state.target_lang not in target_options:
        st.session_state.target_lang = "ta"
        
    tgt_idx = target_options.index(st.session_state.target_lang)
    selected_target = st.selectbox(
        "Target Language",
        options=target_options,
        index=tgt_idx,
        format_func=get_target_label,
        key="tgt_dropdown",
        help="Select language to translate into.",
    )
    if selected_target != st.session_state.target_lang:
        st.session_state.target_lang = selected_target

# Language selection validation alert
identical_languages = (
    st.session_state.source_lang != AUTO_DETECT_CODE
    and st.session_state.source_lang == st.session_state.target_lang
)
if identical_languages:
    st.warning(
        f"⚠ Source and Target are both set to **{SUPPORTED_LANGUAGES.get(st.session_state.target_lang)}**. "
        "Please select a different target language."
    )


# ==============================================================================
# Translation Panels: Input & Output Side-by-Side
# ==============================================================================

col_input_panel, col_output_panel = st.columns(2, gap="medium")

# --- LEFT PANEL: SOURCE INPUT ---
with col_input_panel:
    st.markdown('<div class="panel-label"><span>Input Text</span></div>', unsafe_allow_html=True)
    
    input_text = st.text_area(
        label="Input Text",
        value=st.session_state.input_text,
        height=240,
        placeholder="Enter or paste text here to translate (e.g., 'Hello, welcome to LinguaBridge!')...",
        label_visibility="collapsed",
        key="main_input_area",
    )
    # Sync state
    st.session_state.input_text = input_text
    
    # Character & word count indicators
    char_len = len(input_text)
    word_len = len(input_text.split()) if input_text.strip() else 0
    char_counter_color = "#ef4444" if char_len > MAX_INPUT_CHARACTERS else "#6b7280"
    st.markdown(
        f'<div class="char-counter" style="color: {char_counter_color};">'
        f'{char_len:,} / {MAX_INPUT_CHARACTERS:,} characters &nbsp;|&nbsp; {word_len:,} words'
        f'</div>',
        unsafe_allow_html=True,
    )

# --- RIGHT PANEL: TRANSLATED OUTPUT ---
with col_output_panel:
    # Build output label with detected language metadata if available
    det_badge = ""
    if st.session_state.detected_lang:
        det_name = SUPPORTED_LANGUAGES.get(st.session_state.detected_lang, st.session_state.detected_lang)
        det_badge = f'<span class="meta-tag">Detected: {det_name}</span>'
    
    st.markdown(
        f'<div class="panel-label"><span>Translation Result</span>{det_badge}</div>',
        unsafe_allow_html=True,
    )
    
    # Output display box
    if st.session_state.translated_text:
        st.markdown(
            f'<div class="output-box">{st.session_state.translated_text}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="output-box"><span class="output-placeholder">Translated text will appear here once you click Translate...</span></div>',
            unsafe_allow_html=True,
        )
    
    # Copy & TTS Controls row
    col_out_copy, col_out_tts = st.columns([1, 1])
    with col_out_copy:
        if st.session_state.translated_text:
            # One-click copy helper using Streamlit code snippet
            with st.popover("📋 Copy Text", use_container_width=True):
                st.caption("Click the copy icon in the top right of the code block:")
                st.code(st.session_state.translated_text, language="text")
        else:
            st.button("📋 Copy Text", disabled=True, use_container_width=True)

    with col_out_tts:
        if st.session_state.translated_text:
            if st.button("🔊 Listen (Speech)", use_container_width=True):
                with st.spinner("Generating speech..."):
                    audio_bytes = TranslationService.generate_speech(
                        text=st.session_state.translated_text,
                        lang=st.session_state.target_lang,
                    )
                    if audio_bytes:
                        st.session_state.tts_audio = audio_bytes
                    else:
                        st.warning("Text-to-speech audio could not be generated for this language/text.")
        else:
            st.button("🔊 Listen (Speech)", disabled=True, use_container_width=True)

    # Audio playback display
    if st.session_state.tts_audio:
        st.audio(st.session_state.tts_audio, format="audio/mp3")


# ==============================================================================
# Action Control Bar
# ==============================================================================

col_btn_trans, col_btn_clear, col_btn_swap_extra = st.columns([3, 1, 1], gap="small")

with col_btn_trans:
    translate_disabled = identical_languages or len(input_text.strip()) == 0
    if st.button(
        "🚀 Translate Now",
        type="primary",
        use_container_width=True,
        disabled=translate_disabled,
        help="Translate the text through Google Cloud Translation API.",
    ):
        try:
            spinner_msg = (
                "Translating via Google Cloud API..."
                if st.session_state.provider == PROVIDER_GOOGLE_CLOUD
                else "Translating via Google Translate Engine..."
            )
            with st.spinner(spinner_msg):
                result = service.translate(
                    text=input_text,
                    target_lang=st.session_state.target_lang,
                    source_lang=st.session_state.source_lang,
                )
                st.session_state.translated_text = result.translated_text
                st.session_state.detected_lang = result.detected_language
                st.session_state.tts_audio = None  # Reset prior audio for new text
                st.rerun()
        except ValidationError as e:
            st.warning(f"Validation Notice: {e}")
        except MissingConfigurationError as e:
            st.error(f"Configuration Required: {e}")
            st.info("💡 You can enter your API key in the configuration panel above to proceed.")
        except AuthenticationError as e:
            st.error(f"Authentication Failure: {e}")
        except QuotaExceededError as e:
            st.error(f"Quota Notice: {e}")
        except NetworkError as e:
            st.error(f"Network Failure: {e}")
        except LinguaBridgeError as e:
            st.error(f"Translation Error: {e}")
        except Exception as e:
            st.error(f"Unexpected Error: {e}")

with col_btn_clear:
    if st.button("🗑 Clear All", use_container_width=True, help="Clear input text, translation result, and audio."):
        st.session_state.input_text = ""
        st.session_state.translated_text = ""
        st.session_state.detected_lang = None
        st.session_state.tts_audio = None
        st.rerun()

with col_btn_swap_extra:
    if st.button("⇄ Swap", use_container_width=True, disabled=swap_disabled, help="Swap source & target languages"):
        old_src = st.session_state.source_lang
        old_tgt = st.session_state.target_lang
        st.session_state.source_lang = old_tgt
        st.session_state.target_lang = old_src
        if st.session_state.translated_text:
            st.session_state.input_text = st.session_state.translated_text
            st.session_state.translated_text = ""
            st.session_state.tts_audio = None
        st.rerun()


# ==============================================================================
# Project Information & Usage Instructions
# ==============================================================================

st.markdown("---")

tab_about, tab_instructions, tab_api_docs = st.tabs([
    "📖 About Project",
    "💡 Instructions for Use",
    "⚙ API & Technical Architecture"
])

with tab_about:
    st.markdown(
        """
        ### LinguaBridge — Language Translation Tool
        **LinguaBridge** is a real-world translation platform built with Python and Streamlit,
        engineered to demonstrate clean architecture, robust error boundaries, and integration with the
        official **Google Cloud Translation API v2**.

        **Key Features:**
        - **30+ Supported Languages**: Including Indian regional languages (Tamil, Hindi, Telugu, Kannada, Malayalam, Marathi, Bengali, Gujarati, Punjabi, Urdu) and global languages (French, German, Spanish, Japanese, Chinese, Arabic, Russian, and more).
        - **Automatic Language Detection**: Identifies source language automatically.
        - **Language Swap & Content Rotation**: Instantly swap source and target with one click.
        - **Text-to-Speech (TTS)**: Built-in voice audio playback powered by Google Text-to-Speech.
        - **Zero Data Loss**: User inputs are strictly preserved across API errors and network timeouts.
        - **Comprehensive Unit Tests**: Mocked pytest test suite covering all failure scenarios without incurring API charges.
        """
    )

with tab_instructions:
    st.markdown(
        """
        ### How to Use LinguaBridge
        1. **Select Languages**:
           - Choose your **Source Language** (or leave as `Detect Language (Auto)`).
           - Choose your **Target Language** from the dropdown.
        2. **Enter Text**:
           - Type or paste text into the **Input Text** area.
           - Monitor the live character counter (up to 5,000 characters).
        3. **Translate**:
           - Click **Translate Now**. The loading spinner indicates API communication.
           - The translated output will appear in the right panel.
        4. **Copy & Speech**:
           - Click **Copy Text** to grab the translated text.
           - Click **Listen (Speech)** to hear the translated text pronounced.
        5. **Swap Languages**:
           - Click **⇄ Swap** to reverse languages and verify translations back to the source.
        """
    )

with tab_api_docs:
    st.markdown(
        """
        ### Architecture & Security Details
        - **API Integration**: Connects to `https://translation.googleapis.com/language/translate/v2` via secure HTTPS POST requests.
        - **Security Best Practices**:
          - No hardcoded keys in source code.
          - Keys loaded from environment variables (`.env`) or Streamlit secrets (`st.secrets`).
          - Strict `.gitignore` protects secrets from source control.
        - **HTML Entity Handling**: Google Cloud Translation API returns HTML-escaped characters (e.g. `&#39;`, `&quot;`). LinguaBridge automatically decodes them with `html.unescape()` to deliver clean text.
        - **Error Classification**:
          - `ValidationError`: Client-side input and language checks.
          - `AuthenticationError`: HTTP 401/403 credentials and project billing errors.
          - `QuotaExceededError`: HTTP 429 rate limit errors.
          - `NetworkError`: Timeouts and socket dropouts.
        """
    )
