import csv

def lire_prix_actuels_csv(nom_fichier):
    current_prices = {}
    try:
        with open(nom_fichier, mode="r", encoding="utf-8") as csvfile:
            lecteur = csv.DictReader(csvfile)
            for ligne in lecteur:
                try:
                    symbol = ligne["symbol"].strip().upper()
                    price = float(ligne["purchase_price"])
                    current_prices[symbol] = price
                except (KeyError, ValueError) as e:
                    print(f"Erreur de parsing ligne {ligne} : {e}")
    except FileNotFoundError:
        print(f"Erreur : le fichier {nom_fichier} n'a pas été trouvé.")
    return current_prices