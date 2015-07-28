#!/usr/bin/env python3
from __future__ import print_function

import configparser
import os
import socket
import subprocess
import time

import zmq
ctx = zmq.Context.instance()

def running_on_pi():
    uname_m = subprocess.check_output('uname -m', shell=True).strip()
    # Assume that an ARM processor means we're on the Pi
    return uname_m == b'armv7l' # Pi2 is arm7l vs Pi1's arm6l

def get_default_ip():
    """
    This sets up to send a UDP packet but doesn't actually send anything.
    It uses that to figure out what IP would be used to send.

    # TODO - does this work without a default gateway set?

    From: http://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 53))
    ip = s.getsockname()[0]
    s.close()
    return ip

class DreamlandConfig():
    def __init__(self, config_filename):
        self.filename = config_filename
        self.read_config()

    def read_config(self):
        if not os.path.exists(self.filename):
            raise Exception("Config file %s not found." % (self.filename, ))
        exec_var_dir = {}
        with open(self.filename) as f:
            code = compile(f.read(), self.filename, 'exec')
            exec(code, exec_var_dir)
        self.config = exec_var_dir['config']
        print('Config read:', self.config)

    def master(self):
        return self.config['master']

    def topic(self):
        return self.config['topic']

    def input(self):
        return self.config['input']

    def output(self):
        return self.config['output']

class SubClient():
    def __init__(self, master, topic=''):
        self.master = master
        self.topic = topic
        self.sub = ctx.socket(zmq.SUB)
        self.sub.connect("tcp://%s:6000" % (master,) )
        self.sub.setsockopt_string(zmq.SUBSCRIBE, topic)

    def recv(self, raw=False):
        # Subscribers sign up for the topic during initialization, so split
        # that off.
        data = self.sub.recv_string()
        if raw:
            return data
        return data.split('|')[1].split('#')
    
class PubClient():
    def __init__(self, master, topic=''):
        self.master = master
        self.topic = topic

        self.pub = ctx.socket(zmq.PUB)
        self.pub.connect("tcp://%s:6001" % (master,) )
        self.topic = str(topic)
        time.sleep(.01)

    def send_with_topic(self, which, level):
        return self.pub.send_string('%s|%s' % (self.topic, msg))

    def send(self, which, level):
        return self.raw_send('%s#%d' % (which, level))

    def raw_send(self, msg, topic=None):
        if topic is None: # Override used by behavior client
            topic = self.topic
        return self.pub.send_string('%s|%s' % (topic, msg))

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
