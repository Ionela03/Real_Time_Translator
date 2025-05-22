import streamlit as st
import requests


st.set_page_config(page_title="Smart Translator", layout="centered")
st.title("🌍 Smart Translator")


languages = {
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


uploaded_file = st.file_uploader("📄 Upload a .txt file (optional)", type=["txt"])
text_input = st.text_area("✍️ Or type/paste text here", height=150)

target_lang = st.selectbox("Target language", [k for k in languages if languages[k] is not None])
target_code = languages[target_lang]


def get_text_content():
    if uploaded_file:
        return uploaded_file.read().decode("utf-8")
    return text_input

def detect_language(text, key, region, endpoint):
    url = f"{endpoint}/detect?api-version=3.0"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Ocp-Apim-Subscription-Region": region,
        "Content-type": "application/json"
    }
    body = [{"text": text}]
    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    return response.json()[0]["language"]

def translate_line(text, from_lang, to_lang, key, region, endpoint):
    if not text.strip():
        return ""
    url = f"{endpoint}/translate?api-version=3.0"
    if from_lang is not None:
        url += f"&from={from_lang}"
    url += f"&to={to_lang}"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Ocp-Apim-Subscription-Region": region,
        "Content-type": "application/json"
    }
    body = [{"text": text}]
    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    return response.json()[0]["translations"][0]["text"]

if st.button("Translate"):
    content = get_text_content()

    if not content.strip():
        st.warning("Please provide text or upload a file.")
        st.stop()

    endpoint = st.secrets["AZURE_ENDPOINT"]
    key = st.secrets["AZURE_KEY"]
    region = st.secrets["AZURE_REGION"]

    with st.spinner("🔄 Translating line by line..."):
        try:
            detected_languages = set()
            translated_lines = []

            for line in content.splitlines():
                if not line.strip():
                    translated_lines.append("")
                    continue

                
                detected_lang = detect_language(line, key, region, endpoint)
                detected_languages.add(detected_lang)

                
                from_lang = detected_lang

                translated = translate_line(line, from_lang, target_code, key, region, endpoint)
                translated_lines.append(translated)


            final_text = "\n".join(translated_lines)

            st.subheader("📄 Translation Result")
            st.text_area("Result", final_text.strip(), height=300)

            st.download_button(
                label="💾 Download Translated File",
                data=final_text.encode("utf-8"),
                file_name="translated.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"Translation failed: {e}")
