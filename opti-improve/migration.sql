-- ============================================================
-- OPTI SYSTEM - SQL MIGRATION
-- Run this in MySQL Workbench on your opti_test database
-- ============================================================

-- Add the 4 new columns to opti_settings
ALTER TABLE opti_settings
  ADD COLUMN IF NOT EXISTS break_start VARCHAR(5) NULL COMMENT 'Break start time HH:MM (24hr)',
  ADD COLUMN IF NOT EXISTS break_end   VARCHAR(5) NULL COMMENT 'Break end time HH:MM (24hr)',
  ADD COLUMN IF NOT EXISTS pay_start   VARCHAR(5) NULL COMMENT 'Pay window start HH:MM (24hr)',
  ADD COLUMN IF NOT EXISTS pay_end     VARCHAR(5) NULL COMMENT 'Pay window end HH:MM (24hr)';

-- Make sure row id=1 exists (it should, but just in case)
INSERT IGNORE INTO opti_settings (id, salary_per_minute)
VALUES (1, 5.00);

-- Verify
SELECT * FROM opti_settings WHERE id = 1;

-- ============================================================
-- COLUMN MEANINGS:
--   pay_start  : Salary counting starts at this time (e.g. '05:00')
--   pay_end    : Salary counting stops at this time  (e.g. '21:00')
--   break_start: Break begins — salary paused        (e.g. '12:00')
--   break_end  : Break ends  — salary resumes        (e.g. '13:00')
-- All stored as 'HH:MM' strings. NULL = feature disabled.
-- ============================================================
