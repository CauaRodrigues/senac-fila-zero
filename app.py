
from flask import Flask, jsonify, render_template

from services.fila_service import consultar_caixas

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/caixas", methods=["GET"])
def listar_caixas():
    try:
        caixas = consultar_caixas()

        return jsonify({
            "sucesso": True,
            "total": len(caixas),
            "caixas": caixas
        }), 200

    except (OSError, ValueError, KeyError) as erro:
        return jsonify({
            "sucesso": False,
            "mensagem": "Erro ao consultar os caixas.",
            "detalhes": str(erro)
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
