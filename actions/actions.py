import csv
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ReadCSVAction(Action):
    def name(self) -> Text:
        return "action_read_csv"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Leer el archivo CSV de grupos
        with open('../Grupos.csv', 'r', encoding='utf-8') as file:
            grupos_data = list(csv.DictReader(file, delimiter=';'))

        # Leer el archivo CSV de módulos
        with open('../Modulos.csv', 'r', encoding='utf-8') as file:
            modulos_data = list(csv.DictReader(file, delimiter=';'))

        # Obtener las familias profesionales existentes
        familias_profesionales = set(
            [grupo['Familia'] for grupo in grupos_data])

        # Obtener la oferta de estudios en la familia de informática
        oferta_informatica = []
        for modulo in modulos_data:
            if modulo['Grupo'].startswith('1C') or modulo['Grupo'].startswith('2C'):
                oferta_informatica.append({
                    'Nombre': modulo['Nom_Cas_Modulo'],
                    'Horas': modulo['HORAS'],
                    'Modalidad': 'Presencial' if modulo['Grupo'].endswith('D') else 'Semipresencial'
                })

        # Construir y enviar la respuesta
        respuesta = f"Familias profesionales existentes: {', '.join(familias_profesionales)}\n\n"
        respuesta += "Oferta de estudios en la familia de informática:\n"
        for modulo in oferta_informatica:
            respuesta += f"- {modulo['Nombre']} ({modulo['Horas']} horas, {modulo['Modalidad']})\n"

        dispatcher.utter_message(text=respuesta)

        return []
