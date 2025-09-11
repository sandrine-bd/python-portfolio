try:
    print(1/0)
except ZeroDivisionError:
    print("Divison par zéro impossible")

try:
    with open("portfolio_sample.csv") as file:
        read_data = file.read()
except FileNotFoundError as fnf_error:
    print(fnf_error)
    print("Explication : impossible de charger le fichier 'portfolio_sample.csv'")