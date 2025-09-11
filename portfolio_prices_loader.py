import csv

def lire_prix_actuels_csv(nom_fichier):
    current_prices = {}
    try:
        with open(nom_fichier, mode="r", encoding="utf-8") as csvfile:
            lecteur = csv.DictReader(csvfile)
            for ligne in lecteur:
                try:
                    symbol = ligne["symbol"].strip().upper()
                    prix_actuel = float(ligne["current_price"])
                    current_prices[symbol] = prix_actuel
                except (KeyError, ValueError) as e:
                    print(f"Erreur de parsing ligne {ligne} : {e}")
    except FileNotFoundError:
        print(f"Erreur : le fichier {nom_fichier} n'a pas été trouvé.")
    return current_prices