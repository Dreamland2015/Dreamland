#!/usr/bin/env python3
from __future__ import print_function

import time

import configparser

import zmq
ctx = zmq.Context.instance()

def running_on_pi():
    uname_m = subprocess.check_output('uname -m', shell=True).strip()
    # Assume that an ARM processor means we're on the Pi
    return uname_m == 'armv7l' # Pi2 is arm7l vs Pi1's arm6l

def get_config():
    if onPi():
        pass #cp = ConfigParser("/etc/dreamland/dreamland.conf")
    

class SubClient():
    def __init__(self, master, topic=''):
        #ctx = zmq.Context.instance()
        self.sub = ctx.socket(zmq.SUB)
        self.sub.connect("tcp://%s:6000" % (master,) )
        #self.sub.setsockopt(zmq.SUBSCRIBE, bytes(topic, encoding='ascii'))
        self.sub.setsockopt_string(zmq.SUBSCRIBE, topic)

    def recv(self, raw=False):
        # Subscribers sign up for the topic during initialization, so split
        # that off.
        data = self.sub.recv_string()
        if raw:
            return data
        return data.split('|')[1]
        #return self.sub.recv().split('|')[1]
    
class PubClient():
    def __init__(self, master, topic):
        #ctx = zmq.Context.instance()
        self.pub = ctx.socket(zmq.PUB)
        self.pub.connect("tcp://%s:6001" % (master,) )
        self.topic = str(topic)
        time.sleep(.01)

    def send(self, msg):
        b = str('%s|%s' % (self.topic, msg))
        print('b:',b)
        return self.pub.send_string('%s|%s' % (self.topic, msg))

class PubSubProxy():
    def __init__(self):
        self.xpub = ctx.socket(zmq.XPUB)
        self.xpub.bind("tcp://*:6000")

        self.xsub = ctx.socket(zmq.XSUB)
        self.xsub.bind("tcp://*:6001")

    def run(self):
        try:
            zmq.proxy(self.xpub, self.xsub) # This blocks
        except KeyboardInterrupt:
            pass
        finally:
            ctx.destroy()
