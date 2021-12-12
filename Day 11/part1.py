import argparse
import time
import os
import sys

os.system('')

RED = "\033[31;1m"
WHITE = "\033[32;1m"
REDBG = "\033[41;1m"
ENDC = "\033[m"

parser = argparse.ArgumentParser('Provide octopus energy file path')
parser.add_argument('octos', help='A path to a file with octopus energy data')
parser.add_argument('steps', help='Number of steps to cycle through')
parser.add_argument('check', help='Do a check if flag is 1')

args = parser.parse_args()

initial_data = ''

with open(args.octos, 'r') as file:
    initial_data = file.read().strip()

steps = int(args.steps)

#### PARSER ####
# split data by blank line?
a = [x.strip() for x in initial_data.split('\n\n')]

octostates = []
# parse data
for b in a:
    octostate_s = [list(x) for x in b.split('\n')[1:]]
    octostate = [] 
    for row in octostate_s:
        octostate.append([int(x) for x in row])
    octostates.append(octostate)

#### END PARSER ####

# first row in octostates is always starting state
# other states are test states (if they exist)

# Each "step" is a two part process
# 
# 1) increase energy - at which point octos will both flash and increase energy of octos 
#       around them
# 2) drop energy to zero
# 
# It doesn't matter if an octos energy goes to 14 or however high, they flash only one time
# and then drop back to zero 

# how many steps to take
steps_to_take = steps
# get the starting positions
octos = octostates[0].copy()

def display_octos(os,as_string=False,flush=False,title='',test_os=None):
    print(RED + title + ENDC)
    do_check = False
    if not test_os == None:
        do_check = True
     
    for n in range(0,len(os)):
        row = os[n]
        if as_string:
            r = []
            c = []
            for i in range(0,len(row)):
                # if do_check display a different bg if wrong
                if not do_check:
                    if row[i] == 0:
                        r.append(' ' + WHITE + "0" + ENDC)
                    elif row[i] < 10:
                        r.append(' ' + str(row[i]))
                    else:
                        r.append(' ' + RED + "F" + ENDC)
                else:
                    if row[i] == 0:
                        if test_os[n][i] == 0:
                            r.append(' ' + WHITE + "0" + ENDC)
                            c.append(' ' + WHITE + "0" + ENDC)
                        else:
                            r.append(' ' + REDBG + WHITE + "0" + ENDC)
                            c.append(' ' + WHITE + str(test_os[n][i]) + ENDC)
                    elif row[i] < 10:
                        if row[i] == test_os[n][i]:
                            r.append(' ' + str(row[i]))
                            c.append(' ' + WHITE + str(test_os[n][i]) + ENDC)
                        else:
                            r.append(' ' + REDBG + str(row[i]) + ENDC)
                            c.append(' ' + WHITE + str(test_os[n][i]) + ENDC)
                    else:
                        if row[i] == test_os[n][i]:
                            r.append(' ' + RED + "F" + ENDC)
                            c.append(' ' + WHITE + str(test_os[n][i]) + ENDC)
                        else:
                            r.append(' ' + REDBG + "F" + ENDC)
                            c.append(' ' + WHITE + str(test_os[n][i]) + ENDC)

            sys.stdout.write(''.join(r) + ' '*5 + ''.join(c) + '\r\n')
            #time.sleep(0.01)
        else:
            print(row)
    if(flush):
        time.sleep(0.03)
        print('\033[F'*(len(os)+2))

def energise_neighbours(os, pos):
    # pos is x,y so os[y][x]
    x,y = pos[0],pos[1]
    for yy in range(y-1, y+2):
        for xx in range(x-1, x+2):
            if xx < 0 or xx >= len(os[0]) or yy < 0 or yy >= len(os):
                # don't do anything
                a = 1
            elif xx == x and yy == y:
                a = 1
            else:
                octos[yy][xx] += 1

def flash(octos, pos):
    # pos is x,y so os[y][x]
    x,y = pos[0],pos[1]
    #print('FLASH:',pos)
    octos[y][x] = 0

os.system('clear')

'''
for i in range(0,len(octostates)):
    print('\nState:',i)
    for o in octostates[i]:
        print(' '.join([str(x) for x in o]))
print()
'''
print()

total_flashes = 0

started_with = octos.copy()
for step in range(1, steps_to_take+1):
    #display_octos(octos,True,True,' '*30)
    # part 1: increase every octo based on current numbers
    above_10 = 0
    for y in range(0,len(octos)):
        for x in range(0,len(octos[y])):
            octos[y][x] += 1
            if octos[y][x] > 9:
                above_10 += 1
    display_octos(octos,True,True,'Step {} p1 - iterating    '.format(str(step)))

    # part 2: let's make them *flash* 
    ### WE HAVE TO RUN THIS UNTIL THERE ARE NO MORE FLASHES LEFT ###
    flashes = True
    # count the number of numbers above 10
    fn = 0
    if above_10 == 0:
        flashes = False # NO flashes needed
    flashed = []
    while flashes:
        flashes = False
        for y2 in range(0,len(octos)):
            for x2 in range(0,len(octos[y2])):
                sformat = '{}-{}'.format(str(x2),str(y2))
                if octos[y2][x2] > 9 and not sformat in flashed:
                    flashes = True
                    total_flashes += 1
                    flashed.append(sformat)
                    energise_neighbours(octos, [x2,y2])
        display_octos(octos,True,True,'Step {} p2 - flashing {}    '.format(str(step), fn))
        sys.stdout.write('\033[E'*12)
        sys.stdout.write('Flashes:' + str(total_flashes))
        sys.stdout.write('\033[F'*12)
        

        new_above_10 = 0
        for n in range(0,len(octos)):
            for m in range(0,len(octos)):
                if octos[m][n] > 9:
                    new_above_10 += 1
        if new_above_10 == above_10:
            flashes = False
        else:
            above_10 = new_above_10
            flashes = True
        fn += 1

    # part 3: Decrease to zero
    zeroes = False
    for y in range(0,len(octos)):
        for x in range(0,len(octos[y])):
            if octos[y][x] > 9:
                zeroes = True
                octos[y][x] = 0
    display_octos(octos,True,True,'Step {} p3 - zeroing      '.format(str(step)))

    # do check if flag True
    if args.check == '1':
        test_octos = octostates[step]
        display_octos(octos,True,True,'Step {} p4 - checker      '.format(str(step)), test_octos)
        # check whether the data is the correct data
        check_fail = False
        failed = []
        if check_fail:
            '''
            print('FAILURE')
            print('\nStarted with:')
            display_octos(started_with,True)
            print('\nCalculated:')
            display_octos(octos,True)
            print('\nRequired:')
            display_octos(octostates[steps-1],True)
            print('\nFailed positions:')
            print(failed)
            print('Failed count:', len(failed))
            '''
            exit(0)

sys.stdout.write('\033[E'*12)

print('FINAL',' '*20)
display_octos(octos,True)     
print()

print('Total Flashes:', total_flashes)

