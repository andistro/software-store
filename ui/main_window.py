import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
import gettext
gettext.bindtextdomain('software-store', '/opt/software-store/i18n')
gettext.textdomain('software-store')
_ = gettext.gettext

from apt_utils import search_packages, update_packages
from ui.package_details import PackageDetailsDialog

class MainWindow(Gtk.Window):
    def __init__(self, lang):
        Gtk.Window.__init__(self, title="Software Store")
        self.set_default_size(400, 600)
        self.set_resizable(True)
        # ...aplicar tema GTK...
        # Layout principal
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_margin_top(16)
        vbox.set_margin_bottom(16)
        vbox.set_margin_start(16)
        vbox.set_margin_end(16)
        self.add(vbox)

        # Saudação dinâmica
        self.greeting = Gtk.Label(label=self.get_greeting())
        vbox.pack_start(self.greeting, False, False, 0)

        # Descrição breve
        self.desc = Gtk.Label(label=_("Bem-vindo à loja de aplicativos Debian/Ubuntu para Termux!"))
        vbox.pack_start(self.desc, False, False, 0)

        # Campo de busca
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.search_entry = Gtk.Entry()
        self.search_entry.set_placeholder_text(_("Pesquisar aplicativos"))
        self.search_entry.set_hexpand(True)
        self.search_entry.set_margin_bottom(8)
        self.search_entry.connect("activate", self.on_search_clicked)  # Enter faz pesquisa
        hbox.pack_start(self.search_entry, True, True, 0)
        self.search_btn = Gtk.Button(label=_("Pesquisar"))
        self.search_btn.connect("clicked", self.on_search_clicked)
        hbox.pack_start(self.search_btn, False, False, 0)
        vbox.pack_start(hbox, False, False, 0)

        # Botão de atualizar pacotes
        self.update_btn = Gtk.Button(label=_("Procurar atualizações"))
        self.update_btn.connect("clicked", self.on_update_clicked)
        vbox.pack_start(self.update_btn, False, False, 0)

        # Status de atualização
        self.status_label = Gtk.Label(label="")
        vbox.pack_start(self.status_label, False, False, 0)

        # Área de resultados
        self.results_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        vbox.pack_start(self.results_box, True, True, 0)

    def get_greeting(self):
        from datetime import datetime
        hour = datetime.now().hour
        if 5 <= hour < 12:
            return _("Bom dia!")
        elif 12 <= hour < 18:
            return _("Boa tarde!")
        elif 18 <= hour < 24:
            return _("Boa noite!")
        else:
            return _("Boa madrugada!")

    def on_search_clicked(self, btn_or_entry):
        text = self.search_entry.get_text()
        self.show_search_results(text)

    def show_search_results(self, term):
        self.results_box.foreach(lambda w: self.results_box.remove(w))
        pkgs = search_packages(term)
        if not pkgs:
            self.results_box.pack_start(Gtk.Label(label=_("Nenhum pacote encontrado.")), False, False, 0)
        for pkg in pkgs:
            card = self.create_package_card(pkg)
            self.results_box.pack_start(card, False, False, 0)
        self.results_box.show_all()

    def create_package_card(self, pkg):
        # Card com ícone, nome, versão, botão instalar
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        # ...ícone...
        name_label = Gtk.Label(label=f"{pkg['name']} ({pkg['version']})")
        hbox.pack_start(name_label, True, True, 0)
        btn = Gtk.Button(label=_("Instalar"))
        btn.connect("clicked", lambda b: self.on_install_clicked(pkg))
        hbox.pack_start(btn, False, False, 0)
        # ...arredondamento via CSS...
        return hbox

    def on_install_clicked(self, pkg):
        dialog = PackageDetailsDialog(self, pkg)
        dialog.run()
        dialog.destroy()

    def on_update_clicked(self, btn):
        self.status_label.set_text(_("Procurando por atualizações, aguarde..."))
        while Gtk.events_pending():
            Gtk.main_iteration()
        updates = update_packages()
        if not updates:
            self.status_label.set_text(_("Tudo atualizado!"))
        else:
            self.status_label.set_text(_("Há atualizações disponíveis!"))
        # ...pode abrir diálogo para confirmar atualização...

