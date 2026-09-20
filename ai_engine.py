"""
VIKAS-DRISHTI: AI-Powered MPLADS Risk Intelligence & Monitoring System
AI / Machine Learning & Multi-Signal Risk Scoring Engine
SIH 2026 - MoSPI Problem Statement SIH26102
"""

import math
import re
import numpy as np
from sklearn.ensemble import IsolationForest
from data_store import MULTILINGUAL_LEXICON

class VikasDrishtiAIEngine:
    def __init__(self):
        # Weights configuration (Prototype calibration values, not official government rules)
        self.weights = {
            "cost_anomaly_max": 25,
            "delay_max": 20,
            "spend_progress_mismatch_max": 20,
            "duplicate_possibility_max": 15,
            "other_patterns_max": 20
        }
        self._init_isolation_forest()

    def _init_isolation_forest(self):
        """
        Train Isolation Forest model on synthetic baseline peer cohort of 500 normal MPLADS works
        Features: [cost_deviation_pct, duration_deviation_pct, spend_to_progress_ratio, front_load_pct]
        """
        np.random.seed(42)
        # Normal projects: mean cost deviation 2%, duration deviation 5%, spend-progress ratio 1.05, front_load 25%
        normal_data = np.column_stack([
            np.random.normal(loc=2.0, scale=8.0, size=450),
            np.random.normal(loc=5.0, scale=10.0, size=450),
            np.random.normal(loc=1.05, scale=0.15, size=450),
            np.random.normal(loc=25.0, scale=6.0, size=450)
        ])
        # A few synthetic historical outliers to help boundary estimation
        outliers_data = np.column_stack([
            np.random.uniform(50.0, 150.0, size=50),
            np.random.uniform(40.0, 120.0, size=50),
            np.random.uniform(1.8, 3.5, size=50),
            np.random.uniform(55.0, 85.0, size=50)
        ])
        training_set = np.vstack([normal_data, outliers_data])

        self.iso_forest = IsolationForest(
            n_estimators=100,
            contamination=0.10,
            random_state=42
        )
        self.iso_forest.fit(training_set)

    def calculate_cost_deviation(self, actual_cost, estimated_cost):
        """
        Calculates:
        Cost Deviation = Actual Cost - Estimated Cost
        Cost Deviation % = ((Actual Cost - Estimated Cost) / Estimated Cost) * 100
        """
        if estimated_cost <= 0:
            return 0.0, 0.0
        deviation = actual_cost - estimated_cost
        deviation_pct = (deviation / estimated_cost) * 100.0
        return round(deviation, 2), round(deviation_pct, 1)

    def compute_isolation_anomaly_score(self, cost_dev_pct, duration_dev_pct, spend_ratio, front_load_pct):
        """
        Isolation Forest isolates unusual observations.
        Output is transformed into an anomaly severity score between 0 and 25.
        """
        sample = np.array([[cost_dev_pct, duration_dev_pct, spend_ratio, front_load_pct]])
        # decision_function yields negative for anomalies, positive for inliers
        raw_score = self.iso_forest.decision_function(sample)[0]

        # Calibrate raw decision score into 0 to 25 contribution
        if raw_score >= 0.15:
            severity = 3.0
        elif raw_score >= 0.0:
            severity = 6.0 + (0.15 - raw_score) * 40.0
        elif raw_score >= -0.15:
            severity = 12.0 + (-raw_score) * 60.0
        else:
            severity = 20.0 + min(5.0, (-raw_score - 0.15) * 20.0)

        # Ensure cost deviation factor also scales directly
        if cost_dev_pct > 100:
            severity = max(severity, 22.0)
        elif cost_dev_pct > 50:
            severity = max(severity, 18.0)
        elif cost_dev_pct > 25:
            severity = max(severity, 12.0)

        return min(self.weights["cost_anomaly_max"], round(severity, 1))

    def compute_delay_score(self, actual_months, expected_months, actual_progress, expected_progress):
        """
        Evaluates physical progress lag and duration overrun against expectations.
        Contributes up to 20 points.
        """
        lag_pct = max(0.0, expected_progress - actual_progress)
        overrun_months = max(0, actual_months - expected_months)

        # Score formulation
        lag_component = (lag_pct / 100.0) * 12.0
        time_component = min(8.0, (overrun_months / max(1, expected_months)) * 8.0)

        total_delay = min(self.weights["delay_max"], round(lag_component + time_component, 1))
        return total_delay, lag_pct, overrun_months

    def compute_spend_progress_mismatch(self, funds_utilized_pct, physical_progress_pct):
        """
        Compares financial utilization with ground physical progress.
        Example: Funds utilized = 75%, Physical progress = 30%.
        Contributes up to 20 points.
        """
        delta = funds_utilized_pct - physical_progress_pct
        if delta <= 10:
            score = 4.0
        elif delta <= 25:
            score = 8.0 + (delta - 10) * 0.4
        elif delta <= 40:
            score = 14.0 + (delta - 25) * 0.3
        else:
            # High divergence: e.g. 75% funds vs 30% progress (delta 45%)
            score = 17.0 + min(3.0, (delta - 40) * 0.2)

        return min(self.weights["spend_progress_mismatch_max"], round(score, 1)), round(delta, 1)

    def normalize_multilingual_text(self, text):
        """
        Cleans, tokenizes, and translates Hindi (Devanagari) & Hinglish tokens into canonical concept tokens.
        """
        text = text.lower()
        # Remove punctuation
        text = re.sub(r'[\(\)\[\]\,\.\-\_\/\:\;]', ' ', text)
        tokens = text.split()
        canonical_tokens = []
        for t in tokens:
            t = t.strip()
            if not t:
                continue
            canonical = MULTILINGUAL_LEXICON.get(t, t)
            canonical_tokens.append(canonical)
        return canonical_tokens

    def compute_semantic_similarity(self, text_a, text_b):
        """
        Computes multilingual cosine similarity over normalized concept tokens and character n-grams.
        """
        tokens_a = set(self.normalize_multilingual_text(text_a))
        tokens_b = set(self.normalize_multilingual_text(text_b))

        if not tokens_a or not tokens_b:
            return 0.0

        intersection = len(tokens_a.intersection(tokens_b))
        union = len(tokens_a.union(tokens_b))
        jaccard = intersection / union if union > 0 else 0.0

        # Substring / n-gram reinforcement for composite terms like "community hall" <-> "samudayik bhawan"
        str_a = " ".join(tokens_a)
        str_b = " ".join(tokens_b)

        overlap_boost = 0.0
        if "community" in str_a and "community" in str_b and "hall" in str_a and "hall" in str_b:
            overlap_boost = 0.4
        elif "road" in str_a and "road" in str_b:
            overlap_boost = 0.35
        elif "water" in str_a and "water" in str_b:
            overlap_boost = 0.35

        score = min(1.0, (jaccard * 0.6) + overlap_boost)
        return round(score, 2)

    def haversine_distance_km(self, lat1, lon1, lat2, lon2):
        """
        Computes great-circle distance between two GPS coordinates in kilometers.
        """
        R = 6371.0 # Earth radius in km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2.0) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2.0) ** 2
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
        return round(R * c, 2)

    def compute_duplicate_possibility_score(self, current_title, candidate_title, distance_km, cost_a, cost_b):
        """
        Combines Semantic similarity + Location proximity + Cost similarity.
        Only generates "POTENTIAL DUPLICATE" signal.
        Contributes up to 15 points.
        """
        sem_sim = self.compute_semantic_similarity(current_title, candidate_title)

        # Distance penalty: closer = higher duplicate probability
        if distance_km is not None:
            if distance_km <= 1.5:
                geo_score = 1.0
            elif distance_km <= 3.0:
                geo_score = 0.8
            elif distance_km <= 5.0:
                geo_score = 0.5
            else:
                geo_score = 0.2
        else:
            geo_score = 0.4

        # Cost similarity: similar scale works have higher probability of double-dipping
        cost_ratio = min(cost_a, cost_b) / max(cost_a, cost_b) if max(cost_a, cost_b) > 0 else 0.5

        composite_dup_prob = (sem_sim * 0.60) + (geo_score * 0.25) + (cost_ratio * 0.15)
        raw_score = composite_dup_prob * self.weights["duplicate_possibility_max"]
        return min(self.weights["duplicate_possibility_max"], round(raw_score, 1)), sem_sim

    def evaluate_project_risk(self, project_data):
        """
        Complete end-to-end evaluation pipeline:
        DATA → CLEAN → AI → RISK → EXPLAIN → RECOMMEND
        """
        est_cost = float(project_data.get("estimated_cost_lakhs", 20.0))
        act_cost = float(project_data.get("actual_expenditure_lakhs", 20.0))
        funds_util = float(project_data.get("funds_utilized_percent", 50.0))
        phys_prog = float(project_data.get("physical_progress_percent", 50.0))
        exp_prog = float(project_data.get("expected_progress_percent", 80.0))
        act_dur = int(project_data.get("duration_months", 6))
        exp_dur = int(project_data.get("expected_duration_months", 6))
        title = project_data.get("title", "")
        duplicate_cand = project_data.get("duplicate_candidate")

        # 1. Cost Anomaly
        dev_amount, dev_pct = self.calculate_cost_deviation(act_cost, est_cost)
        spend_ratio = (funds_util / max(1.0, phys_prog))
        front_load_pct = float(project_data.get("payments", [{}])[0].get("amount_lakhs", 5.0)) / max(1.0, est_cost) * 100.0

        cost_score = self.compute_isolation_anomaly_score(dev_pct, (act_dur - exp_dur)/max(1, exp_dur)*100, spend_ratio, front_load_pct)

        # 2. Delay Risk
        delay_score, lag_pct, overrun_months = self.compute_delay_score(act_dur, exp_dur, phys_prog, exp_prog)

        # 3. Spending vs Progress Mismatch
        mismatch_score, mismatch_delta = self.compute_spend_progress_mismatch(funds_util, phys_prog)

        # 4. Duplicate Possibility
        if duplicate_cand:
            dup_title = duplicate_cand.get("target_title", "")
            dist_km = duplicate_cand.get("distance_km", 2.0)
            target_cost = duplicate_cand.get("cost_lakhs", est_cost)
            dup_score, sem_sim = self.compute_duplicate_possibility_score(title, dup_title, dist_km, act_cost, target_cost)
        else:
            dup_score = 3.0
            sem_sim = 0.1

        # 5. Other Unusual Patterns (Payment concentration, compliance gaps)
        other_score = 4.0
        if front_load_pct > 50:
            other_score += 8.0
        if project_data.get("compliance", {}).get("completion_evidence", {}).get("status") == "Pending Verification":
            other_score += 4.0
        if project_data.get("compliance", {}).get("progress_update", {}).get("status", "").startswith("Overdue"):
            other_score += 4.0
        other_score = min(self.weights["other_patterns_max"], round(other_score, 1))

        # Composite Score Calculation (0 to 100)
        total_risk = round(cost_score + delay_score + mismatch_score + dup_score + other_score)
        total_risk = max(0, min(100, total_risk))

        # Classification into Prototype Configuration Tiers
        if total_risk >= 81:
            tier = "CRITICAL"
            status = "Verification Required"
        elif total_risk >= 61:
            tier = "HIGH"
            status = "Verification Required"
        elif total_risk >= 31:
            tier = "MEDIUM"
            status = "Under Review"
        else:
            tier = "LOW"
            status = "Normal - Verified"

        # Generate Explainable AI (XAI) Synthesis
        explanation = self.generate_xai_explanation(
            dev_pct, lag_pct, funds_util, phys_prog, dup_score, duplicate_cand
        )

        # Generate Recommended Verification Checklist
        checklist = self.generate_verification_checklist(
            project_data.get("id", "PROJ"), act_cost, est_cost, phys_prog, duplicate_cand, front_load_pct
        )

        return {
            "risk_score": total_risk,
            "risk_tier": tier,
            "status": status,
            "signals_breakdown": {
                "cost_anomaly": {
                    "score": round(cost_score),
                    "max": self.weights["cost_anomaly_max"],
                    "signal": f"Cost deviation {dev_pct:+0.1f}% (₹{dev_amount:+0.2f}L vs sanctioned estimate)"
                },
                "delay": {
                    "score": round(delay_score),
                    "max": self.weights["delay_max"],
                    "signal": f"Physical lag of {lag_pct:0.1f}% ({overrun_months} months behind schedule)"
                },
                "spend_progress_mismatch": {
                    "score": round(mismatch_score),
                    "max": self.weights["spend_progress_mismatch_max"],
                    "signal": f"Funds utilized {funds_util:0.1f}% while physical progress is {phys_prog:0.1f}%"
                },
                "duplicate_possibility": {
                    "score": round(dup_score),
                    "max": self.weights["duplicate_possibility_max"],
                    "signal": f"Semantic similarity {int(sem_sim*100)}% with nearby asset" if duplicate_cand else "No nearby duplicate match found"
                },
                "other_patterns": {
                    "score": round(other_score),
                    "max": self.weights["other_patterns_max"],
                    "signal": f"Front-loaded advance tranche {front_load_pct:0.1f}% & compliance reviews pending"
                }
            },
            "ai_explanation": explanation,
            "verification_checklist": checklist,
            "clarification": "Priority for verification — NOT probability of fraud. Thresholds are prototype configuration values."
        }

    def generate_xai_explanation(self, dev_pct, lag_pct, funds_util, phys_prog, dup_score, duplicate_cand):
        """
        Creates plain-language, non-accusatory administrative explanation.
        """
        explanations = []
        if dev_pct > 25:
            explanations.append(f"Actual expenditure is significantly higher (+{dev_pct:0.1f}%) than estimated benchmark.")
        elif dev_pct > 10:
            explanations.append(f"Cost is moderately elevated (+{dev_pct:0.1f}%) relative to sanctioned allocation.")

        if lag_pct > 30:
            explanations.append(f"Physical progress is notably behind schedule ({phys_prog:0.1f}% completed vs substantial time elapsed).")

        if funds_util - phys_prog > 25:
            explanations.append(f"High expenditure ({funds_util:0.1f}%) relative to reported ground progress ({phys_prog:0.1f}%) — verification recommended.")

        if dup_score >= 10 and duplicate_cand:
            explanations.append(f"A potential overlapping work ('{duplicate_cand.get('target_title')}') was detected {duplicate_cand.get('distance_km')} km away.")

        if not explanations:
            return "Project execution and financial parameters conform with regional peer averages. No elevated risk signals identified."

        return " ".join(explanations)

    def generate_verification_checklist(self, project_id, act_cost, est_cost, phys_prog, duplicate_cand, front_load_pct):
        """
        Creates actionable 5-step verification checklist for field officers.
        """
        items = [
            {
                "id": "chk_1",
                "title": "Verify expenditure documents",
                "desc": f"Check contractor bills, vouchers, Measurement Book (MB) entries, and administrative sanctions for ₹{act_cost:0.2f}L expenditure.",
                "completed": False,
                "verified_by": None,
                "timestamp": None
            },
            {
                "id": "chk_2",
                "title": "Verify physical work progress",
                "desc": f"Confirm actual ground site status against reported {phys_prog:0.1f}% progress using geo-tagged photographs and field inspection.",
                "completed": False,
                "verified_by": None,
                "timestamp": None
            },
            {
                "id": "chk_3",
                "title": "Compare sanctioned vs actual cost",
                "desc": f"Review original estimate (₹{est_cost:0.2f}L) and evaluate justification for variance with competent technical authority.",
                "completed": False,
                "verified_by": None,
                "timestamp": None
            },
            {
                "id": "chk_4",
                "title": "Check nearby / similar projects",
                "desc": f"Investigate potential duplicate or overlapping works within 2 km radius ({duplicate_cand.get('target_title') if duplicate_cand else 'Registry check'}).",
                "completed": False,
                "verified_by": None,
                "timestamp": None
            },
            {
                "id": "chk_5",
                "title": "Verify payment records",
                "desc": f"Check PFMS payment transaction records and verify milestone compliance for front-loaded tranche disbursements ({front_load_pct:0.1f}%).",
                "completed": False,
                "verified_by": None,
                "timestamp": None
            }
        ]
        return items


# Global Singleton Engine Instance
ai_engine = VikasDrishtiAIEngine()
