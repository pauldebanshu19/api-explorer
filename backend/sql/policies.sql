-- Row Level Security Policies

-- Enable RLS on all tables
ALTER TABLE api_specs ENABLE ROW LEVEL SECURITY;
ALTER TABLE safety_verdicts ENABLE ROW LEVEL SECURITY;
ALTER TABLE policies ENABLE ROW LEVEL SECURITY;

-- Policies for api_specs
CREATE POLICY "Enable insert public" ON api_specs FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable select public" ON api_specs FOR SELECT USING (true);

-- Policies for safety_verdicts
CREATE POLICY "Enable insert public" ON safety_verdicts FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable select public" ON safety_verdicts FOR SELECT USING (true);

-- Policies for policies table
CREATE POLICY "Enable select public" ON policies FOR SELECT USING (true);
