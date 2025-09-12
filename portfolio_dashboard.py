from portfolio_loader import lire_portfolio_csv
from portfolio_prices_loader import lire_prix_actuels_csv
from portfolio_class import Portfolio
from portfolio_validation import valider_portfolio_complet, afficher_rapport_validation, filtrer_positions_valides


def main():
    print("=== DEBUT DU PROGRAMME ===\n")

    # Chargement du portfolio initial
    print("Chargement du portfolio...")
    portfolio_brut = lire_portfolio_csv("portfolio_sample.csv")
    print(f"Nombre de positions chargées : {len(portfolio_brut)}")

    if not portfolio_brut:
        print("ERREUR: Aucune position chargée depuis le CSV")
        return

    # Validation complète du portfolio
    print("\nValidation du portfolio...")
    rapport_validation = valider_portfolio_complet(portfolio_brut)
    afficher_rapport_validation(rapport_validation)

    # Filtre uniquement les positions valides
    positions_valides = filtrer_positions_valides(portfolio_brut)

    if not positions_valides:
        print("ERREUR: Aucune position valide trouvée")
        return

    print(f"\nPortfolio validé : {len(positions_valides)} positions retenues")

    # Création du portfolio avec les positions valides
    portfolio = Portfolio(positions_valides)
    print(portfolio)

    # Chargement des prix actuels
    print("\nChargement des prix actuels...")
    prix_actuels = lire_prix_actuels_csv("portfolio_actual_prices_sample.csv")
    print(f"Prix actuels chargés : {len(prix_actuels)}")

    if not prix_actuels:
        print("ATTENTION: Aucun prix actuel chargé")
        return

    # Vérification de la cohérence prix/symboles
    print("\nVérification cohérence prix/symboles...")
    symboles_portfolio = {pos.symbol for pos in positions_valides}
    symboles_prix = set(prix_actuels.keys())

    symboles_manquants = symboles_portfolio - symboles_prix
    prix_inutiles = symboles_prix - symboles_portfolio

    if symboles_manquants:
        print(f"Prix manquants pour : {', '.join(symboles_manquants)}")
    if prix_inutiles:
        print(f"Prix non utilisés : {', '.join(prix_inutiles)}")

    symboles_communs = symboles_portfolio & symboles_prix
    print(f"Symboles avec prix : {', '.join(sorted(symboles_communs))}")

    # Calcul des performances (uniquement pour les symboles ayant des prix)
    dividendes = {
        "AAPL": 1.04,
        "GOOGL": 0.84,
        "MSFT": 3.32,
        "NVDA": 0.04,
        "META": 2.10,
        "AMZN": 0.0,
        "TSLA": 0.0,
    }

    print("\nCalcul des performances...")
    rapport, perf_globale = portfolio.calculer_performance(prix_actuels, dividendes)

    # Affichage des résultats
    print(f"\n--- RAPPORT DETAILLE ---")
    for r in rapport:
        print(
            f"{r['symbole']:<6} | Init : {r['valeur_initiale']:>8.2f} | "
            f"Actuel : {r['valeur_actuelle']:>8.2f} | Gain : {r['gain_absolu']:+8.2f} | "
            f"Rendement : {r['rendement_%']:+6.2f}% | Poids : {r['poids_%']:5.2f} | "
            f"Dividendes : {r['dividendes']:.2f} | Frais : {r['frais_courtage']:.2f}"
        )

    print("\n--- PERFORMANCE GLOBALE ---")
    print(
        f"Valeur initiale totale : {perf_globale['total_initial']:.2f} €\n"
        f"Valeur actuelle totale : {perf_globale['total_actuel']:.2f} €\n"
        f"Gain total : {perf_globale['gain_total']:+.2f} €\n"
        f"Rendement global : {perf_globale['rendement_portfolio_%']:+.2f}%"
    )

    print("\n=== Test des méthodes spéciales ===")
    # __getitem__
    print("Recherche index 1 : ", end="")
    print(portfolio[1])
    print("Recherche mot 'AAPL' : ", end="")
    print(portfolio["AAPL"])

    # __iter__
    print("\nItération dans le portfolio avec symbole et quantité : ")
    for pos in portfolio:
        print(pos.symbol, pos.quantity)

    # __contains__
    print("\nRecherche du symbole TSLA", end=" : ")
    if "TSLA" in portfolio:
        print("Tesla est dans le portfolio")

    print("\n=== FIN DU PROGRAMME ===")

if __name__ == "__main__":
    main()