import re

def valider_symbole_action(symbole):
    if not isinstance(symbole, str):
        return False
    # Expression régulière : ^ = début, $ = fin, [A-Z] = lettres majuscules, {1,5} = 1 à 5 caractères
    pattern = r'^[A-Z]{1,5}$'
    return bool(re.match(pattern, symbole))

def nettoyer_symbole(symbole_brut):
    if not isinstance(symbole_brut, str):
        return ""
    # Supprime espaces début/fin, convertit en majuscules, supprime espaces internes
    symbole_nettoye = re.sub(r'\s+', '', symbole_brut.strip().upper())
    return symbole_nettoye

def valider_position_complete(position):
    """Renvoie un tuple : (bool, list) - (est_valide, liste_erreurs)"""
    erreurs = []

    # Validation du symbole
    if not valider_symbole_action(position.symbol):
        erreurs.append(f"Symbole invalide : '{position.symbol}' (doit être 1-5 lettres majuscules)")

    # Validation de la quantité
    try:
        quantity = int(position.quantity)
        if quantity <= 0:
            erreurs.append(f"Quantité invalide : {quantity} (doit être > 0)")
    except (ValueError, TypeError):
        erreurs.append(f"Quantité non numérique : {position.quantity}")

    # Validation du prix
    try:
        price = float(position.purchase_price)
        if price <= 0:
            erreurs.append(f"Prix invalide : {price} (doit être > 0")
    except (ValueError, TypeError):
        erreurs.append(f"Prix non numérique : {position.purchase_price}")

    return len(erreurs) == 0, erreurs
