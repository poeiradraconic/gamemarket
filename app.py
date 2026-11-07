from flask import Flask, render_template, request, redirect
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

os.makedirs("database", exist_ok=True)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../database/gamemarket.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(300), nullable=False)
    preco = db.Column(db.Float, nullable=False)


@app.route("/")
def inicio():
    produtos = Produto.query.all()
    return render_template("index.html", produtos=produtos)

@app.route("/adicionar", methods=["POST"])
def adicionar():
    nome = request.form["nome"]
    descricao = request.form["descricao"]
    preco = float(request.form["preco"])

    produto = Produto(
        nome=nome,
        descricao=descricao,
        preco=preco
    )

    db.session.add(produto)
    db.session.commit()

    return redirect("/")

@app.route("/editar/<int:id>", methods=["POST"])
def editar(id):
    produto = Produto.query.get_or_404(id)

    produto.nome = request.form["nome"]
    produto.descricao = request.form["descricao"]
    produto.preco = float(request.form["preco"])

    db.session.commit()

    return redirect("/")


@app.route("/excluir/<int:id>", methods=["POST"])
def excluir(id):
    produto = Produto.query.get_or_404(id)

    db.session.delete(produto)
    db.session.commit()

    return redirect("/")

with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
