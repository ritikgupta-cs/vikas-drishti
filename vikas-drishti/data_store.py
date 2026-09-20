"""
VIKAS-DRISHTI: AI-Powered MPLADS Risk Intelligence & Monitoring System
Data Store & Prototype Sample Repository
SIH 2026 - MoSPI Problem Statement SIH26102
"""

import datetime
import hashlib
import json

# Top-level portfolio metrics (clearly labeled as Prototype Sample Data)
PORTFOLIO_SUMMARY = {
    "total_projects": 12458,
    "critical_risk": 64,
    "high_risk": 98,
    "medium_risk": 62,
    "low_risk": 24,
    "total_sanctioned_amount_cr": 4820.50,
    "total_expenditure_cr": 3614.20,
    "compliance_rate_percent": 84.6,
    "pending_officer_verifications": 162,
    "last_model_sync": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
    "disclaimer": "Prototype Dashboard — Sample Data for MoSPI SIH26102 Evaluation. Not official government statistics."
}

# 6-Month Trend Data for Anomaly Types
TREND_DATA = {
    "months": ["Apr 2026", "May 2026", "Jun 2026", "Jul 2026", "Aug 2026", "Sep 2026"],
    "cost_anomalies": [14, 18, 22, 31, 45, 64],
    "project_delays": [28, 35, 42, 58, 71, 98],
    "spend_progress_mismatches": [19, 24, 30, 41, 52, 62],
    "duplicate_possibilities": [8, 12, 11, 15, 19, 24],
    "officer_verifications": [12, 19, 28, 44, 60, 89],
    "early_warning_alert": "Cost anomaly signals increased by +42% over the last 3 months in Rural Infrastructure works."
}

