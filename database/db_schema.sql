-- ===================================
-- MNEE Sentinel Database Schema (Enhanced)
-- UUID-based, Indonesian Vendor Data
-- Run this in your Supabase SQL Editor
-- ===================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Table 1: Budget Limits per Category
CREATE TABLE IF NOT EXISTS budgets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    category VARCHAR(100) NOT NULL UNIQUE,
    monthly_limit_mnee DECIMAL(18, 6) NOT NULL,
    current_spent DECIMAL(18, 6) DEFAULT 0,
    last_reset_date TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Table 2: Whitelisted Vendors
CREATE TABLE IF NOT EXISTS whitelisted_vendors (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    vendor_name VARCHAR(255) NOT NULL,
    wallet_address VARCHAR(42) NOT NULL UNIQUE,
    category VARCHAR(100) NOT NULL,
    max_transaction_limit DECIMAL(18, 6) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (category) REFERENCES budgets(category) ON DELETE RESTRICT
);

-- Table 3: Audit Logs (Immutable Trail)
CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    proposal_text TEXT NOT NULL,
    vendor_name VARCHAR(255),
    vendor_address VARCHAR(42),
    amount DECIMAL(18, 6) NOT NULL,
    category VARCHAR(100),
    decision VARCHAR(20) NOT NULL CHECK (decision IN ('APPROVED', 'REJECTED')),
    reasoning TEXT NOT NULL,
    ai_confidence DECIMAL(5, 2),
    ai_provider VARCHAR(50),
    transaction_hash VARCHAR(66),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Table 4: Transaction Velocity Tracking (Anti-Fraud)
CREATE TABLE IF NOT EXISTS transaction_velocity (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    vendor_address VARCHAR(42) NOT NULL,
    transaction_count INTEGER DEFAULT 0,
    total_amount DECIMAL(18, 6) DEFAULT 0,
    window_start TIMESTAMP DEFAULT NOW(),
    last_updated TIMESTAMP DEFAULT NOW()
);

-- ===================================
-- Seed Data: Budgets (Indonesian Context)
-- ===================================

INSERT INTO budgets (category, monthly_limit_mnee) VALUES
    ('FX', 250),
    ('Remittance', 120),
    ('Settlement', 180),
    ('Software', 90),
    ('Consulting', 150),
    ('Travel', 75),
    ('Office', 40),
    ('Data', 60),
    ('Cybersecurity', 110),
    ('Legal', 80)
ON CONFLICT (category) DO NOTHING;

-- ===================================
-- Seed Data: Indonesian Vendors
-- ===================================

INSERT INTO whitelisted_vendors (vendor_name, wallet_address, category, max_transaction_limit) VALUES
    ('PT Nusantara FX Services', '0xA1b2C3D4e5F60718293aBcD4E5F6071829Ab', 'FX', 100),
    ('PT Global Money Transfer', '0xB2c3D4E5F60718293aBcD4E5F6071829Abc', 'Remittance', 50),
    ('PT Bank Settlement Partner', '0xC3d4E5F60718293aBcD4E5F6071829AbcD', 'Settlement', 80),
    ('PT Cloud Treasury Tools', '0xD4e5F60718293aBcD4E5F6071829AbcD4', 'Software', 40),
    ('PT Audit & Compliance Advisory', '0xE5f60718293aBcD4E5F6071829AbcD4E', 'Consulting', 60),
    ('PT Corporate Travel Provider', '0xF60718293aBcD4E5F6071829AbcD4E5F', 'Travel', 30),
    ('PT Office Supplies Jakarta', '0x0718293aBcD4E5F6071829AbcD4E5F607', 'Office', 20),
    ('PT Data & Market Feeds', '0x18293aBcD4E5F6071829AbcD4E5F60718', 'Data', 25),
    ('PT Cybersecurity Services', '0x293aBcD4E5F6071829AbcD4E5F607182', 'Cybersecurity', 50),
    ('PT Legal Retainer Partner', '0x3aBcD4E5F6071829AbcD4E5F60718293', 'Legal', 35)
