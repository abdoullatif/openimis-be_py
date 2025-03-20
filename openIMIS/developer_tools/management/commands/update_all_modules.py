import os
import subprocess
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = "Met à jour tous les modules Git présents dans un dossier spécifique."

    def add_arguments(self, parser):
        parser.add_argument("src_folder", type=str, help="Chemin du dossier contenant les modules")

    def handle(self, *args, **kwargs):
        src_folder = kwargs["src_folder"]

        self.stdout.write(f"🔄 Recherche des modules dans '{src_folder}'...\n")

        # Vérifier si le dossier existe
        if not os.path.isdir(src_folder):
            raise CommandError(f"❌ Le dossier {src_folder} n'existe pas.")

        # Parcourir les dossiers dans src/
        for module in os.listdir(src_folder):
            module_path = os.path.join(src_folder, module)

            # Vérifier si c'est un dossier et s'il contient un dépôt Git
            if os.path.isdir(module_path) and os.path.isdir(os.path.join(module_path, ".git")):
                self.update_all_module(module_path)

    def update_all_module(self, module_path):
        """ Met à jour un module en exécutant les commandes Git nécessaires. """
        module_name = os.path.basename(module_path)
        self.stdout.write(f"🔄 Mise à jour du module: {module_name}...\n")

        try:
            # Se positionner dans le dossier du module
            os.chdir(module_path)

            # Ajouter 'upstream' s'il n'existe pas encore
            # subprocess.run("git remote add upstream $(git config --get remote.origin.url)", shell=True, check=True)

            # Récupérer les dernières mises à jour
            subprocess.run("git fetch upstream", shell=True, check=True)

            # Rebaser la branche develop sur upstream/develop
            subprocess.run("git rebase upstream/develop", shell=True, check=True)

            self.stdout.write(self.style.SUCCESS(f"✅ {module_name} mis à jour avec succès !\n"))

        except subprocess.CalledProcessError as e:
            self.stderr.write(self.style.ERROR(f"❌ Erreur lors de la mise à jour du module {module_name}: {e}\n"))

        finally:
            # Revenir au dossier initial
            os.chdir("..")


# utilisation 
# 
# python manage.py update_all_modules ../src