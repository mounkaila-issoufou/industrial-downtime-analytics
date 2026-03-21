-- ==========================================================
-- RESET OPS LAYER
-- ==========================================================

TRUNCATE TABLE ops.shift_operator_assignment CASCADE;
TRUNCATE TABLE ops.shift_supervision CASCADE;
TRUNCATE TABLE ops.hourly_production CASCADE;
TRUNCATE TABLE ops.production_events CASCADE;
TRUNCATE TABLE ops.production_line CASCADE;
TRUNCATE TABLE ops.operator CASCADE;
TRUNCATE TABLE ops.team_lead CASCADE;
TRUNCATE TABLE ops.workshop CASCADE;
TRUNCATE TABLE ops.factory CASCADE;
TRUNCATE TABLE ops.quality_inspection CASCADE;
TRUNCATE TABLE ops.quality_event CASCADE;