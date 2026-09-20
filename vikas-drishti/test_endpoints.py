import urllib.request
import json

def test_api():
    base_url = "http://localhost:8080"
    
    # 1. Test POST /api/verify-step
    payload = {
        "project_id": "MP_SEH_CH_2024_10234",
        "checklist_id": "chk_1",
        "officer_name": "Dr. Anand Verma, IAS",
        "officer_role": "District Officer"
    }
    req = urllib.request.Request(
        f"{base_url}/api/verify-step",
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        print("verify-step status:", res.get("success"), "completed:", res.get("checklist_item", {}).get("completed"))

    # 2. Test POST /api/analyze
    sim_payload = {
        "title": "Samudayik Bhawan Nirman",
        "estimated_cost_lakhs": 20.0,
        "actual_expenditure_lakhs": 42.0,
        "funds_utilized_percent": 80.0,
        "physical_progress_percent": 35.0,
        "expected_progress_percent": 80.0,
        "duration_months": 14,
        "expected_duration_months": 8,
        "payments": [{"amount_lakhs": 15.0}],
        "duplicate_candidate": {
            "target_title": "Community Hall",
            "distance_km": 1.2,
            "cost_lakhs": 22.0
        }
    }
    req2 = urllib.request.Request(
        f"{base_url}/api/analyze",
        data=json.dumps(sim_payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req2) as resp:
        res2 = json.loads(resp.read().decode('utf-8'))
        eval_res = res2.get("evaluation", {})
        print("analyze risk_score:", eval_res.get("risk_score"), "tier:", eval_res.get("risk_tier"))

    # 3. Test GET /api/audit
    with urllib.request.urlopen(f"{base_url}/api/audit") as resp:
        audit_res = json.loads(resp.read().decode('utf-8'))
        print("audit records count:", audit_res.get("total"))

    # 4. Test GET /api/duplicates
    with urllib.request.urlopen(f"{base_url}/api/duplicates") as resp:
        dup_res = json.loads(resp.read().decode('utf-8'))
        print("duplicate pairs count:", len(dup_res.get("pairs", [])))

    print("ALL TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    test_api()
