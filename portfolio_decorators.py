import functools
import logging
import time

# Configuration du logger (portfolio.log) en utilisant le système de logging Python
logging.basicConfig(
    filename="portfolio.log", # messages de logs enregistrés dans ce fichier
    level=logging.INFO, # seuil minimal de gravité des messages que je veux conserver
    format="%(asctime)s - %(levelname)s - %(message)s" # date et heure - niveau du message - texte passé dans logging.info
)

def logger_portfolio(func):
    """Log les appels de méthodes du portfolio"""
    @functools.wraps(func) # décorateur utilitaire qui conserve nom, docstring et métadonnées de la func
    def wrapper(*args, **kwargs):
        logging.info(f"Appel de {func.__name__} avec args={args[1:]} et kwargs={kwargs}") # 1: ignore le 1er arg (self)
        try:
            result = func(*args, **kwargs)
            logging.info(f"{func.__name__} -> Succès, résutat : {result}")
            return result
        except Exception as e:
            logging.error(f"{func.__name__} -> Erreur : {e}")
            raise
    return wrapper

def chronometre(func):
    """Mesure le temps d'exécution d'une fonction"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        duration = (end - start) * 1000 # en ms
        print(f"[Chronomètre] {func.__name__} exécutée en {duration:.2f} ms")
        return result
    return wrapper

def cache_prix(func):
    """Cache les résultats (clé = args + kwargs) pour éviter les recalculs"""
    cache = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = (args[1:], frozenset(kwargs.items())) # clé unique pour identifier un appel de fonction ; frozenset rend les args immuables
        if key in cache:
            print(f"[Cache] Résultat trouvé pour {func.__name__} avec {key}") # évite de recalculer si la clé existe déjà
            return cache[key]
        result = func(*args, **kwargs)
        cache[key] = result # sauvegarde le résultat dans cache pour le réutiliser
        print(f"[Cache] Résultat sauvegardé pour {func.__name__} avec {key}")
        return result
    return wrapper