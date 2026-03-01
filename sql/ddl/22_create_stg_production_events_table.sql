-- ==========================================================
-- STAGING : production_events
-- Données brutes issues du CSV (aucune transformation métier)
-- ==========================================================

CREATE TABLE IF NOT EXISTS stg.production_events (
    event_id VARCHAR(50) PRIMARY KEY,
    hourly_prod_id VARCHAR(50) NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    event_category VARCHAR(20) NOT NULL,
    organ VARCHAR(50),
    element VARCHAR(50),
    operator_action VARCHAR(100),
    duration_minutes INTEGER NOT NULL,
    comment TEXT
);

COMMENT ON TABLE stg.production_events IS
'Données brutes des événements de production (arrêts, pauses, incidents).';

COMMENT ON COLUMN stg.production_events.hourly_prod_id IS
'Clé métier faisant référence à une heure de production (sera reliée en ops).';

COMMENT ON COLUMN stg.production_events.event_category IS
'Typologie de l’événement : planned ou technical.';

COMMENT ON COLUMN stg.production_events.duration_minutes IS
'Durée de l’événement en minutes.';
