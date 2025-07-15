import subprocess
import json

def search_packages(term):
    # Busca pacotes usando apt-cache
    result = subprocess.run(["apt-cache", "search", term], capture_output=True, text=True)
    pkgs = []
    for line in result.stdout.splitlines():
        if line:
            name, desc = line.split(" - ", 1)
            pkgs.append({"name": name, "description": desc, "version": get_package_version(name)})
    return pkgs

def get_package_version(name):
    result = subprocess.run(["apt-cache", "policy", name], capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if "Candidate:" in line:
            return line.split(":", 1)[1].strip()
    return ""

def install_package(name, dialog=None):
    # ...desabilitar botão, mostrar barra de progresso...
    subprocess.run(["apt-get", "install", "-y", name])
    # ...atualizar UI...

def remove_package(name):
    subprocess.run(["apt-get", "remove", "-y", name])
    # ...atualizar UI...

def is_installed(name):
    result = subprocess.run(["dpkg", "-s", name], capture_output=True, text=True)
    return "Status: install ok installed" in result.stdout

def update_packages():
    subprocess.run(["apt-get", "update"])
    result = subprocess.run(["apt-get", "-s", "upgrade"], capture_output=True, text=True)
    updates = []
    for line in result.stdout.splitlines():
        if line.startswith("Inst "):
            updates.append(line)
    return updates

def get_special_exec(name):
    with open("special_exec.json") as f:
        data = json.load(f)
    return data.get(name, None)
