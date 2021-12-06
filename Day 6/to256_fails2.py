import argparse

parser = argparse.ArgumentParser('Provide lanternfish data file path')
parser.add_argument('lanternfish', help='A path to a file with lanternfish data')

args = parser.parse_args()

initial_data = ''

with open(args.lanternfish, 'r') as file:
    initial_data = file.read().strip()

def age_school(data='', days=1):
    # treat the data purely as text, and process it byte by byte
    next_day = ''
    added = ''
    for i in range(0, len(data)):
        if data[i] == ',':
            next_day += ','
        else:
            num = int(data[i])
            if num > 0:
                next_day += str(num - 1)
            elif num == 0:
                next_day += '6'
                added += ',8'
    next_day += added

    days -= 1

    if days == 0:
        return next_day
    else:
        return age_school(data=next_day, days=days)

final_80_data = age_school(data=initial_data, days=80)

# to get total number of fish
# add one and halve the total
# (commas are always one less than half the total as all numbers are single digits)
total_fish = (len(final_80_data) + 1)/2

print('80 days:',total_fish)

f86 = age_school(data=final_80_data, days=6)
total_fish = (len(f86)+1)/2

print('86 days:',total_fish)

n = 10
days = 96
f = f86
for i in range(days, 256 + n, n):
    print(i)
    f = age_school(data=f, days=n)
    total_fish = (len(f)+1)/2
    print(i,'days:',total_fish)
