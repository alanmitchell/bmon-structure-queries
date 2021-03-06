SELECT 
	building.title AS building_name,
	sensor.title AS sensor_name,
	alert.condition AS alert_condition,
	alert.test_value AS test_value
FROM 
	bmsapp_sensor AS sensor,  
	bmsapp_building AS building,
	bmsapp_alertcondition AS alert,
	bmsapp_bldgtosensor AS bldg_to_sensor
WHERE
	building.id = bldg_to_sensor.building_id AND
	sensor.id = bldg_to_sensor.sensor_id AND
	sensor.id = alert.sensor_id AND
	alert.active = 1
ORDER BY
	building_name, bldg_to_sensor.sort_order
;
