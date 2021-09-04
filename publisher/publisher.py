from google.cloud import pubsub_v1
import asyncio
import json
from faker import Faker

faker = Faker()

class Data:
    def __init__(self, deviceId, temperature, location, time):
        self.deviceId = deviceId
        self.temperature = temperature
        self.Location = location
        self.time = time

class Location:
    def __init__(self, lat, long):
        self.lat = lat
        self.long = long

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path('iot-simulator', 'iot-topic')
publisher.create_topic(request={"name": topic_path})

async def publish_data_point(deviceId, location):
    while True:
        data = json.dumps(
            Data(
                deviceId=deviceId,
                temperature=str(faker.random_int(21,29)),
                location=location.__dict__,
                time=str(faker.unix_time(
                    start_datetime='-30d', end_datetime='now')
                )
            ).__dict__
        ).encode('utf-8')

        future = publisher.publish(topic_path, data)
        print(f"Published {data} to {topic_path}: {future.result()}")
        await asyncio.sleep(1.0)

loop = asyncio.get_event_loop()
asyncio.ensure_future(
    publish_data_point(
        deviceId=str(faker.uuid4()),
        location=Location('3.1552843960706554', '101.59710065578479')
    )
)
asyncio.ensure_future(
    publish_data_point(
        deviceId=str(faker.uuid4()),
        location=Location('2.9256061054944578', '2.9256061054944578')
    ),
)
asyncio.ensure_future(
    publish_data_point(
        deviceId=str(faker.uuid4()),
        location=Location('3.0318117541349343', '101.48630495540324')
    ),
)

loop.run_forever()