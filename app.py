import os
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, Familia, Atendimento

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "troque-esta-chave")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db.init_app(app)

with app.app_context():
    db.create_all()


def login_obrigatorio(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("logado"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["usuario"] == "admin" and request.form["senha"] == "123456":
            session["logado"] = True
            return redirect(url_for("familias"))
        flash("Usuário ou senha inválidos", "danger")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/familias")
@login_obrigatorio
def familias():
    return render_template("familias.html", familias=Familia.query.order_by(Familia.responsavel).all())


@app.route("/familias/nova", methods=["GET", "POST"])
@login_obrigatorio
def nova_familia():
    if request.method == "POST":
        db.session.add(Familia(responsavel=request.form["responsavel"],
                               telefone=request.form["telefone"],
                               endereco=request.form["endereco"]))
        db.session.commit()
        flash("Família cadastrada com sucesso", "success")
        return redirect(url_for("familias"))
    return render_template("cadastrar_familia.html")


@app.route("/familias/<int:id>")
@login_obrigatorio
def historico(id):
    return render_template("historico.html", familia=Familia.query.get_or_404(id))


@app.route("/atendimento", methods=["GET", "POST"])
@login_obrigatorio
def atendimento():
    if request.method == "POST":
        db.session.add(Atendimento(descricao=request.form["descricao"],
                                   familia_id=int(request.form["familia"])))
        db.session.commit()
        flash("Atendimento registrado com sucesso", "success")
        return redirect(url_for("historico", id=request.form["familia"]))
    return render_template("atendimento.html", familias=Familia.query.all(),
                           selecionada=request.args.get("familia", type=int))


if __name__ == "__main__":
    app.run(debug=True)
