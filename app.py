import streamlit as st
import requests

st.set_page_config(page_title="Real-Time Translator", layout="centered")

st.title("🌐 Real-Time Translator with Azure")

text = st.text_area("Enter text to translate:")

source_lang = st.selectbox("Source language", ["en", "fr", "de", "es", "ro"])
target_lang = st.selectbox("Target language", ["fr", "en", "de", "es", "ro"])

if st.button("Translate"):
    if not text:
        st.warning("Please enter text to translate.")
    else:
        endpoint = st.secrets["AZURE_ENDPOINT"]
        key = st.secrets["AZURE_KEY"]
        region = st.secrets["AZURE_REGION"]  

        url = f"{endpoint}/translate?api-version=3.0&from={source_lang}&to={target_lang}"
        headers = {
            "Ocp-Apim-Subscription-Key": key,
            "Ocp-Apim-Subscription-Region": region,
            "Content-type": "application/json"
        }
        body = [{"text": text}]
        response = requests.post(url, headers=headers, json=body)
        if response.status_code == 200:
            translated_text = response.json()[0]["translations"][0]["text"]
            st.success(f"Translated: {translated_text}")
        else:
            st.error("Something went wrong. Check your API key and endpoint.")
