from portfolio_calculs import (
    valeur_position,
    valeur_actuelle,
    gain_absolu,
    rendement_pourcent,
)

def calculer_valeurs_positions(positions):
    """Retourne une liste des valeurs d'achat de chaque position."""
    return list(map(valeur_position, positions))


def calculer_gains_portfolio(positions, prix_actuels_dict):
    """Retourne les gains absolus de toutes les positions."""
    return list(map(
        lambda pos: gain_absolu(pos, prix_actuels_dict.get(pos.symbol, 0.0)),
        positions
    ))


def calculer_rendements_portfolio(positions, prix_actuels_dict):
    """Retourne les rendements (%) de toutes les positions."""
    return list(map(
        lambda pos: rendement_pourcent(pos, prix_actuels_dict.get(pos.symbol, 0.0)),
        positions
    ))


def generer_rapport_complet(positions, prix_actuels_dict):
    """Génère un rapport global avec valeurs, gains et rendements."""
    return list(map(
        lambda pos: {
            "symbol": pos.symbol,
            "valeur_initiale": valeur_position(pos),
            "valeur_actuelle": valeur_actuelle(pos, prix_actuels_dict.get(pos.symbol, 0.0)),
            "gain_absolu": gain_absolu(pos, prix_actuels_dict.get(pos.symbol, 0.0)),
            "rendement_%": rendement_pourcent(pos, prix_actuels_dict.get(pos.symbol, 0.0)),
        },
        positions
    ))
