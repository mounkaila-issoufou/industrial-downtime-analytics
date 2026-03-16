-- ==========================================================
-- PARTITION SETUP FOR DATA WAREHOUSE FACT TABLES
-- Creates monthly partitions for a full year
-- Idempotent (safe to run multiple times)
-- ==========================================================

DO $$

DECLARE

target_year INT := 2026;
month INT;

start_key BIGINT;
end_key BIGINT;

partition_name TEXT;

BEGIN

-- ==========================================================
-- FACT_HOURLY_PERFORMANCE
-- ==========================================================

FOR month IN 1..12 LOOP

start_key :=
(target_year * 1000000)
+ (month * 10000)
+ 100;

end_key :=
CASE
WHEN month < 12
THEN (target_year * 1000000) + ((month + 1) * 10000) + 100
ELSE ((target_year + 1) * 1000000) + 10100
END;

partition_name :=
'fact_hourly_performance_' ||
target_year || '_' ||
LPAD(month::text,2,'0');

EXECUTE format(
'
CREATE TABLE IF NOT EXISTS dw.%I
PARTITION OF dw.fact_hourly_performance
FOR VALUES FROM (%s) TO (%s)
',
partition_name,
start_key,
end_key
);

END LOOP;



-- ==========================================================
-- FACT_PRODUCTION_EVENTS
-- ==========================================================

FOR month IN 1..12 LOOP

start_key :=
(target_year * 1000000)
+ (month * 10000)
+ 100;

end_key :=
CASE
WHEN month < 12
THEN (target_year * 1000000) + ((month + 1) * 10000) + 100
ELSE ((target_year + 1) * 1000000) + 10100
END;

partition_name :=
'fact_production_events_' ||
target_year || '_' ||
LPAD(month::text,2,'0');

EXECUTE format(
'
CREATE TABLE IF NOT EXISTS dw.%I
PARTITION OF dw.fact_production_events
FOR VALUES FROM (%s) TO (%s)
',
partition_name,
start_key,
end_key
);

END LOOP;

END $$;
