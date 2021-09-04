## Running the simulation

run ``` docker-compose up ``` in root directory

## API usage
```127.0.0.1:5000/api/devices/<deviceID>/count```

```127.0.0.1:5000/api/devices/<deviceID>/maxTemp```

```127.0.0.1:5000/api/devices/<deviceID>/maxTempPerDay```

## SQL queries
1. The maximum temperatures measured for every device.
```sql 
SELECT 
	deviceId, 
	MAX(temperature) as max_temperature
FROM iot_db.Device
GROUP BY deviceId; 
```
2. The amount of data points aggregated for every device.
```sql
SELECT 
	deviceId, 
    Count(*) as data_points
FROM iot_db.Device
GROUP BY deviceId;
```
3. The highest temperature measured on a given day for every device.
```sql
SELECT
	deviceId, 
    DATE(from_unixtime(time)) as day_created,
	MAX(temperature) as max_temperature
FROM iot_db.Device
GROUP BY deviceId, day_created
```

## Screenshots
![enter image description here](https://i.ibb.co/WyWkms3/containers.png)
![enter image description here](https://i.ibb.co/q9RQqHm/container-emulator.png)
![enter image description here](https://i.ibb.co/9V70PBh/container-mysql.png)
![enter image description here](https://i.ibb.co/QmwKBds/container-publisher.png)
![enter image description here](https://i.ibb.co/BPvxGJp/container-api.png)
![enter image description here](https://i.ibb.co/hcNjxJ6/container-subscriber.png)
![enter image description here](https://i.ibb.co/4WD8Kdf/api-max-temp.png)
![enter image description here](https://i.ibb.co/tHvr3qY/api-count.png)
![enter image description here](https://i.ibb.co/FD6kPMM/api-max-temp-per-day.png)
![enter image description here](https://i.ibb.co/Qddpg7V/workbench-max-temp-per-devicer-by-day.png)
![enter image description here](https://i.ibb.co/2ZSj4yD/workbench-data-points-per-device.png)
![enter image description here](https://i.ibb.co/VWCbWfW/workbench-max-temp-per-device.png)