# Sample Projects Repository featuring Flagship Case Study and Diverse Real-World Scenarios
PROJECTS = [
    {
        "id": "MP_SEH_CH_2024_10234",
        "display_id": "MP/SEH/CH/2024/10234",
        "title": "Construction of Community Hall",
        "title_hi": "सामुदायिक भवन निर्माण",
        "sector": "Community Infrastructure",
        "state": "Madhya Pradesh",
        "district": "Sehore",
        "block": "Ichhawar",
        "village": "Pipaliya",
        "coordinates": {"lat": 23.0185, "lng": 77.0862},
        "mp_name": "Shri Ramakant Bhargava (Lok Sabha - Vidisha)",
        "sanction_date": "2024-03-12",
        "target_completion_date": "2024-12-15",
        "estimated_cost_lakhs": 22.00,
        "actual_expenditure_lakhs": 48.45,
        "sanctioned_amount_lakhs": 22.00,
        "physical_progress_percent": 30.0,
        "expected_progress_percent": 85.0,
        "duration_months": 17,
        "expected_duration_months": 9,
        "funds_utilized_percent": 75.0,
        "implementing_agency": "Rural Engineering Services (RES), Sehore",
        "contractor": "M/s Vindhya Infrastructure Ltd.",
        "risk_score": 92,
        "risk_tier": "CRITICAL",
        "status": "Verification Required",
        "signals_breakdown": {
            "cost_anomaly": {"score": 22, "max": 25, "signal": "Cost overrun +120.2% vs sanctioned estimate"},
            "delay": {"score": 18, "max": 20, "signal": "Delay of 8 months (actual progress 30% vs expected 85%)"},
            "spend_progress_mismatch": {"score": 17, "max": 20, "signal": "Funds utilized 75% while physical progress is only 30%"},
            "duplicate_possibility": {"score": 15, "max": 15, "signal": "High semantic match (94%) with nearby project MP/SEH/RES/2023/8892"},
            "other_patterns": {"score": 20, "max": 20, "signal": "Payment concentration: 68% released in first tranche before plinth level"}
        },
        "peer_comparison": {
            "cohort_name": "Rural Community Halls (Tier-3 Districts, Central India)",
            "cohort_sample_size": 42,
            "cost_range_lakhs": "₹19.00L – ₹23.50L",
            "avg_cost_lakhs": 21.20,
            "this_project_cost": 48.45,
            "progress_range_percent": "75% – 85%",
            "this_project_progress": 30.0,
            "duration_range_months": "9 – 11 months",
            "this_project_duration": 17,
            "deviation_callout": "Cost and progress are significantly outside the typical peer cohort range (+120% cost, -55% progress lag)."
        },
        "payments": [
            {"tranche": 1, "date": "2024-04-05", "amount_lakhs": 15.00, "stage": "Advance Mobilization", "status": "Disbursed", "anomaly": "High advance tranche (68% of sanction)"},
            {"tranche": 2, "date": "2024-07-20", "amount_lakhs": 18.00, "stage": "Plinth Level Completion", "status": "Disbursed", "anomaly": "MB Book measurement unverified"},
            {"tranche": 3, "date": "2024-11-10", "amount_lakhs": 15.45, "stage": "Superstructure Progress", "status": "Disbursed", "anomaly": "Exceeded sanctioned limit without revised approval"}
        ],
        "compliance": {
            "sanction_approval": {"status": "Available", "icon": "check", "doc_ref": "SAN-2024-RES-4091"},
            "payment_records": {"status": "Available", "icon": "check", "doc_ref": "PFMS-TX-904128"},
            "progress_update": {"status": "Updated (30 Days Ago)", "icon": "check", "doc_ref": "eSAKSHI-M-112"},
            "completion_evidence": {"status": "Pending Verification", "icon": "alert", "doc_ref": "Geo-tag photos missing"},
            "nearby_comparison": {"status": "Review Required", "icon": "alert", "doc_ref": "Overlapping asset located at 1.4km"}
        },
        "verification_checklist": [
            {"id": "chk_1", "title": "Verify expenditure documents", "desc": "Check bills, measurement books (MB), payment vouchers, and sanction orders for ₹48.45L expenditure.", "completed": False, "verified_by": None, "timestamp": None},
            {"id": "chk_2", "title": "Verify physical work progress", "desc": "Confirm actual site status against reported 30% progress via geo-tagged ground photos and physical inspection.", "completed": False, "verified_by": None, "timestamp": None},
            {"id": "chk_3", "title": "Compare sanctioned vs actual cost", "desc": "Review sanctioned estimate (₹22.00L) against actual spend (₹48.45L) to identify basis for ₹26.45L cost deviation.", "completed": False, "verified_by": None, "timestamp": None},
            {"id": "chk_4", "title": "Check nearby/similar projects", "desc": "Review potential duplicate work MP/SEH/RES/2023/8892 ('सामुदायिक भवन निर्माण - पिपलिया') located 1.4km away.", "completed": False, "verified_by": None, "timestamp": None},
            {"id": "chk_5", "title": "Verify payment records", "desc": "Check PFMS payment timelines and verify justification for 68% front-loaded tranche disbursement.", "completed": False, "verified_by": None, "timestamp": None}
        ],
        "ai_explanation": "Actual expenditure is significantly higher (+120%) than similar projects. Physical progress is below expectation (30% vs 85% expected), while 75% of funds have already been utilized. A potential duplicate work was also detected 1.4 km away with high multilingual semantic similarity.",
        "duplicate_candidate": {
            "target_id": "MP/SEH/RES/2023/8892",
            "target_title": "Samudayik Bhawan Nirman - Pipaliya",
            "target_title_hi": "सामुदायिक भवन निर्माण - पिपलिया",
            "distance_km": 1.4,
            "semantic_similarity": 0.94,
            "cost_lakhs": 20.50,
            "scheme": "Gram Panchayat Development Fund (GPDP)",
            "sanction_year": 2023
        }
    },
    {
        "id": "UP_VAR_RD_2024_08142",
        "display_id": "UP/VAR/RD/2024/08142",
        "title": "Construction of Interlocking CC Road and Drain",
        "title_hi": "सीसी सड़क एवं नाली निर्माण कार्य",
        "sector": "Rural Roads & Drainage",
        "state": "Uttar Pradesh",
        "district": "Varanasi",
        "block": "Kashi Vidyapeeth",
        "village": "Shivpur",
        "coordinates": {"lat": 25.3524, "lng": 82.9739},
        "mp_name": "Shri Narendra Modi (Lok Sabha - Varanasi)",
        "sanction_date": "2024-01-18",
        "target_completion_date": "2024-06-30",
        "estimated_cost_lakhs": 35.00,
        "actual_expenditure_lakhs": 34.20,
        "sanctioned_amount_lakhs": 35.00,
        "physical_progress_percent": 95.0,
        "expected_progress_percent": 100.0,
        "duration_months": 8,
        "expected_duration_months": 5,
        "funds_utilized_percent": 97.7,
        "implementing_agency": "Public Works Department (PWD) CD-1, Varanasi",
        "contractor": "M/s Ganga Constructions",
        "risk_score": 28,
        "risk_tier": "LOW",
        "status": "Normal - Completed",
        "signals_breakdown": {
            "cost_anomaly": {"score": 4, "max": 25, "signal": "Within ±5% peer threshold"},
            "delay": {"score": 8, "max": 20, "signal": "Minor delay of 2 months due to monsoon"},
            "spend_progress_mismatch": {"score": 5, "max": 20, "signal": "Spending 97.7% aligns with 95% physical progress"},
            "duplicate_possibility": {"score": 3, "max": 15, "signal": "No nearby duplicate work found within 5km"},
            "other_patterns": {"score": 8, "max": 20, "signal": "Standard milestone-linked tranches verified"}
        },
        "peer_comparison": {
            "cohort_name": "CC Roads & Drainage Works (Eastern UP)",
            "cohort_sample_size": 86,
            "cost_range_lakhs": "₹30.00L – ₹38.00L",
            "avg_cost_lakhs": 33.50,
            "this_project_cost": 34.20,
            "progress_range_percent": "90% – 100%",
            "this_project_progress": 95.0,
            "duration_range_months": "6 – 8 months",
            "this_project_duration": 8,
            "deviation_callout": "Project parameters lie comfortably within the expected peer cohort distribution."
        },
        "payments": [
            {"tranche": 1, "date": "2024-02-10", "amount_lakhs": 10.00, "stage": "Earthwork & Base Course", "status": "Disbursed", "anomaly": "None"},
            {"tranche": 2, "date": "2024-04-12", "amount_lakhs": 15.00, "stage": "CC Pavement Layer", "status": "Disbursed", "anomaly": "None"},
            {"tranche": 3, "date": "2024-07-02", "amount_lakhs": 9.20, "stage": "Drainage & Curing Final", "status": "Disbursed", "anomaly": "None"}
        ],
        "compliance": {
            "sanction_approval": {"status": "Available", "icon": "check", "doc_ref": "SAN-2024-PWD-1102"},
            "payment_records": {"status": "Available", "icon": "check", "doc_ref": "PFMS-TX-440192"},
            "progress_update": {"status": "Updated (7 Days Ago)", "icon": "check", "doc_ref": "eSAKSHI-M-481"},
            "completion_evidence": {"status": "Available", "icon": "check", "doc_ref": "Geo-tagged photos verified"},
            "nearby_comparison": {"status": "Cleared", "icon": "check", "doc_ref": "No overlapping roads"}
        },
        "verification_checklist": [
            {"id": "chk_1", "title": "Verify expenditure documents", "desc": "Check MB books and final settlement vouchers.", "completed": True, "verified_by": "District Engineer", "timestamp": "2024-08-10 11:30"},
            {"id": "chk_2", "title": "Verify physical work progress", "desc": "Confirm 95% completion on site.", "completed": True, "verified_by": "Junior Engineer", "timestamp": "2024-08-11 14:15"}
        ],
        "ai_explanation": "Project metrics reflect normal progress with minor seasonal delay. Expenditure aligns closely with physical output. No risk signals flagged.",
        "duplicate_candidate": None
    },
    {
        "id": "MH_PUN_DW_2024_03419",
        "display_id": "MH/PUN/DW/2024/03419",
        "title": "Installation of Solar-Powered Drinking Water RO Plant",
        "title_hi": "सौर ऊर्जा चालित पेयजल आरओ प्लांट स्थापना",
        "sector": "Drinking Water & Sanitation",
        "state": "Maharashtra",
        "district": "Pune",
        "block": "Haveli",
        "village": "Uruli Kanchan",
        "coordinates": {"lat": 18.4874, "lng": 74.1332},
        "mp_name": "Smt. Supriya Sule (Lok Sabha - Baramati)",
        "sanction_date": "2024-02-01",
        "target_completion_date": "2024-07-15",
        "estimated_cost_lakhs": 18.50,
        "actual_expenditure_lakhs": 27.80,
        "sanctioned_amount_lakhs": 18.50,
        "physical_progress_percent": 45.0,
        "expected_progress_percent": 90.0,
        "duration_months": 11,
        "expected_duration_months": 5,
        "funds_utilized_percent": 82.0,
        "implementing_agency": "Zilla Parishad Rural Water Supply Division, Pune",
        "contractor": "M/s Sahyadri Aqua Tech",
        "risk_score": 76,
        "risk_tier": "HIGH",
        "status": "Verification Required",
        "signals_breakdown": {
            "cost_anomaly": {"score": 19, "max": 25, "signal": "Cost escalation +50.3% beyond sanctioned limit"},
            "delay": {"score": 16, "max": 20, "signal": "Overdue by 6 months; progress stagnant at 45%"},
            "spend_progress_mismatch": {"score": 16, "max": 20, "signal": "82% funds drawn against 45% equipment commissioning"},
            "duplicate_possibility": {"score": 11, "max": 15, "signal": "Potential duplicate with Jal Jeevan Mission RO plant 800m away"},
            "other_patterns": {"score": 14, "max": 20, "signal": "Frequent contractor sub-letting reported"}
        },
        "peer_comparison": {
            "cohort_name": "Solar RO Drinking Water Plants (Western Maharashtra)",
            "cohort_sample_size": 54,
            "cost_range_lakhs": "₹16.00L – ₹19.50L",
            "avg_cost_lakhs": 17.80,
            "this_project_cost": 27.80,
            "progress_range_percent": "80% – 95%",
            "this_project_progress": 45.0,
            "duration_range_months": "4 – 6 months",
            "this_project_duration": 11,
            "deviation_callout": "Cost is +56% above cohort average; progress is lagging by 45 percentage points."
        },
        "payments": [
            {"tranche": 1, "date": "2024-03-01", "amount_lakhs": 10.00, "stage": "Machinery Procurement Advance", "status": "Disbursed", "anomaly": "Vendor invoices pending verification"},
            {"tranche": 2, "date": "2024-06-15", "amount_lakhs": 12.80, "stage": "Civil Shed and Borewell", "status": "Disbursed", "anomaly": "Photographic proof missing"}
        ],
        "compliance": {
            "sanction_approval": {"status": "Available", "icon": "check", "doc_ref": "SAN-2024-ZP-881"},
            "payment_records": {"status": "Available", "icon": "check", "doc_ref": "PFMS-TX-102948"},
            "progress_update": {"status": "Overdue (60+ Days)", "icon": "alert", "doc_ref": "eSAKSHI-M-091"},
            "completion_evidence": {"status": "Pending Verification", "icon": "alert", "doc_ref": "RO plant commissioning certificate pending"},
            "nearby_comparison": {"status": "Review Required", "icon": "alert", "doc_ref": "Jal Jeevan Mission asset at 800m"}
        },
        "verification_checklist": [
            {"id": "chk_1", "title": "Verify equipment delivery", "desc": "Check membrane and solar panel serial numbers on site.", "completed": False, "verified_by": None, "timestamp": None},
            {"id": "chk_2", "title": "Check Jal Jeevan Mission overlap", "desc": "Ensure scheme funds are not co-claimed with JJM village RO asset.", "completed": False, "verified_by": None, "timestamp": None},
            {"id": "chk_3", "title": "Verify water quality test reports", "desc": "Inspect certified lab water potability test reports.", "completed": False, "verified_by": None, "timestamp": None}
        ],
        "ai_explanation": "Severe cost deviation (+50%) paired with low physical execution (45%). High expenditure drawn upfront while equipment installation remains unverified. Proximity to existing Jal Jeevan unit requires de-duplication review.",
        "duplicate_candidate": {
            "target_id": "JJM/PUN/2023/4491",
            "target_title": "Gramin Shudh Jal Yojna RO Kendra",
            "target_title_hi": "ग्रामीण शुद्ध जल योजना आरओ केंद्र",
            "distance_km": 0.8,
            "semantic_similarity": 0.88,
            "cost_lakhs": 18.00,
            "scheme": "Jal Jeevan Mission (State-Centre 50:50)",
            "sanction_year": 2023
        }
    },
    {
        "id": "RJ_JAI_ED_2024_05921",
        "display_id": "RJ/JAI/ED/2024/05921",
        "title": "Addition of 2 Additional Classrooms & Computer Lab in Govt Senior Secondary School",
        "title_hi": "राजकीय उच्च माध्यमिक विद्यालय में 2 अतिरिक्त कक्षा-कक्ष एवं कंप्यूटर लैब निर्माण",
        "sector": "Education & Youth Development",
        "state": "Rajasthan",
        "district": "Jaipur Rural",
        "block": "Chomu",
        "village": "Morija",
        "coordinates": {"lat": 27.1723, "lng": 75.7289},
        "mp_name": "Col. Rajyavardhan Singh Rathore (Lok Sabha - Jaipur Rural)",
        "sanction_date": "2024-02-20",
        "target_completion_date": "2024-09-30",
        "estimated_cost_lakhs": 28.00,
        "actual_expenditure_lakhs": 32.50,
        "sanctioned_amount_lakhs": 28.00,
        "physical_progress_percent": 65.0,
        "expected_progress_percent": 80.0,
        "duration_months": 9,
        "expected_duration_months": 7,
        "funds_utilized_percent": 72.0,
        "implementing_agency": "Samagra Shiksha Abhiyan (SSA) Engineering Cell, Jaipur",
        "contractor": "M/s Shekhawati Builders",
        "risk_score": 48,
        "risk_tier": "MEDIUM",
        "status": "Under Review",
        "signals_breakdown": {
            "cost_anomaly": {"score": 11, "max": 25, "signal": "Moderate cost variance +16% due to IT lab cabling"},
            "delay": {"score": 10, "max": 20, "signal": "Delay of 2 months in IT procurement tender"},
            "spend_progress_mismatch": {"score": 9, "max": 20, "signal": "Expenditure (72%) slightly leads progress (65%)"},
            "duplicate_possibility": {"score": 8, "max": 15, "signal": "State education budget had classroom allotment in 2022"},
            "other_patterns": {"score": 10, "max": 20, "signal": "Standard compliance documentation submitted"}
        },
        "peer_comparison": {
            "cohort_name": "School Classrooms & ICT Labs (Semi-Arid Rajasthan)",
            "cohort_sample_size": 68,
            "cost_range_lakhs": "₹26.00L – ₹30.50L",
            "avg_cost_lakhs": 28.20,
            "this_project_cost": 32.50,
            "progress_range_percent": "70% – 85%",
            "this_project_progress": 65.0,
            "duration_range_months": "6 – 8 months",
            "this_project_duration": 9,
            "deviation_callout": "Slight cost elevation (+15%) related to solar battery backup integration."
        },
        "payments": [
            {"tranche": 1, "date": "2024-03-15", "amount_lakhs": 12.00, "stage": "Civil Structure Construction", "status": "Disbursed", "anomaly": "None"},
            {"tranche": 2, "date": "2024-06-25", "amount_lakhs": 11.50, "stage": "Roofing and Wiring", "status": "Disbursed", "anomaly": "None"}
        ],
        "compliance": {
            "sanction_approval": {"status": "Available", "icon": "check", "doc_ref": "SAN-2024-SSA-710"},
            "payment_records": {"status": "Available", "icon": "check", "doc_ref": "PFMS-TX-665123"},
            "progress_update": {"status": "Updated (14 Days Ago)", "icon": "check", "doc_ref": "eSAKSHI-M-332"},
            "completion_evidence": {"status": "In Progress", "icon": "alert", "doc_ref": "IT equipment delivery challan awaited"},
            "nearby_comparison": {"status": "Cleared", "icon": "check", "doc_ref": "SSA campus verification ok"}
        },
        "verification_checklist": [
            {"id": "chk_1", "title": "Verify IT equipment specifications", "desc": "Check 15 desktops and UPS batch numbers against tender specs.", "completed": False, "verified_by": None, "timestamp": None},
            {"id": "chk_2", "title": "Check building safety certificate", "desc": "Obtain structural stability memo from PWD AE.", "completed": True, "verified_by": "Block Education Officer", "timestamp": "2024-09-02 10:00"}
        ],
        "ai_explanation": "Moderate risk flagged primarily due to slight delay in IT lab outfitting and 16% cost variance. Routine verification recommended before releasing final payment tranche.",
        "duplicate_candidate": None
    },
    {
        "id": "WB_HOW_HL_2024_09115",
        "display_id": "WB/HOW/HL/2024/09115",
        "title": "Establishment of Health Sub-Centre & Diagnostic Clinic",
        "title_hi": "स्वास्थ्य उप-केंद्र एवं निदान क्लिनिक निर्माण",
        "sector": "Public Health & Sanitation",
        "state": "West Bengal",
        "district": "Howrah",
        "block": "Uluberia I",
        "village": "Baniban",
        "coordinates": {"lat": 22.4744, "lng": 88.1065},
        "mp_name": "Sajda Ahmed (Lok Sabha - Uluberia)",
        "sanction_date": "2023-11-10",
        "target_completion_date": "2024-05-30",
        "estimated_cost_lakhs": 42.00,
        "actual_expenditure_lakhs": 58.90,
        "sanctioned_amount_lakhs": 42.00,
        "physical_progress_percent": 35.0,
        "expected_progress_percent": 95.0,
        "duration_months": 15,
        "expected_duration_months": 7,
        "funds_utilized_percent": 88.0,
        "implementing_agency": "Howrah Zilla Parishad Health Cell",
        "contractor": "M/s Hooghly River Infrastructure",
        "risk_score": 87,
        "risk_tier": "CRITICAL",
        "status": "Escalated to State Authority",
        "signals_breakdown": {
            "cost_anomaly": {"score": 23, "max": 25, "signal": "Cost overrun +40.2% with multiple revised estimates"},
            "delay": {"score": 19, "max": 20, "signal": "9 months delayed; work stalled at brickwork stage"},
            "spend_progress_mismatch": {"score": 18, "max": 20, "signal": "88% funds disbursed with only 35% physical construction"},
            "duplicate_possibility": {"score": 9, "max": 15, "signal": "Nearby National Health Mission (NHM) primary clinic sanctioned"},
            "other_patterns": {"score": 18, "max": 20, "signal": "Sudden burst of 4 payments within 12 days in March closing"}
        },
        "peer_comparison": {
            "cohort_name": "Health Sub-Centres (Gangetic Plains / Delta)",
            "cohort_sample_size": 39,
            "cost_range_lakhs": "₹38.00L – ₹44.00L",
            "avg_cost_lakhs": 41.50,
            "this_project_cost": 58.90,
            "progress_range_percent": "85% – 95%",
            "this_project_progress": 35.0,
            "duration_range_months": "6 – 8 months",
            "this_project_duration": 15,
            "deviation_callout": "Significant divergence from peer benchmarks in both cost (+42%) and duration (+88%)."
        },
        "payments": [
            {"tranche": 1, "date": "2024-01-10", "amount_lakhs": 15.00, "stage": "Civil Foundation", "status": "Disbursed", "anomaly": "None"},
            {"tranche": 2, "date": "2024-03-24", "amount_lakhs": 12.00, "stage": "Brickwork Stage", "status": "Disbursed", "anomaly": "March rush release"},
            {"tranche": 3, "date": "2024-03-28", "amount_lakhs": 15.00, "stage": "Roof Casting Advance", "status": "Disbursed", "anomaly": "Released within 4 days of Tranche 2"},
            {"tranche": 4, "date": "2024-03-31", "amount_lakhs": 9.90, "stage": "Internal Plaster & Fixtures", "status": "Disbursed", "anomaly": "Site physical verification missing"}
        ],
        "compliance": {
            "sanction_approval": {"status": "Available", "icon": "check", "doc_ref": "SAN-2023-HZP-204"},
            "payment_records": {"status": "Available", "icon": "check", "doc_ref": "PFMS-TX-990231"},
            "progress_update": {"status": "Stale (90+ Days)", "icon": "alert", "doc_ref": "eSAKSHI-M-019"},
            "completion_evidence": {"status": "Pending Verification", "icon": "alert", "doc_ref": "Civil sub-structure uninspected"},
            "nearby_comparison": {"status": "Review Required", "icon": "alert", "doc_ref": "NHM Sub-Centre located 1.1 km away"}
        },
        "verification_checklist": [
            {"id": "chk_1", "title": "Audit March financial tranche rush", "desc": "Investigate justification for ₹36.90L disbursed across 7 days in March 2024 without updated MB book entries.", "completed": False, "verified_by": None, "timestamp": None},
            {"id": "chk_2", "title": "Physical ground audit of clinic structure", "desc": "Send flying inspection squad with geo-tag camera to verify actual physical completion.", "completed": False, "verified_by": None, "timestamp": None},
            {"id": "chk_3", "title": "Check NHM scheme convergence", "desc": "Ensure MPLADS allocation does not overlap with ongoing NHM clinic refurbishment.", "completed": False, "verified_by": None, "timestamp": None}
        ],
        "ai_explanation": "Critical priority: Disproportionate expenditure velocity (₹36.9L released in 7 days before financial year close) against stalled ground progress (35%). Cost exceeds regional peer cohort by 42%.",
        "duplicate_candidate": {
            "target_id": "NHM/WB/HOW/2023/1102",
            "target_title": "Primary Ayush Sub-Centre Modernisation",
            "target_title_hi": "प्राथमिक आयुष उप-केंद्र आधुनिकीकरण",
            "distance_km": 1.1,
            "semantic_similarity": 0.81,
            "cost_lakhs": 25.00,
            "scheme": "National Health Mission (NHM)",
            "sanction_year": 2023
        }
    },
    {
        "id": "KA_BLR_CM_2024_01108",
        "display_id": "KA/BLR/CM/2024/01108",
        "title": "Development of Public Park & Senior Citizen Open Gymnasium",
        "title_hi": "सार्वजनिक उद्यान एवं वरिष्ठ नागरिक ओपन जिम विकास",
        "sector": "Community Infrastructure & Sports",
        "state": "Karnataka",
        "district": "Bengaluru South",
        "block": "Jayanagar",
        "village": "Ward 153 Jayanagar",
        "coordinates": {"lat": 12.9304, "lng": 77.5838},
        "mp_name": "Shri Tejasvi Surya (Lok Sabha - Bengaluru South)",
        "sanction_date": "2024-03-01",
        "target_completion_date": "2024-08-31",
        "estimated_cost_lakhs": 25.00,
        "actual_expenditure_lakhs": 24.50,
        "sanctioned_amount_lakhs": 25.00,
        "physical_progress_percent": 90.0,
        "expected_progress_percent": 95.0,
        "duration_months": 6,
        "expected_duration_months": 6,
        "funds_utilized_percent": 92.0,
        "implementing_agency": "BBMP Horticulture & Engineering Cell",
        "contractor": "M/s Green Canopy Landscapes",
        "risk_score": 19,
        "risk_tier": "LOW",
        "status": "Normal - Near Completion",
        "signals_breakdown": {
            "cost_anomaly": {"score": 3, "max": 25, "signal": "Within ±2% of sanctioned budget"},
            "delay": {"score": 4, "max": 20, "signal": "On-schedule milestone completion"},
            "spend_progress_mismatch": {"score": 4, "max": 20, "signal": "Expenditure (92%) matches physical progress (90%)"},
            "duplicate_possibility": {"score": 4, "max": 15, "signal": "Distinct municipal asset registry entry"},
            "other_patterns": {"score": 4, "max": 20, "signal": "All vendor invoices & warranties in order"}
        },
        "peer_comparison": {
            "cohort_name": "Urban Open Gyms & Parks (Metro BBMP / MMRDA)",
            "cohort_sample_size": 72,
            "cost_range_lakhs": "₹22.00L – ₹28.00L",
            "avg_cost_lakhs": 24.80,
            "this_project_cost": 24.50,
            "progress_range_percent": "85% – 95%",
            "this_project_progress": 90.0,
            "duration_range_months": "5 – 7 months",
            "this_project_duration": 6,
            "deviation_callout": "Exemplary performance metrics aligned with urban public amenity benchmarks."
        },
        "payments": [
            {"tranche": 1, "date": "2024-03-20", "amount_lakhs": 8.00, "stage": "Civil Pathway & Landscaping", "status": "Disbursed", "anomaly": "None"},
            {"tranche": 2, "date": "2024-05-18", "amount_lakhs": 10.00, "stage": "Gym Equipment Delivery", "status": "Disbursed", "anomaly": "None"},
            {"tranche": 3, "date": "2024-07-29", "amount_lakhs": 6.50, "stage": "Lighting, Benches & Greenery", "status": "Disbursed", "anomaly": "None"}
        ],
        "compliance": {
            "sanction_approval": {"status": "Available", "icon": "check", "doc_ref": "SAN-2024-BBMP-910"},
            "payment_records": {"status": "Available", "icon": "check", "doc_ref": "PFMS-TX-338102"},
            "progress_update": {"status": "Updated (3 Days Ago)", "icon": "check", "doc_ref": "eSAKSHI-M-771"},
            "completion_evidence": {"status": "Available", "icon": "check", "doc_ref": "Ground geo-tagged photos uploaded"},
            "nearby_comparison": {"status": "Cleared", "icon": "check", "doc_ref": "Dedicated park parcel"}
        },
        "verification_checklist": [
            {"id": "chk_1", "title": "Verify gym equipment installation", "desc": "Check BIS certification on 12 outdoor gym units.", "completed": True, "verified_by": "BBMP Assistant Engineer", "timestamp": "2024-08-01 16:00"}
        ],
        "ai_explanation": "Project operates within normal operational parameters. Cost, progress velocity, and disbursement tranches show high concordance with peer benchmarks.",
        "duplicate_candidate": None
    }
]

