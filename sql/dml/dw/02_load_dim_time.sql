--=============================================================================
-- Script : 15_load_dim_time.sql    
-- Description : Alimentation de la dimension temps (DW)
-- Correction :
--   - Gestion des shifts traversant minuit (NUIT)
--   - Normalisation heure (0–23) avec % 24
--   - Ajustement de la date si dépassement >= 24h
--=============================================================================

INSERT INTO dw.dim_time (
    time_key,
    date,
    year,
    month,
    month_name,
    iso_week,
    day_of_week,
    day_name,
    hour_of_day,
    session,
    is_weekend
)
SELECT DISTINCT

    -- ==========================
    -- ✅ TIME KEY CORRECT
    -- ==========================
    (
        TO_CHAR(
            CASE 
                WHEN base_hour + h.hour_index >= 24
                    THEN h.date + INTERVAL '1 day'
                ELSE h.date
            END,
            'YYYYMMDD'
        )::INT * 100
        +
        ((base_hour + h.hour_index) % 24)
    ) AS time_key,

    -- ==========================
    -- ✅ DATE CORRIGÉE
    -- ==========================
    CASE 
        WHEN base_hour + h.hour_index >= 24
            THEN h.date + INTERVAL '1 day'
        ELSE h.date
    END AS date,

    EXTRACT(YEAR FROM 
        CASE 
            WHEN base_hour + h.hour_index >= 24
                THEN h.date + INTERVAL '1 day'
            ELSE h.date
        END
    )::INT,

    EXTRACT(MONTH FROM 
        CASE 
            WHEN base_hour + h.hour_index >= 24
                THEN h.date + INTERVAL '1 day'
            ELSE h.date
        END
    )::INT,

    TO_CHAR(
        CASE 
            WHEN base_hour + h.hour_index >= 24
                THEN h.date + INTERVAL '1 day'
            ELSE h.date
        END,
        'FMMonth'
    ),

    EXTRACT(WEEK FROM 
        CASE 
            WHEN base_hour + h.hour_index >= 24
                THEN h.date + INTERVAL '1 day'
            ELSE h.date
        END
    )::INT,

    EXTRACT(ISODOW FROM 
        CASE 
            WHEN base_hour + h.hour_index >= 24
                THEN h.date + INTERVAL '1 day'
            ELSE h.date
        END
    )::INT,

    TO_CHAR(
        CASE 
            WHEN base_hour + h.hour_index >= 24
                THEN h.date + INTERVAL '1 day'
            ELSE h.date
        END,
        'FMDay'
    ),

    -- ==========================
    -- ✅ HEURE NORMALISÉE
    -- ==========================
    ((base_hour + h.hour_index) % 24) AS hour_of_day,

    h.session,

    (
        EXTRACT(DOW FROM 
            CASE 
                WHEN base_hour + h.hour_index >= 24
                    THEN h.date + INTERVAL '1 day'
                ELSE h.date
            END
        ) IN (0,6)
    )

FROM (
    SELECT
        h.*,

        -- ==========================
        -- ✅ BASE HOUR CENTRALISÉ
        -- ==========================
        CASE 
            WHEN h.session = 'MATIN' THEN 5
            WHEN h.session = 'SOIR'  THEN 13
            WHEN h.session = 'NUIT'  THEN 21
            WHEN h.session = 'SD'    THEN 6
        END AS base_hour

    FROM ops.hourly_production h
) h

ON CONFLICT (time_key) DO NOTHING;