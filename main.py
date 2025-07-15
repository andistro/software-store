# Este programa busca apenas nos repositórios apt do sistema.
# Pacotes Snap e Flatpak são ignorados e não suportados, pois não funcionam no Debian via Termux/proot-distro.

import sys
import locale
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from ui.main_window import MainWindow
from deeplink import handle_deeplink

def main():
    # Detecta idioma do sistema
    lang, _ = locale.getdefaultlocale()
    # ...carregar gettext...

    # Verifica se foi chamado por deeplink
    if len(sys.argv) > 1 and sys.argv[1].startswith("software-store://"):
        # O handle_deeplink abre uma janela de detalhes do pacote solicitado pelo deeplink
        handle_deeplink(sys.argv[1])
    else:
        win = MainWindow(lang)
        win.connect("destroy", Gtk.main_quit)
        win.show_all()
        Gtk.main()

if __name__ == "__main__":
    main()
