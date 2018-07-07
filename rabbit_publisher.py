import redis, time, pika, os, logging
import simplejson as json
# example_publisher.py

logging.basicConfig()

# Parse CLODUAMQP_URL (fallback to localhost)
url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost/%2f')
params = pika.URLParameters(url)
params.socket_timeout = 5

connection = pika.BlockingConnection(params) # Connect to CloudAMQP
channel = connection.channel() # start a channel
channel.queue_declare(queue='publisher') # Declare a queue

r = redis.StrictRedis(host='localhost', port=6379, db=0)
r_list = r.keys()

for r_id in r_list:
	to_json = json.dumps(r.get(r_id))
	teste = to_json.replace("[","").replace("]","").replace("'",'"')
	channel.basic_publish(exchange='', routing_key='publisher', body=str(teste))
	time.sleep(5)
