import csv
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import re
from unidecode import unidecode


class ReadCSVAction(Action):
    def name(self) -> Text:
        return "action_read_csv"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        with open('../Grupos.csv', 'r', encoding='utf-8') as file:
            grupos_data = list(csv.DictReader(file, delimiter=';'))

        with open('../Modulos.csv', 'r', encoding='utf-8') as file:
            modulos_data = list(csv.DictReader(file, delimiter=';'))

        user_input = tracker.latest_message.get("text")

        print(user_input)

        response = self.generate_response(
            user_input, grupos_data, modulos_data)

        dispatcher.utter_message(text=response)

        return []

    def generate_response(self, user_input: Text, grupos_data: List[Dict[Text, Any]], modulos_data: List[Dict[Text, Any]]) -> Text:
        response = ""

        if "estudiar" in user_input.lower():
            tema_regex = re.compile(
                r'estudiar\s+(\w+(?:\s+\w+)*)', re.IGNORECASE)
            match = tema_regex.search(user_input)
            if match:
                tema = unidecode(match.group(1)).lower()
            else:
                tema = None
            if tema:
                for modulo in modulos_data:
                    if tema in unidecode(modulo['Nom_Cas_Modulo']).lower():
                        for grupo in grupos_data:
                            if modulo['Grupo'] == grupo['Grupo']:
                                response += f"<strong>{grupo['Nombre']}</strong> {modulo['Nom_Cas_Modulo']} <br>"
                if not response:
                    response = f"Lo siento, no se encontró información sobre {tema}."
                else:
                    response = f"Puedes estudiar {tema} en: <br>" + response
            else:
                response = "Lo siento, no se reconoce el tema que mencionaste."
        elif "asignaturas" in user_input.lower():
            response += f"Asignaturas: <br>"
            grupo_interes = None
            for nombre_grupo in ['DAW', 'ASIR', 'SMR_A', 'S.M.X.', 'CIBER', 'IABIG', 'DAM_SEMI', 'DAW._SEMIP', 'SMX_SEMI', 'S.M.R_SEMI']:
                if nombre_grupo.lower() in user_input.lower():
                    grupo_interes = nombre_grupo
                    break
            if grupo_interes:
                for grupo in grupos_data:
                    if grupo['Nombre'].lower() == grupo_interes.lower():
                        response += f"<strong>{grupo['Grupo']}</strong><br>"
                        for modulo in modulos_data:
                            if modulo['Grupo'] == grupo['Grupo']:
                                response += f"{modulo['Nom_Cas_Modulo']} <br>"
            else:
                response = "Lo siento, no se encontró información sobre asignaturas."
        else:
            response = "Lo siento, no entiendo la pregunta."
        return response
