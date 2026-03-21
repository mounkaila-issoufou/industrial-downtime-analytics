DO $$

DECLARE

target_year INT := 2026;
month INT;

start_key BIGINT;
end_key BIGINT;

partition_name TEXT;
fact_table TEXT;

fact_tables TEXT[] := ARRAY[
    'fact_hourly_performance',
    'fact_production_events',
    'fact_quality_events',
    'fact_oee_hourly'
];

BEGIN

FOREACH fact_table IN ARRAY fact_tables LOOP

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
            fact_table || '_' ||
            target_year || '_' ||
            LPAD(month::text,2,'0');

        EXECUTE format(
            '
            CREATE TABLE IF NOT EXISTS dw.%I
            PARTITION OF dw.%I
            FOR VALUES FROM (%s) TO (%s)
            ',
            partition_name,
            fact_table,
            start_key,
            end_key
        );

    END LOOP;

END LOOP;

END $$;
