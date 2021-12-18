ATTACH "sensor_stats.sqlite" AS stats;
SELECT 
	building.title AS building_name,
	sensor_group.title AS group_name,
	sensor.title AS sensor_name, 
	sensor_unit.label AS unit_type,
	stats.last_report as last_report_minutes,
	stats.reading_count as reading_count
FROM 
	bmsapp_sensor AS sensor, 
	bmsapp_unit AS sensor_unit, 
	bmsapp_building AS building,
	bmsapp_sensorgroup AS sensor_group,
	bmsapp_bldgtosensor AS bldg_to_sensor,
	stats.sensor_info as stats
WHERE
	sensor_unit.id = sensor.unit_id AND
	building.id = bldg_to_sensor.building_id AND
	sensor.id = bldg_to_sensor.sensor_id AND
	sensor_group.id = bldg_to_sensor.sensor_group_id AND
	sensor.sensor_id = stats.sensor_id
ORDER BY
    building_name, sensor_group.sort_order, bldg_to_sensor.sort_order
;
DETACH DATABASE stats;