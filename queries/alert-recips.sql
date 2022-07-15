SELECT 
	building.title AS building_name,
	sensor.title AS sensor_name,
	alert.condition AS alert_condition,
	alert.test_value AS test_value,
	recipient.name AS person_alerted,
	recipient.email_address AS alerted_email
FROM 
	bmsapp_sensor AS sensor,  
	bmsapp_building AS building,
	bmsapp_alertcondition AS alert,
	bmsapp_alertrecipient AS recipient,
	bmsapp_alertcondition_recipients AS alert_recipients,
	bmsapp_bldgtosensor AS bldg_to_sensor
WHERE
	building.id = bldg_to_sensor.building_id AND
	sensor.id = bldg_to_sensor.sensor_id AND
	alert.id = alert_recipients.alertcondition_id AND
	recipient.id = alert_recipients.alertrecipient_id AND 
	sensor.id = alert.sensor_id AND
	alert.active = 1
ORDER BY
	building_name, bldg_to_sensor.sort_order, person_alerted
;
