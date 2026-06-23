{{ config(
    materialized = "table",
    contract = {
        "enforced": true,
        "checks": [
            {"name": "not_null", "column": "registration_date"},
            {"name": "not_null", "column": "domains_registered"}
        ]
    }
) }}

SELECT
    registration_date,
    domains_registered,
    unique_owners
FROM {{ ref("int_domain_metrics") }}
ORDER BY registration_date DESC
