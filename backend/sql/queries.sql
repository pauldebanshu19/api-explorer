-- Common SQL Queries

-- Insert API Spec
INSERT INTO api_specs (name, spec_text)
VALUES ($1, $2)
RETURNING id;

-- Insert Safety Verdict
INSERT INTO safety_verdicts (api_spec_id, user_intent, verdict_json, ui_contract_json, risk_score)
VALUES ($1, $2, $3, $4, $5)
RETURNING id;

-- Get Active Policies
SELECT * FROM policies WHERE active = true;

-- Get Recent Verdicts
SELECT * FROM safety_verdicts ORDER BY created_at DESC LIMIT 100;

-- Get Verdict by API Spec ID
SELECT * FROM safety_verdicts WHERE api_spec_id = $1;
