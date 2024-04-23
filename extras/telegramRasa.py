import requests
from flask import Flask, request, jsonify
import json
import re

app = Flask(__name__)

TELEGRAM_TOKEN = ''
RASA_ENDPOINT = 'https://18.214.170.176.nip.io:5008/webhooks/rest/webhook'


@app.route("/webhooks/telegram/webhook", methods=["POST"])
def webhook_handler():
    update = request.json
    # Verificar si la actualización tiene la estructura esperada
    if "message" in update and "chat" in update["message"] and "text" in update["message"]:
        chat_id = update["message"]["chat"]["id"]
        message = update["message"]["text"]
        sender = update["message"]["from"]["first_name"]

        if message == '/start':
            message = 'Hola'
    else:
        print("Actualización inesperada de Telegram:", update)
        return '', 200

    # Enviar el mensaje a Rasa
    rasa_response = send_message_to_rasa(message, sender)

    # Enviar la respuesta de Rasa a Telegram
    send_message_to_telegram(chat_id, rasa_response)

    return '', 200


def send_message_to_rasa(message, sender):
    payload = {
        "sender": sender,
        "message": message
    }
    response = requests.post(RASA_ENDPOINT, json=payload)

    rasa_response = response.json()

    # Inicializar listas para almacenar texto e imágenes
    texts = []
    images = []

    # Verificar si la respuesta es una lista
    if isinstance(rasa_response, list):
        for item in rasa_response:
            # Verificar si el elemento de la respuesta contiene texto
            if "text" in item:
                texts.append(item["text"])
            # Verificar si el elemento de la respuesta contiene una imagen
            if "image" in item:
                images.append(item["image"])
    else:
        # Si la respuesta no es una lista, asumir que es un solo elemento
        if "text" in rasa_response:
            texts.append(rasa_response["text"])
        if "image" in rasa_response:
            images.append(rasa_response["image"])

    # Unir todos los textos en un solo mensaje
    all_text = "\n".join(texts)

    return {"texts": all_text if all_text else f"Lo siento {sender}, no entendí tu pregunta.",
            "images": images}


def convert_to_markdown(text):
    # Reemplazar <br> por saltos de línea en Markdown
    text = text.replace("<br>", "\n")

    text = text.replace("_", "\\_")

    # Reemplazar <strong> y </strong> por negrita en Markdown
    text = text.replace("<strong>", "*").replace("</strong>", "*")

    # Expresión regular para detectar enlaces HTML
    link_pattern = re.compile(
        '<a href=[\'"](https?:\/\/[^\'"]+)[\'"][^>]*>([^<]+)<\/a>')

    # Reemplazar enlaces HTML por formato Markdown
    text = re.sub(link_pattern, r'[\2](\1)', text)
    print(text)

    return text


def send_message_to_telegram(chat_id, response):
    url_send_text = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    url_send_photo = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"

    # Enviar texto si está presente
    if "texts" in response:
        text = response["texts"]
        if is_valid_json(text):
            json_list = json.loads(text)
            list_text = format_json_list_to_markdown(json_list)
            text = list_text if list_text else text
        text = convert_to_markdown(text)
        # Dividir el texto en partes de longitud máxima permitida por Telegram
        max_length = 4096
        text_parts = [text[i:i+max_length]
                      for i in range(0, len(text), max_length)]
        for part in text_parts:
            payload_text = {
                "chat_id": chat_id,
                "text": part,
                "parse_mode": "Markdown"
            }
            requests.post(url_send_text, json=payload_text)

    # Enviar imágenes si están presentes
    if "images" in response:
        for image_url in response["images"]:
            payload_photo = {
                "chat_id": chat_id,
                "photo": image_url
            }
            requests.post(url_send_photo, json=payload_photo)


def is_valid_json(text):
    try:
        json.loads(text)
        return True
    except ValueError:
        return False


def format_json_list_to_markdown(json_list):
    list_text = ""
    for item in json_list:
        for value in item.values():
            if isinstance(value, list):
                for element in value:
                    if isinstance(element, dict):
                        for sub_value in element.values():
                            if isinstance(sub_value, list):
                                for sub_element in sub_value:
                                    list_text += "  _{}_\n".format(
                                        sub_element)
                            else:
                                list_text += " {}\n".format(sub_value)
            else:
                list_text += "*{}*\n".format(value)
        list_text += "\n"  # Agregar una línea en blanco después de cada elemento
    return list_text


if __name__ == "__main__":
    app.run()
