import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib
import gettext
gettext.bindtextdomain('software-store', '/opt/software-store/i18n')
gettext.textdomain('software-store')
_ = gettext.gettext

from apt_utils import install_package, remove_package, is_installed, get_special_exec

class PackageDetailsDialog(Gtk.Dialog):
    def __init__(self, parent, pkg):
        Gtk.Dialog.__init__(self, title=pkg['name'], transient_for=parent, flags=0)
        self.set_default_size(320, 240)
        box = self.get_content_area()

        icon_theme = Gtk.IconTheme.get_default()
        icon_name = pkg.get('name', 'application-x-executable')
        if icon_theme.has_icon(icon_name):
            icon = Gtk.Image.new_from_icon_name(icon_name, Gtk.IconSize.DIALOG)
        else:
            icon = Gtk.Image.new_from_icon_name("application-x-executable", Gtk.IconSize.DIALOG)
        box.add(icon)

        box.add(Gtk.Label(label=f"{pkg['name']} ({pkg['version']})"))

        self.status_label = Gtk.Label(label="")
        box.add(self.status_label)

        self.progress = Gtk.ProgressBar()
        self.progress.set_visible(False)
        box.add(self.progress)

        if is_installed(pkg['name']):
            btn_open = Gtk.Button(label=_("Abrir"))
            btn_open.connect("clicked", lambda b: self.open_package(pkg['name']))
            box.add(btn_open)
            btn_remove = Gtk.Button(label=_("Remover"))
            btn_remove.connect("clicked", lambda b: self.remove_package(pkg['name']))
            box.add(btn_remove)
        else:
            btn_install = Gtk.Button(label=_("Instalar"))
            btn_install.connect("clicked", lambda b: self.install_package(pkg['name']))
            box.add(btn_install)

        self.show_all()

    def open_package(self, pkg_name):
        import subprocess
        special = get_special_exec(pkg_name)
        cmd = [pkg_name]
        if special:
            cmd.append(special)
        subprocess.Popen(cmd)
        self.destroy()

    def install_package(self, pkg_name):
        self.status_label.set_text(_("Instalando..."))
        self.progress.set_visible(True)
        self.progress.set_fraction(0.1)
        GLib.idle_add(self._install_pkg, pkg_name)

    def _install_pkg(self, pkg_name):
        install_package(pkg_name, progress_callback=self._progress_callback)
        self.progress.set_fraction(1.0)
        self.status_label.set_text(_("Instalação concluída!"))
        return False

    def remove_package(self, pkg_name):
        self.status_label.set_text(_("Removendo..."))
        self.progress.set_visible(True)
        self.progress.set_fraction(0.1)
        GLib.idle_add(self._remove_pkg, pkg_name)

    def _remove_pkg(self, pkg_name):
        remove_package(pkg_name, progress_callback=self._progress_callback)
        self.progress.set_fraction(1.0)
        self.status_label.set_text(_("Remoção concluída!"))
        return False

    def _progress_callback(self, frac):
        self.progress.set_fraction(frac)
        while Gtk.events_pending():
            Gtk.main_iteration()
