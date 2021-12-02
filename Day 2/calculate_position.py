import argparse

parser = argparse.ArgumentParser('Provide movement instructions file path')
parser.add_argument('instructions', help='A path to a file with submarine instructions')

args = parser.parse_args()

instructions = ''

with open(args.instructions, 'r') as file:
    instructions = file.read().strip()

position = [0,0]

print('Start:', position, '\n')

for instruction in instructions.split('\n'):
    direction, units = instruction.split(' ')

    print('MOVE', direction, units, 'UNITS')

    if direction == 'forward':
        position[0] += int(units)
    elif direction == 'down':
        position[1] += int(units)
    elif direction == 'up':
        position[1] -= int(units)

    print('New position:', position)

print()
print('Final position:', position)
print('x and y multiplied =', position[0]*position[1])