import os
import subprocess
from django.core.management.base import BaseCommand

# Liste des modules (remplace par tes modules)
MODULES = {
    "module1": "/chemin/vers/module1",
    "module2": "/chemin/vers/module2",
    "module3": "/chemin/vers/module3",
}

class Command(BaseCommand):
    help = "Met à jour un module ou tous les modules via Git"

    def add_arguments(self, parser):
        parser.add_argument("module", type=str, help="Nom du module à mettre à jour ou 'all' pour tout")

    def handle(self, *args, **options):
        module_name = options["module"]

        if module_name == "all":
            self.stdout.write(self.style.SUCCESS("🔄 Mise à jour de tous les modules..."))
            for mod in MODULES.keys():
                self.update_module(mod)
        elif module_name in MODULES:
            self.update_module(module_name)
        else:
            self.stdout.write(self.style.ERROR(f"❌ Le module '{module_name}' n'existe pas !"))

    def update_module(self, module):
        module_path = MODULES[module]

        if not os.path.isdir(module_path):
            self.stdout.write(self.style.ERROR(f"❌ Le dossier du module '{module}' n'existe pas !"))
            return

        self.stdout.write(self.style.SUCCESS(f"🔄 Mise à jour du module: {module}..."))

        try:
            # Aller dans le dossier du module
            os.chdir(module_path)

            # Exécuter les commandes Git
            subprocess.run(["git", "fetch", "upstream"], check=True)
            subprocess.run(["git", "rebase", "upstream/develop"], check=True)
            subprocess.run(["git", "push", "origin", "dev"], check=True)

            self.stdout.write(self.style.SUCCESS(f"✅ {module} mis à jour avec succès !"))

        except subprocess.CalledProcessError as e:
            self.stdout.write(self.style.ERROR(f"❌ Erreur lors de la mise à jour de {module}: {e}"))

        finally:
            # Revenir au dossier du projet Django
            os.chdir(os.path.dirname(os.path.abspath(__file__)))




# Utilisation 

# python manage.py update_modules all

# python manage.py update_modules module1
