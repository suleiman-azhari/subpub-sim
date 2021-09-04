import os
from google.cloud import pubsub_v1
from mysql.connector import Error, connect
from mysql.connector.pooling import MySQLConnectionPool
import json

# Create a connection pool of size 5 (default)
try:
    cnx_pool = MySQLConnectionPool(
    host = os.getenv('DB_HOST'),
     user = os.getenv('DB_USER'),
     password = os.getenv('DB_PASSWORD'),
     database = os.getenv('DB_NAME'),
     auth_plugin = 'mysql_native_password',
    )
except Error as e:
    print('Error while connecting', e)

subscriber = pubsub_v1.SubscriberClient()
publisher = pubsub_v1.PublisherClient()

subscription_path = subscriber.subscription_path(
    'iot-simulator', 'iot-sensors-sub')
topic_path = publisher.topic_path('iot-simulator', 'iot-topic')

def callback(message):
    print(f'Received {message.data}')
    message.ack()
    print(f'Acknowledged {message.message_id}')

    data = json.loads(message.data)

    cnx = cnx_pool.get_connection()
    cursor = cnx.cursor()

    insert_record = """
    INSERT INTO Device (deviceId, temperature, location, time)
    VALUES
    (%s, %s, point(%s,%s), %s)
    """

    record = (data['deviceId'], data['temperature'], data['Location']
              ['lat'], data['Location']['long'], data['time'])
    cursor.execute(insert_record, record)
    cnx.commit()
    cursor.close()
    cnx.close()

subscriber.create_subscription(name=subscription_path, topic=topic_path)

streaming_pull_future = subscriber.subscribe(
    subscription_path, callback=callback)
print(f'Listening for messages on {subscription_path}')

with subscriber:
    try:
        streaming_pull_future.result()
    except TimeoutError:
        streaming_pull_future.cancel()
        streaming_pull_future.result()