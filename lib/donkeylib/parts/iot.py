import json
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import requests
import zlib, pickle, os


class AwsIotCore:
    '''
    Use Iot Core MQTT broker and services.
    pip install AWSIoTPythonSDK
    '''

    def __init__(self, cfg, broker="iot.eclipse.org", inputs=['pos']):
        self.client = AWSIoTMQTTClient(cfg.AWS_CLIENT_ID, useWebsocket=cfg.AWS_IOT_USE_WEBSOCKET)
        self.topic = 'image_telemetry'
        self.session_topic = 'sessionupdate/{}'.format(cfg.AWS_CLIENT_ID)
        self.model_deploy_topic = 'modeldeploy/{}'.format(cfg.AWS_CLIENT_ID)
        self.session_id = None
        self.session_name = None
        self.inputs = inputs
        self.cfg = cfg
        port = 443 if cfg.AWS_IOT_USE_WEBSOCKET else 8883
        print('AWS_IOT:: using port: {}'.format(port))
        self.client.configureEndpoint(broker, port)
        print("connecting to broker", broker)

        self.client.configureOfflinePublishQueueing(-1) # Infinite offline Publish queueing
        self.client.configureDrainingFrequency(2) # Draining: 20 Hz
        self.client.configureConnectDisconnectTimeout(20)  # 10 sec
        self.client.configureCredentials(self.cfg.AWS_IOT_ROOT_CA, self.cfg.AWS_IOT_KEY, self.cfg.AWS_IOT_CERT)
        self.client.configureMQTTOperationTimeout(10)  # 5 sec

        self.client.connect()

        print("connected.")

        def session_callback(client, userdata, message):
            print("updating session")
            print("from topic: ")
            print(message.topic)
            data = json.loads(message.payload.decode())
            self.session_name = data['name']
            self.session_id = data['id']
            print(data)
            print("--------------\n\n")
            # print('saving session: {}'.format(message.data))

        def model_deploy_callback(client, userdata, message):
            print("updating session")
            print("from topic: ")
            print(message.topic)
            data = json.loads(message.payload.decode())
            print(data)
            self.download_model(data['weightsUrl'], filename='model.weights')
            self.download_model(data['archUrl'], filename='model.json')
            print("--------------\n\n")
            # print('saving session: {}'.format(message.data))

        self.counter = 0
        self.client.subscribe(self.session_topic, 1, session_callback)
        self.client.subscribe(self.model_deploy_topic, 1, model_deploy_callback)

    def download_model(self, url, filename):
        print('downloading model from url {}. saving with filename {}'.format(url, filename))
        with requests.get(url) as r:
            if r.status_code > 400:
                print("couldn't fetch model with code: {}".format(r.status_code))
            with open(os.path.join(self.cfg.MODELS_PATH, filename), 'wb') as f:
                for chunk in r.iter_content(chunk_size=512):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)

    def run(self, *args):
        if self.session_id and self.session_name: # negotiated a session.
            values = dict(zip(self.inputs, args))

            packet = {"name": self.topic, "val": values}
            p = pickle.dumps(packet)
            z = zlib.compress(p)
            print('publishing data {}'.format(values))
            self.counter += 1
            self.client.publishAsync(os.path.join(self.topic, self.session_name, str(self.session_id),  str(self.counter) + '.pickle'), bytearray(z), 0)

    def shutdown(self):
        self.client.disconnect()
