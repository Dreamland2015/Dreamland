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
	print("poof")
	poofer.send('flame',0)
	time.sleep(delay)
	poofer.send('flame',1)
	time.sleep(delay * 3)

def multiPoof(poofers, delay):
	for poofer in poofers:
		poofer.send('flame',0)
	time.sleep(delay)
	for poofer in poofers:
		poofer.send('flame',1)
	time.sleep(delay * 4)

poofpat1_count = 0
def poofpattern1:
	message = sub.recv()
	position, velocity = message[0].split(",")
	position = (360 - float(position))

    spacing = 10
	if (position % spacing == 0)
		poofpat1_count += 1
	if (poofpat1_count % 4 ==0)
		poofCenter(pubC, topSidePoofers, 0.02)
	if (poofpat1_count % 4 ==1)
		poofCenter(pubC, topSidePoofers, 0.02)
	if (poofpat1_count % 4 ==2)
		poofCenter(pubC, topSidePoofers, 0.02)
	if (poofpat1_count % 4 ==3)
		poofCenter(pubC, topSidePoofers, 0.02)
		pass

rotations = 0
while True:
	message = sub.recv()
	# print(message)
	# print("rotations")
	position, velocity = message[0].split(",")
        print("pos: %d, vel: %d" % position, velocity)
	if 0 < float(position) < 5:
		rotations += 1
	if rotations > 20:
		rotations = 0

	print(rotations)

	position = (360 - float(position))

	if 0 < position < 5:
		sendPoof(pub1, 0.03)
		sendPoof(pub2, 0.03)
		# poofCenter(pubC, topPoofers, 0.03)
	elif 120 < position < 125:
		sendPoof(pub2, 0.03)
		sendPoof(pub3, 0.03)
		# poofCenter(pubC, topPoofers, 0.03)
		# poofCenter(pubC, topSidePoofers, 0.1)
	elif 240 < position < 245:
		sendPoof(pub3, 0.03)
		sendPoof(pub1, 0.03)
		# poofCenter(pubC, topSidePoofers, 0.1)
		poofCenter(pubC, topPoofers, 0.1)
		# if rotations == 0:
		# 	poofCenter(pubC, ['center'], 0.1)
		# else:
		# 	poofCenter(pubC, topSidePoofers, 0.3)
	elif rotations == 4:
		poofCenter(pubC, topSidePoofers, 0.02)

	elif rotations == 5:
		poofHorizSeq(pubC, topSidePoofers, 0.015)

	# if rotations == 4:
	# 	poofCenter(pubC, topSidePoofers, 0.02)

	# elif rotations == 15:
	# 	poofHorizSeq(pubC, topSidePoofers, 0.015)



	#if velocity


	# sendPoof(pub1, 0.11)

	# for poofer in lps:
	# 	sendPoof(poofer, 0.2)

	# time./sleep(1)