ON CONFLICT (wallet_address) DO NOTHING;

-- ===================================
-- Sample Audit Logs for Demo
-- ===================================

INSERT INTO audit_logs (proposal_text, vendor_name, vendor_address, amount, category, decision, reasoning, ai_confidence, ai_provider) VALUES
    ('Transfer 50 MNEE to PT Nusantara FX Services for monthly FX hedging', 
     'PT Nusantara FX Services', 
     '0xA1b2C3D4e5F60718293aBcD4E5F6071829Ab', 
     50.00, 
     'FX', 
     'APPROVED', 
     'All compliance checks passed: Vendor whitelisted, within budget, velocity OK', 
     0.95,
     'groq'),
    ('Pay PT Global Money Transfer 80 MNEE for remittance services', 
     'PT Global Money Transfer', 
     '0xB2c3D4E5F60718293aBcD4E5F6071829Abc', 
     80.00, 
     'Remittance', 
     'REJECTED', 
     'Amount exceeds vendor transaction limit (50 MNEE)', 
     0.92,
     'openai'),
    ('Send 25 MNEE to PT Office Supplies Jakarta for stationery', 
     'PT Office Supplies Jakarta', 
     '0x0718293aBcD4E5F6071829AbcD4E5F607', 
     25.00, 
     'Office', 
     'APPROVED', 
     'All compliance checks passed', 
     0.88,
     'groq');

-- ===================================
-- Indexes for Performance
-- ===================================

CREATE INDEX idx_vendor_address ON whitelisted_vendors(wallet_address);
CREATE INDEX idx_vendor_category ON whitelisted_vendors(category);
CREATE INDEX idx_audit_created ON audit_logs(created_at DESC);
CREATE INDEX idx_audit_decision ON audit_logs(decision);
CREATE INDEX idx_velocity_vendor ON transaction_velocity(vendor_address);

-- ===================================
-- Views for Analytics
-- ===================================

CREATE OR REPLACE VIEW v_budget_summary AS
SELECT 
    category,
    monthly_limit_mnee,
    current_spent,
    (monthly_limit_mnee - current_spent) AS remaining,
    ROUND((current_spent / NULLIF(monthly_limit_mnee, 0) * 100)::numeric, 2) AS percent_used
FROM budgets
ORDER BY percent_used DESC;

CREATE OR REPLACE VIEW v_vendor_stats AS
SELECT 
    v.vendor_name,
    v.category,
    v.max_transaction_limit,
    COUNT(a.id) AS total_transactions,
    SUM(CASE WHEN a.decision = 'APPROVED' THEN 1 ELSE 0 END) AS approved_count,
    SUM(CASE WHEN a.decision = 'REJECTED' THEN 1 ELSE 0 END) AS rejected_count,
    COALESCE(SUM(CASE WHEN a.decision = 'APPROVED' THEN a.amount ELSE 0 END), 0) AS total_approved_amount
FROM whitelisted_vendors v
LEFT JOIN audit_logs a ON v.wallet_address = a.vendor_address
GROUP BY v.vendor_name, v.category, v.max_transaction_limit
ORDER BY total_approved_amount DESC;

-- ===================================
-- Function: Reset Monthly Budgets
-- ===================================

CREATE OR REPLACE FUNCTION reset_monthly_budgets()
RETURNS void AS $$
BEGIN
    UPDATE budgets 
    SET current_spent = 0, 
        last_reset_date = NOW(),
        updated_at = NOW();
END;
$$ LANGUAGE plpgsql;

-- ===================================
-- Trigger: Update timestamp on changes
-- ===================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_budgets_updated_at BEFORE UPDATE ON budgets
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_vendors_updated_at BEFORE UPDATE ON whitelisted_vendors
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
