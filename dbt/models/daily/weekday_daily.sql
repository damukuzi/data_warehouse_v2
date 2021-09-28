SELECT *
FROM
    {{ ref('station_summary') }}
GROUP BY ID