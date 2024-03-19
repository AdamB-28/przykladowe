import os
from sqlAl import app, db, InventoryItem, AccountBalance
from sqlAl import History as sqHistory

# SQL PART
def query_inventory_items():
    with app.app_context():
        items = InventoryItem.query.all()
        all_dict = {}
        for i in items:
            all_dict[i.name] = [i.price, i.quantity]        
        if not all_dict:
            print("No items found in the database.")
        return all_dict
        
def query_history():
    with app.app_context():
        history_items = sqHistory.query.all()
        if history_items:
            actions_list = [item.name_action for item in history_items]
            return actions_list
        else:
            print("Nie ma historii.")
            return []
        
def check_balance():
    with app.app_context():
        item = AccountBalance.get_balance()
        print("BALANS:",item)
        return item


def save_data_to_db(element, stan, magazyn):
    with app.app_context():
        for e in element:
            new_item = sqHistory(name_action=e)
            db.session.add(new_item)        

        for key, value in magazyn.items():
            new_item = InventoryItem(name=key, price=value[0], quantity=value[1])
            db.session.add(new_item)

        AccountBalance.update_balance(stan)

        db.session.commit()

# END SQL

class History:
    @staticmethod
    def save_history(element, stan, magazyn):
        save_data_to_db(element, stan, magazyn)

    @staticmethod    
    def read_history():
        return query_history()
    
    @staticmethod
    def read_account():
        return check_balance()
    
    @staticmethod
    def read_inventory():
        return query_inventory_items()
    
class Manager():
    def __init__(self):
        self.actions = {}
        self.historia = History.read_history()
        self.stan_konta = History.read_account()
        self.stan_magazynu = History.read_inventory()
        self.rachunek = 0
        self.user_input = ""
        self.user_input_amount = 0
        self.price_input = 0
        self.message = ""

    def assign(self, name):
        def decorate(callback):
            self.actions[name] = callback
            def wrapper(*args,**kwargs):
                pass
            return wrapper
        return decorate

    def execute(self, name):
        if name in self.actions:
            self.actions[name]()
        else:
            print("\nNie ma takiej funckji\n")

    def print_actions(self):
        for key, value in self.actions.items():
            print("ACTION: ", key, value)

manager = Manager()

#KOMENDY
def historia():
    History.save_history(manager.historia, manager.stan_konta, manager.stan_magazynu)
    print("\nHistoria zapisana\n")

@manager.assign("saldo")
def saldo():
    if manager.stan_konta >= manager.rachunek:
        manager.stan_konta += manager.rachunek
        manager.historia.append(f"saldo: {manager.rachunek}")
        print(f"\nTwoje saldo wynosi {manager.stan_konta} PLN. Ostatnia transakcja: {manager.rachunek} PLN")
        manager.rachunek = 0
    else:
        print("Nie masz wystarczająco dużo pieniędzy. Sprzedaj towar!")
    historia()

@manager.assign("sprzedaz")
def sprzedaz():
    hist_input = "sprzedaż"
    # manager.user_input = input("\nJaki towar chcesz sprzedać? Wpisz tutaj: ")
    hist_input += f": {manager.user_input}"
    if manager.user_input in manager.stan_magazynu.keys():
        # user_input_amount = input("\nJaką ilość chcesz sprzedać? Wpisz tutaj: ")
        print()
        try:
            user_input_amount = int(manager.user_input_amount)
            hist_input += f": {user_input_amount}"
            print(manager.stan_magazynu[manager.user_input][1])
            if manager.stan_magazynu[manager.user_input][1] >= user_input_amount:
                manager.stan_magazynu[manager.user_input][1] -= user_input_amount
                manager.rachunek += manager.stan_magazynu[manager.user_input][0] * user_input_amount
                print(f"\nPrzedmiot: {manager.user_input}, w liczbie {user_input_amount} został sprzedany. Balans wynosi obecnie: {manager.rachunek}")
                manager.message = f"Przedmiot: {manager.user_input}, w liczbie {user_input_amount} został sprzedany."
            else:
                print("Nie ma takiego/tyle produktu w magazynie.")
                manager.message = "Nie ma takiego/tyle produktu w magazynie."
                hist_input += " -> niemożliwe do wykonania "
                manager.historia.append(hist_input)
        except:
            print("Nieprawidłowa wartość")
            hist_input += f", {manager.user_input}"
            manager.historia.append(hist_input)
        
    else:
        print("Nie ma takiego produktu w magazynie.")
    historia()

