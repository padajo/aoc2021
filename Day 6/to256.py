import argparse

parser = argparse.ArgumentParser('Provide lanternfish data file path')
parser.add_argument('lanternfish', help='A path to a file with lanternfish data')

args = parser.parse_args()

initial_data = ''

with open(args.lanternfish, 'r') as file:
    initial_data = file.read().strip()

# counts of 0-8 (9 actual numbers)
school = [0]*9

def age_school(data, days):
    spawning = data.pop(0)
    data.append(spawning)
    data[6] += spawning
    days -= 1
    if days == 0:
        return data
    else:
        return age_school(data, days) 

for f in initial_data.split(','):
    school[int(f)] += 1

print(initial_data)
print(school)

d18 = age_school(school, 18)
print('total (day 18):', sum(d18))

d80 = age_school(school, 80-18)
print('total (day 18):', sum(d80))

d256 = age_school(school, 256-80)
print('total (day 256):', sum(d256))
