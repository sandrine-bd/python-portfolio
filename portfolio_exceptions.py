from portfolio_calculs import gain_absolu
from portfolio_structures import Position


class ErreurDonneesPortfolio(Exception):
    """Exception personnalisée pour signaler un problème dans les données du portfolio"""
    def __init__(self, message, position=None):
        self.message = message
        self.position = position
        super().__init__(message) # super appelle le constructeur du parent Exception

    def __str__(self):
        if self.position:
            return f"[Erreur données portfolio] {self.message} | Position : {self.position}"
        return f"[Erreur données portfolio] {self.message}"

def charger_portfolio_securise(fichier, loader_func):
    """Version sécurisée du chargement du porfolio (ignore les positions invalides"""
    try:
        portfolio = loader_func(fichier)
    except FileNotFoundError:
        raise ErreurDonneesPortfolio(f"Le fichier {fichier} est introuvable.")
    except Exception as e:
        raise ErreurDonneesPortfolio(f"Erreur inattendue lors du chargement : {e}")

    portfolio_valide = []
    for pos in portfolio:
        try:
            if pos.quantity <= 0:
                raise ErreurDonneesPortfolio("Quantité invalide (<= 0)", pos)
            if pos.purchase_price <= 0:
                raise ErreurDonneesPortfolio("Prix d'achat invalide (<= 0)", pos)
            if not pos.symbol.isalpha():
                raise ErreurDonneesPortfolio("Symbole d'action invalide", pos)
            # Si la position est valide, on l'ajoute
            portfolio_valide.append(pos)

        except ErreurDonneesPortfolio as e:
            print(e) # affiche l'erreur mais le programme continue
            continue
        except Exception as e:
            print (f"Erreur inattendue sur position {getattr(pos, 'symbol', 'INCONNU')} : {e}")
            continue

    return portfolio_valide

def calculer_gains_securise(positions, prix_actuels_dict):
    """Vérifie que les prix sont présents et valides"""
    resultats = []
    for pos in positions:
        try:
            prix_actuel = prix_actuels_dict.get(pos.symbol)
            if prix_actuel is None:
                raise ErreurDonneesPortfolio("Prix actuel manquant", pos)
            if prix_actuel <= 0:
                raise ErreurDonneesPortfolio("Prix actuel invalide (<= 0)", pos)

            gain = gain_absolu(pos, prix_actuel)
            resultats.append({"symbol": pos.symbol, "gain": gain})

        except ErreurDonneesPortfolio as e:
            print(e)
            resultats.append({"symbol": pos.symbol, "gain": None, "erreur": str(e)})

        except Exception as e:
            print(f"Erreur inattendue pour {pos.symbol} : {e}")
            resultats.append({"symbol": pos.symbol, "gain": None, "erreur": str(e)})

    return resultats

# Test avec des données corrompues
positions_problematiques = [
    Position('AAPL', 10, 0.0, '2023-01-15'), # Prix d'achat = 0 !
    Position('', 5, 100.0, '2023-02-01'), # Symbole inexistant
    Position('GOOGL', -10, 2500.0, '2023-03-01'), # Quantité négative !
    Position('MSFT', 20, 300.0, '2023-01-20') # Valide
]

portfolio = charger_portfolio_securise("portfolio_sample.csv", lambda _: positions_problematiques)