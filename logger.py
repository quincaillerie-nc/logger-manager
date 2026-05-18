# -*- coding: utf-8 -*-
import logging
from pathlib import Path
from datetime import datetime


def generer_nom_log(prefixe: str = "log") -> str:
    horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefixe}_{horodatage}.log"


def init_logger(nom_module: str) -> logging.Logger:
    """
    Initialise un logger avec :
    - fichier dans dev/log_scripts/<nom_module>/
    - console
    - garde anti-doublon

    Paramètres
    ----------
    nom_module : str — nom du script (ex: "com_isee")
    """
    logger = logging.getLogger(nom_module)

    # Garde anti-doublon
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    # Dossier log : dev/log_scripts/<nom_module>/
    base    = Path(__file__).resolve().parent.parent.parent
    dossier = base / "log_scripts" / nom_module
    dossier.mkdir(parents=True, exist_ok=True)

    nom_fichier = generer_nom_log(nom_module)
    chemin_log  = dossier / nom_fichier

    # Handler fichier
    handler_fichier = logging.FileHandler(chemin_log, encoding="utf-8")
    handler_fichier.setLevel(logging.DEBUG)

    # Handler console
    handler_console = logging.StreamHandler()
    handler_console.setLevel(logging.INFO)

    # Format
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler_fichier.setFormatter(formatter)
    handler_console.setFormatter(formatter)

    logger.addHandler(handler_fichier)
    logger.addHandler(handler_console)

    return logger