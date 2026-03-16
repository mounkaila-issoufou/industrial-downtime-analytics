-- ==========================================================
-- DATA WAREHOUSE INDEXES
-- Optimisation pour Power BI et requêtes analytiques
-- ==========================================================



-- ==========================================================
-- DIM_TIME
-- ==========================================================

CREATE INDEX IF NOT EXISTS idx_dim_time_date
ON dw.dim_time(date);

CREATE INDEX IF NOT EXISTS idx_dim_time_year_month
ON dw.dim_time(year, month);



-- ==========================================================
-- DIM_MACHINE
-- ==========================================================

CREATE INDEX IF NOT EXISTS idx_dim_machine_line
ON dw.dim_machine(line_id);

CREATE INDEX IF NOT EXISTS idx_dim_machine_factory
ON dw.dim_machine(factory_id);

CREATE INDEX IF NOT EXISTS idx_dim_machine_workshop
ON dw.dim_machine(workshop_id);



-- ==========================================================
-- DIM_TEAM
-- ==========================================================

CREATE INDEX IF NOT EXISTS idx_dim_team_session
ON dw.dim_team(session);

CREATE INDEX IF NOT EXISTS idx_dim_team_scope_line
ON dw.dim_team(scope_line_id);



-- ==========================================================
-- DIM_ORGANE_ELEMENT
-- ==========================================================

CREATE INDEX IF NOT EXISTS idx_dim_organe
ON dw.dim_organe_element(organe);

CREATE INDEX IF NOT EXISTS idx_dim_element
ON dw.dim_organe_element(element);

CREATE INDEX IF NOT EXISTS idx_dim_cause_category
ON dw.dim_organe_element(cause_category);



-- ==========================================================
-- FACT_HOURLY_PERFORMANCE
-- ==========================================================

-- Index pour filtrer par machine et période
CREATE INDEX IF NOT EXISTS idx_fact_hourly_machine_time
ON dw.fact_hourly_performance(machine_key, time_key);

-- Index pour analyse par équipe
CREATE INDEX IF NOT EXISTS idx_fact_hourly_team_time
ON dw.fact_hourly_performance(team_key, time_key);

-- Index pour analyses temporelles
CREATE INDEX IF NOT EXISTS idx_fact_hourly_time
ON dw.fact_hourly_performance(time_key);



-- ==========================================================
-- FACT_PRODUCTION_EVENTS
-- ==========================================================

-- Analyse des arrêts par machine
CREATE INDEX IF NOT EXISTS idx_events_machine_time
ON dw.fact_production_events(machine_key, time_key);

-- Analyse par équipe
CREATE INDEX IF NOT EXISTS idx_events_team
ON dw.fact_production_events(team_key);

-- Analyse par cause
CREATE INDEX IF NOT EXISTS idx_events_cause
ON dw.fact_production_events(organe_element_key);



-- ==========================================================
-- BRIN INDEX (optimisation très efficace pour tables temporelles)
-- ==========================================================

-- BRIN = Block Range Index
-- Très léger et très rapide pour grandes tables ordonnées par date

CREATE INDEX IF NOT EXISTS brin_fact_hourly_time
ON dw.fact_hourly_performance
USING BRIN(time_key);

CREATE INDEX IF NOT EXISTS brin_events_time
ON dw.fact_production_events
USING BRIN(time_key);
