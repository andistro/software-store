from ui.package_details import PackageDetailsDialog
from apt_utils import search_packages

def handle_deeplink(url):
    # Exemplo: software-store://pkg?search=inkscape
    import urllib.parse
    parsed = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qs(parsed.query)
    term = query.get("search", [""])[0]
    pkgs = search_packages(term)
    if pkgs:
        # Mostra janela modal com detalhes do pacote
        import gi
        gi.require_version("Gtk", "3.0")
        from gi.repository import Gtk
        win = Gtk.Window()
        dialog = PackageDetailsDialog(win, pkgs[0])
        dialog.run()
        dialog.destroy()
    else:
        # Pergunta se deseja pesquisar pelo termo
        # ...mostrar diálogo informando que não achou...
        pass
