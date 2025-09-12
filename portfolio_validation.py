import re

from portfolio_structures import Position


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

def valider_portfolio_complet(positions):
    """Args : Liste des positions à valider / Renvoie un dict : Rapport de validation"""
    rapport = {
        'nb_total': len(positions),
        'nb_valides': 0,
        'nb_invalides': 0,
        'positions_valides': [],
        'positions_invalides': [],
        'symboles_uniques': set(),
        'doublons': []
    }

    symboles_vus = {}

    for i, position in enumerate(positions):
        est_valide, erreurs = valider_position_complete(position)

        if est_valide:
            rapport['nb_valides'] += 1
            rapport['positions_valides'].append(position)

            # Détection des doublons
            symbole = position.symbol
            if symbole in symboles_vus:
                rapport['doublons'].append({
                    'symbole': symbole,
                    'positions': [symboles_vus[symbole], i]
                })
            else:
                symboles_vus[symbole] = i

            rapport['symboles_uniques'].add(symbole)
        else:
            rapport['nb_invalides'] += 1
            rapport['positions_invalides'].append({
                'position': position,
                'index': i,
                'erreurs': erreurs
            })

    return rapport

def afficher_rapport_validation(rapport):
    """Args: rapport (dict): Rapport généré par valider_portfolio_complet()"""
    print("\n" + "=" * 50)
    print("           RAPPORT DE VALIDATION")
    print("=" * 50)

    print(f"Total des positions analysées : {rapport['nb_total']}")
    print(f"Positions valides : {rapport['nb_valides']}")
    print(f"Positions invalides : {rapport['nb_invalides']}")
    print(f"Symboles uniques : {len(rapport['symboles_uniques'])}")

    if rapport['positions_invalides']:
        print(f"\nPOSITIONS INVALIDES ({rapport['nb_invalides']}) :")
        for invalid in rapport['positions_invalides']:
            pos = invalid['position']
            print(f"   [{invalid['index']}] {pos.symbol} - {pos.quantity} @ {pos.purchase_price}")
            for erreur in invalid['erreurs']:
                print(f"      → {erreur}")

    if rapport['doublons']:
        print(f"\nDOUBLONS DÉTECTÉS ({len(rapport['doublons'])}) :")
        for doublon in rapport['doublons']:
            print(f"   {doublon['symbole']} aux positions {doublon['positions']}")

    if rapport['positions_valides']:
        print(f"\nSYMBOLES VALIDES :")
        symboles_tries = sorted(rapport['symboles_uniques'])
        print(f"   {', '.join(symboles_tries)}")

    print("=" * 50)

def tester_validation():
    """Fonction de test avec des données valides et invalides."""
    print("TEST DES VALIDATIONS")
    print("-" * 30)

    # Test des symboles individuels
    print("\n1. Test de validation des symboles :")
    symboles_test = ['AAPL', 'GOOGL', 'apple', 'TOOLONG', 'AA PL', '', '123', 'A', 'ABCDE']

    for symbole in symboles_test:
        nettoyé = nettoyer_symbole(symbole)
        valide = valider_symbole_action(nettoyé)
        status = "✅" if valide else "❌"
        print(f"   '{symbole}' → '{nettoyé}' {status}")

    # Test avec un portfolio mixte (valide + invalide)
    print("\n2. Test de portfolio complet :")
    positions_test = [
        Position('AAPL', 50, 150.25, '2023-01-15'),  # ✅ Valide
        Position('GOOGL', 20, 2500.50, '2023-02-01'),  # ✅ Valide
        Position('apple', 30, 300.75, '2023-01-20'),  # ❌ Minuscules
        Position('TOOLONG', 15, 450.00, '2023-03-10'),  # ❌ Trop long
        Position('MSFT', 0, 200.30, '2023-02-15'),  # ❌ Quantité = 0
        Position('AMZN', 10, -100, '2023-01-30'),  # ❌ Prix négatif
        Position('123', 35, 180.50, '2023-03-05'),  # ❌ Chiffres
        Position('', 25, 200.00, '2023-04-01'),  # ❌ Symbole vide
        Position('AAPL', 25, 155.00, '2023-05-01'),  # ⚠️ Doublon
    ]

    rapport = valider_portfolio_complet(positions_test)
    afficher_rapport_validation(rapport)

    return rapport

def filtrer_positions_valides(positions):
    rapport = valider_portfolio_complet(positions)
    return rapport['positions_valides']

# Tests et démonstration si le script est exécuté directement
if __name__ == "__main__":
    print("DÉMARRAGE DU MODULE DE VALIDATION")

    # Lancer les tests
    rapport_test = tester_validation()

    # Exemple d'utilisation pratique
    print("\n" + "=" * 50)
    print("           EXEMPLE D'UTILISATION")
    print("=" * 50)

    print("\nFiltre des positions valides uniquement :")
    positions_exemple = [
        Position('AAPL', 50, 150.25, '2023-01-15'),
        Position('invalid', 30, 300.75, '2023-01-20'),
        Position('MSFT', 25, 340.80, '2023-03-01')
    ]

    positions_valides = filtrer_positions_valides(positions_exemple)
    print(f"Positions valides récupérées : {len(positions_valides)}")
    for pos in positions_valides:
        print(f"  {pos.symbol}: {pos.quantity} @ {pos.purchase_price}€")

    print(f"\nModule de validation prêt à l'emploi !")