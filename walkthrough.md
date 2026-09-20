# VIKAS-DRISHTI: AI-Powered MPLADS Risk Intelligence & Monitoring System
### Smart India Hackathon 2026 Prototype — Ministry of Statistics & Programme Implementation (MoSPI SIH26102)

---

## Executive Summary

**VIKAS-DRISHTI** (*विकास दृष्टि — Development Vision & Oversight*) is an AI-powered risk-intelligence and monitoring layer designed specifically for the **Members of Parliament Local Area Development Scheme (MPLADS)** ecosystem under the **Ministry of Statistics & Programme Implementation (MoSPI)**.

> [!IMPORTANT]
> **Complementary Architecture — Not a Replacement for eSAKSHI**:
> - **eSAKSHI**: Manages official administrative workflows, project sanctions, disbursements, and physical progress reporting.
> - **VIKAS-DRISHTI**: Operates as an analytical intelligence layer that ingests project, financial, progress, payment, geospatial, and multilingual text data to identify unusual patterns and prioritize projects for field verification.
> - **Core Philosophy**: `Detect → Explain → Recommend → Verify → Track`
> - **Conceptual Architecture Memory**: `DATA → CLEAN → AI → RISK → EXPLAIN → HUMAN → AUDIT`
> - **Institutional Governance Rule**: The AI **never** claims confirmed fraud. It identifies *"Potential anomalies"*, *"Risk signals"*, *"Duplicate possibilities"*, and generates verification priorities. Final administrative authority remains with authorized human officers.

---

## Key Modules Implemented

### 1. Executive Government-Tech Dashboard
- **Top Metrics Banner**: Displays prototype portfolio statistics:
  - **Total Monitored Projects**: 12,458
  - **Critical Risk (81–100)**: 64
  - **High Risk (61–80)**: 98
  - **Medium Risk (31–60)**: 62
  - **Low Risk (0–30)**: 24
  - Clearly labeled: *"Prototype Dashboard — Sample Data"*.
- **Live Anomaly Signals Feed**: Real-time ticker streaming incoming cost anomalies, front-loading spikes, timeline lags, and duplicate warnings.
- **6-Month Risk Trend Analytics**: Interactive historical chart tracking anomalies and delays, with an automated Early Warning alert for rural infrastructure cost escalations.
- **Interactive District / Location Risk Map**: Leaflet.js GIS map with color-coded risk markers (Red, Orange, Amber, Green), popup summaries, and one-click *"Open in Copilot"* navigation.
- **Prioritized Projects Explorer Table**: Real-time search by ID, title (English/Hindi), MP, village, and filtering by Risk Tier and District.

### 2. AI Investigation Copilot (Signature Feature)
- **Flagship Project**: `MP/SEH/CH/2024/10234` (*Construction of Community Hall, Village Pipaliya, Sehore, Madhya Pradesh*).
- **Verification Priority Score**: **92 / 100 (CRITICAL — VERIFY)**.
- **Transparent Multi-Signal Breakdown**:
  1. **Cost Anomaly Detection**: `22 / 25` (Cost deviation +120.2%: ₹48.45L actual vs ₹22.00L sanctioned estimate).
  2. **Project Delay & Velocity Lag**: `18 / 20` (Expected progress 85% vs actual 30%, 8 months delay).
  3. **Spending vs Physical Progress Mismatch**: `17 / 20` (75% funds drawn against 30% physical ground completion).
  4. **Multilingual Duplicate Possibility**: `15 / 15` (94% semantic match with nearby asset `MP/SEH/RES/2023/8892` located 1.4 km away).
  5. **Other Unusual Patterns**: `20 / 20` (68% front-loaded advance tranche disbursed before plinth level, missing completion photos).
- **Explainable AI (XAI)**: Plain-language administrative summary explaining why the project was prioritized.
- **Project Twin / Peer Cohort Benchmark**:
  - **This Project**: ₹48.45L | 30% progress | 17 months
  - **Similar Peer Cohort (n=42)**: ₹19.00L–₹23.50L | 75%–85% progress | 9–11 months
  - **Callout**: *"Cost and progress are significantly outside the typical peer cohort range."*
- **Interactive AI Recommended 5-Step Verification Checklist**:
  1. *Verify expenditure documents (bills, MB books, vouchers for ₹48.45L)*
  2. *Verify physical work progress (geo-tagged photos and ground inspection)*
  3. *Compare sanctioned vs actual cost (evaluate ₹26.45L cost deviation)*
  4. *Check nearby/similar projects (de-duplication review with GPDP asset 1.4km away)*
  5. *Verify payment records (PFMS tranche timeline and advance justification)*
  - Officers can click `[VERIFY]` $\rightarrow$ `[✓ COMPLETED]`, recording the officer's name, role, timestamp, and triggering a cryptographic audit entry.
- **Administrative Action Console**: Field inspection dispatch, show-cause notices to implementing agencies, state nodal escalations, and official justification records.
- **Printable / Exportable Official Verification Dossier**: Formats a formal MoSPI inspection memo ready for printing or saving as PDF.

