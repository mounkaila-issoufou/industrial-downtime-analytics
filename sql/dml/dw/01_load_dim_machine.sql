-- ==========================================================
-- Alimentation de la dimension MACHINE (DW)
-- Source : schéma OPS (factory, workshop, production_line)
-- ==========================================================

INSERT INTO dw.dim_machine (
    line_id,
    workshop_id,
    factory_id,
    machine_name,
    workshop_name,
    factory_name,
    theoretical_capacity_per_hour,
    reliability_target,
    line_status
)
SELECT
    l.line_id,
    w.workshop_id,
    f.factory_id,
    l.machine_name,
    w.workshop_name,
    f.factory_name,
    l.theoretical_capacity_per_hour,
    l.reliability_target,
    l.line_status

FROM ops.production_line l
JOIN ops.workshop w
  ON l.workshop_id = w.workshop_id
JOIN ops.factory f
  ON w.factory_id = f.factory_id

WHERE NOT EXISTS (
    SELECT 1
    FROM dw.dim_machine m
    WHERE m.line_id = l.line_id
);
