-- ==========================================================
-- Alimentation DW.fact_hourly_performance
-- Grain : 1 ligne = 1 heure
-- ==========================================================

CREATE TABLE IF NOT EXISTS  dw.fact_hourly_performance (

    -- =========================
    -- Clés dimensionnelles
    -- =========================

    time_key        INTEGER NOT NULL,
    machine_key     INTEGER NOT NULL,
    team_key        INTEGER NOT NULL,

    -- =========================
    -- KPI Core Production
    -- =========================

    theoretical_production      INTEGER NOT NULL,
    actual_production           INTEGER NOT NULL,

    -- =========================
    -- Pertes
    -- =========================

    non_production_minutes      INTEGER NOT NULL,
    explained_minutes           INTEGER NOT NULL,
    unexplained_minutes         INTEGER NOT NULL,

    -- =========================
    -- KPI Dérivés
    -- =========================

    reliability_rate    FLOAT,
    explained_ratio     FLOAT,
    unexplained_ratio   FLOAT,

    -- =========================
    -- Métadonnées
    -- =========================

    load_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- =========================
    -- Contraintes
    -- =========================

    CONSTRAINT fk_fact_time
        FOREIGN KEY (time_key)
        REFERENCES dw.dim_time(time_key),

    CONSTRAINT fk_fact_machine
        FOREIGN KEY (machine_key)
        REFERENCES dw.dim_machine(machine_key),

    CONSTRAINT fk_fact_team
        FOREIGN KEY (team_key)
        REFERENCES dw.dim_team(team_key),

    -- Empêche doublons au grain défini
    CONSTRAINT uq_fact_hour UNIQUE (
        time_key,
        machine_key,
        team_key
    )
)

PARTITION BY RANGE (time_key);

COMMENT ON TABLE dw.fact_hourly_performance IS
'Table de faits centrale pour piloter la performance horaire des lignes de production.';

COMMENT ON COLUMN dw.fact_hourly_performance.theoretical_production IS
'Production attendue sur l’heure (capacité théorique).';

COMMENT ON COLUMN dw.fact_hourly_performance.actual_production IS
'Production réellement réalisée sur l’heure.';

COMMENT ON COLUMN dw.fact_hourly_performance.non_production_minutes IS
'Minutes totales perdues sur l’heure.';

COMMENT ON COLUMN dw.fact_hourly_performance.explained_minutes IS
'Minutes de perte couvertes par des événements documentés.';

COMMENT ON COLUMN dw.fact_hourly_performance.unexplained_minutes IS
'Minutes de perte sans cause documentée.';

COMMENT ON COLUMN dw.fact_hourly_performance.reliability_rate IS
'Taux de fiabilité = actual_production / theoretical_production.';

