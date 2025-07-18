#!/bin/bash
# Script para GERAR uma nova migração.
# Uso: ./migrar_banco.sh "mensagem"

set -e

if [ -z "$1" ]; then
  echo "Erro: Forneça uma mensagem para a migração."
  echo "Uso: $0 \"mensagem\""
  exit 1
fi

echo "[1/2] Gerando nova migração..."
sudo docker compose exec backend flask db migrate -m "$1"

echo "[2/2] Aplicando a nova migração..."
sudo docker compose exec backend flask db upgrade

echo "Nova migração gerada e aplicada com sucesso!"