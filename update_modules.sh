#!/bin/bash

# Liste des modules (ajoute tes modules ici)
MODULES=("module1" "module2" "module3") # Remplace par les noms de tes modules

# Vérifie si un argument est fourni
if [ -z "$1" ]; then
    echo "Usage: $0 <module_name> | all"
    exit 1
fi

update_module() {
    MODULE=$1
    MODULE_PATH="chemin/vers/$MODULE"  # Remplace par le chemin réel des modules

    if [ -d "$MODULE_PATH" ]; then
        echo "🔄 Mise à jour du module: $MODULE"
        cd "$MODULE_PATH" || exit

        # Récupérer les dernières mises à jour du dépôt central
        git fetch upstream
        git rebase upstream/develop

        # Pousser les modifications sur ton fork
        git push origin dev

        cd - > /dev/null  # Revenir au dossier précédent
    else
        echo "❌ Le module $MODULE n'existe pas !"
    fi
}

if [ "$1" == "all" ]; then
    # Mise à jour de tous les modules
    for MOD in "${MODULES[@]}"; do
        update_module "$MOD"
    done
else
    # Mise à jour d'un seul module
    update_module "$1"
fi

echo "✅ Mise à jour terminée !"
