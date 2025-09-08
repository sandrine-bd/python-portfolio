import csv
import json

def lire_portfolio_csv(portfolio_sample):
    """ Charge le portfolio depuis un fichier CSV avec colonnes """
    portfolio = []
    try:
        with open(portfolio_sample, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for ligne in reader:
                position = {
                    'symbol': ligne.get('symbol', 'N/A'),
                    'quantity': int(ligne.get('quantity', 0)),
                    'purchase_price': float(ligne.get('purchase_price', 0.0)),
                    'purchase_date': ligne.get('purchase_date', 'N/A')
                }
                portfolio.append(position)
    except FileNotFoundError:
        print(f"Erreur : le fichier {portfolio_sample} n'a pas été trouvé.")
    except Exception as e:
        print(f"Erreur lors de la lecture du CSV : {e}")
    return portfolio

def lire_portfolio_json(portfolio_sample):
    """ Charge le portfolio depuis un fichier JSON avec métadonnées """
    portfolio = []
    try:
        with open(portfolio_sample, mode='r', encoding='utf-8') as file:
            data = json.load(file)
            positions = data.get('positions', [])
            for pos in positions:
                position = {
                    'symbol': pos.get('symbol'),
                    'quantity': pos.get('quantity', 0),
                    'purchase_price': pos.get('purchase_price', 0.0),
                    'purchase_date': pos.get('purchase_date')
                }
                portfolio.append(position)
    except FileNotFoundError:
        print(f"Erreur : le fichier {portfolio_sample} n'a pas été trouvé.")
    except json.JSONDecodeError:
        print(f"Erreur : le fichier {portfolio_sample} n'est pas un JSON valide.")
    except Exception as e:
        print(f"Erreur lors de la lecture du JSON : {e}")
    return portfolio

def afficher_portfolio(portfolio):
    """ Affiche un résumé lisible du portfolio avec valeur totale """
    if not portfolio:
        print("Le portfolio est vide.")
        return

    print(f"{'Symbole':<6} {'Quantité':<8} {'Prix (€)':<10} {'Date achat':<12} {'Valeur (€)':<12}") # Entêtes < alignées à gauche avec nb de caractères
    print("-" * 40) # crée une ligne de 40 tirets

    valeur_totale = 0
    for position in portfolio:
        symbole = position.get('symbol', 'N/A')
        quantite = position.get('quantity', 0)
        prix = position.get('purchase_price', 0)
        date_achat = position.get('purchase_date', 'N/A')
        valeur = quantite * prix
        valeur_totale += valeur

        # Affichage avec alignement
        print(f"{symbole:<6} {quantite:<8} {prix:<10.2f} {date_achat:<12} {valeur:<12.2f}") # 2f formate le nombre avec 2 décimales

    print("-" * 40)
    print(f"{'Valeur totale du portfolio (€)':<46}: {valeur_totale:.2f}")


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
    """
        Retourne le dictionnaire de la position si trouvé, sinon None.
        La recherche est insensible à la casse.
    """
    symbole = symbole.upper() # normalise pour ignorer la casse
    for position in portfolio:
        if position.get('symbol', '').upper() == symbole:
            return position
        return None

# Exemples d'utilisation
if __name__ == "__main__":
    portfolio_csv = lire_portfolio_csv('portfolio_sample.csv')
    print("\nPortfolio chargé depuis CSV :")
    afficher_portfolio(portfolio_csv)

    portfolio_json = lire_portfolio_json('portfolio_sample.json')
    print("\nPortfolio chargé depuis JSON :")
    afficher_portfolio(portfolio_json)

    sauvegarder_portfolio(portfolio_json, 'portfolio_updated.json')

    position = chercher_par_symbole(portfolio_json, "AAPL")
    if position:
        print("\nPosition trouvée :", position)
    else:
        print("\nSymbole non trouvé dans le portfolio.")