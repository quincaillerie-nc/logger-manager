# 📝 LOGGER MODULE - Gestion centralisée des logs Python

## 📌 Présentation

Ce module Python permet de créer facilement un système de logs standardisé pour les scripts internes.

Il permet :

- de générer automatiquement un nom de fichier log horodaté,
- de créer automatiquement un dossier de logs par script appelant,
- d’écrire les logs dans un fichier,
- d’afficher les logs importants dans la console,
- d’utiliser le module officiel Python `logging`.

Ce module est particulièrement utile pour les scripts métiers automatisés, les traitements DBF, les exports Excel, les envois d’emails et les scripts planifiés.

---

## 🎯 Objectif du module

L’objectif est de standardiser les logs dans tous les scripts Python internes.

Au lieu d’utiliser uniquement :

```python
print("message")
```

on utilise un vrai logger :

```python
logger.info("Traitement terminé")
logger.error("Erreur pendant le traitement")
```

Cela permet de conserver un historique complet des traitements.

---

## 🏗️ Structure recommandée

Exemple d’organisation du projet :

```bash
dev/
│
├── modules/
│   │
│   └── logger/
│       └── logger.py
│
├── scripts/
│   │
│   └── com_isee/
│       └── com_isee.py
│
└── log_scripts/
    │
    └── com_isee/
        └── com_isee_20260518_083015.log
```

---

## ⚙️ Fonctionnement général

Le module fonctionne en trois étapes :

1. génération d’un nom de fichier log,
2. génération du chemin de stockage,
3. initialisation du logger fichier + console.

---

## 📦 Dépendances

Ce module utilise uniquement des bibliothèques standards Python :

```python
from pathlib import Path
from datetime import datetime
import logging
```

Aucune installation externe n’est nécessaire.

---

# 🚀 Fonctions disponibles

---

## 1. `generer_nom_log()`

### Description

Génère automatiquement un nom de fichier log avec un horodatage.

### Signature

```python
generer_nom_log(prefixe: str = "log") -> str
```

### Exemple

```python
nom_log = generer_nom_log("com_isee")
print(nom_log)
```

Résultat possible :

```text
com_isee_20260518_083015.log
```

### Utilité

Cette fonction permet d’éviter d’écraser les anciens fichiers logs.

Chaque exécution du script crée un fichier différent.

---

## 2. `generer_chemin_log()`

### Description

Génère automatiquement le chemin complet du fichier log.

Le module détecte le script appelant grâce à :

```python
inspect.stack()
```

Puis il crée un dossier dédié dans :

```bash
log_scripts/
```

### Signature

```python
generer_chemin_log(nom_log: str) -> Path
```

### Exemple

```python
chemin = generer_chemin_log("com_isee_20260518_083015.log")
print(chemin)
```

Résultat possible :

```text
C:/Users/Support/Desktop/dev/log_scripts/com_isee/com_isee_20260518_083015.log
```

---

## 3. `init_logger()`

### Description

Initialise un logger complet avec :

- un handler fichier,
- un handler console,
- un format standardisé,
- un niveau `DEBUG` pour le fichier,
- un niveau `INFO` pour la console.

### Signature

```python
init_logger(nom_module: str = None) -> logging.Logger
```

### Exemple simple

```python
from logger import init_logger

logger = init_logger()

logger.info("Début du script")
logger.warning("Attention : donnée manquante")
logger.error("Erreur lors du traitement")
```

---

# 📊 Niveaux de logs

Le module utilise les niveaux standards de Python.

| Niveau | Usage recommandé | Visible console | Écrit fichier |
|---|---|---:|---:|
| DEBUG | détail technique | Non | Oui |
| INFO | étape normale | Oui | Oui |
| WARNING | avertissement | Oui | Oui |
| ERROR | erreur | Oui | Oui |
| CRITICAL | erreur critique | Oui | Oui |

---

## Exemple

```python
logger.debug("Chargement du fichier article.dbf")
logger.info("Fichier chargé avec succès")
logger.warning("Aucune donnée trouvée pour une référence")
logger.error("Impossible d’envoyer l’email")
logger.critical("Arrêt complet du script")
```

---

# 🧾 Format des logs

Le format utilisé est :

```text
YYYY-MM-DD HH:MM:SS - nom_module - LEVEL - message
```

Exemple :

```text
2026-05-18 08:30:15 - com_isee - INFO - Début du script
2026-05-18 08:30:20 - com_isee - ERROR - Erreur pendant l’envoi email
```

---

# 📁 Organisation automatique des dossiers

Le module crée automatiquement un dossier par script appelant.

Exemple :

Si le script appelant est :

```bash
scripts/com_isee/com_isee.py
```

Les logs seront stockés dans :

```bash
log_scripts/com_isee/
```

Si le script appelant est :

```bash
scripts/import_stock/import_stock.py
```

Les logs seront stockés dans :

```bash
log_scripts/import_stock/
```

---

# 🧠 Exemple d’intégration dans un script métier

```python
# -*- coding: utf-8 -*-
from logger import init_logger

logger = init_logger()

def main():
    logger.info("Début du traitement")

    try:
        logger.debug("Chargement des données")
        # traitement ici

        logger.info("Traitement terminé avec succès")

    except Exception as e:
        logger.error(f"Erreur : {e}", exc_info=True)

if __name__ == "__main__":
    main()
```

