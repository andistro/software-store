import gi
gi.require_version("Gtk", "3.0")
gi.require_version("WebKit2", "4.0")
from gi.repository import Gtk, WebKit2
import gettext
gettext.bindtextdomain('software-store', '/opt/software-store/i18n')
gettext.textdomain('software-store')
_ = gettext.gettext

from apt_utils import search_packages, update_packages, is_installed, get_special_exec
from ui.package_details import PackageDetailsDialog

class MainWindow(Gtk.Window):
    def __init__(self, lang):
        Gtk.Window.__init__(self, title="Software Store")
        self.set_default_size(400, 600)
        self.set_resizable(True)

        self.webview = WebKit2.WebView()
        self.add(self.webview)
        self.load_main_page()

        # Exemplo de como receber eventos do JS
        self.webview.connect("decide-policy", self.on_decide_policy)

    def load_main_page(self):
        html = open("/opt/software-store/resources/main.html").read()
        self.webview.load_html(html, "file:///opt/software-store/resources/main.html")

    def load_search_results(self, term):
        pkgs = search_packages(term, literal=False)
        # Gera HTML dinamicamente com os resultados
        html = "<html><head><link rel='stylesheet' href='file:///opt/software-store/resources/style.css'></head><body>"
        html += f"<h2>{_('Resultados para')} '{term}'</h2><div class='results'>"
        for pkg in pkgs:
            installed = is_installed(pkg['name'])
            html += f"""
            <div class='card'>
                <img src='file:///opt/software-store/resources/icons/{pkg['name']}.png' class='icon' onerror="this.src='file:///opt/software-store/resources/icons/default.png'">
                <div class='info'>
                    <span class='name'>{pkg['name']} ({pkg['version']})</span>
                    <button onclick="window.location.href='app-action://details/{pkg['name']}'">{_('Detalhes')}</button>
                    {'<button onclick="window.location.href=\'app-action://open/%s\'">%s</button>' % (pkg['name'], _('Abrir')) if installed else '<button onclick="window.location.href=\'app-action://install/%s\'">%s</button>' % (pkg['name'], _('Instalar'))}
                    {'<button onclick="window.location.href=\'app-action://remove/%s\'">%s</button>' % (pkg['name'], _('Remover')) if installed else ''}
                </div>
            </div>
            """
        html += "</div></body></html>"
        self.webview.load_html(html, "file:///opt/software-store/resources/search.html")

    def load_details_page(self, pkg_name):
        pkgs = search_packages(pkg_name, literal=True)
        if pkgs:
            pkg = pkgs[0]
            installed = is_installed(pkg['name'])
            html = "<html><head><link rel='stylesheet' href='file:///opt/software-store/resources/style.css'></head><body>"
            html += f"""
            <div class='details-card'>
                <img src='file:///opt/software-store/resources/icons/{pkg['name']}.png' class='icon' onerror="this.src='file:///opt/software-store/resources/icons/default.png'">
                <h2>{pkg['name']} ({pkg['version']})</h2>
                <p>{pkg.get('description', '')}</p>
                {'<button onclick="window.location.href=\'app-action://open/%s\'">%s</button>' % (pkg['name'], _('Abrir')) if installed else '<button onclick="window.location.href=\'app-action://install/%s\'">%s</button>' % (pkg['name'], _('Instalar'))}
                {'<button onclick="window.location.href=\'app-action://remove/%s\'">%s</button>' % (pkg['name'], _('Remover')) if installed else ''}
            </div>
            """
            html += "</body></html>"
            self.webview.load_html(html, "file:///opt/software-store/resources/details.html")

    def on_decide_policy(self, webview, decision, decision_type):
        uri = decision.get_request().get_uri()
        if uri.startswith("app-action://"):
            action, pkg_name = uri.replace("app-action://", "").split("/", 1)
            if action == "install":
                from apt_utils import install_package
                install_package(pkg_name)
                self.load_search_results(pkg_name)
            elif action == "remove":
                from apt_utils import remove_package
                remove_package(pkg_name)
                self.load_search_results(pkg_name)
            elif action == "open":
                self.open_package(pkg_name)
            elif action == "details":
                self.load_details_page(pkg_name)
            decision.ignore()
            return True
        return False

    def open_package(self, pkg_name):
        import subprocess
        special = get_special_exec(pkg_name)
        cmd = [pkg_name]
        if special:
            cmd.append(special)
        subprocess.Popen(cmd)

    def remove_package(self, pkg_name, parent):
        self.status_label.set_text(_("Removendo..."))
        self.progress.set_visible(True)
        self.progress.set_fraction(0.1)
        if self.btn_open:
            self.btn_open.hide()
        if self.btn_remove:
            self.btn_remove.hide()
        from apt_utils import remove_package
        def on_finish():
            self.progress.set_fraction(1.0)
            self.status_label.set_text(_("Remoção concluída!"))
            self.progress.set_visible(False)
            if self.btn_install:
                self.btn_install.show()
            self.show_all()
            parent.show_search_results(pkg_name)
        remove_package(pkg_name, progress_callback=self._progress_callback, finish_callback=on_finish)

    def _progress_callback(self, frac):
        self.progress.set_fraction(frac)
        while Gtk.events_pending():
            Gtk.main_iteration()

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
        self.status_label.set_text(_("Buscando pacotes..."))
        while Gtk.events_pending():
            Gtk.main_iteration()
        self.results_box.foreach(lambda w: self.results_box.remove(w))
        pkgs = search_packages(term, literal=False)
        self.status_label.set_text("")
        if not pkgs:
            self.results_box.pack_start(Gtk.Label(label=_("Nenhum pacote encontrado.")), False, False, 0)
        else:
            for pkg in pkgs:
                card = PackageCard(pkg, self)
                self.results_box.pack_start(card, False, False, 0)
        self.results_box.show_all()

    def open_details(self, pkg):
        dialog = PackageDetailsDialog(self, pkg)
        dialog.run()
        dialog.destroy()

    def open_package(self, pkg_name):
        import subprocess
        special = get_special_exec(pkg_name)
        cmd = [pkg_name]
        if special:
            cmd.append(special)
        subprocess.Popen(cmd)

    def install_package(self, pkg_name):
        from apt_utils import install_package
        install_package(pkg_name)
        self.show_search_results(pkg_name)

    def remove_package(self, pkg_name):
        from apt_utils import remove_package
        remove_package(pkg_name)
        self.show_search_results(pkg_name)

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

