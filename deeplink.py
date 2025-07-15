from ui.package_details import PackageDetailsDialog
from apt_utils import search_packages

def handle_deeplink(url):
    import urllib.parse
    parsed = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qs(parsed.query)
    term = query.get("search", [""])[0]
    pkgs = search_packages(term)
    import gi
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk
    win = Gtk.Window()
    win.set_default_size(320, 240)
    win.show()
    if pkgs:
        dialog = PackageDetailsDialog(win, pkgs[0])
        dialog.run()
        dialog.destroy()
    else:
        msg = Gtk.MessageDialog(win, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK,
                                f"Pacote '{term}' não encontrado. Deseja pesquisar pelo termo?")
        msg.run()
        msg.destroy()
    win.destroy()
