SELECT *
FROM
    {{ source('instacart_raw_data', 'station_summary') }}
GROUP BY ID