# VIKAS-DRISHTI (विकास दृष्टि)
### AI-Powered MPLADS Risk Intelligence & Monitoring System
**Smart India Hackathon 2026 Prototype — Ministry of Statistics & Programme Implementation (MoSPI SIH26102)**

[![MoSPI](https://img.shields.io/badge/Ministry-MoSPI%20India-blue?style=for-the-badge)](https://mospi.gov.in)
[![SIH 2026](https://img.shields.io/badge/SIH%202026-Problem%20SIH26102-orange?style=for-the-badge)](https://sih.gov.in)
[![Python](https://img.shields.io/badge/Python-3.13-brightgreen?style=for-the-badge&logo=python)](https://python.org)
[![Scikit-Learn](https://img.shields.io/badge/ML-Isolation%20Forest%20%2B%20NLP-purple?style=for-the-badge)](https://scikit-learn.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

---

## 🏛️ Project Vision & Purpose

**VIKAS-DRISHTI** (*Vikas Drishti — Development Vision & Oversight*) is an AI-powered risk-intelligence and monitoring layer designed specifically for the **Members of Parliament Local Area Development Scheme (MPLADS)** ecosystem.

> [!IMPORTANT]
> **Complementary Architecture — Not a Replacement for eSAKSHI**:
> - **eSAKSHI**: Manages the official administrative implementation workflow, project sanctions, disbursements, and physical milestone tracking.
> - **VIKAS-DRISHTI**: Operates as an analytical intelligence layer that ingests project, financial, progress, payment, geospatial, and multilingual text data to identify unusual patterns and prioritize projects for officer verification.
> - **Core Objective**: `Detect → Explain → Recommend → Verify → Track`
> - **Institutional Governance Rule**: The AI **never** claims confirmed fraud. It identifies *"Potential anomalies"*, *"Risk signals"*, and *"Duplicate possibilities"*, prioritizing projects for human officer review. The final administrative authority always remains with the authorized human officer.

---

## 🧠 System Flow & Architecture

```
MPLADS / eSAKSHI DATA
       ↓
DATA INGESTION
       ↓
DATA CLEANING & VALIDATION
       ↓
FEATURE ENGINEERING
       ↓
AI/ML + RULE ENGINE (Isolation Forest + Multilingual NLP)
       ↓
MULTIPLE RISK SIGNALS
       ↓
RISK SCORING ENGINE (0 – 100)
       ↓
EXPLAINABLE AI (XAI Attribution)
       ↓
RISK ALERTS
       ↓
AI INVESTIGATION COPILOT
       ↓
HUMAN VERIFICATION (Gazetted Officer On-Site Review)
       ↓
ACTION / STATUS UPDATE
       ↓
IMMUTABLE AUDIT TRAIL (SHA-256)
```

**Conceptual Memory Anchor**: `DATA → CLEAN → AI → RISK → EXPLAIN → HUMAN → AUDIT`

---

## 🚀 Key Modules & Capabilities

### 1. Executive Government-Tech Dashboard
- **Sample Portfolio KPIs**: Monitored Works (12,458), Critical Risk (64), High Risk (98), Medium Risk (62), Low Risk (24).
- **Live Anomaly Signals Feed**: Real-time ticker streaming incoming cost anomalies, front-loading disbursements, timeline lags, and duplicate warnings.
- **6-Month Risk Trend Analytics**: Interactive historical chart tracking anomalies and delays, with an automated Early Warning alert for rural infrastructure cost escalations.
- **Interactive District / Location Risk Map**: Leaflet.js GIS map with color-coded risk markers (Red, Orange, Amber, Green), popup summaries, and one-click *"Open in Copilot"* navigation.
- **Prioritized Projects Explorer Table**: Real-time search by ID, title (English/Hindi), MP, village, and filtering by Risk Tier and District.

### 2. AI Investigation Copilot (Signature Feature)
- **Flagship Case Study**: `MP/SEH/CH/2024/10234` (*Construction of Community Hall, Village Pipaliya, Sehore, Madhya Pradesh*).
- **Verification Priority Score**: **92 / 100 (CRITICAL — VERIFY)**.
- **Transparent Multi-Signal Breakdown**:
  - *Cost Anomaly Detection*: `22 / 25` (Cost overrun +120.2%: ₹48.45L actual vs ₹22.00L sanctioned estimate).
  - *Project Delay & Velocity Lag*: `18 / 20` (Expected progress 85% vs actual 30%, 8 months delay).
  - *Spending vs Physical Progress Mismatch*: `17 / 20` (75% funds drawn against 30% physical ground completion).
  - *Multilingual Duplicate Possibility*: `15 / 15` (94% semantic match with nearby asset `MP/SEH/RES/2023/8892` located 1.4 km away).
  - *Other Unusual Patterns*: `20 / 20` (68% front-loaded advance tranche disbursed before plinth level, missing completion photos).
- **Explainable AI (XAI)**: Synthesizes plain-language administrative rationales for non-technical officers.
- **Project Twin / Peer Cohort Benchmark**: Side-by-side contrast comparing subject project (`₹48.45L`, `30%`, `17mo`) against regional peer cohort (`₹19.00L–₹23.50L`, `75%–85%`, `9–11mo`).
- **Interactive AI Recommended 5-Step Verification Checklist**:
  1. *Verify expenditure documents (bills, MB books, vouchers for ₹48.45L)*
  2. *Verify physical work progress (geo-tagged photos and ground inspection)*
  3. *Compare sanctioned vs actual cost (evaluate ₹26.45L cost deviation)*
  4. *Check nearby/similar projects (de-duplication review with GPDP asset 1.4km away)*
  5. *Verify payment records (PFMS tranche timeline and advance justification)*
  - Officers can click `[VERIFY]` $\rightarrow$ `[✓ COMPLETED]`, recording the officer's name, role, timestamp, and triggering a cryptographic audit entry.
- **Administrative Action Console**: Field inspection dispatch, show-cause notices to implementing agencies, state nodal escalations, and official justification records.
- **Printable / Exportable Official Verification Dossier**: Formats a formal MoSPI inspection memo ready for printing or saving as PDF.

### 3. Multilingual NLP Duplicate Detection Matrix
- Normalizes and vectorizes project titles in **English**, **Hindi (Devanagari script)**, and **Romanized Hinglish transliterations** (e.g. *"Construction of Community Hall"* vs *"सामुदायिक भवन निर्माण - पिपलिया"* or *"Samudayik Bhawan Nirman"*).
- Combines **Semantic Cosine Similarity + Spatial Haversine Distance (km) + Cost Bracket Scale** to identify potential overlaps across schemes (MPLADS, Jal Jeevan Mission, GPDP).
- Non-accusatory labeling: `POTENTIAL DUPLICATE SIGNAL` (never claims confirmed duplication).

### 4. Cost & Payment Intelligence
- **Isolation Forest Model**: Scikit-Learn unsupervised anomaly model identifying multidimensional outliers based on cost deviation, duration deviation, expenditure velocity, and tranche front-loading.
- **Spending vs Physical Progress Divergence**: Scatter chart against a 45-degree parity curve.
- **Tranche Velocity Table**: Detailed inspection of advance releases and milestone compliance.

### 5. Compliance & Early Warning Center
- **eSAKSHI Compliance Checkpoints**: Sanction / Approval (✓), Payment Record (✓), Progress Update (✓), Completion Evidence (⚠), Nearby Project Comparison (⚠).
- **Early Warning Bulletins**: Sectoral cost escalation trends and Q4 fiscal year-end tranche rush alerts.

### 6. Interactive AI Ingestion Simulator Sandbox
- Live test bench allowing evaluators to input custom project metrics (title in English/Hindi, costs, progress, duration, candidate duplicate titles) or choose one of 4 realistic presets.
- Executes the full pipeline `DATA → CLEAN → AI → RISK → EXPLAIN → RECOMMEND` live and displays the resulting score, breakdown, and checklist.

### 7. 5-Tier Role-Based Access Control (RBAC) & Immutable Audit Trail
- **Roles**: District Officer, State Nodal Authority, Ministry/Admin Officer, MP / Authorized Viewer, System Administrator.
- **Immutable Audit Trail**: Logs every human verification action and administrative decision with timestamp, officer designation, details, and tamper-evident SHA-256 cryptographic hashes.

---

## 🛠️ Quickstart Installation & Local Setup

### Prerequisites
- Python 3.10+ (tested on Python 3.13)
- Web Browser (Chrome, Edge, Firefox, or Safari)

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/vikas-drishti.git
cd vikas-drishti
```

### 2. Install Dependencies
```bash
python -m pip install -r requirements.txt
```

### 3. Start the Server
```bash
python server.py
```

### 4. Open in Browser
Visit:
```
http://localhost:8080
```

---

## 📡 REST API Reference

| Endpoint | Method | Description |
|---|---|---|
| `/api/summary` | `GET` | Portfolio metrics, 6-month trends, sector breakdown, live alerts. |
| `/api/projects` | `GET` | Filterable project dataset (`?tier=CRITICAL&district=Sehore&search=...`). |
| `/api/projects/<id>` | `GET` | Complete project dossier, financial tranches, peer comparisons. |
| `/api/verify-step` | `POST` | Interactive field verification toggle (`[VERIFY]` $\rightarrow$ `[✓ COMPLETED]`). |
| `/api/action` | `POST` | Officer administrative decisions (Inspection, Clarification Notice, Escalation). |
| `/api/analyze` | `POST` | Live AI pipeline execution (`DATA → CLEAN → AI → RISK → EXPLAIN`). |
| `/api/duplicates` | `GET` | Multilingual cross-lingual duplicate candidate matches. |
| `/api/audit` | `GET` | Tamper-evident audit trail records with SHA-256 hashes. |

---

## ⚖️ Institutional Governance & Disclaimer
- All statistics, project IDs, and locations are generated as **Sample Prototype Data** for demonstration purposes during the Smart India Hackathon 2026 evaluation.
- The risk scoring thresholds (0–30 Low, 31–60 Medium, 61–80 High, 81–100 Critical) and weight distributions (Cost 25, Delay 20, Spending-Progress 20, Duplication 15, Unusual Patterns 20) are prototype configuration values.
- **Risk Score represents priority for human verification**, not probability of fraud.
