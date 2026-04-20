# 🎨 Assistant RAG — Filière Art Numérique ENSPY

Un assistant intelligent basé sur la technologie **RAG (Retrieval-Augmented Generation)** 
permettant d'interroger le document officiel de la filière Art Numérique de l'ENSPY 
(École Nationale Supérieure Polytechnique de Yaoundé).

---

## Comment ça fonctionne ?
1. Le document PDF est lu et découpé en blocs de texte (chunks)
2. Chaque chunk est transformé en vecteur numérique (embedding)
3. Les vecteurs sont stockés localement dans ChromaDB
4. Quand l'utilisateur pose une question, elle est vectorisée
5. Les chunks les plus proches sont récupérés par similarité cosinus
6. Groq (LLaMA 3.3 70B) génère une réponse à partir de ces extraits

---

## Stack technique

| Composant | Technologie |
|---|---|
| Extraction PDF | pdfplumber |
| Embeddings | sentence-transformers — paraphrase-multilingual-MiniLM-L12-v2 |
| Base vectorielle | ChromaDB |
| LLM | Groq — LLaMA 3.3 70B Versatile |
| Backend | Flask |
| Frontend | HTML / CSS / JavaScript |

---

## Structure du projet
---

## Installation et lancement

### 1. Cloner le projet

```bash
git clone https://github.com/dnl-pro/AN-ENSPY.git
cd AN-ENSPY
```

### 2. Créer un environnement virtuel

```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer la clé API

Crée un fichier `.env` à la racine du projet :

```env
GROQ_API_KEY=ta_cle_api_groq
```

> Obtiens ta clé gratuitement sur [console.groq.com](https://console.groq.com)

### 5. Indexer le document PDF

Ouvre et exécute toutes les cellules du notebook :
### 6. Lancer l'application

```bash
python app/main.py
```

Ouvre ensuite [http://127.0.0.1:5000](http://127.0.0.1:5000) dans ton navigateur.

---

## Auteur

Projet réalisé dans le cadre de la filière **Art Numérique** de l'**ENSPY**.
