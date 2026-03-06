#!/bin/bash
set -e

echo "📦 Instalando dependencias..."
pip install -r requirements.txt

echo ""
echo "🧪 Ejecutando pruebas..."
pytest tests/ --cov=app --cov-report=term-missing

echo ""
echo "🚀 Iniciando la aplicación en http://localhost:5000"
python app/app.py