@manager.assign("zakup")
def zakup():
    hist_input = "zakup"
    # manager.user_input = input("\nJaki towar chcesz kupić? Wpisz tutaj: ")
    hist_input += f": {manager.user_input}"
    # user_input_amount = int(input("\nJaką ilość chcesz kupić? Wpisz tutaj: "))
    hist_input += f": {manager.user_input_amount}"
    manager.historia.append(hist_input)
    if manager.user_input in manager.stan_magazynu.keys():
        if manager.price_input != manager.stan_magazynu[manager.user_input][0]:
            manager.message = "Nieprawidłowa cena"
        else:
            manager.stan_magazynu[manager.user_input][1] += manager.user_input_amount
    else:
        manager.stan_magazynu[manager.user_input] = [manager.price_input,manager.user_input_amount]
    manager.rachunek -= manager.stan_magazynu[manager.user_input][0]*manager.user_input_amount
    manager.message = f"Kupiłeś: {manager.user_input} w ilości: {manager.user_input_amount} za {manager.stan_magazynu[manager.user_input][0]*manager.user_input_amount} PLN."
    print(f"Dodałeś do koszyka: {manager.user_input} w ilości: {manager.user_input_amount} za {manager.stan_magazynu[manager.user_input][0]*manager.user_input_amount} PLN. Balans wynosi obecnie: {manager.rachunek}")
    historia()

@manager.assign("konto")
def konto():
    print(f"\nTwoje saldo wynosi {manager.stan_konta} PLN")

@manager.assign("lista")
def lista():
    for nazwa, cena_liczba in manager.stan_magazynu.items():
            print(f"Przedmiot: {nazwa}; cena {cena_liczba[0]}; liczba: {cena_liczba[1]}")

@manager.assign("magazyn")
def magazyn():
    manager.user_input = input("\nPodaj nazwę produktu, który chciałbyś wyświetlić. Wpisz tutaj: ")
    if manager.user_input in manager.stan_magazynu.keys():
        print(f"\nPrzedmiot: {manager.user_input}; cena: {manager.stan_magazynu[manager.user_input][0]}; liczba: {manager.stan_magazynu[manager.user_input][1]}")
    else:
        print("\nNie ma takiego produktu w magazynie.")

@manager.assign("przeglad")
def przeglad():
    manager.user_input =  input(f"Podaj zakres przeglądu w formacie N-N, bądź wciśnij ENTER aby zobczyć pełny przegląd. Dostępny zakres to 1-{len(manager.historia)}.\n")
    if manager.user_input == "":
        for e in manager.historia:
            print(e)
    else:
        number_1 = int(manager.user_input.split("-")[0])
        number_2 = int(manager.user_input.split("-")[1])
        if number_1 >= 1 and number_2 <= len(manager.historia):
            print(f"Zakres od {number_1} do {number_2}\n")
            for e in range(number_1-1, number_2):
                print(manager.historia[e])
        else:
            print("\nPodano nieprawidłowy zakres.\n")

# manager.print_actions()
#KONIEC KOMEND

def print_komendy():
    komendy = (
            "saldo",
            "sprzedaz",
            "zakup",
            "konto",
            "lista",
            "magazyn",
            "przeglad",
            "koniec"
            )
    tekst = ""
    for k in komendy:
        tekst += f"| {k} "

    print(f"\nDostępne komendy: {tekst}|")
    manager.user_input = input("Wybierz jedną z powyższych komend: ")



if __name__ == "__main__":
    while True:
        print_komendy()
        manager.execute(manager.user_input)