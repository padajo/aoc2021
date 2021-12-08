import argparse
import statistics

parser = argparse.ArgumentParser('Provide crab data file path')
parser.add_argument('crabs', help='A path to a file with crabs data')

args = parser.parse_args()

initial_data = ''

with open(args.crabs, 'r') as file:
    initial_data = file.read().strip()

crabs = [int(x) for x in initial_data.split(',')]

print('Mean:', statistics.mean(crabs))
print('Median:', statistics.median(crabs))
print('Mode:', statistics.mode(crabs))

# make the median an int as the point to focus on
median = round(statistics.median(crabs))
fuel_crabs = [abs(median-x) for x in crabs]
fuel = sum(fuel_crabs)

print('fuel (pt 1):', fuel)

# use the mean as the point to focus on for part 2
mean = round(statistics.mean(crabs))
# as it's between 2 numbers, check both the upper and lower one
fuel2_crabs = [round(abs(mean-x)*((abs(mean-x)+1))/2) for x in crabs]
fuel2 = sum(fuel2_crabs)
print('fuel a (pt 2):',fuel2,'mean:', mean)
fuel3_crabs = [round(abs(mean-x-1)*((abs(mean-x-1)+1))/2) for x in crabs]
fuel3 = sum(fuel3_crabs)
print('fuel b (pt 2):',fuel3,'mean:', mean-1)

