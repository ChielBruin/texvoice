from tvMainApp import MainApp
import argparse
import sys


def getOptions(args):
	'''
	Get the options from the passed arguments
	'''
	options = { }

	#TODO: remove these overrides
	args.output = 'result.pdf'
	args.input = 'timesheet2.csv'
	
	
	options['keepSource'] = ('Keep the compiled text sources', args.keepSource)
	options['resultFile'] = ('The file location where to store the result', args.output)
	options['inputFile']  = ('The file location where to load the data from', args.input)
	options['template']   = ('The template to use when compiling', 'templateTest.zip')

	return options

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-m', '--mode', choices=['compile', 'load'],
		help='Modes of operation, none for normal operation (GUI)')
	
	parser.add_argument('-k', '--keepSource', type=bool, default=False,
		help='Whether to keep the source files')
	parser.add_argument('-i', '--input', type=argparse.FileType('r'), default=sys.stdin,
		help='The input to process, stdin by default')
	parser.add_argument('-o', '--output', type=argparse.FileType('w'), default=sys.stdout,
		help='The location to store the result, stdout by default')

	args = parser.parse_args()
	
	options = getOptions(args)
	
	if args.mode:
		if args.mode is 'compile':
			print('Compile mode')
		if args.mode is 'load':
			print('Load mode')
	else :
		MainApp().draw(options)
