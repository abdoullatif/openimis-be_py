import json
import subprocess

# Charger le fichier JSON
with open("openimis-dev.json", "r") as file:
    data = json.load(file)

# Installer chaque module
for module in data["modules"]:
    module_name = module["name"]
    module_path = module["pip"].split(" ")[1]  # Extraire le chemin du module
    print(f"Installation du module {module_name}...")
    try:
        subprocess.run(["pip", "install", "-e", module_path], check=True)
        print(f"Module {module_name} installé avec succès.")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'installation du module {module_name}: {e}")


# utilisation 
# use openIMIS dev
# python install_modules.py
# pip list 