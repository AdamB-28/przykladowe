from flask import Flask, render_template, request
from ksiegowosc_dekoratory_strona_sql import manager

app = Flask(__name__)

@app.route("/")
def start():
    print(manager.stan_magazynu)
    return render_template("index.html", saldo=manager.stan_konta, stan_magazynu=manager.stan_magazynu)

@app.route("/purchase", methods=["POST"])
def purchase_product():
    product_name = request.form["productName"]
    price = int(request.form["productPrice"])
    quantity = int(request.form["productQuantity"])
    
    manager.user_input = product_name
    manager.user_input_amount = quantity
    manager.price_input = price
    manager.execute("zakup")    
    manager.execute("saldo")
    return render_template("index.html", message=manager.message, saldo=manager.stan_konta, stan_magazynu=manager.stan_magazynu)

@app.route("/sell", methods=["POST"])
def sell():
    selected_product = None
    selected_price = 0
    message = ""
    if request.method == "POST":
        if "selectedProductName" in request.form:
            selected_product = request.form["selectedProductName"]
            if selected_product in manager.stan_magazynu:
                selected_price = manager.stan_magazynu[selected_product][0]
            else:
                message = "Nie znaleźono takiego produktu."
        if "selectedProductQuantity" in request.form:
            manager.user_input = request.form["selectedProductName"]
            manager.user_input_amount = request.form["selectedProductQuantity"]
            manager.price_input = request.form["selectedProductPrice"]
            manager.execute("sprzedaz")    
            manager.execute("saldo")
            message = manager.message
    return render_template("index.html", stan_magazynu=manager.stan_magazynu, selected_product=selected_product, selected_price=selected_price, message=message, saldo=manager.stan_konta)

@app.route("/balance", methods=["POST"])
def balance():
    balance = request.form["newBalance"]
    manager.stan_konta += int(balance)
    manager.historia.append(f"Ręczna zmiana salda: {balance}")
    manager.execute("saldo")
    return render_template("index.html", stan_magazynu=manager.stan_magazynu, message=f"Ręcznie zmieniono stan konta o {balance}", saldo=manager.stan_konta)

@app.route("/history")
def history():
    return render_template("historia.html", historia=manager.historia)

@app.route("/history/<od>/<do>/")
def uczestnicy(od, do):
    print(od,do)
    max_value = len(manager.historia)
    if int(do) <= max_value and int(od) >=0:
        return render_template("historia.html", historia=manager.historia[int(od):int(do)], message=f" - Slice {od}-{do}")
    else:
        return render_template("historia.html", historia=manager.historia[int(0):int(max_value)], message=f" - Slice {0}-{max_value} (maksymalna wartość)")

if __name__ == "__main__":
    app.run(debug = True)