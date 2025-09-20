USE cement_dispatch_v2;

SHOW TABLES;
SELECT 
    tl.event_id, 
    tl.truck_id, 
    tm.truck_number, 
    tm.truck_type, 
    twl.weight_log_id, 
    twl.cement_loaded_kg, 
    tl.assignment_timestamp, 
    tl.detection_timestamp, 
    twl.loading_start_time, 
    twl.loading_end_time
FROM truck_loading_events tl
JOIN truck_master tm ON tl.truck_id = tm.truck_id
JOIN truck_weight_logs twl ON tl.truck_id = twl.truck_id
LIMIT 1000;

#Mean
SELECT AVG(cement_loaded_kg) AS mean_cement_loaded
FROM cleaned_truck_data;

#Median
WITH ordered_data AS (
    SELECT
        cement_loaded_kg,
        ROW_NUMBER() OVER (ORDER BY cement_loaded_kg) AS rn,
        COUNT(*) OVER () AS total_count
    FROM cleaned_truck_data
)
SELECT AVG(cement_loaded_kg) AS median_cement_loaded
FROM ordered_data
WHERE rn IN (
    FLOOR((total_count + 1) / 2),
    CEIL((total_count + 1) / 2)
);

#Mode
SELECT cement_loaded_kg AS mode_cement_loaded
FROM cleaned_truck_data
GROUP BY cement_loaded_kg
ORDER BY COUNT(*) DESC
LIMIT 1;

#Variance, Std Dev, and Range
SELECT
    VAR_SAMP(cement_loaded_kg) AS variance_cement_loaded,
    STDDEV_SAMP(cement_loaded_kg) AS stddev_cement_loaded,
    MAX(cement_loaded_kg) - MIN(cement_loaded_kg) AS range_cement_loaded
FROM cleaned_truck_data;

# Calculate Skewness 
WITH stats AS (
    SELECT
        COUNT(*) AS n,
        AVG(cement_loaded_kg) AS mean,
        STDDEV_SAMP(cement_loaded_kg) AS stddev
    FROM cleaned_truck_data
),
cubed_sum AS (
    SELECT SUM(POWER((cement_loaded_kg - stats.mean) / stats.stddev, 3)) AS sum_cubed_dev
    FROM cleaned_truck_data, stats
)
SELECT
    (stats.n * cubed_sum.sum_cubed_dev) / ((stats.n - 1) * (stats.n - 2)) AS skewness
FROM stats, cubed_sum;


#Kurtosis
WITH stats AS (
    SELECT
        COUNT(*) AS n,
        AVG(cement_loaded_kg) AS mean,
        STDDEV_SAMP(cement_loaded_kg) AS stddev
    FROM cleaned_truck_data
),
quad_sum AS (
    SELECT SUM(POWER((cement_loaded_kg - stats.mean) / stats.stddev, 4)) AS sum_quad_dev
    FROM cleaned_truck_data, stats
)
SELECT
    (
        (stats.n * (stats.n + 1) * quad_sum.sum_quad_dev)
        / ((stats.n - 1) * (stats.n - 2) * (stats.n - 3))
    ) - (
        (3 * POWER(stats.n - 1, 2))
        / ((stats.n - 2) * (stats.n - 3))
    ) AS kurtosis
FROM stats, quad_sum;

