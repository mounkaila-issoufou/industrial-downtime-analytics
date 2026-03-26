CREATE TABLE IF NOT EXISTS ops.production_events (

    -- ======================
    -- IDENTIFIANTS
    -- ======================
    event_id TEXT PRIMARY KEY,
    hourly_prod_id TEXT NOT NULL,

    -- ======================
    -- DESCRIPTION EVENT
    -- ======================
    event_type TEXT NOT NULL,

    cause_category TEXT NOT NULL,
    cause_family TEXT NOT NULL,

    organ TEXT,
    element TEXT,

    -- ======================
    -- TEMPOREL
    -- ======================
    start_minute INTEGER,
    end_minute INTEGER,
    duration_minutes INTEGER NOT NULL CHECK (duration_minutes >= 0),

    -- ======================
    -- KPI
    -- ======================
    severity TEXT CHECK (severity IN ('minor', 'medium', 'critical')),
    severity_score INTEGER CHECK (severity_score BETWEEN 1 AND 3),
    business_impact TEXT CHECK (business_impact IN ('low', 'medium', 'high')),

    -- ======================
    -- OPERATIONNEL
    -- ======================
    operator_action TEXT,
    escalation TEXT,

    -- ======================
    -- ANALYTICS / ML
    -- ======================
    is_recurrent BOOLEAN,
    repetition_count INTEGER CHECK (repetition_count >= 0),

    -- ======================
    -- META
    -- ======================
    source TEXT,
    comment TEXT,

    -- ======================
    -- FK
    -- ======================
    FOREIGN KEY (hourly_prod_id)
        REFERENCES ops.hourly_production(hourly_prod_id)
);