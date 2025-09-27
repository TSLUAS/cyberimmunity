import paho.mqtt.client as mqtt 
import time
import ujson as json

# функция проверки сообщения на соответствие политики безопасности
def check_policies(message) -> bool:
    if message['sender'] == "ServiceA" and message['destination'] == 'ServiceB' and message['operation'] == 'string_message':
        return True
    else:
        return False 

# сущность сервиса, способная общаться с другими сущностями
class MQTT_service:
    def __init__(self, name, broker_host='localhost', broker_port=1883):
        self.name = name 
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=name)
        
        # обработчики
        self.client.on_connect = self.on_connect 
        self.client.on_message = self.on_message 

        # параметры брокера
        self.broker_host = broker_host 
        self.broker_port = broker_port

    def on_connect(self, client, user_data, flags, rc, properties=None) -> None:
        if rc == 0:
            print(f'{self.name} подключен к Mosquitto с кодом [{rc}]')
        else:
            print(f'{self.name} не подключен. Код ошибки - [{rc}]')
        return 
    
    def on_message(self, client, user_data, msg) -> None:
        try:
            payload = json.loads(msg.payload.decode())
            sender = payload['sender']
            data = payload['data']
            destination = payload['destination']
            if destination == self.name:
                print(f'[{self.name}] получил сообщение от [{sender}] через топик [{msg.topic}]: [{data}]')
        except Exception as e:
            print(f'Ошибка при обработке соощения - {e}')
        return 
    
    def send_message(self, topic, data, destination) -> None:
        message = {
            'sender': self.name,
            'destination': destination,
            'data': data,
            'timestamp': time.time(),
            'operation': 'string_message'
        }
        print(f'[{self.name}] пытается отправить сообщение [{message}]')
        if check_policies(message=message):
            self.client.publish(topic, json.dumps(message))
            print(f'[{self.name}] отправил сообщение [{destination}] в [{topic}]: [{data}]')
        else:
            print(f'[{self.name}] не смог отправить сообщение из-за несоответствия политике безопасности')
        return 

    def start(self, topics) -> None:
        self.client.connect(self.broker_host, self.broker_port, 60)
        for topic in topics:
            self.client.subscribe(topic)
            print(f'[{self.name}] подписался на топик [{topic}]')
        self.client.loop_start()
        return
    
    def stop(self) -> None:
        self.client.loop_stop()
        self.client.disconnect()
        return 
    
def run_system() -> None:
    # инициализация сервисов
    service_a = MQTT_service(name='ServiceA')
    service_b = MQTT_service(name='ServiceB')

    # топик MQTT для общения 
    topic = 'network'

    # запуск сервисов
    service_a.start([topic])
    service_b.start([topic])

    # корректная попытка отправить сообщение
    time.sleep(3)
    service_a.send_message(topic=topic, data='Привет от ServiceA', destination='ServiceB')

    # некорректная попытка отправить сообщение
    time.sleep(3)
    service_b.send_message(topic=topic, data='Проверка связи', destination='ServiceA')

    print('Oстановка сервисов')
    service_a.stop()
    service_b.stop()
    print('Работа завершена')
        
    return 

if __name__ == '__main__':
    run_system()