# Audit Trail entries tracking human-in-the-loop actions
AUDIT_TRAIL = [
    {
        "id": "AUD-2026-0920-001",
        "timestamp": "2026-09-20 11:15:22 UTC",
        "officer_name": "Dr. Anand Verma, IAS",
        "officer_role": "District Officer (Collector & DM)",
        "district": "Sehore",
        "project_id": "MP/SEH/CH/2024/10234",
        "action": "Inspection Squad Dispatched",
        "details": "Initiated formal verification for cost anomaly (+120%) and duplicate check. Dispatched RES Sub-Divisional Engineer for ground audit.",
        "decision_category": "Verification In-Progress",
        "sha256_hash": "a8f90c4d7e218903bfe4d8721c09e13a48e710293bf65a12093e871cd0123fab"
    },
    {
        "id": "AUD-2026-0920-002",
        "timestamp": "2026-09-20 09:40:11 UTC",
        "officer_name": "Smt. Meenakshi Rao",
        "officer_role": "State Nodal Authority",
        "district": "Howrah",
        "project_id": "WB/HOW/HL/2024/09115",
        "action": "Escalation Notice Issued",
        "details": "Flagged March financial disbursement rush (₹36.90L in 7 days). Requested Zilla Parishad CEO for detailed MB measurement vouchers.",
        "decision_category": "Escalated for Audit",
        "sha256_hash": "b2c3d4e5f60718293a4b5c6d7e8f90123456789abcdef0123456789abcdef012"
    },
    {
        "id": "AUD-2026-0919-014",
        "timestamp": "2026-09-19 16:22:05 UTC",
        "officer_name": "Shri Rajesh Kumar, IDAS",
        "officer_role": "Ministry/Admin Officer (MoSPI)",
        "district": "National Portfolio",
        "project_id": "ALL_PORTFOLIO",
        "action": "Model Weights Recalibration Run",
        "details": "Calibrated Isolation Forest sensitivity threshold for rural works. Recalculated risk priorities across 12,458 active works.",
        "decision_category": "System Governance",
        "sha256_hash": "c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4"
    }
]

