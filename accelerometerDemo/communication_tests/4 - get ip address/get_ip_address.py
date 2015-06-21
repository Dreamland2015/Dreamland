# -*- coding: utf-8 -*-
"""
Code to get the 
"""

import socket
#import struct
#import fcntl

#def get_ip_address(ifname):
#    """ get IP address associated with a network interface
#    
#    Works on unix only
#    Parameter:
#       ifname - interface name, such as "eth0" or "lo"
#    Examples:
#    get_ip_address('lo')
#    get_ip_address('eth0')  # get address of ethernet interface
#    """
#    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#    return socket.inet_ntoa(fcntl.ioctl(
#        s.fileno(),
#        0x8915,  # SIOCGIFADDR
#        struct.pack('256s', ifname[:15])
#    )[20:24])

#def getHwAddr(ifname):
#    """ get hardware/MAC address of interface
#    
#    Works on unix only
#    Parameter:
#       ifname - interface name, such as "eth0" or "lo"
#    """
#    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
#    return ''.join(['%02x:' % ord(char) for char in info[18:24]])[:-1]


def get_local_ip_address(target):
  ipaddr = ''
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((target, 8000))
    ipaddr = s.getsockname()[0]
    s.close()
  except:
    pass

  return ipaddr

def get_ip_address_fallback():
    return socket.gethostbyname(socket.gethostname())