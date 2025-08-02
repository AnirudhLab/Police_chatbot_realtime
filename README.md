# Police Legal Chatbot (Offline RAG)

A fully offline, retrieval-augmented chatbot for Indian legal and police queries. Users can ask questions in English or Tamil and get actionable, law-backed answers with references to IPC, IT Act, Taxation, and more. No cloud LLMs or external APIs required.

---

## Features
- **Multilingual**: Supports English and Tamil queries and answers.
- **Offline RAG**: All legal knowledge is loaded from local CSV/Excel files. No internet or cloud LLM required.
- **Practical Guidance**: Answers include step-by-step actions, legal references, and real-life examples.
- **Covers Multiple Domains**: IPC, IT Act, Taxation, Motor Vehicles, and more.
- **Modern UI**: Clean React frontend for easy interaction.

---

## Project Structure
```
Police_chatbot_realtime/
├── app.py                  # Flask backend entrypoint
├── requirements.txt        # Python dependencies
├── data/                   # All legal CSV/Excel files (IPC, IT, Tax, etc.)
├── app/                   # Backend modules (core, services, api)
│   ├── core/              # Document loader, embeddings, vector store
│   ├── services/          # Retrieval, translation, chat logic
│   └── api/               # API routes
└── frontend/              # React frontend (Create React App)
```

---

## Data Files
- Place all legal data files (CSV/XLSX) in the `data/` folder.
- Each file should have headers like:
  - `Law Type`, `Law Name/Section`, `Law Details`, `Law Summary`, `Applicability`, `Whom to Approach`, `Historical Context`, `Real-life Example`
- Example: `ipc_laws_updated.csv`, `it_cyber_laws_Version.csv`, `taxation_laws_Version3.csv`

---

## Backend (Flask)
- Loads and processes all data files at startup.
- Splits documents, generates embeddings, and builds a vector store for retrieval.
- Exposes API endpoints:
  - `POST /api/chat` — Query the chatbot (`{"query": "...", "language": "en|ta"}`)
  - `GET /api/health` — Health check
- Uses sentence-transformers for embeddings, scikit-learn for vector search, and googletrans/langdetect for translation.
- CORS enabled for frontend communication.

### Run Backend
```sh
pip install -r requirements.txt
python app.py
```

---

## Frontend (React)
- Located in `frontend/` (Create React App)
- Modern, responsive UI for chat
- Calls backend API directly (edit API URL in `App.js` if needed)

### Run Frontend
```sh
cd frontend
npm install
npm start
```

---

## Adding/Updating Legal Data
- Edit or add CSV/XLSX files in `data/`.
- Use clear, user-focused language in `Law Summary`, `Applicability`, and `Whom to Approach` fields for best results.
- Restart backend after updating data files.

---

## Example Query/Response
**Q:** My mobile phone was stolen. What should I do?

**A:**
- Main Answer: Protects your belongings from theft. Ensures police investigate and recover your property.
- Applicability: If your phone, vehicle, or any item is stolen.
- Whom to Approach: Report to your local police station and get a copy of the FIR.
- Legal Reference: IPC Section 379 - Theft

---

## Technical Stack
- **Backend**: Python, Flask, pandas, sentence-transformers, scikit-learn, googletrans, langdetect
- **Frontend**: React (CRA), fetch API
- **Data**: CSV/XLSX files (IPC, IT Act, Tax, etc.)

---

## Deployment
- For production, use `gunicorn` or similar WSGI server for Flask.
- Serve frontend with any static file server or via Flask if desired.

---

## License
MIT (or specify your own)

---

## Maintainers
- [Your Name/Org]

---

## Troubleshooting
- If answers are not relevant, improve the `Law Summary` and `Applicability` fields in your data files.
- For multilingual support, ensure translation packages are installed and data is clear.
- Restart backend after any data changes.
