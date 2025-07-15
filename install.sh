#!/bin/bash

set -e

# O instalador garante o funcionamento do Software Store e sua integração ao sistema.
# Para que todos os pacotes funcionem, é necessário que:
# - Os repositórios estejam configurados corretamente.
# - O usuário tenha permissões para instalar/remover pacotes via apt.
# - Dependências específicas de cada pacote sejam resolvidas pelo apt.
# - Pacotes que exigem parâmetros especiais (ex: --no-sandbox) serão tratados pelo Software Store.
# Se algum pacote exigir configuração extra, adicione ao script conforme necessário.

echo "Instalando dependências..."
sudo apt-get update
sudo apt-get install -y python3 python3-gi python3-apt gir1.2-gtk-3.0 gettext

echo "Instalando Software Store..."
INSTALL_DIR="/opt/software-store"
sudo mkdir -p "$INSTALL_DIR"
sudo cp -r ./* "$INSTALL_DIR"

echo "Os arquivos do Software Store serão movidos de $(pwd) para $INSTALL_DIR."
echo "Certifique-se de que todos os arquivos do projeto estão nesta pasta antes de instalar."

echo "Criando atalho no menu..."
sudo cp "$INSTALL_DIR/resources/software-store.desktop" /usr/share/applications/
sudo chmod 644 /usr/share/applications/software-store.desktop
sudo update-desktop-database
sudo xdg-mime default software-store.desktop x-scheme-handler/software-store

echo "Criando link executável..."
sudo ln -sf "$INSTALL_DIR/main.py" /usr/local/bin/software-store

echo "Compilando traduções..."
(cd "$INSTALL_DIR/i18n" && for f in *.po; do msgfmt "$f" -o "${f%.po}.mo"; done)

echo "Instalação concluída! Execute 'software-store' para abrir."
