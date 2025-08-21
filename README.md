# Extracción de Información de Recibos

## Descripción:
Este proyecto permite la comunicación entre pacientes y profesionales de salud que hablan distintos idiomas, mediante una app web que integra modelos de IA open-source para transcripción, traducción y síntesis de voz.  
No se utilizan APIs externas, priorizando privacidad, sostenibilidad y reproducibilidad.


## Tabla de Contenidos 
- [Entorno](#entorno)
- [Componentes](#componentes)
- [Procedimiento](#procedimiento)
- [Resultados](#resultados)
- [Conclusiones](#Conclusiones)

## Entorno
- Se decidió usar Hugging Face Spaces por lo que ofrecen de manera gratis, es una solución momentanea para el problema que se intenta solucionar.
- El entorno es gratis y algo limitada, usa una CPU.
- Pueden ver la demo en [https://huggingface.co/spaces/JamesKevinStar/HealthcareTranslation]

## Componentes 
- El proyecto usa diferentes modelos para poder hacerlo funcionar:
  - Whisper: Se usó para obtener el texto del audio de la persona.
  - Llama 3.2 Instruct: Usado para traducir el texto y detectar el idioma del texto original.
  - gTTS: Se usa para generar audio del texto, por defecto está para que lo hable con acento inglés.
  - Gradio: Se utilizó para la parte de la interfaz de usuario, funciona tanto en web y movil.
 
## Procedimiento

### 1. Entrada de Voz. 
- La primera parte es permitir al usuario que suba un archivo de voz o que use un micrófono.
- El audio se almacena en formato .wav y se enviará a los diferentes módulos para su procesamiento.

### 2. Obtención de Texto.
- El audio se envia a ser procesado usando Whisper, el cual retorna el texto del audio con muy buena precisión.
- El texto obtenido se envia a los siguentes módulos para seguir siendo procesado.

### 3. Traducción y Detección de Idioma.
- El texto obtenido par por el modelo Llama 3.2 Instruct, el cual se le asigna un rol y se le da una orden.
- El modelo devuelve el texto traducido, también detecta el idioma original.
- Para ambas tareas se hace uso de la API.

### 4. Generación de Voz 
- El texto traducido se pasa al módulo que lo convertirá a audio, para el cual se usa gTTS.

## Resultados
- Se logró hacer un prototipo funcional.
- Se logró utilizar modelos de IA generativa para el propósito.
- También se logró hacer una interfaz para ver la funcionalidad.

## Conclusiones
- El entorno que se usa para que funcione la app usa una CPU, si se cambiara por una GPU daría mejores resultados.
- La app tarda un tiempo al principio porque está procesando el texto en el modelo Whisper, el cual no se está usando una API.
- Si se usara una API para la parte del obtención de texto sería muy rápida y de mejor calidad el output.
- En la parte de convertir texto a audio, no se usó un modelo de IA generativa porque demoraba mucho tiempo en generar el output, por eso se decidió hacerlo con otros métodos.
