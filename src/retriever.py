import os
from sentence_transformers import SentenceTransformer
import chromadb

MODEL_NAME      = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
COLLECTION_NAME = "an_enspy"

# chroma_db est dans le dossier notebooks/
BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROMA_PATH = os.path.join(BASE_DIR, "notebooks", "chroma_db")

class Retriever:
    def __init__(self):
        print(f"📂 ChromaDB path : {CHROMA_PATH}")
        print("⏳ Chargement du modèle d'embedding...")
        self.model = SentenceTransformer(MODEL_NAME)
        
        self.client     = chromadb.PersistentClient(path=CHROMA_PATH)
        self.collection = self.client.get_collection(COLLECTION_NAME)
        
        print(f"✅ Retriever prêt — {self.collection.count()} chunks disponibles")

    def rechercher(self, question, n_resultats=4):
        embedding = self.model.encode([question]).tolist()
        
        resultats = self.collection.query(
            query_embeddings=embedding,
            n_results=n_resultats
        )
        
        chunks    = resultats["documents"][0]
        distances = resultats["distances"][0]
        metadatas = resultats["metadatas"][0]
        
        docs = []
        for chunk, distance, meta in zip(chunks, distances, metadatas):
            docs.append({
                "texte"  : chunk,
                "score"  : round(1 - distance, 3),
                "source" : meta.get("source", "AN.pdf"),
                "index"  : meta.get("chunk_index", "?")
            })
        
        docs.sort(key=lambda x: x["score"], reverse=True)
        return docs

    def construire_contexte(self, docs):
        contexte = ""
        for i, doc in enumerate(docs):
            contexte += f"[Extrait {i+1} — score {doc['score']}]\n"
            contexte += doc["texte"]
            contexte += "\n\n"
        return contexte.strip()