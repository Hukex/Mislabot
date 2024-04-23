#!/bin/bash

# Cambiar al directorio Mislabot
cd Mislabot

# Ejecutar el servidor de acciones de Rasa en segundo plano
nohup rasa run actions &

# Ejecutar Rasa API habilitando CORS
nohup rasa run --enable-api --cors "*" &

# Mensaje de confirmación
echo "Comandos ejecutados en segundo plano."