### 3. Multilingual NLP Duplicate Detection Engine
- Normalizes and vectorizes project titles in **English**, **Hindi (Devanagari script)**, and **Romanized Hinglish transliterations** (e.g. *"Construction of Community Hall"* vs *"सामुदायिक भवन निर्माण - पिपलिया"* or *"Samudayik Bhawan Nirman"*).
- Combines **Semantic Cosine Similarity + Spatial Haversine Distance (km) + Cost Bracket Scale** to identify potential overlaps across schemes (MPLADS, JJM, GPDP).
- Non-accusatory labeling: `POTENTIAL DUPLICATE SIGNAL` (never claims confirmed duplication).

### 4. Cost & Payment Intelligence
- **Isolation Forest Model**: Scikit-Learn unsupervised anomaly model identifying multidimensional outliers based on cost deviation, duration deviation, expenditure velocity, and tranche front-loading.
- **Spending vs Physical Progress Divergence**: Scatter chart against a 45-degree parity curve.
- **Tranche Velocity Table**: Detailed inspection of advance releases and milestone compliance.

### 5. Compliance & Early Warning Center
- **eSAKSHI Compliance Checkpoints**:
  - Sanction / Approval Document: `✓ AVAILABLE`
  - PFMS Payment Records: `✓ AVAILABLE`
  - eSAKSHI Progress Update: `✓ UPDATED`
  - Geo-Tagged Completion Evidence: `⚠ PENDING VERIFICATION`
  - Nearby Project De-Duplication Comparison: `⚠ REVIEW REQUIRED`
- **Early Warning Bulletins**: Sectoral cost escalation trends and Q4 fiscal year-end tranche rush alerts.

### 6. Interactive AI Ingestion Simulator Sandbox
- Live test bench allowing evaluators to input custom project metrics (title in English/Hindi, costs, progress, duration, candidate duplicate titles) or choose one of 4 realistic presets.
- Executes the full pipeline `DATA → CLEAN → AI → RISK → EXPLAIN → RECOMMEND` live and displays the resulting score, breakdown, and checklist.

### 7. Role-Based Access Control (RBAC) & Immutable Audit Trail
- **5 Dynamic Roles**:
  1. *District Officer* (Sehore Collectorate)
  2. *State Nodal Authority* (Madhya Pradesh Planning)
  3. *Ministry/Admin Officer* (MoSPI National Directorate)
  4. *MP / Authorized Viewer* (Vidisha Constituency)
  5. *System Administrator* (Governance & Calibration)
- **Immutable Audit Trail**: Logs every human verification action and administrative decision with timestamp, officer designation, details, and tamper-evident SHA-256 cryptographic hashes.

---

## Verification & Test Results

All automated and manual tests passed successfully:

1. **Python AI Engine Test (`test_ai.py`)**:
   - Isolation Forest training on 500 peer records: **PASSED**
   - Multi-signal scoring and classification: **PASSED** (Output: Risk Score `92/100`, Tier `CRITICAL`).
   - Multilingual text normalization (Hindi, English, Hinglish): **PASSED**.

2. **REST API Endpoints Test (`test_endpoints.py`)**:
   - `GET /api/summary`: Status 200, returned 12,458 monitored works and trend series: **PASSED**.
   - `GET /api/projects`: Status 200, filtered query support: **PASSED**.
   - `GET /api/projects/MP_SEH_CH_2024_10234`: Status 200, full dossier loaded: **PASSED**.
   - `POST /api/verify-step`: Status 200, toggled checklist item to `completed: True` and generated audit entry: **PASSED**.
   - `POST /api/analyze`: Status 200, live AI execution on custom payload returned score and tier: **PASSED**.
   - `GET /api/audit`: Status 200, records returned with SHA-256 hashes: **PASSED**.
   - `GET /api/duplicates`: Status 200, cross-lingual pairs returned: **PASSED**.

3. **HTTP Server Status**:
   - Running live at: `http://localhost:8080`
   - Static asset delivery (`index.html`, `styles.css`, `app.js`): Status 200.

---

## How to Access the Live Application

1. Open your web browser (Chrome, Edge, Firefox, or Opera).
2. Navigate to:
   ```
   http://localhost:8080
   ```
3. **Interactive Demo Highlights to Explore**:
   - **Switch RBAC Roles**: Use the dropdown in the top right to switch between *District Officer*, *State Nodal Authority*, *Ministry/Admin Officer*, *MP Viewer*, and *System Administrator*.
   - **Explore the Executive Dashboard**: Inspect the 5 KPI cards, live anomaly feed, 6-month trend chart, and interactive Leaflet map.
   - **Test the AI Investigation Copilot**: Click the *"AI Investigation Copilot"* tab or click *"Copilot"* next to `MP/SEH/CH/2024/10234`. Inspect the 92/100 score breakdown, Project Twin comparison, and click the `[VERIFY]` buttons to toggle checklist items.
   - **Execute Administrative Actions**: In the Copilot, select an action (e.g., *Schedule On-Site Inspection*), enter remarks, and click *Execute Administrative Action* to watch it log to the Audit Trail.
   - **Export Official Dossier**: Click *Export Official Verification Dossier* to preview the printable formal government report.
   - **Review Multilingual Duplicates**: Open the *Multilingual Duplicate Matrix* tab to observe cross-lingual matching between English and Hindi descriptions.
   - **Run the AI Ingestion Simulator**: Go to the *AI Ingestion Sandbox* tab, select a preset (or type custom values), and click *Execute AI Pipeline* to see real-time calculation.
   - **Audit Trail**: Check the *Immutable Audit Trail* tab to review cryptographic SHA-256 records.
