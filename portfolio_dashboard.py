from portfolio_loader import lire_portfolio_csv, afficher_portfolio, chercher_par_symbole
from portfolio_prices_loader import lire_prix_actuels_csv
from portfolio_calculs import (
    valeur_position, valeur_actuelle, gain_absolu, rendement_pourcent, poids_portfolio,
    dividendes_annuels, frais_courtage
)
from portfolio_map import (
    calculer_valeurs_positions, calculer_gains_portfolio, calculer_rendements_portfolio,
    generer_rapport_complet
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

    total_actuel = sum( # valeur totale actuelle du portefeuille
        valeur_actuelle(pos, prix_actuels[pos.symbol])
        for pos in portfolio_csv if pos.symbol in prix_actuels
    )

    dividende_par_action = {
        "AAPL": 1.04,
        "GOOGL": 0.84,
        "MSFT": 3.32,
        "NVDA": 0.04,
        "META": 2.10,
        "AMZN": 0.0,
        "TSLA": 0.0,
    }

    print("\n--- Tableau récapitulatif (calculs unitaires via Lambda) ---")
    for pos in portfolio_csv:
        if pos.symbol in prix_actuels:
            prix_actuel = prix_actuels[pos.symbol]
            val_init = valeur_position(pos)
            val_now = valeur_actuelle(pos, prix_actuel)
            gain = gain_absolu(pos, prix_actuel)
            rendement = rendement_pourcent(pos, prix_actuel)
            poids = poids_portfolio(pos, prix_actuel, total_actuel)
            div = dividendes_annuels(pos, dividende_par_action.get(pos.symbol, 0))
            frais = frais_courtage(val_now)

            print(f"{pos.symbol:<6} | Achat : {val_init:>8.2f} | "
                  f"Actuel : {val_now:>8.2f}€ | "
                  f"Gain: {gain:+8.2f}€ | "
                  f"Rendement: {rendement:+6.2f}% | "
                  f"Poids: {poids:5.2f}% | "
                  f"Valeur actuelle : {val_now:.2f}€ | "
                  f"Dividendes annuels : {div:.2f}€ | "
                  f"Frais de courtage (vente) : {frais:.2f}€")

    # Exemple avec map() : rapport global
    print("\n--- Rapport complet (via map) ---")
    valeurs = calculer_valeurs_positions(portfolio_csv)
    gains = calculer_gains_portfolio(portfolio_csv, prix_actuels)
    rendements = calculer_rendements_portfolio(portfolio_csv, prix_actuels)
    rapport = generer_rapport_complet(portfolio_csv, prix_actuels)

    print("Valeurs initiales :", valeurs)
    print("Gains absolus :", gains)
    print("Rendements % :", rendements)

    print("\n--- Rapport détaillé ---")
    for ligne in rapport:
        print(ligne)

if __name__ == "__main__":
    main()