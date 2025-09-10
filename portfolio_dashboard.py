from portfolio_loader import lire_portfolio_csv, afficher_portfolio, chercher_par_symbole
from portfolio_prices_loader import lire_prix_actuels_csv
from portfolio_calculs import (
    valeur_position, valeur_actuelle, gain_absolu, rendement_pourcent, poids_portfolio
)

def main():
    portfolio_csv = lire_portfolio_csv("portfolio_sample.csv") # charge le portfolio initial
    print("\nPortfolio chargé depuis CSV :")
    afficher_portfolio(portfolio_csv)

    position = chercher_par_symbole(portfolio_csv, "AAPL") # test de la recherche
    if position:
        print("\nPosition trouvée :", position)
    else:
        print("\nSymbole non trouvé dans le portfolio.")

    prix_actuels = lire_prix_actuels_csv("portfolio_actual_prices_sample.csv") # charge les prix actuels

    total_actuel = sum(
        valeur_actuelle(pos, prix_actuels[pos.symbol])
        for pos in portfolio_csv if pos.symbol in prix_actuels
    )

    print("\n--- Tableau récapitulatif ---")
    for pos in portfolio_csv:
        if pos.symbol in prix_actuels:
            prix_actuel = prix_actuels[pos.symbol]
            val_init = valeur_position(pos)
            val_now = valeur_actuelle(pos, prix_actuel)
            gain = gain_absolu(pos, prix_actuel)
            rendement = rendement_pourcent(pos, prix_actuel)
            poids = poids_portfolio(pos, prix_actuel, total_actuel)

            print(f"{pos.symbol:<6} | Achat : {val_init:>8.2f} | "
                  f"Actuel : {val_now:>8.2f}€ | "
                  f"Gain: {gain:+8.2f}€ | "
                  f"Rendement: {rendement:+6.2f}% | "
                  f"Poids: {poids:5.2f}%")

if __name__ == "__main__":
    main()