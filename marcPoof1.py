#
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
      print("poof a center")
      sendPoofCenterOn(centerPub, poofer)

   time.sleep(delay)

   for poofer in poofers:
      sendPoofCenterOff(centerPub, poofer)

def poofHorizSeq(centerPub, poofers, delay):
   for poofer in poofers:
      print("poof a horizontal: %s" % poofer)
      sendPoofCenter(centerPub, poofer, delay)

def sendPoofCenter(centerPub, poofer, delay):
   centerPub.send(poofer,0)
   time.sleep(delay)
   centerPub.send(poofer,1)

def sendPoofCenterOn(centerPub, poofer):
   # print("center poof on")
   centerPub.send(poofer,0)

def sendPoofCenterOff(centerPub, poofer):
   # print("center poof off")
   centerPub.send(poofer,1)

def sendPoof(poofer, delay):
   print("poof a lp")
   poofer.send('flame',0)
   time.sleep(delay)
   poofer.send('flame',1)
   time.sleep(delay * 3)

def multiPoof(poofers, delay, multiplier):
   for poofer in poofers:
      poofer.send('flame',0)
   time.sleep(delay)
   for poofer in poofers:
      poofer.send('flame',1)
   time.sleep(delay * multiplier)

def go_big():
        #poofHorizSeq(pubC, topSidePoofers, 0.015)
        print("starting gobig")
        for poofer in topSidePoofers:
            print("poofer %s" % poofer)
            sendPoofCenter(pubC, poofer, .001)
        sendPoofCenter(pubC, ['center'], 1)
        print("ending gobig")
        pass

def seqLampPost(poofers, delay):
	for poofer in poofers:
		poofer.send('flame',0)
		time.sleep(delay)
		poofer.send('flame',1)
		time.sleep(delay)
		print('lp ')

kill_all()
rotations = 0
lastposition = 4
while True:
   message = sub.recv()
   # print(message)
   # print("rotations")
   position, velocity = message[0].split(",")
   #position = (360 - float(position))
   position = float(position)

   print("lastpos: %.1f  pos: %.1f" % (lastposition, position))

   if position <= lastposition:
      lastposition = position
      print("lastpos: %.1f  pos: %.1f" % (lastposition, position))
      rotations += 1
      print("rotations: %s" % rotations)
      sendPoof(pub1, 0.03)
      sendPoof(pub2, 0.03)
      sendPoof(pub3, 0.03)
      # poofCenter(pubC, topPoofers, 0.03)
      #elif 120 < position < 125:
      #	sendPoof(pub1, 0.03)
      #	sendPoof(pub2, 0.03)
      #	sendPoof(pub3, 0.03)
      #elif 240 < position < 245:
      #	sendPoof(pub1, 0.03)
      #	sendPoof(pub2, 0.03)
      #	sendPoof(pub3, 0.03)
      # elif rotations == 4:
      # 	poofCenter(pubC, topSidePoofers, 0.05)
      # 	pass

   #if rotations == 10:
   #   poofHorizSeq(pubC, topSidePoofers, 0.001)
   #   pass

   if rotations >= 10:
      rotations = 0
      print("rotations: %s" % rotations)
      go_big()
      poofCenter(pubC, ['center'], 1.5)
      pass
