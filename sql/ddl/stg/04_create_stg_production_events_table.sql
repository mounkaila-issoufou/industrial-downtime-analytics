-- ==========================================================
-- STAGING : production_events
-- Données brutes issues du simulateur (Markov / CSV / API)
-- ==========================================================

CREATE TABLE IF NOT EXISTS stg.production_events (

    -- ======================
    -- IDENTIFIANTS
    -- ======================
    event_id VARCHAR(50) PRIMARY KEY,
    hourly_prod_id VARCHAR(50) NOT NULL,

    -- ======================
    -- DESCRIPTION EVENT
    -- ======================
    event_type VARCHAR(100) NOT NULL,

    cause_category VARCHAR(20) NOT NULL,
    cause_family VARCHAR(30) NOT NULL,

    organ VARCHAR(50),
    element VARCHAR(50),

    -- ======================
    -- TEMPOREL (🔥 important)
    -- ======================
    start_minute INTEGER,
    end_minute INTEGER,

    duration_minutes INTEGER NOT NULL CHECK (duration_minutes >= 0),

    -- ======================
    -- KPI / ANALYTICS
    -- ======================
    severity VARCHAR(10) CHECK (severity IN ('minor', 'medium', 'critical')),
    severity_score INTEGER CHECK (severity_score BETWEEN 1 AND 3),
    business_impact VARCHAR(10) CHECK (business_impact IN ('low', 'medium', 'high')),

    -- ======================
    -- OPÉRATIONNEL
    -- ======================
    operator_action VARCHAR(100),
    escalation VARCHAR(20),

    -- ======================
    -- SMART / ML FEATURES
    -- ======================
    is_recurrent BOOLEAN,
    repetition_count INTEGER CHECK (repetition_count >= 0),

    -- ======================
    -- META
    -- ======================
    source VARCHAR(50),
    comment TEXT
);


-- ==========================================================
-- COMMENTAIRES
-- ==========================================================

COMMENT ON TABLE stg.production_events IS
'Données brutes des événements de production générés (simulation ou réel).';

COMMENT ON COLUMN stg.production_events.hourly_prod_id IS
'Référence à une heure de production (grain = 1 heure).';

COMMENT ON COLUMN stg.production_events.event_type IS
'Type précis d’événement (ex: stacker_jam, sensor_fault).';

COMMENT ON COLUMN stg.production_events.cause_category IS
'Catégorie macro : technical, process, quality, etc.';

COMMENT ON COLUMN stg.production_events.cause_family IS
'Famille technique utilisée pour analyse root cause et Markov.';

COMMENT ON COLUMN stg.production_events.start_minute IS
'Minute de début dans l’heure (0-60).';

COMMENT ON COLUMN stg.production_events.end_minute IS
'Minute de fin dans l’heure (0-60).';

COMMENT ON COLUMN stg.production_events.duration_minutes IS
'Durée réelle de l’événement en minutes.';

COMMENT ON COLUMN stg.production_events.severity IS
'Niveau de sévérité basé sur la durée.';

COMMENT ON COLUMN stg.production_events.business_impact IS
'Impact métier estimé (OEE).';

COMMENT ON COLUMN stg.production_events.is_recurrent IS
'Indique si l’événement est répétitif (pattern détecté).';