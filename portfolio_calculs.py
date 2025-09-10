# Valeur d'achat d'une position (en €)
valeur_position = lambda position: float(position.quantity) * float(position.purchase_price)

# Valeur actuelle d'une position (en €)
valeur_actuelle = lambda position, prix_actuel: float(position.quantity) * float(prix_actuel)

# Gain absolu (en €) : (prix_actuel - prix_achat) × quantité
gain_absolu = lambda position, prix_actuel: (float(prix_actuel) - float(position.purchase_price)) * float(position.quantity)

# Rendement en % : ((prix_actuel - prix_achat) / prix_achat) × 100
rendement_pourcent = lambda position, prix_actuel: (
    ((float(prix_actuel) - float(position.purchase_price)) / float(position.purchase_price)) * 100
    if float(position.purchase_price) > 0 else 0.0
)

# Poids d'une position dans le portfolio (en %)
poids_portfolio = lambda position, prix_actuel, total_portfolio: (
    (valeur_actuelle(position, prix_actuel) / float(total_portfolio)) * 100
    if float(position.purchase_price) > 0 else 0.0
)