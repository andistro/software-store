from ui.package_details import PackageDetailsDialog
from apt_utils import search_packages

def handle_deeplink(url):
    import urllib.parse
    import gi
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk

    parsed = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qs(parsed.query)
    term = query.get("search", [""])[0]

    win = Gtk.Window()
    win.set_default_size(320, 240)
    status = Gtk.Label(label=f"Buscando pacote '{term}'...")
    vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vbox.set_margin_top(16)
    vbox.set_margin_bottom(16)
    vbox.set_margin_start(16)
    vbox.set_margin_end(16)
    vbox.pack_start(status, False, False, 0)
    win.add(vbox)
    win.show_all()

    pkgs = search_packages(term, literal=True)
    if not pkgs:
        # Tenta busca não literal se literal falhar
        pkgs = search_packages(term, literal=False)

    if pkgs:
        status.set_text(f"Pacote '{pkgs[0]['name']}' encontrado.")
        dialog = PackageDetailsDialog(win, pkgs[0])
        dialog.run()
        dialog.destroy()
    else:
        status.set_text(f"Pacote '{term}' não encontrado.")
        msg = Gtk.MessageDialog(win, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK,
                                f"Pacote '{term}' não encontrado. Deseja pesquisar pelo termo?")
        msg.run()
        msg.destroy()
    win.destroy()
