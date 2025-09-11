from portfolio_calculs import valeur_position, valeur_actuelle, gain_absolu, rendement_pourcent, poids_portfolio, \
    dividendes_annuels, frais_courtage

class Portfolio:
    """Classe principale pour encapsuler les opérations sur un portfolio d'actions"""

    def __init__(self, positions):
        """Initialise le portfolio avec une liste de positions"""
        if not isinstance(positions, list):
            raise TypeError("Le portfolio doit être initialisé avec une liste de positions")
        self.positions = positions

    def __str__(self):
        """Vue lisible du portfolio"""
        lignes = ["--- Portfolio ---"]
        for pos in self.positions:
            lignes.append(f"{pos.symbol:<6} | Quantité : {pos.quantity:<8} | "
                          f"Achat : {pos.purchase_price:<8.2f} | Date : {pos.purchase_date}")
        return "\n".join(lignes)

    def __len__(self):
        """Nombre de positions dans le portfolio"""
        return len(self.positions)

    def __getitem__(self, key):
        """Pour accéder aux positions comme dans une liste ou un dict"""
        if isinstance(key, int):
            return self.positions[key]
        elif isinstance(key, str):
            return self.obtenir_position(key)
        raise TypeError("L'index doit être un entier ou un symbole d'action")

    def __iter__(self):
        """Pour parcourir le portfolio avec une boucle for"""
        return iter(self.positions)

    def __contains__(self, symbol):
        """Pour utiliser 'in'"""
        return any(pos.symbol == symbol.upper() for pos in self.positions)

    def __eq__(self, other):
        """Pour comparer deux portfolios"""
        if not isinstance(other, Portfolio):
            return False
        return set(self.positions) == set(other.positions)

    def __add__(self, other):
        """Pour fusionner deux portfolios"""
        if not isinstance(other, Portfolio):
            raise TypeError("On ne peut additionner qu'avec un autre Portfolio")
        return Portfolio(self.positions + other.positions)

    def calculer_valeur_totale(self, prix_actuels=None):
        """Si prix_actuels=None : valeur d'achat initiale, sinon : valeur de marché actuelle"""
        if prix_actuels is None:
            return sum(map(valeur_position, self.positions))
        else:
            return sum(
                map(lambda pos: valeur_actuelle(pos, prix_actuels.get(pos.symbol, 0)), self.positions)
            )

    def obtenir_position(self, symbol):
        """Recherche une position par symbole"""
        symbol = symbol.upper()
        for pos in self.positions:
            if pos.symbol.upper() == symbol:
                return pos
        return None

    def calculer_performance(self, prix_actuels, dividendes=None):
        """Performance du portfolio : valeur initiale, valeur actuelle, gain, rendement, poids, dividende & frais"""
        rapport = []
        total_actuel = self.calculer_valeur_totale(prix_actuels)
        total_initial = self.calculer_valeur_totale()

        for pos in self.positions:
            if pos.symbol not in prix_actuels:
                continue

            prix_actuel = prix_actuels[pos.symbol]
            val_init = valeur_position(pos)
            val_now = valeur_actuelle(pos, prix_actuel)
            gain = gain_absolu(pos, prix_actuel)
            rendement = rendement_pourcent(pos, prix_actuel)
            poids = poids_portfolio(pos, prix_actuel, total_actuel)
            div = dividendes_annuels(pos, dividendes.get(pos.symbol, 0)) if dividendes else 0
            frais = frais_courtage(val_now)

            rapport.append({
                "symbole": pos.symbol,
                "valeur_initiale": val_init,
                "valeur_actuelle": val_now,
                "gain_absolu": gain,
                "rendement_%": rendement,
                "poids_%": poids,
                "dividendes": div,
                "frais_courtage": frais
            })

            performance_globale = {
                "total_initial": total_initial,
                "total_actuel": total_actuel,
                "gain_total": total_actuel - total_initial,
                "rendement_portfolio_%": ((total_actuel - total_initial) / total_initial * 100)
                if total_initial > 0 else 0
            }

            return rapport, performance_globale