---

# 🔥 Utilisation avec traceback automatique

Pour enregistrer le détail complet d’une erreur :

```python
try:
    resultat = 10 / 0
except Exception as e:
    logger.error(f"Erreur détectée : {e}", exc_info=True)
```

Le fichier log contiendra alors la trace complète de l’erreur.

---

# ✅ Avantages

Ce module permet :

- une meilleure traçabilité,
- une maintenance simplifiée,
- un suivi des erreurs,
- un historique des traitements,
- une meilleure qualité professionnelle des scripts,
- une intégration facile dans tous les scripts internes.

---

# ⚠️ Point important

Le logger ajoute des handlers à chaque appel de `init_logger()`.

Si la fonction est appelée plusieurs fois dans le même script, les logs peuvent être affichés plusieurs fois.

## Amélioration recommandée

Ajouter une vérification :

```python
if logger.handlers:
    return logger
```

Version améliorée :

```python
def init_logger(nom_module: str = None) -> logging.Logger:
    if nom_module is None:
        import inspect
        nom_module = Path(inspect.stack()[1].filename).stem

    logger = logging.getLogger(nom_module)

    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    nom_fichier = generer_nom_log(nom_module)
    chemin_log = generer_chemin_log(nom_fichier)

    handler_fichier = logging.FileHandler(chemin_log, encoding="utf-8")
    handler_fichier.setLevel(logging.DEBUG)

    handler_console = logging.StreamHandler()
    handler_console.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    handler_fichier.setFormatter(formatter)
    handler_console.setFormatter(formatter)

    logger.addHandler(handler_fichier)
    logger.addHandler(handler_console)

    return logger
```

---

# 🛠️ Exemple de module complet

```python
# -*- coding: utf-8 -*-
from pathlib import Path
from datetime import datetime
import logging


def generer_nom_log(prefixe: str = "log") -> str:
    horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefixe}_{horodatage}.log"


def generer_chemin_log(nom_log: str) -> Path:
    import inspect
    appelant = Path(inspect.stack()[1].filename).stem
    base = Path(__file__).parent.parent.parent
    dossier = base / "log_scripts" / appelant
    dossier.mkdir(parents=True, exist_ok=True)
    return dossier / nom_log


def init_logger(nom_module: str = None) -> logging.Logger:
    if nom_module is None:
        import inspect
        nom_module = Path(inspect.stack()[1].filename).stem

    logger = logging.getLogger(nom_module)

    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    nom_fichier = generer_nom_log(nom_module)
    chemin_log = generer_chemin_log(nom_fichier)

    handler_fichier = logging.FileHandler(chemin_log, encoding="utf-8")
    handler_fichier.setLevel(logging.DEBUG)

    handler_console = logging.StreamHandler()
    handler_console.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    handler_fichier.setFormatter(formatter)
    handler_console.setFormatter(formatter)

    logger.addHandler(handler_fichier)
    logger.addHandler(handler_console)

    return logger
```

---

# 📄 `.gitignore` recommandé

```gitignore
__pycache__/
*.pyc
.env
.venv/
venv/
*.log
log_scripts/
```

---

# 🚀 Initialisation Git

Depuis le dossier du module :

```powershell
git init
git add .
git commit -m "initial commit"
```

---

# 🔗 Ajouter le dépôt distant en SSH

Méthode recommandée :

```powershell
git remote add origin git@github.com:quincaillerie-nc/logger.git
git branch -M main
git push -u origin main
```

Si le remote existe déjà :

```powershell
git remote set-url origin git@github.com:quincaillerie-nc/logger.git
git push -u origin main
```

---

# 🧪 Vérifier le remote

```powershell
git remote -v
```

Résultat attendu :

```text
origin  git@github.com:quincaillerie-nc/logger.git (fetch)
origin  git@github.com:quincaillerie-nc/logger.git (push)
```

---

# 🧼 Nettoyer les fichiers inutiles

Si des fichiers Python compilés ont été ajoutés par erreur :

```powershell
git rm -r --cached __pycache__
git add .
git commit -m "clean repository files"
git push
```

---

# 🧩 Exemple d’utilisation dans `com_isee`

```python
logger = init_logger("com_isee")

logger.info("Début du script ComISEE")
logger.debug("Chargement du DBF article")
logger.info("Fichier Excel généré")
logger.error("Erreur pendant l’envoi email")
```

---

# 📌 Bonnes pratiques

## À faire

- utiliser `logger.info()` pour les grandes étapes,
- utiliser `logger.debug()` pour les détails techniques,
- utiliser `logger.error(..., exc_info=True)` dans les blocs `except`,
- créer un fichier log par exécution,
- ignorer les fichiers logs dans Git.

## À éviter

- utiliser uniquement `print()`,
- versionner les fichiers `.log`,
- appeler plusieurs fois `init_logger()` inutilement,
- cacher les erreurs sans les logger.

---

# 📜 Conclusion

Ce module permet d’ajouter une gestion professionnelle des logs à tous les scripts Python internes.

Il améliore :

- le suivi des traitements,
- la résolution des erreurs,
- la maintenance,
- la traçabilité,
- la qualité globale du projet.
