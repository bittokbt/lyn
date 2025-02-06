import os
import random

from cs50 import SQL
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__, static_folder='static')

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)

@app.route("/comer", methods=["GET", "POST"])
def comer():
    if 'quantidade_comida' not in session:
        session['quantidade_comida'] = 0

    if request.method == "POST":
        session['quantidade_comida'] += 1
        session.modified = True
        return redirect(url_for("comer"))

    return render_template("comer.html", quantidade_comida=session['quantidade_comida'])

@app.route("/loja")
def loja():
    if request.method == "GET":
        if 'saldo' not in session:
            session['saldo'] = 300
        return render_template("loja.html", saldo=session['saldo'])

@app.route("/trabalhar", methods=["POST"])
def trabalhar():
    if "saldo" not in session:
        session["saldo"] = 300
    session["saldo"] += 50
    return redirect(url_for("loja"))

@app.route("/comprar", methods=["POST"])
def comprar():
    produto = request.form.get("produto")
    preco = int(request.form.get("preco"))
    if "saldo" not in session:
        session["saldo"] = 300
    if session["saldo"] >= preco:
        session["saldo"] -= preco
    return redirect(url_for("loja"))
