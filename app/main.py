import os
import sys

# Ajouter la racine du projet au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, jsonify
from src.rag_chain import RAGChain

app = Flask(__name__)

print("⏳ Initialisation du RAG...")
rag = RAGChain()
print("✅ Application prête !")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data     = request.get_json()
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "Question vide"}), 400

    try:
        resultat = rag.repondre(question)
        return jsonify({
            "reponse" : resultat["reponse"],
            "sources" : resultat["sources"]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)