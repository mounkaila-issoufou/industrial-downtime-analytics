-- ==========================================================
-- Dimension Organe / Élément
-- ==========================================================

CREATE TABLE IF NOT EXISTS dw.dim_organe_element (
    
    organe_element_key SERIAL PRIMARY KEY,  

    organe TEXT NOT NULL,
    element TEXT NOT NULL,

    valid_from TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    valid_to TIMESTAMP,
    is_current BOOLEAN DEFAULT TRUE,

    -- 🔥 CRUCIAL POUR ON CONFLICT
    CONSTRAINT uq_organe_element UNIQUE (organe, element)
);