#!/bin/bash
# Script para instalar dependências no ambiente virtual

set -e

echo "=========================================="
echo "Instalando Dependências"
echo "=========================================="
echo ""

# Verificar se o venv existe
if [ ! -d "venv" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv venv
    echo "✅ Ambiente virtual criado"
fi

# Ativar ambiente virtual
echo "Ativando ambiente virtual..."
source venv/bin/activate

# Atualizar pip
echo ""
echo "Atualizando pip..."
pip install --upgrade pip setuptools wheel

# Instalar dependências
echo ""
echo "Instalando dependências do requirements.txt..."
pip install -r requirements.txt

echo ""
echo "=========================================="
echo "✅ Instalação concluída!"
echo "=========================================="
echo ""
echo "Para ativar o ambiente virtual:"
echo "  source venv/bin/activate"
echo ""
echo "Para desativar:"
echo "  deactivate"
