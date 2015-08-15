#!/usr/bin/env python
# Simple program to do math tables for fcserver.json
# This is for lantern 1 but is easily tweaked for others
#
# Numbers don't match real life, they were pulled from Model.pde
#
# before L1 is:
#
carousel_top = 9 * 34 * 2

#   CarouselBottom = 6 * 19
carousel_bottom = 6 * (30 + 6)

inner_bench = 2 * (5 + 6)
inner_bench_tot = 3 * inner_bench

outer_bench = 2 * (16 + 17 + 18)
outer_bench_tot = outer_bench * 3

offset = carousel_top + carousel_bottom + inner_bench_tot + outer_bench_tot

per_strand = 19
opc_per = 64

for i in xrange(8):
    print '[ 0,', offset + per_strand * i, ', ', opc_per * i, ', ', per_strand, ", \"brg\" ],"
