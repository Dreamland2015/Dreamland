#!/usr/bin/env python
# Simple program to do math tables for fcserver.json
# This is for lantern 1 but is easily tweaked for others
#
# Numbers don't match real life, they were pulled from Model.pde
#
# before L1 is:
#   Carousel (top) = 7 bars * 30 leds per leg * 2 bars per leg
carousel_top = 7 * 30 * 2

#   CarouselBottom = 6 * 19
carousel_bottom = 6 * 19

offset = carousel_top + carousel_bottom

per_strand = 19
opc_per = 64

for i in xrange(8):
    print '[ 0,', offset + per_strand * i, ', ', opc_per * i, ', ', per_strand, ", \"brg\" ],"
