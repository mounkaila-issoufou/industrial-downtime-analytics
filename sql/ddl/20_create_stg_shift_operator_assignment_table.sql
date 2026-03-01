-- ==========================================================
-- STAGING : shift_operator_assignment
-- Données brutes issues du CSV (aucune transformation métier)
-- ==========================================================

CREATE TABLE IF NOT EXISTS stg.shift_operator_assignment (
    shift_operator_assignment_id VARCHAR(50) PRIMARY KEY,
    shift_supervision_id VARCHAR(50) NOT NULL,
    operator_id VARCHAR(20) NOT NULL,
    line_id VARCHAR(20) NOT NULL,
    date DATE NOT NULL,
    session VARCHAR(10) NOT NULL
);

COMMENT ON TABLE stg.shift_operator_assignment IS
'Données brutes d’affectation des opérateurs aux shifts issues du fichier CSV.';

COMMENT ON COLUMN stg.shift_operator_assignment.shift_supervision_id IS
'Clé métier faisant référence au shift (sera liée dans le schéma ops).';

COMMENT ON COLUMN stg.shift_operator_assignment.session IS
'Session de production : MATIN / SOIR / NUIT / SD';
