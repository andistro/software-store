#!/bin/bash

set -e

echo "Removendo arquivos do Software Store..."
sudo rm -rf /opt/software-store

echo "Removendo atalho do menu..."
sudo rm -f /usr/share/applications/software-store.desktop
sudo update-desktop-database

echo "Removendo link executável..."
sudo rm -f /usr/local/bin/software-store

echo "Removendo associação de deeplink..."
sudo xdg-mime default "" x-scheme-handler/software-store

echo "Desinstalação concluída!"
