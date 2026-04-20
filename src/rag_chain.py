import os
from groq import Groq
from dotenv import load_dotenv
from src.retriever import Retriever

load_dotenv()

GROQ_MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = """Tu es un assistant spécialisé dans la filière Art Numérique de l'ENSPY 
(École Nationale Supérieure Polytechnique de Yaoundé).

Tu réponds uniquement en te basant sur les extraits du document fournis dans le contexte.
Si la réponse ne se trouve pas dans le contexte, dis-le clairement sans inventer.
Tes réponses sont précises, complètes et en français.
Quand tu vois des tableaux dans le contexte (balises [TABLEAU]), utilise-les pour structurer ta réponse."""

class RAGChain:
    def __init__(self):
        self.retriever = Retriever()
        self.client    = Groq(api_key=os.getenv("GROQ_API_KEY"))
        print("✅ RAGChain prêt")

    def repondre(self, question):
        # Étape 1 : retrieval
        docs     = self.retriever.rechercher(question, n_resultats=4)
        contexte = self.retriever.construire_contexte(docs)

        # Étape 2 : prompt
        prompt_utilisateur = f"""Contexte extrait du document AN.pdf :

{contexte}

---

Question : {question}

Réponds de manière complète en te basant uniquement sur le contexte ci-dessus."""

        # Étape 3 : appel Groq
        reponse = self.client.chat.completions.create(
            model    = GROQ_MODEL,
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": prompt_utilisateur}
            ],
            temperature = 0.2,
            max_tokens  = 1024
        )

        texte_reponse = reponse.choices[0].message.content

        # Étape 4 : retourner réponse + sources
        return {
            "reponse" : texte_reponse,
            "sources" : [
                {
                    "index"  : doc["index"],
                    "score"  : doc["score"],
                    "extrait": doc["texte"][:150] + "..."
                }
                for doc in docs
            ]
        }