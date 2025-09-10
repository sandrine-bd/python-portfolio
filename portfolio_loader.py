import csv
import json

from portfolio_structures import convertir_vers_positions, afficher_positions

def lire_portfolio_csv(nom_fichier):
    """ Charge le portfolio depuis un fichier CSV avec colonnes """
    raw_data = []
    try:
        with open(nom_fichier, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for i, ligne in enumerate(reader, start=1):
                try:
                    raw_data.append({
                        "symbol": ligne.get("symbol", "").strip().upper(),
                        "quantity": int(ligne.get("quantity", 0)),
                        "purchase_price": float(ligne.get("purchase_price", 0.0)),
                        "purchase_date": ligne.get("purchase_date", "N/A").strip()
                    })
                except Exception as e:
                    print(f"[Ligne {i}] Erreur inattendue : {e} -> ignorée")
    except FileNotFoundError:
        print(f"Erreur : le fichier {nom_fichier} n'a pas été trouvé.")
    return convertir_vers_positions(raw_data)

def lire_portfolio_json(nom_fichier):
    """ Charge le portfolio depuis un fichier JSON avec métadonnées """
    raw_data = []
    try:
        with open(nom_fichier, mode='r', encoding='utf-8') as file:
            data = json.load(file)
            positions = data.get("positions", [])
            for i, pos in enumerate(positions, start=1):
                try:
                    raw_data.append({
                        "symbol": str(pos.get("symbol", "")).strip().upper(),
                        "quantity": int(pos.get("quantity", 0)),
                        "purchase_price": float(pos.get("purchase_price", 0.0)),
                        "purchase_date": str(pos.get("purchase_price", "N/A")).strip()
                    })
                except Exception as e:
                    print(f"[Position {i}] Erreur inattendue : {e} -> ignorée")
    except FileNotFoundError:
        print(f"Erreur : le fichier {nom_fichier} n'a pas été trouvé.")
    except json.JSONDecodeError:
        print(f"Erreur : le fichier {nom_fichier} n'est pas un JSON valide.")
    return convertir_vers_positions(raw_data)

# Affichage avec les structures
def afficher_portfolio(positions):
    afficher_positions(positions)

def sauvegarder_portfolio(portfolio, nom_fichier):
    """
        Sauvegarde le portfolio dans un fichier JSON.
        Le portfolio doit être une liste de dictionnaires avec les clés :
        'symbol', 'quantity', 'price', 'purchase_date' (facultatif)
    """
    try:
        data_to_save = { # prépare les données à sauvegarder
            "positions": portfolio
        }

        with open(nom_fichier, 'w', encoding='utf-8') as file: # écriture dans le fichier
           json.dump(data_to_save, file, ensure_ascii=False, indent=4)
           # dump transforme la liste de dictionnaires portfolio en JSON / ascii False conserve les caractères spéciaux / indentation

        print(f"\nPortfolio sauvegardé avec succès dans '{nom_fichier}'.")

    except Exception as e:
        print(f"\nErreur lors de la sauvegarde du portfolio : {e}")

def chercher_par_symbole(portfolio, symbole):
    """ Retourne la Position si trouvés, sinon None. La recherche est insensible à la casse. """
    symbole = symbole.upper() # normalise pour ignorer la casse
    for position in portfolio:
        if position.symbol.upper() == symbole:
            return position
    return None
