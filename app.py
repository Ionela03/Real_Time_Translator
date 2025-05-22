import streamlit as st
import requests

st.set_page_config(page_title="Real-Time Translator with Azure", layout="centered")
st.title("🌍 Real-Time Translator with Azure")

language_options = {
    "Detect Automatically 🌐": None,
    "English 🇬🇧": "en",
    "French 🇫🇷": "fr",
    "German 🇩🇪": "de",
    "Romanian 🇷🇴": "ro",
    "Spanish 🇪🇸": "es",
    "Italian 🇮🇹": "it",
    "Portuguese 🇵🇹": "pt",
    "Russian 🇷🇺": "ru",
    "Chinese (Simplified) 🇨🇳": "zh-Hans",
    "Japanese 🇯🇵": "ja",
    "Korean 🇰🇷": "ko",
    "Arabic 🇸🇦": "ar",
    "Turkish 🇹🇷": "tr",
    "Hindi 🇮🇳": "hi"
}

# Fără "Detect Automatically" pentru Target
target_languages = {k: v for k, v in language_options.items() if v is not None}


text = st.text_area("Enter text to translate:", height=150)

col1, col2 = st.columns(2)
with col1:
    source_lang = st.selectbox("Source language", list(language_options.keys()))
with col2:
    target_lang = st.selectbox("Target language", list(target_languages.keys()))

source_code = language_options[source_lang]
target_code = language_options[target_lang]

if st.button("Translate"):
    if not text:
        st.warning("Please enter text to translate.")
        st.stop()

    source_code = language_options[source_lang]
    target_code = target_languages[target_lang]

    if source_code == target_code and source_code is not None:
        st.warning("Source and target languages are the same.")
        st.stop()

    endpoint = st.secrets["AZURE_ENDPOINT"]
    key = st.secrets["AZURE_KEY"]
    region = st.secrets["AZURE_REGION"]


    if source_code is None:
        url = f"{endpoint}/translate?api-version=3.0&to={target_code}"
    else:
        url = f"{endpoint}/translate?api-version=3.0&from={source_code}&to={target_code}"

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Ocp-Apim-Subscription-Region": region,
        "Content-type": "application/json"
    }
    body = [{"text": text}]

    with st.spinner("Translating..."):
        try:
            response = requests.post(url, headers=headers, json=body)
            response.raise_for_status()
            result = response.json()[0]
            translated_text = result["translations"][0]["text"]
            st.success(f"Translation: {translated_text}")

            
            if source_code is None:
                detected_lang_code = result.get("detectedLanguage", {}).get("language")
                reversed_langs = {v: k for k, v in language_options.items() if v is not None}
                detected_lang_name = reversed_langs.get(detected_lang_code, detected_lang_code)
                st.info(f"Detected source language: **{detected_lang_name}**")

        except Exception as e:
            st.error(f"Something went wrong: {e}")
