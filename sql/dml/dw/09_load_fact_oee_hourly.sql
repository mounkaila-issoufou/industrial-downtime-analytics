INSERT INTO dw.fact_oee_hourly (

    time_key,
    machine_key,
    team_key,

    availability,
    performance,
    quality,
    oee

)

SELECT

    hp.time_key,
    hp.machine_key,
    hp.team_key,

    -- 🟢 Availability
    (60 - hp.non_production_minutes) / 60.0,

    -- 🟢 Performance
    CASE 
        WHEN hp.theoretical_production > 0
        THEN hp.actual_production::float / hp.theoretical_production
        ELSE 0
    END,

    -- 🟢 Quality
    CASE
        WHEN hp.actual_production > 0
        THEN (hp.actual_production - COALESCE(q.defective_units, 0))::float
             / hp.actual_production
        ELSE 0
    END,

    -- 🏆 OEE
    (
        (60 - hp.non_production_minutes) / 60.0
        *
        CASE 
            WHEN hp.theoretical_production > 0
            THEN hp.actual_production::float / hp.theoretical_production
            ELSE 0
        END
        *
        CASE
            WHEN hp.actual_production > 0
            THEN (hp.actual_production - COALESCE(q.defective_units, 0))::float
                 / hp.actual_production
            ELSE 0
        END
    ) AS oee

FROM dw.fact_hourly_performance hp

LEFT JOIN (
    SELECT
        time_key,
        machine_key,
        SUM(defective_units) AS defective_units
    FROM dw.fact_quality_events
    GROUP BY time_key, machine_key
) q
ON hp.time_key = q.time_key
AND hp.machine_key = q.machine_key

-- 🛡️ IDEMPOTENCE
WHERE NOT EXISTS (
    SELECT 1
    FROM dw.fact_oee_hourly o
    WHERE o.time_key = hp.time_key
      AND o.machine_key = hp.machine_key
      AND o.team_key = hp.team_key
);
