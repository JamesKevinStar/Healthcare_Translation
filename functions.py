import os
import torch
import requests
from gtts import gTTS
from transformers import pipeline


# Asignar CPU
device = "cpu"
torch_dtype = torch.float16

# Obtener acceso a Llama desde la API
API_URL = "https://router.huggingface.co/v1/chat/completions"
HF_TOKEN = os.environ.get("HF_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

# Cargar pipeline de Whisper
whisper_pipe = pipeline("automatic-speech-recognition", 
                model = "openai/whisper-tiny",
                torch_dtype = torch_dtype, 
                device = device, 
                chunk_length_s = 5, 
                batch_size = 1)

# Definir función para transcribir
def transcribir_audio(audio):
    # Verificar si existe audio
    if audio == None:
        return "No Audio"
    # Obtener transcripción
    resultado = whisper_pipe(audio, return_language=True)
    texto = resultado["text"]
    return texto

# Definir función para detectar idioma
def detectar_idioma(texto):
    if not texto:
        return ""
    # Prompt para ordenarle que detecte el idioma
    prompt = (
        "You are a language identification assistant. "
        "Identify the language of the following text. "
        "Respond with only the language name in English, "
        "must be one of the following: 'Spanish', 'English', 'French', 'Japanese'."
        "No explanations.\n\n"
        f"Text:\n{texto}\n\nLanguage:"
    )
    payload = {"model": "meta-llama/Llama-3.2-1B-Instruct:novita",
               "messages": [{"role": "user", "content": prompt}],
               "temperature": 0.0,
               "max_tokens": 20}
    respuesta = requests.post(API_URL, headers=HEADERS, json=payload)
    respuesta.raise_for_status()
    data = respuesta.json()
    return data["choices"][0]["message"]["content"].strip()

# Definir función para traducir
def traducir(texto, src, tgt):
    if not texto:
        return ""
    # Prompt para ordenarle que traduzca el texto, y que no omita terminología médica
    prompt = (
        "You are a professional translator. Translate the text accurately, "
        "preserving register and medical terminology. Respond with only the translation and nothing more.\n\n"
        f"From: {src}\nTo: {tgt}\nText:\n{texto}\n\nTranslation:"
    )
    payload = {"model": "meta-llama/Llama-3.2-1B-Instruct:novita",
               "messages": [{"role": "user", "content": prompt}],
               "temperature": 0.0,
               "max_tokens": 70
    }
    respuesta = requests.post(API_URL, headers=HEADERS, json=payload)
    respuesta.raise_for_status()
    data = respuesta.json()
    return data["choices"][0]["message"]["content"].strip()

# Definir función para convertir texto a audio
def generar_audio(texto, lang='en'):
    tts = gTTS(text = texto, lang = lang)
    output_path = "output.mp3"
    tts.save(output_path)

    return output_path
