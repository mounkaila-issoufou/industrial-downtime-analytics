-- ==========================================================
-- PARTITION SETUP (CORRIGÉ PRO)
-- Compatible format time_key = YYYYMMDDHH
-- ==========================================================

-- ==========================================================
-- FACT_HOURLY_PERFORMANCE
-- ==========================================================

CREATE TABLE IF NOT EXISTS dw.fact_hourly_performance_2026_01
PARTITION OF dw.fact_hourly_performance
FOR VALUES FROM (2026010100) TO (2026020100);

CREATE TABLE IF NOT EXISTS dw.fact_hourly_performance_2026_02
PARTITION OF dw.fact_hourly_performance
FOR VALUES FROM (2026020100) TO (2026030100);

CREATE TABLE IF NOT EXISTS dw.fact_hourly_performance_2026_03
PARTITION OF dw.fact_hourly_performance
FOR VALUES FROM (2026030100) TO (2026040100);



-- ==========================================================
-- FACT_PRODUCTION_EVENTS
-- ==========================================================

CREATE TABLE IF NOT EXISTS dw.fact_production_events_2026_01
PARTITION OF dw.fact_production_events
FOR VALUES FROM (2026010100) TO (2026020100);

CREATE TABLE IF NOT EXISTS dw.fact_production_events_2026_02
PARTITION OF dw.fact_production_events
FOR VALUES FROM (2026020100) TO (2026030100);

CREATE TABLE IF NOT EXISTS dw.fact_production_events_2026_03
PARTITION OF dw.fact_production_events
FOR VALUES FROM (2026030100) TO (2026040100);



-- ==========================================================
-- FACT_QUALITY_EVENTS (NOUVEAU)
-- ==========================================================

CREATE TABLE IF NOT EXISTS dw.fact_quality_events_2026_01
PARTITION OF dw.fact_quality_events
FOR VALUES FROM (2026010100) TO (2026020100);

CREATE TABLE IF NOT EXISTS dw.fact_quality_events_2026_02
PARTITION OF dw.fact_quality_events
FOR VALUES FROM (2026020100) TO (2026030100);

CREATE TABLE IF NOT EXISTS dw.fact_quality_events_2026_03
PARTITION OF dw.fact_quality_events
FOR VALUES FROM (2026030100) TO (2026040100);



-- ==========================================================
-- FACT_OEE_HOURLY (CRITIQUE 🔥)
-- ==========================================================

CREATE TABLE IF NOT EXISTS dw.fact_oee_hourly_2026_01
PARTITION OF dw.fact_oee_hourly
FOR VALUES FROM (2026010100) TO (2026020100);

CREATE TABLE IF NOT EXISTS dw.fact_oee_hourly_2026_02
PARTITION OF dw.fact_oee_hourly
FOR VALUES FROM (2026020100) TO (2026030100);

CREATE TABLE IF NOT EXISTS dw.fact_oee_hourly_2026_03
PARTITION OF dw.fact_oee_hourly
FOR VALUES FROM (2026030100) TO (2026040100);
