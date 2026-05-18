# -*- coding: utf-8 -*-
from pathlib import Path
from datetime import datetime
import logging


def generer_nom_log(prefixe: str = "log") -> str:
    """Génère un nom de fichier log avec horodatage"""
    horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefixe}_{horodatage}.log"


def generer_chemin_log(nom_log: str) -> Path:
    """Génère le chemin du fichier log avec structure de dossiers"""
    import inspect
    appelant = Path(inspect.stack()[1].filename).stem
    base = Path(__file__).parent.parent.parent
    dossier = base / "log_scripts" / appelant
    dossier.mkdir(parents=True, exist_ok=True)
    return dossier / nom_log


def init_logger(nom_module: str = None) -> logging.Logger:
    """Initialise un logger avec fichier et console"""
    if nom_module is None:
        import inspect
        nom_module = Path(inspect.stack()[1].filename).stem
    
    logger = logging.getLogger(nom_module)
    logger.setLevel(logging.DEBUG)
    
    # Fichier log
    nom_fichier = generer_nom_log(nom_module)
    chemin_log = generer_chemin_log(nom_fichier)
    
    handler_fichier = logging.FileHandler(chemin_log, encoding='utf-8')
    handler_fichier.setLevel(logging.DEBUG)
    
    # Console
    handler_console = logging.StreamHandler()
    handler_console.setLevel(logging.INFO)
    
    # Format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler_fichier.setFormatter(formatter)
    handler_console.setFormatter(formatter)
    
    logger.addHandler(handler_fichier)
    logger.addHandler(handler_console)
    
    return logger
