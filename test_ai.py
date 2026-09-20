import ai_engine
import data_store

p = data_store.PROJECTS[0]
res = ai_engine.ai_engine.evaluate_project_risk(p)
print(f"Risk Score: {res['risk_score']}")
print(f"Risk Tier: {res['risk_tier']}")
print(f"Signals: {res['signals_breakdown']}")
print("AI Engine Test Successful!")
