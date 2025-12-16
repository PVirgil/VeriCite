# 📚 VeriCite 

**VeriCite** is a next-generation blockchain designed to track, verify, and timestamp web sources and cited material for transparency, research integrity, and intellectual ownership. It immutably records source metadata, author identity, validation input, and hash summaries for anti-fraud and content trust applications.

Built in **Python using Flask**, VeriCite is fully deployable on **Vercel**, requiring no server management. With a clean public explorer, RESTful API, and file-based persistent ledger, VeriCite delivers decentralized source integrity.

---

## 🔍 Key Features

- 🔗 Immutable, timestamped record of submitted sources
- 🧾 Includes hash summaries, validators, and author info
- ⚒️ Proof-of-Work consensus for source authenticity
- 🌐 HTML web explorer with full chain visualization
- 🧠 REST API for submitting and mining verifiable content
- 💾 Local JSON ledger for offline backup or migration

---

## 📁 File Structure

```
/
├── vericite_app.py         # Main Flask app for Vercel
├── vericite_chain.json     # JSON ledger storage
├── requirements.txt        # Python dependency list
└── vercel.json             # Vercel deployment config
```

---

## 📦 Local Testing

```bash
pip install -r requirements.txt
python vericite_app.py
```

Open `http://localhost:5000` in your browser to view the blockchain explorer.

---

## 🌐 API Reference

| Method | Endpoint     | Description                       |
|--------|--------------|-----------------------------------|
| GET    | `/`          | Web-based blockchain explorer     |
| GET    | `/chain`     | Full chain JSON data              |
| GET    | `/mine`      | Mine the next pending submission  |
| POST   | `/submit`    | Submit a new source verification  |

### Example: `POST /submit`
```json
{
  "url": "https://example.com/research.pdf",
  "hash_summary": "f16e9a0...",
  "author": "Alice Author",
  "validator": "Verifier Org",
  "tags": ["climate", "peer-reviewed"]
}
```

---

## 🧠 Use Cases

- ✅ Journalism integrity and source validation
- ✅ Academic citation verification
- ✅ Digital content ownership and plagiarism tracking
- ✅ Proof-of-existence for research documents
- ✅ AI-generated content anchoring

---

> VeriCite ensures that the internet's most important content can be **verifiably cited, publicly reviewed, and permanently preserved.**
