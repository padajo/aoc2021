import argparse
import statistics

parser = argparse.ArgumentParser('Provide segments signals file path')
parser.add_argument('signals', help='A path to a file with signals data')

args = parser.parse_args()

initial_data = ''

with open(args.signals, 'r') as file:
    initial_data = file.read().strip()

# splitlines and split on | and split *that* on spaces
# this gives us all signals
output_data = [list(x.split('|'))[1].strip().split(' ') for x in initial_data.splitlines()]

# now count how many of the signals have 2, 3, 4 or 7 characters
# which corresponds to 1, 7, 4 or 8 in display

count = 0
for segments in output_data:
    for segment in segments:
        l = len(segment)
        if l == 2 or l == 3 or l == 4 or l == 7:
            count += 1

print('count (pt 1):', count)
    

