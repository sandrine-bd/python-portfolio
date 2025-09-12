from portfolio_loader import lire_portfolio_csv
from portfolio_prices_loader import lire_prix_actuels_csv
from portfolio_class import Portfolio

def main():
    # Charge le portfolio initial
    portfolio_csv = lire_portfolio_csv("portfolio_sample.csv")
    portfolio = Portfolio(portfolio_csv)
    print("\nPortfolio chargé depuis CSV :")
    print(portfolio) # __str__ est appelé

    print(f"\nNombre de positions : {len(portfolio)}\n") # __len__ est appelé

    # Charge les prix actuels
    prix_actuels = lire_prix_actuels_csv("portfolio_actual_prices_sample.csv")

    dividendes = { # dividendes annuels simulés
        "AAPL": 1.04,
        "GOOGL": 0.84,
        "MSFT": 3.32,
        "NVDA": 0.04,
        "META": 2.10,
        "AMZN": 0.0,
        "TSLA": 0.0,
    }

    # Performance globale
    rapport, perf_globale = portfolio.calculer_performance(prix_actuels, dividendes)

    print(f"--- Rapport détaillé ---")
    for r in rapport:
        print(
            f"{r['symbole']:<6} | Init : {r['valeur_initiale']:>8.2f} | "
            f"Actuel : {r['valeur_actuelle']:>8.2f} | Gain : {r['gain_absolu']:+8.2f} | "
            f"Rendement : {r['rendement_%']:+6.2f}% | Poids : {r['poids_%']:5.2f} | "
            f"Dividendes : {r['dividendes']:.2f} | Frais : {r['frais_courtage']:.2f}"
        )

    print("\n--- Performance globale ---")
    print(
        f"Valeur initiale totale : {perf_globale['total_initial']:.2f} €\n"
        f"Valeur actuelle totale : {perf_globale['total_actuel']:.2f} €\n"
        f"Gain total : {perf_globale['gain_total']:+.2f} €\n"
        f"Rendement global : {perf_globale['rendement_portfolio_%']:+.2f}%"
    )

    print("=== DEBUG ===")
    print("Prix actuels :", prix_actuels)
    print("Portfolio :", portfolio.positions)

    # __getitem__
    portfolio[0]
    portfolio["AAPL"]

    # __iter__
    for pos in portfolio:
        print(pos.symbol, pos.quantity)

    # __contains__
    if "TSLA" in portfolio:
        print("Tesla est dans le portfolio")

if __name__ == "__main__":
    main()