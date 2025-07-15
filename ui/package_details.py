import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from apt_utils import install_package, remove_package, is_installed

class PackageDetailsDialog(Gtk.Dialog):
    def __init__(self, parent, pkg):
        Gtk.Dialog.__init__(self, title=pkg['name'], transient_for=parent, flags=0)
        self.set_default_size(320, 240)
        box = self.get_content_area()
        # Ícone
        # ...carregar ícone...
        # Nome, versão
        box.add(Gtk.Label(label=f"{pkg['name']} ({pkg['version']})"))
        # Descrição
        box.add(Gtk.Label(label=pkg.get('description', '')))
        # Screenshots
        # ...carregar screenshots se houver...
        # Botões
        if is_installed(pkg['name']):
            btn_open = Gtk.Button(label=_("Abrir"))
            btn_remove = Gtk.Button(label=_("Remover"))
            btn_remove.connect("clicked", lambda b: remove_package(pkg['name']))
            box.add(btn_open)
            box.add(btn_remove)
        else:
            btn_install = Gtk.Button(label=_("Instalar"))
            btn_install.connect("clicked", lambda b: install_package(pkg['name'], self))
            box.add(btn_install)
        self.show_all()
