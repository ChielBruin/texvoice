from tvMainApp import MainApp
import argparse


if __name__ == '__main__':
	# TODO use subparsers:
	# texvoice [compile | loadData | full], where
	# compile:  <inputFile, outputFile, template> [keepSource]
	# loadData: <inputFile, outputFile> [loaderOptions]
	# full:     <inputFile, outputFile, template> [loaderOptions, keepsource]
	# Input and output file should be stdin and stdout by default
	
	#parser = argparse.ArgumentParser()
	#parser.add_argument('-m', '--mode', choices=['compile', 'load'],
		#help='Modes of operation, none for normal operation (GUI)')
	
	#parser.add_argument('-k', '--keepSource', type=bool, default=False,
		#help='Whether to keep the source files')
	#parser.add_argument('-i', '--input', type=argparse.FileType('r'), default=sys.stdin,
		#help='The input to process, stdin by default')
	#parser.add_argument('-o', '--output', type=argparse.FileType('w'), default=sys.stdout,
		#help='The location to store the result, stdout by default')

	#args = parser.parse_args()
	
	if args.mode:
		if args.mode is 'compile':
			print('Compile mode')
		if args.mode is 'load':
			print('Load mode')
	else :
		MainApp().draw()
