import gradio as gr
from functions import transcribir_audio, detectar_idioma, traducir, generar_audio

def flujo(audio, src_lang_value, tgt_lang_value):
    # Transcribir
    texto_original = transcribir_audio(audio)
    if texto_original == "No Audio":
        return "No se detectó audio", ""
    # Determinar idioma de origen
    if src_lang_value == "Auto":
        idioma_origen = detectar_idioma(texto_original)
    else:
        idioma_origen = src_lang_value
    # Traducir texto
    traduccion = traducir(texto_original, idioma_origen, tgt_lang_value)

    # Las 3 variables que se usarán
    return idioma_origen, texto_original, traduccion

def create_interface():
    with gr.Blocks(title = "Healthcare Translation App") as demo:

        # Encabezado principal
        gr.Markdown(
            """
            # 🩺 Healthcare Translation Web App
            ### Real-time medical translation with AI
            ---
            """,
            elem_id="header"
        )

        # Subir o grabar audio
        with gr.Row():
            audio_input = gr.Audio(
                # Habilitar opciones para subir o grabar audio
                sources = ["microphone", "upload"],
                type="filepath",
                # Mensaje encabezado
                label = "🎙️ Upload o Record Audio"
            )

        # Selección de idiomas
        with gr.Row():
            src_lang = gr.Dropdown(
                # Posibles opciones a elegir, de momento 4 y 1 por defecto
                choices = ["Auto", "Spanish", "English", "French"],
                # Encabezado
                label = "🌐 Origen Language",
                # Valor por defecto
                value = "Auto",
                # Habilitar para interactuar
                interactive = True
            )
            tgt_lang = gr.Dropdown(
                # Posibles opciones a elegir, de momento 4
                choices = ["Spanish", "English", "French"],
                # Encabezado
                label = "🗣️ Translated Language",
                # Valor por defecto
                value = "English",
                # Habilitar para interactuar
                interactive = True
            )

        # Cuadros de texto: original y traducción
        with gr.Row():
            original_text = gr.Textbox(
                # Cuadro para mostrar texto original
                label = "Original Text",
                lines = 4,
                # Valor por defecto
                placeholder = "Original text detected...",
                # Usuario no podrá modificarlo
                interactive = False
            )
            translated_text = gr.Textbox(
                # Cuadro para mostrar texto traducido
                label = "Translated Text",
                lines = 4,
                # Valor por defecto
                placeholder = "Translated text by AI...",
                # Usuario no podrá modificarlo
                interactive = False
            )

        # Conectar audio con backend
        audio_input.change(fn = flujo, 
                           inputs = [audio_input, src_lang, tgt_lang], 
                           outputs = [src_lang, original_text, translated_text])

        # Generar el audio al ahcer click al botón
        with gr.Row():
            generar_audio_btn = gr.Button("🔊 Generar Audio con gTTS")
            audio_output = gr.Audio(label="Generated Audio", type="filepath")

            generar_audio_btn.click(
                fn = generar_audio,
                inputs = translated_text,
                outputs = audio_output)

    return demo
