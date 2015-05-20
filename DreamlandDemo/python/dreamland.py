#!/usr/bin/env python

import argparse
from dreamlandObject import DreamlandServer, DreamlandStructure


def parseAndRun():
	parser = argparse.ArgumentParser(description='Lets setup this dreamland object!')

	# What type of object will this be?
	parser.add_argument('-s', '--server', help='launch pi as the server')
	parser.add_argument("-c", "--carousel", help="launch pi as carousel")
	parser.add_argument("-b", "--bench", help="launch pi as a bench")
	parser.add_argument("-l", "--lampPost", help="launch pi as a lamppost")

	args = parser.parse_args()

	if args.server:
		DreamlandServer('server')
	elif args.carousel:
		DreamlandStructure('carousel')
	elif args.bench:
		DreamlandStructure(args.bench)
	elif args.lampPost:
		DreamlandStructure(args.lampPost)


if __name__ == "__main__":
	parseAndRun()
