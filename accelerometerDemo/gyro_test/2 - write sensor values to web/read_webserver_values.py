import urllib.request
import urllib.error
import requests

SERVERADDRESS = "http://192.168.0.3:8080"  # Change this address to your settings

def read_values1():
    link = SERVERADDRESS
    # code below modified so it works with python3
    try:
        with urllib.request.urlopen(link) as url:
            myfile = url.read()     # in python3 this is binary data, not string
        myfilestr = str(myfile, encoding='utf8') # so we need to convert to str
        return myfilestr.split(" ")
    except urllib.URLError:
        return ("couldn't read web data")

def read_values():
    link = SERVERADDRESS
    r = requests.get(link)