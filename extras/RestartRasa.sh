#!/bin/bash

pkill -f "rasa run actions"
pkill -f "rasa run --enable-api"

# Esperar unos segundos para asegurarse de que los procesos se detienen completamente
sleep 5

cd Mislabot

# Ejecutar nuevamente los comandos para iniciar los servicios
nohup rasa run actions &
nohup rasa run --enable-api --cors "*" &

# Mensaje de confirmación
echo "Servicios de Rasa reiniciados."
