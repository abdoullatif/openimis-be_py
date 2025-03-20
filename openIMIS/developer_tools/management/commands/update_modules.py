import os
import subprocess
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Met à jour tous les modules Git dans un dossier donné"

    def add_arguments(self, parser):
        parser.add_argument("modules_dir", type=str, help="Chemin du dossier contenant les modules")

    def handle(self, *args, **options):
        modules_dir = options["modules_dir"]

        if not os.path.isdir(modules_dir):
            self.stdout.write(self.style.ERROR(f"❌ Le dossier '{modules_dir}' n'existe pas !"))
            return

        self.stdout.write(self.style.SUCCESS(f"🔄 Recherche des modules dans '{modules_dir}'..."))

        for module in os.listdir(modules_dir):
            module_path = os.path.join(modules_dir, module)
            if os.path.isdir(module_path) and os.path.exists(os.path.join(module_path, ".git")):
                self.update_module(module, module_path)

    def update_module(self, module, module_path):
        self.stdout.write(self.style.SUCCESS(f"🔄 Mise à jour du module: {module}..."))

        try:
            # Aller dans le dossier du module
            os.chdir(module_path)

            # Exécuter les commandes Git
            subprocess.run(["git", "fetch", "upstream"], check=True)
            subprocess.run(["git", "rebase", "upstream/develop"], check=True)
            # subprocess.run(["git", "push", "origin", "dev"], check=True)

            self.stdout.write(self.style.SUCCESS(f"✅ {module} mis à jour avec succès !"))

        except subprocess.CalledProcessError as e:
            self.stdout.write(self.style.ERROR(f"❌ Erreur lors de la mise à jour de {module}: {e}"))

        finally:
            # Revenir au dossier du projet Django
            os.chdir(os.path.dirname(os.path.abspath(__file__)))

