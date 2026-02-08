-- ==========================================================
-- Alimentation de la dimension MACHINE (DW)
-- Source : schéma OPS (factory, workshop, production_line)
-- ==========================================================

INSERT INTO dw.dim_machine (
    machine_key,
    factory_id,
    factory_name,
    workshop_id,
    workshop_name,
    line_id,
    line_name
)
SELECT DISTINCT
    -- clé surrogée analytique stable
    f.factory_id || '_' || w.workshop_id || '_' || l.line_id AS machine_key,

    f.factory_id,
    f.factory_name,
    w.workshop_id,
    w.workshop_name,
    l.line_id,
    l.line_name

FROM ops.production_line l
JOIN ops.workshop w
  ON l.workshop_id = w.workshop_id
JOIN ops.factory f
  ON w.factory_id = f.factory_id

WHERE NOT EXISTS (
    SELECT 1
    FROM dw.dim_machine m
    WHERE m.machine_key =
          f.factory_id || '_' || w.workshop_id || '_' || l.line_id
);
