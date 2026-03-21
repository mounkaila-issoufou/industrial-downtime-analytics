INSERT INTO dw.dim_quality_defect (
    defect_category,
    defect_family,
    defect_type
)
SELECT DISTINCT
    defect_category,
    defect_family,
    defect_type
FROM ops.quality_event q
WHERE NOT EXISTS (
    SELECT 1
    FROM dw.dim_quality_defect d
    WHERE d.defect_category = q.defect_category
      AND d.defect_family = q.defect_family
      AND d.defect_type = q.defect_type
);
