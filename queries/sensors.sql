SELECT 
	building.title AS building_name,
	sensor_group.title AS group_name,
	sensor.title AS sensor_name, 
	sensor_unit.label AS unit_type
FROM 
	bmsapp_sensor AS sensor, 
	bmsapp_unit AS sensor_unit, 
	bmsapp_building AS building,
	bmsapp_sensorgroup AS sensor_group,
	bmsapp_bldgtosensor AS bldg_to_sensor
WHERE
	sensor_unit.id = sensor.unit_id AND
	building.id = bldg_to_sensor.building_id AND
	sensor.id = bldg_to_sensor.sensor_id AND
	sensor_group.id = bldg_to_sensor.sensor_group_id
ORDER BY
    building_name, sensor_group.sort_order, bldg_to_sensor.sort_order
;
