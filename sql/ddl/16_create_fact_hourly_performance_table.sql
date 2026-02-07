-- ==========================================================
-- Fait analytique : performance horaire de production
-- Grain : 1 ligne = 1 heure x 1 ligne de production
-- ==========================================================
DROP TABLE IF EXISTS dw.fact_hourly_performance CASCADE;

CREATE TABLE IF NOT EXISTS dw.fact_hourly_performance (

    -- Clés étrangères vers les dimensions analytiques
    time_key            INTEGER NOT NULL,
    machine_key         INTEGER NOT NULL,
    team_key            INTEGER NOT NULL,

    -- Mesures de production (KPI core)
    theoretical_production      INTEGER NOT NULL,
    actual_production           INTEGER NOT NULL,

    -- Mesures de pertes
    non_production_minutes      INTEGER NOT NULL,
    explained_minutes           INTEGER NOT NULL,
    unexplained_minutes         INTEGER NOT NULL,

    -- KPI dérivés (facilitent la BI)
    reliability_rate            FLOAT,   -- actual / theoretical
    explained_ratio             FLOAT,   -- explained / non_prod
    unexplained_ratio           FLOAT,   -- unexplained / non_prod

    -- Métadonnées de chargement
    load_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Contraintes de clé étrangère
    CONSTRAINT fk_time
        FOREIGN KEY (time_key) REFERENCES dw.dim_time(time_key),

    CONSTRAINT fk_machine
        FOREIGN KEY (machine_key) REFERENCES dw.dim_machine(machine_key),

    CONSTRAINT fk_team
        FOREIGN KEY (team_key) REFERENCES dw.dim_team(team_key)
);

COMMENT ON TABLE dw.fact_hourly_performance IS
'Table de faits centrale pour piloter la performance horaire des lignes.';

COMMENT ON COLUMN dw.fact_hourly_performance.theoretical_production IS
'Production attendue sur l’heure (capacité théorique).';

COMMENT ON COLUMN dw.fact_hourly_performance.actual_production IS
'Production réellement réalisée sur l’heure.';

COMMENT ON COLUMN dw.fact_hourly_performance.non_production_minutes IS
'Minutes totales perdues sur l’heure.';

COMMENT ON COLUMN dw.fact_hourly_performance.explained_minutes IS
'Minutes de perte couvertes par des événements tracés.';

COMMENT ON COLUMN dw.fact_hourly_performance.unexplained_minutes IS
'Minutes de perte sans cause documentée.';

COMMENT ON COLUMN dw.fact_hourly_performance.reliability_rate IS
'Taux de fiabilité = actual / theoretical.';
