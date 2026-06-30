# PathFinder

### AI-Powered Legal Documentation Navigator for Aadhaar Inclusion

PathFinder is a full-stack decision-support system that helps frontline caseworkers, ASHA workers, and legal aid volunteers discover practical, rule-backed Aadhaar enrollment pathways for residents who lack standard identity or address documents.

---

## 📌 The Problem
Many vulnerable residents who most need public services are also the least likely to have complete documentation. Aadhaar enrollment becomes an insurmountable barrier for:
- Homeless or displaced individuals.
- Migrant workers.
- Children or young adults with limited school/birth records.
- Stateless residents or displaced communities.

Frontline workers often know the resident's local facts, but they get stuck navigating a complex web of government circulars, resulting in high application rejection rates.

## 💡 The Solution
PathFinder turns fragmented procedural knowledge into a guided, automated workflow. By combining a directed-graph recommendation engine, secure cloud storage, and automated PDF document generation, PathFinder enables ground teams to go from intake to action in minutes.

### 🌟 Key Features
- **Legal Path Recommendation:** Uses a NetworkX directed graph to trace available evidence, location rules, and witnesses, recommending the highest-confidence legal route to enrollment.
- **Bilingual Interface (English & हिंदी):** Toggle the entire application, form inputs, dynamic legal paths, and instructions instantly between English and Hindi to support local caseworkers.
- **Automated PDF Generation:** Generates print-ready ReportLab PDF documents (cover letters, community affidavits, and introducer declarations) pre-filled with the resident's details and legal references.
- **Hybrid Database Architecture:** Backed by **Neon PostgreSQL** in production for secure, scalable cloud storage, with a transparent local **SQLite** fallback for offline developer setup.
- **Interactive Dashboard Analytics:** Provides supervisors with real-time statistics on case volume, average path confidence, common enrollment blockages, and cases by district.

---

## ⚙️ Tech Stack
- **Frontend:** Next.js (React, TypeScript), Tailwind CSS (Premium glassmorphic theme), Lucide React.
- **Backend:** Python, FastAPI, Pydantic, NetworkX (Graph library), ReportLab (PDF Engine).
- **Database:** Neon PostgreSQL (Production Cloud) / SQLite (Local Fallback).
- **Localization:** Custom Language Context Provider (English / Hindi).

---

## 🏗️ Architecture

```mermaid
flowchart TD
  Worker["ASHA / Field Worker"] --> Frontend["Next.js UI (Bilingual)"]
  Frontend --> API["FastAPI Backend"]
  API --> Engine["Legal Graph Engine (NetworkX)"]
  API --> DBRouter["Database Router"]
  DBRouter --> Neon["Neon PostgreSQL (Cloud)"]
  DBRouter --> SQLite["SQLite Database (Local Fallback)"]
  API --> PDF["ReportLab PDF Generator"]
  Engine --> Rules["UIDAI Rules (knowledge/uidai_rules.json)"]
  PDF --> Files["Generated PDFs (pdfs/)"]
```

---

## 📂 Project Structure

```text
.
├── backend/
│   ├── main.py                  FastAPI app and API routes
│   └── app/
│       ├── database.py          PostgreSQL (Neon) & SQLite fallback router
│       ├── graph_engine.py      Directed-graph legal recommendation engine
│       ├── knowledge.py         Rule loader
│       ├── models.py            Pydantic request and response models
│       ├── pdf_generator.py     PDF document generation engine
│       └── seed.py              Automatic demo case seeder
├── frontend/
│   ├── app/
│   │   ├── page.tsx             Analytics Dashboard
│   │   ├── layout.tsx           Global layouts and theme
│   │   └── cases/
│   │       ├── new/page.tsx     3-Step new case wizard
│   │       └── [id]/page.tsx    Case details, legal routes, and PDF downloads
│   ├── components/              
│   │   ├── Header.tsx           Client nav header
│   │   ├── LanguageContext.tsx  Bilingual translation dictionary & toggle
│   │   ├── LanguageSwitcher.tsx Dropdown switcher & request modal
│   │   └── ThemeInitializer.tsx Background theme state loader
│   └── lib/
│       ├── api.ts               Frontend API client
│       └── types.ts             TypeScript types
├── knowledge/
│   └── uidai_rules.json         Legal rules knowledge base
├── requirements.txt             Python backend dependencies
├── package.json                 Root frontend command shortcuts
└── README.md
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.11+
- Node.js 18+

### 2. Backend Setup
Navigate to the `backend` directory, install requirements, and set up your environment:
```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file in the `backend` folder:
```env
PORT=8000
HOST=127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000

# (Optional) Cloud PostgreSQL connection (Neon.tech)
# DATABASE_URL=postgresql://user:password@ep-host.region.neon.tech/dbname?sslmode=require

# Local SQLite fallback configuration (used if DATABASE_URL is not set)
PATHFINDER_DATABASE=../database/pathfinder.db
PATHFINDER_PDF_DIR=../pdfs
```

Start the FastAPI server:
```bash
python main.py
```
*Note: On startup, the server automatically initializes tables and seeds 25 default cases!*

### 3. Frontend Setup
Navigate to the `frontend` directory, install packages, and start the development server:
```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000` to view the application.

---

## 📋 API Reference Summary
- `GET /health` - Service health status.
- `GET /stats` - Graph statistics & dashboard analytics.
- `POST /cases` - Intake a new case, generate path, and store in database.
- `GET /cases` - List saved cases (supports text search).
- `GET /cases/{id}` - Retrieve case details by ID.
- `POST /generate-pdf` - Generate and compile a ReportLab PDF for a case document.

---

## 🌟 Hackathon Demo Flow
1. **Dashboard Overview:** Show analytics, district metrics, common blocks, and the list of 25 seeded cases.
2. **Case Intake:** Click "New Case" and create a case (e.g. resident name: `Devansh`, problem: `Biometric Failure`).
3. **Bilingual Toggle:** Switch the language to **हिंदी** to show how ASHA workers can use the tool comfortably.
4. **Path & Output:** Review the recommended legal steps, explain the legal basis, click **Generate PDF** for the cover letter, and open the resulting document.
