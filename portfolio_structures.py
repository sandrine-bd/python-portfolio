from collections import namedtuple

# Structures de données immuables
Position = namedtuple("Position", ["symbol", "quantity", "purchase_price", "purchase_date"])
Transaction = namedtuple("Transaction", ["date", "symbol", "quantity", "price", "type"])

# Conversion des données : une liste de dictionnaires (CSV/JSON) en liste de namedtuples
def convertir_vers_positions(portfolio_dict):
    positions = []
    for pos in portfolio_dict:
        try:
            positions.append(
                Position(
                    symbol=pos.get("symbol", "").upper(),
                    quantity=int(pos.get("quantity", 0)),
                    purchase_price=float(pos.get("purchase_price", 0.0)),
                    purchase_date=pos.get("purchase_date", "N/A"),
                )
            )
        except Exception as e:
            print(f"Erreur lors de la conversion : {e} -> ignorée")
    return positions

# Affichage lisible basé sur les namedtuples Position
def afficher_positions(positions):
    if not positions:
        print("Le portfolio est vide.")
        return

    total = 0.0
    print("\n--- Résumé du portfolio ---")
    for pos in positions:
        valeur = pos.quantity * pos.purchase_price
        total += valeur
        print(
            f"{pos.symbol:<6} | {pos.quantity:>3} actions "
            f"à {pos.purchase_price:>8.2f}€ "
            f"(Date d'achat: {pos.purchase_date}) -> Valeur : {valeur:>10.2f}€"
        )
        print(f"\nValeur totale estimée : {total:.2f}€\n")

class Portfolio:
    def __init__(self, positions=None):
        self.positions = positions if positions else []

    def ajouter_positions(self, position):
        if isinstance(position, Position):
            self.positions.append(Position)
        else:
            raise TypeError("Seules des instances de Position peuvent être ajoutées")

    def valeur_totale(self):
        return sum(p.quantity * p.purchase_price for p in self.positions)

    def afficher(self):
        afficher_positions(self.positions)
