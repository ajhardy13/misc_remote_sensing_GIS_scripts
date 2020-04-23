import argparse, sys, glob

# definition of arguments
parser = argparse.ArgumentParser(prog='Creates list of jobs', description='Extracts thematic classes from unmixed image using numpy where statements.')
parser.add_argument('-d', metavar='', type=str, default='./', help='Path to the input directory')
args = parser.parse_args()
d=args.d

print('')
print('Directory: ' + d)
print('')

imgList=glob.glob('Fractions*.kea')

# open the jobList that will contain the output list of commands
outTxt='tropwet_bandmath_jobList.sh'
sys.stdout = open(outTxt, 'w')


with open(outTxt, 'w') as f:
	for img in imgList:
			
			f.write('python /Users/Andy/Documents/Python/Remote_sensing/bandmath_tropwet.py -i ' + img + ' -d ' + d + '\n')