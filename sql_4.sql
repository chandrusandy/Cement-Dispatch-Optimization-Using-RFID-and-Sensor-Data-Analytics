USE cement_dispatch_v2;

#Remove NULLs and empty strings
DELETE FROM truck_loading_events
WHERE
    event_id IS NULL OR
    truck_id IS NULL OR
    silo_id IS NULL OR
    assignment_timestamp IS NULL OR
    detection_timestamp IS NULL OR
    truck_id = '' OR
    silo_id = '';


# Remove NULLs and empty strings
DELETE FROM truck_master
WHERE
    truck_id IS NULL OR
    truck_number IS NULL OR
    truck_type IS NULL OR
    rfid_tag IS NULL OR
    registration_date IS NULL OR
    truck_id = '' OR
    truck_number = '' OR
    truck_type = '' OR
    rfid_tag = '';


# Remove NULLs and empty strings
DELETE FROM truck_weight_logs
WHERE
    weight_log_id IS NULL OR
    truck_id IS NULL OR
    timestamp_before IS NULL OR
    weight_before_kg IS NULL OR
    timestamp_after IS NULL OR
    weight_after_kg IS NULL OR
    loading_start_time IS NULL OR
    loading_end_time IS NULL OR
    cement_loaded_kg IS NULL OR
    truck_id = '';

CREATE VIEW cleaned_truck_data AS
SELECT
    tle.event_id,
    tle.truck_id,
    tm.truck_number,
    tm.truck_type,
    tm.rfid_tag,
    twl.weight_log_id,
    twl.timestamp_before,
    twl.weight_before_kg,
    twl.timestamp_after,
    twl.weight_after_kg,
    twl.loading_start_time,
    twl.loading_end_time,
    twl.cement_loaded_kg,
    tle.assignment_timestamp,
    tle.detection_timestamp,
    tm.registration_date
FROM truck_loading_events tle
JOIN truck_master tm ON tle.truck_id = tm.truck_id
JOIN truck_weight_logs twl ON tle.truck_id = twl.truck_id;

SELECT * FROM cleaned_truck_data LIMIT 100;
select count(*) from cleaned_truck_data;
DESCRIBE cleaned_truck_data;


SELECT * FROM truck_loading_events;
select * from truck_master;
select * from truck_weight_logs;


WITH joined_data AS (
    SELECT
        tle.event_id,
        tle.truck_id,
        tm.truck_number,
        tm.truck_type,
        tm.rfid_tag,
        twl.weight_log_id,
        twl.timestamp_before,
        twl.weight_before_kg,
        twl.timestamp_after,
        twl.weight_after_kg,
        twl.loading_start_time,
        twl.loading_end_time,
        twl.cement_loaded_kg,
        tle.assignment_timestamp,
        tle.detection_timestamp,
        tm.registration_date
    FROM truck_loading_events AS tle
    JOIN truck_master AS tm ON tle.truck_id = tm.truck_id
    JOIN truck_weight_logs AS twl ON tle.truck_id = twl.truck_id
)
SELECT * FROM joined_data;

#Count rows
WITH joined_data AS (
    SELECT
        tle.event_id,
        tle.truck_id,
        tm.truck_number,
        tm.truck_type,
        tm.rfid_tag,
        twl.weight_log_id,
        twl.timestamp_before,
        twl.weight_before_kg,
        twl.timestamp_after,
        twl.weight_after_kg,
        twl.loading_start_time,
        twl.loading_end_time,
        twl.cement_loaded_kg,
        tle.assignment_timestamp,
        tle.detection_timestamp,
        tm.registration_date
    FROM truck_loading_events AS tle
    JOIN truck_master AS tm ON tle.truck_id = tm.truck_id
    JOIN truck_weight_logs AS twl ON tle.truck_id = twl.truck_id
)
SELECT COUNT(*) FROM joined_data;



SELECT			#Structure from Join
    tle.event_id,
    tle.truck_id,
    tm.truck_number,
    tm.truck_type,
    tm.rfid_tag,
    tm.registration_date,
    tle.silo_id,
    tle.assignment_timestamp,
    tle.detection_timestamp,
    twl.weight_log_id,
    twl.timestamp_before,
    twl.weight_before_kg,
    twl.timestamp_after,
    twl.weight_after_kg,
    twl.loading_start_time,
    twl.loading_end_time,
    twl.cement_loaded_kg
FROM truck_loading_events AS tle
INNER JOIN truck_master AS tm ON tle.truck_id = tm.truck_id
INNER JOIN truck_weight_logs AS twl ON tle.truck_id = twl.truck_id
LIMIT 10;


DESCRIBE truck_loading_events;
DESCRIBE truck_master;
DESCRIBE truck_weight_logs;

DESCRIBE cleaned_truck_data;












