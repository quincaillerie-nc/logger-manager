# -*- coding: utf-8 -*-
"""
================================================================================
MODULE : logger-manager / logger.py
================================================================================
Initialise un logger Python standard avec :
- handler fichier  (niveau DEBUG) → dev/log_scripts/<script>/
- handler console  (niveau INFO)
- garde anti-doublon (handlers vérifiés avant ajout)
================================================================================
"""

from pathlib import Path
from datetime import datetime
import logging


# =====================================================
# FONCTIONS PUBLIQUES
# =====================================================
def generer_nom_log(prefixe: str = "log") -> str:
    """
    Génère un nom de fichier log horodaté.

    Exemple : generer_nom_log("com_isee")
              → "com_isee_20260518_083015.log"
    """
    horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefixe}_{horodatage}.log"


def generer_chemin_log(nom_log: str) -> Path:
    """
    Génère le chemin du fichier log dans dev/log_scripts/<script_appelant>/.
    Crée le dossier automatiquement.
    """
    import inspect
    appelant = Path(inspect.stack()[1].filename).stem
    base     = Path(__file__).resolve().parent.parent.parent
    dossier  = base / "log_scripts" / appelant
    dossier.mkdir(parents=True, exist_ok=True)
    return dossier / nom_log


def init_logger(nom_module: str = None) -> logging.Logger:
    """
    Initialise et retourne un logger complet.

    Si appelé plusieurs fois avec le même nom, retourne le logger existant
    sans ajouter de handlers en double.

    Paramètres
    ----------
    nom_module : str, optionnel
        Nom du logger. Si None, utilise le nom du script appelant.

    Retourne
    --------
    logging.Logger
    """
    import inspect

    if nom_module is None:
        nom_module = Path(inspect.stack()[1].filename).stem

    logger = logging.getLogger(nom_module)

    # Garde anti-doublon : si handlers déjà présents, on retourne tel quel
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    # --- Handler fichier ---
    nom_fichier  = generer_nom_log(nom_module)
    chemin_log   = generer_chemin_log(nom_fichier)

    handler_fichier = logging.FileHandler(chemin_log, encoding="utf-8")
    handler_fichier.setLevel(logging.DEBUG)

    # --- Handler console ---
    handler_console = logging.StreamHandler()
    handler_console.setLevel(logging.INFO)

    # --- Format commun ---
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler_fichier.setFormatter(formatter)
    handler_console.setFormatter(formatter)

    logger.addHandler(handler_fichier)
    logger.addHandler(handler_console)

    return logger
