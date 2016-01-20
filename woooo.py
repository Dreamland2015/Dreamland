import util
import time

serverIp = util.get_default_ip()

# output = util.output

pub1 = util.PubClient(serverIp, 'lampPost1')
pub2 = util.PubClient(serverIp, 'lampPost2')
pub3 = util.PubClient(serverIp, 'lampPost3')

pubC = util.PubClient(serverIp, 'carousel-top')

topSidePoofers =  ['flame1', 'flame2', 'flame3']
topPoofers = ['flame1', 'flame2', 'flame3', 'center']

sub = util.SubClient(serverIp, 'motion')

lps = [pub1, pub2, pub3]
# lps = [pub1, pub2]
OFF = 1
ON = 1

def kill_all():
	pub1.send('flame', OFF)
	pub2.send('flame', OFF)
	pub2.send('flame', OFF)
	for which in topPoofers:
		pubC.send(which, OFF)

def poofCenter(centerPub, poofers, delay):
	for poofer in poofers:
		sendPoofCenterOn(centerPub, poofer)

	time.sleep(delay)

	for poofer in poofers:
		sendPoofCenterOff(centerPub, poofer)

def poofHorizSeq(centerPub, poofers, delay):
	for poofer in poofers:
		sendPoofCenter(centerPub, poofer, delay)

def sendPoofCenter(centerPub, poofer, delay):
	print("poof")
	centerPub.send(poofer,0)
	time.sleep(delay)
	centerPub.send(poofer,1)

def sendPoofCenterOn(centerPub, poofer):
	print("poof")
	centerPub.send(poofer,0)

def sendPoofCenterOff(centerPub, poofer):
	centerPub.send(poofer,1)

def sendPoof(poofer, delay):
	poofer.send('flame',0)
	time.sleep(delay)
	poofer.send('flame',1)
	time.sleep(delay )

def seqLampPost(poofers, delay):
	for poofer in poofers:
		poofer.send('flame',0)
		time.sleep(delay)
		poofer.send('flame',1)
		time.sleep(delay)
		print('lp ')

def multiPoof(poofers, delay, multiplier):
	for poofer in poofers:
		poofer.send('flame',0)
	time.sleep(delay)
	for poofer in poofers:
		poofer.send('flame',1)
	time.sleep(delay * multiplier)

def go_big():
	#poofHorizSeq(pubC, topSidePoofers, 0.015)
	for poofer in topSidePoofers:
		sendPoofCenter(pubC, poofer, .004)
	sendPoofCenter(pubC, ['center'], .01)

while True:

	for n in range(10):
		seqLampPost(lps, 0.02)
	go_big()
	poofCenter(pubC, ['center'], 1.5)
	for n in range(15):
		poofHorizSeq(pubC, topSidePoofers, 0.05)
	sendPoof(pub1, 0.03)
	sendPoof(pub2, 0.03)
	sendPoof(pub3, 0.03)
	poofCenter(pubC, topPoofers, 0.03)
	poofCenter(pubC, topSidePoofers, 0.1)
	poofCenter(pubC, topSidePoofers, 0.6)
	for n in range(10):
		poofHorizSeq(pubC, topSidePoofers, 0.015)
		time.sleep(0.01)
	# time.sleep(5)
	
