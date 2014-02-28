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
    print('new values: ', message)
    p.document.getElementById('temperature').value \
        = str(message.get('temperature', '-'))

    p.document.getElementById('humidity').value \
        = str(message.get('humidity', '-'))

    p.run('''
        $('.knob_readonly').trigger('change');
        ''')

minion.setup()


def update():
    print('Sending update request')
    minion.send('update:sensor', {})
server.CALLBACKS['update'] = update


def volume(value):
    minion.send('do:mpd.volume', {'value': value})
server.CALLBACKS['volume_low'] = lambda: volume(30)
server.CALLBACKS['volume_high'] = lambda: volume(60)


print('Waiting for client...')
while len(server.LISTENERS) < 1:
    time.sleep(0.1)
print('Client found')


p.document.getElementById('temperature').onclick = update
p.document.getElementById('humidity').onclick = update

minion.run()
