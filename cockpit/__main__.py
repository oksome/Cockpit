#!/usr/bin/env python3

import time
import threading

import skink.server as server
import skink.remote as remote

from intercom.minion import Minion


threading.Thread(target=server.start, args=()).start()

p = page = remote.RemotePage('/')
minion = Minion('controller.cockpit')


@minion.register('sensor.weather')
def weather(topic, message):
    p.document.getElementById('temperature').innerHTML \
        = str(message.get('temperature', '-'))
    p.document.getElementById('humidity').innerHTML \
        = str(message.get('humidity', '-'))

minion.setup()

print('Waiting for client...')
while len(server.LISTENERS) < 1:
    time.sleep(0.1)
print('Client found')


def update():
    minion.send('update:sensor', {})

p.document.getElementById('temperature').onclick = update
p.document.getElementById('humidity').onclick = update

minion.run()