# Multilingual Dictionary for Duplicate Recognition & Translation Normalization
MULTILINGUAL_LEXICON = {
    # Hindi Devanagari -> Standard Concept
    "सामुदायिक": "community",
    "भवन": "hall",
    "निर्माण": "construction",
    "सड़क": "road",
    "नाली": "drain",
    "पेयजल": "drinking water",
    "सोलर": "solar",
    "जल": "water",
    "योजना": "scheme",
    "कक्षा": "classroom",
    "कक्ष": "room",
    "विद्यालय": "school",
    "स्वास्थ्य": "health",
    "उप-केंद्र": "sub-centre",
    "उद्यान": "park",
    "पार्क": "park",
    "जिम": "gym",
    "पुस्तकालय": "library",
    "शौचालय": "sanitation",

    # Hinglish Transliterations -> Standard Concept
    "samudayik": "community",
    "bhawan": "hall",
    "nirman": "construction",
    "sadak": "road",
    "nali": "drain",
    "pejal": "drinking water",
    "ro": "ro",
    "shiksha": "education",
    "swasthya": "health",
    "kendra": "centre",
    "udyan": "park"
}


def add_audit_event(officer_name, officer_role, district, project_id, action, details, category):
    """Generates an immutable audit trail entry with SHA-256 hash."""
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    raw_payload = f"{ts}|{officer_name}|{officer_role}|{project_id}|{action}|{details}"
    event_hash = hashlib.sha256(raw_payload.encode('utf-8')).hexdigest()
    new_entry = {
        "id": f"AUD-{datetime.datetime.now().strftime('%Y-%m%d')}-{len(AUDIT_TRAIL)+1:03d}",
        "timestamp": ts,
        "officer_name": officer_name,
        "officer_role": officer_role,
        "district": district,
        "project_id": project_id,
        "action": action,
        "details": details,
        "decision_category": category,
        "sha256_hash": event_hash
    }
    AUDIT_TRAIL.insert(0, new_entry)
    return new_entry
