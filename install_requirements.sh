#!/bin/bash

echo "📦 Instalando pacotes do requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Instalação concluída."
