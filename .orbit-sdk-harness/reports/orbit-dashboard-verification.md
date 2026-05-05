# Orbit Dashboard Verification

Status: **PASS**

## Token Checks

| Check | Status | Evidence | Observed | Expected | Notes |
|---|---|---|---|---|---|
| `dashboard_sample_evidence_present` | **PASS** | `/Users/nick/Desktop/orbit/examples/sample-evidence.json` | present | present | - |
| `dashboard_render_returncode` | **PASS** | `/Users/nick/Desktop/orbit/.orbit-sdk-harness/reports/evidence/dashboard-verified.html` | returncode=0 | returncode=0 | - |
| `dashboard_token_ORBIT` | **PASS** | `/Users/nick/Desktop/orbit/.orbit-sdk-harness/reports/evidence/dashboard-verified.html` | present | contains 'ORBIT' | - |
| `dashboard_token_Find_drift` | **PASS** | `/Users/nick/Desktop/orbit/.orbit-sdk-harness/reports/evidence/dashboard-verified.html` | present | contains 'Find drift' | - |
| `dashboard_token__C6FF00` | **PASS** | `/Users/nick/Desktop/orbit/.orbit-sdk-harness/reports/evidence/dashboard-verified.html` | present | contains '#C6FF00' | - |
| `dashboard_token__FF8A00` | **PASS** | `/Users/nick/Desktop/orbit/.orbit-sdk-harness/reports/evidence/dashboard-verified.html` | present | contains '#FF8A00' | - |
| `dashboard_token__FF4D36` | **PASS** | `/Users/nick/Desktop/orbit/.orbit-sdk-harness/reports/evidence/dashboard-verified.html` | present | contains '#FF4D36' | - |
| `dashboard_token__8B3DFF` | **PASS** | `/Users/nick/Desktop/orbit/.orbit-sdk-harness/reports/evidence/dashboard-verified.html` | present | contains '#8B3DFF' | - |
| `dashboard_token__1E6BFF` | **PASS** | `/Users/nick/Desktop/orbit/.orbit-sdk-harness/reports/evidence/dashboard-verified.html` | present | contains '#1E6BFF' | - |
| `dashboard_token_Timeline` | **PASS** | `/Users/nick/Desktop/orbit/.orbit-sdk-harness/reports/evidence/dashboard-verified.html` | present | contains 'Timeline' | - |
| `dashboard_token_Claim_Validation` | **PASS** | `/Users/nick/Desktop/orbit/.orbit-sdk-harness/reports/evidence/dashboard-verified.html` | present | contains 'Claim Validation' | - |
| `dashboard_token_Uncertainty` | **PASS** | `/Users/nick/Desktop/orbit/.orbit-sdk-harness/reports/evidence/dashboard-verified.html` | present | contains 'Uncertainty' | - |
| `dashboard_token_Scope` | **PASS** | `/Users/nick/Desktop/orbit/.orbit-sdk-harness/reports/evidence/dashboard-verified.html` | present | contains 'Scope' | - |
| `dashboard_token_Matrix` | **PASS** | `/Users/nick/Desktop/orbit/.orbit-sdk-harness/reports/evidence/dashboard-verified.html` | present | contains 'Matrix' | - |
