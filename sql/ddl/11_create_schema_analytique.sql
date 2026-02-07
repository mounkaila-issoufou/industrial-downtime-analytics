-- ==========================================================
-- Création du schéma analytique (Data Warehouse)
-- ==========================================================
DROP TABLE IF EXISTS dw CASCADE;

CREATE SCHEMA IF NOT EXISTS dw;

COMMENT ON SCHEMA dw IS 
'Schéma analytique (Data Warehouse) destiné aux tables BI, 
aux faits agrégés et aux dimensions décisionnelles.';
