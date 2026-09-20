"""
VIKAS-DRISHTI: AI-Powered MPLADS Risk Intelligence & Monitoring System
High-Performance Python HTTP REST Server
SIH 2026 - MoSPI Problem Statement SIH26102
"""

import datetime
import json
import mimetypes
import os
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler

import data_store
from ai_engine import ai_engine

PORT = 8080
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class VikasDrishtiHandler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        # 1. API: Portfolio Summary
        if path == '/api/summary':
            summary_payload = dict(data_store.PORTFOLIO_SUMMARY)
            summary_payload["trend_data"] = data_store.TREND_DATA
            summary_payload["active_signals_count"] = sum(
                len(p.get("signals_breakdown", {})) for p in data_store.PROJECTS if p.get("risk_tier") in ["CRITICAL", "HIGH"]
            )
            # Add dynamic counts from live store
            critical_live = sum(1 for p in data_store.PROJECTS if p.get("risk_tier") == "CRITICAL")
            high_live = sum(1 for p in data_store.PROJECTS if p.get("risk_tier") == "HIGH")
            summary_payload["live_critical_count"] = critical_live
            summary_payload["live_high_count"] = high_live
            return self._send_json(summary_payload)

        # 2. API: Projects List with Filters
        elif path == '/api/projects':
            tier_filter = query.get('tier', ['ALL'])[0].upper()
            district_filter = query.get('district', ['ALL'])[0]
            sector_filter = query.get('sector', ['ALL'])[0]
            search_query = query.get('search', [''])[0].strip().lower()

            filtered = []
            for p in data_store.PROJECTS:
                if tier_filter != 'ALL' and p.get('risk_tier') != tier_filter:
                    continue
                if district_filter != 'ALL' and p.get('district') != district_filter:
                    continue
                if sector_filter != 'ALL' and p.get('sector') != sector_filter:
                    continue
                if search_query:
                    searchable = f"{p.get('id')} {p.get('display_id')} {p.get('title')} {p.get('title_hi')} {p.get('district')} {p.get('village')} {p.get('mp_name')}".lower()
                    if search_query not in searchable:
                        continue
                filtered.append(p)
            return self._send_json({"total": len(filtered), "projects": filtered})

        # 3. API: Single Project Detail
        elif path.startswith('/api/projects/'):
            project_id = path.split('/api/projects/')[1].strip()
            # Match by id or display_id
            match = None
            for p in data_store.PROJECTS:
                if p.get('id') == project_id or p.get('display_id') == project_id or p.get('id').replace('_', '/') == project_id:
                    match = p
                    break
            if match:
                return self._send_json(match)
            else:
                return self._send_json({"error": f"Project '{project_id}' not found"}, status=404)

        # 4. API: Audit Trail
        elif path == '/api/audit':
            return self._send_json({"audit_records": data_store.AUDIT_TRAIL, "total": len(data_store.AUDIT_TRAIL)})

        # 5. API: Duplicates Matrix
        elif path == '/api/duplicates':
            pairs = []
            for p in data_store.PROJECTS:
                cand = p.get("duplicate_candidate")
                if cand:
                    pairs.append({
                        "source_id": p.get("display_id"),
                        "source_title": p.get("title"),
                        "source_title_hi": p.get("title_hi"),
                        "source_cost": p.get("actual_expenditure_lakhs"),
                        "source_district": p.get("district"),
                        "source_village": p.get("village"),
                        "target_id": cand.get("target_id"),
                        "target_title": cand.get("target_title"),
                        "target_title_hi": cand.get("target_title_hi"),
                        "target_cost": cand.get("cost_lakhs"),
                        "distance_km": cand.get("distance_km"),
                        "semantic_similarity": cand.get("semantic_similarity"),
                        "scheme": cand.get("scheme"),
                        "sanction_year": cand.get("sanction_year")
                    })
            return self._send_json({"pairs": pairs})

        # Static File Serving (index.html, styles.css, app.js, assets)
        else:
            rel_path = path.lstrip('/')
            if not rel_path or rel_path == '':
                rel_path = 'index.html'

            filepath = os.path.join(BASE_DIR, rel_path)
            # Security check
            if not os.path.commonpath([BASE_DIR, os.path.abspath(filepath)]) == BASE_DIR:
                self.send_error(403, "Access Denied")
                return

            if os.path.exists(filepath) and os.path.isfile(filepath):
                ctype, _ = mimetypes.guess_type(filepath)
                if not ctype:
                    ctype = 'application/octet-stream'
                if ctype.startswith('text/') or ctype in ['application/javascript', 'application/json']:
                    ctype += '; charset=utf-8'

                with open(filepath, 'rb') as f:
                    content = f.read()

                self.send_response(200)
                self.send_header('Content-Type', ctype)
                self.send_header('Content-Length', str(len(content)))
                self.end_headers()
                self.wfile.write(content)
            else:
                self.send_error(404, f"File {rel_path} not found")

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # Read JSON body
        content_len = int(self.headers.get('Content-Length', 0))
        post_body = self.rfile.read(content_len).decode('utf-8')
        try:
            payload = json.loads(post_body) if post_body else {}
        except Exception:
            payload = {}

        # 1. API: Toggle Checklist Item Verification
        if path == '/api/verify-step':
            project_id = payload.get('project_id')
            chk_id = payload.get('checklist_id')
            officer_name = payload.get('officer_name', 'Authorized Officer')
            officer_role = payload.get('officer_role', 'District Officer')

            found_project = None
            for p in data_store.PROJECTS:
                if p.get('id') == project_id or p.get('display_id') == project_id:
                    found_project = p
                    break

            if not found_project:
                return self._send_json({"error": "Project not found"}, status=404)

            target_item = None
            for item in found_project.get('verification_checklist', []):
                if item.get('id') == chk_id:
                    target_item = item
                    break

            if not target_item:
                return self._send_json({"error": "Checklist item not found"}, status=404)

            # Toggle state
            new_state = not target_item.get('completed', False)
            target_item['completed'] = new_state
            ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
            target_item['verified_by'] = f"{officer_name} ({officer_role})" if new_state else None
            target_item['timestamp'] = ts if new_state else None

            # Check if all completed
            all_completed = all(i.get('completed') for i in found_project.get('verification_checklist', []))
            if all_completed:
                found_project['status'] = "Field Verified - Under Officer Review"

            # Log to Audit Trail
            action_name = f"Checklist item '{target_item.get('title')}' marked as {'COMPLETED' if new_state else 'PENDING'}"
            audit_entry = data_store.add_audit_event(
                officer_name=officer_name,
                officer_role=officer_role,
                district=found_project.get('district', 'N/A'),
                project_id=found_project.get('display_id'),
                action=action_name,
                details=f"Human-in-the-loop verification update on item {chk_id}. All items completed: {all_completed}",
                category="Field Verification"
            )

            return self._send_json({
                "success": True,
                "checklist_item": target_item,
                "all_completed": all_completed,
                "project_status": found_project.get('status'),
                "audit_entry": audit_entry
            })

        # 2. API: Officer Administrative Decision Action
        elif path == '/api/action':
            project_id = payload.get('project_id')
            action_type = payload.get('action_type', 'Inspection')
            remarks = payload.get('remarks', '')
            officer_name = payload.get('officer_name', 'Dr. Anand Verma, IAS')
            officer_role = payload.get('officer_role', 'District Officer')

            found_project = None
            for p in data_store.PROJECTS:
                if p.get('id') == project_id or p.get('display_id') == project_id:
                    found_project = p
                    break

            if not found_project:
                return self._send_json({"error": "Project not found"}, status=404)

            # Update project status according to action
            if action_type == "SCHEDULE_INSPECTION":
                found_project['status'] = "On-Site Inspection Scheduled"
                desc = f"Field inspection scheduled. Officer Remarks: {remarks}"
                cat = "Site Inspection"
            elif action_type == "CLARIFICATION_NOTICE":
                found_project['status'] = "Clarification Notice Issued to Agency"
                desc = f"Formal show-cause issued to {found_project.get('implementing_agency')}. Remarks: {remarks}"
                cat = "Agency Notice"
            elif action_type == "ESCALATE_STATE":
                found_project['status'] = "Escalated to State Nodal Authority"
                desc = f"Escalated to State Planning Department for specialized technical audit. Remarks: {remarks}"
                cat = "State Escalation"
            elif action_type == "RESOLVE_JUSTIFIED":
                found_project['status'] = "Variance Justified & Approved"
                desc = f"Technical variance explained and approved by competent officer. Remarks: {remarks}"
                cat = "Administrative Resolution"
            else:
                desc = f"Administrative action recorded. Remarks: {remarks}"
                cat = "General Action"

            audit_entry = data_store.add_audit_event(
                officer_name=officer_name,
                officer_role=officer_role,
                district=found_project.get('district', 'N/A'),
                project_id=found_project.get('display_id'),
                action=f"Administrative Action: {action_type}",
                details=desc,
                category=cat
            )

            return self._send_json({
                "success": True,
                "project_status": found_project['status'],
                "audit_entry": audit_entry
            })

        # 3. API: Live AI Ingestion Pipeline Simulator
        elif path == '/api/analyze':
            # Evaluates candidate project data through the complete pipeline:
            # DATA → CLEAN → AI → RISK → EXPLAIN → RECOMMEND
            res = ai_engine.evaluate_project_risk(payload)
            return self._send_json({
                "success": True,
                "input_received": payload,
                "evaluation": res
            })

        else:
            return self._send_json({"error": "Endpoint not found"}, status=404)

def run_server():
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, VikasDrishtiHandler)
    print(f"============================================================")
    print(f"VIKAS-DRISHTI: AI-Powered MPLADS Risk Intelligence System")
    print(f"Server operational at: http://localhost:{PORT}")
    print(f"MoSPI SIH26102 Prototype")
    print(f"============================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Stopping server...")
        httpd.server_close()

if __name__ == '__main__':
    run_server()
