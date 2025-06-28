#!/bin/bash

# Script para rodar as migrações do banco de dados no container Docker
# Uso: bash migrar_banco.sh

set -e

# Inicializa as migrações (apenas na primeira vez)
echo "[1/3] flask db init (pode ignorar se já existe a pasta migrations)"
sudo docker compose exec backend flask db init || true

# Gera as migrações
echo "[2/3] flask db migrate -m 'Migracao Inicial'"
sudo docker compose exec backend flask db migrate -m "Migracao Inicial"

# Aplica as migrações
echo "[3/3] flask db upgrade"
sudo docker compose exec backend flask db upgrade

echo "Migrações aplicadas com sucesso!"
