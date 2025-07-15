import subprocess
import json
import threading

def search_packages(term, literal=False):
    # Busca literal: ^termo$ (apenas para deeplink)
    if literal:
        result = subprocess.run(["apt-cache", "search", f"^{term}$"], capture_output=True, text=True)
    else:
        # Busca não literal: retorna todos que contenham o termo
        result = subprocess.run(["apt-cache", "search", term], capture_output=True, text=True)
    pkgs = []
    for line in result.stdout.splitlines():
        if line.strip():
            parts = line.split(" - ", 1)
            if len(parts) == 2:
                name, desc = parts
                pkgs.append({"name": name.strip(), "description": desc.strip(), "version": get_package_version(name.strip())})
    return pkgs

def get_package_version(name):
    result = subprocess.run(["apt-cache", "policy", name], capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if "Candidate:" in line:
            return line.split(":", 1)[1].strip()
    return ""

def install_package(name, progress_callback=None, finish_callback=None):
    def run_install():
        if progress_callback:
            progress_callback(0.2)
        subprocess.run(["apt-get", "install", "-y", name])
        patch_desktop_exec(name)
        if progress_callback:
            progress_callback(1.0)
        if finish_callback:
            finish_callback()
    t = threading.Thread(target=run_install)
    t.start()

def remove_package(name, progress_callback=None, finish_callback=None):
    def run_remove():
        if progress_callback:
            progress_callback(0.2)
        subprocess.run(["apt-get", "remove", "-y", name])
        if progress_callback:
            progress_callback(1.0)
        if finish_callback:
            finish_callback()
    t = threading.Thread(target=run_remove)
    t.start()

def update_packages():
    subprocess.run(["apt-get", "update"])
    result = subprocess.run(["apt-get", "-s", "upgrade"], capture_output=True, text=True)
    updates = []
    for line in result.stdout.splitlines():
        if line.startswith("Inst "):
            updates.append(line)
    return updates

def is_installed(name):
    result = subprocess.run(["dpkg", "-s", name], capture_output=True, text=True)
    return "Status: install ok installed" in result.stdout

def get_special_exec(name):
    with open("special_exec.json") as f:
        data = json.load(f)
    return data.get(name, None)

def patch_desktop_exec(pkg_name):
    import os
    special = get_special_exec(pkg_name)
    if not special:
        return
    desktop_dir = "/usr/share/applications"
    desktop_file = os.path.join(desktop_dir, f"{pkg_name}.desktop")
    if not os.path.exists(desktop_file):
        # Tenta encontrar arquivo .desktop pelo nome do pacote
        for f in os.listdir(desktop_dir):
            if f.startswith(pkg_name) and f.endswith(".desktop"):
                desktop_file = os.path.join(desktop_dir, f)
                break
    if os.path.exists(desktop_file):
        with open(desktop_file, "r") as f:
            lines = f.readlines()
        with open(desktop_file, "w") as f:
            for line in lines:
                if line.startswith("Exec=") and special not in line:
                    line = line.rstrip() + f" {special}\n"
                f.write(line)
