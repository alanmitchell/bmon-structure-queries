ATTACH "sensor_stats.sqlite" AS stats;
SELECT
	stats.alert_events.ts,
	building.title as building_name,
	sensor.title as sensor_name,
	stats.alert_events.sensor_id,
	stats.alert_events.message
FROM
	stats.alert_events,
	bmsapp_sensor AS sensor, 
	bmsapp_building AS building,
	bmsapp_bldgtosensor AS bldg_to_sensor
WHERE
	stats.alert_events.sensor_id = sensor.sensor_id AND
	building.id = bldg_to_sensor.building_id AND
	sensor.id = bldg_to_sensor.sensor_id
ORDER BY
	stats.alert_events.ts
;
DETACH DATABASE stats;