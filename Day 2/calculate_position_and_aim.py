import argparse

parser = argparse.ArgumentParser('Provide movement instructions file path')
parser.add_argument('instructions', help='A path to a file with submarine instructions')

args = parser.parse_args()

instructions = ''

with open(args.instructions, 'r') as file:
    instructions = file.read().strip()

# [x,y,aim]
position_and_aim = [0,0,0]

print('Start:', position_and_aim, '\n')

for instruction in instructions.split('\n'):
    direction, units = instruction.split(' ')

    print('MOVE AND AIM', direction, units, 'UNITS')

    if direction == 'forward':
        position_and_aim[0] += int(units) # increases horizontal position by UNITS and increases depth by AIM * UNITS
        position_and_aim[1] += position_and_aim[2] * int(units)
    elif direction == 'down':
        position_and_aim[2] += int(units) # increases AIM
    elif direction == 'up':
        position_and_aim[2] -= int(units) # decreases AIM

    print('New position and aim', position_and_aim)

print()
print('Final position and aim', position_and_aim)
print('x and y multiplied =', position_and_aim[0]*position_and_aim[1])