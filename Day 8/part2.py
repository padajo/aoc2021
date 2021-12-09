import argparse
import string

parser = argparse.ArgumentParser('Provide segments signals file path')
parser.add_argument('signals', help='A path to a file with signals data')

args = parser.parse_args()

initial_data = ''

with open(args.signals, 'r') as file:
    initial_data = file.read().strip()

# splitlines and split on | and split *that* on spaces
# this gives us all signals
value_signals = initial_data.splitlines()

def decode_signal(encoded_signal):

    print('INPUT:', encoded_signal.strip())
    data = encoded_signal.split('|')

    # we are trying to determine which input (wires) correspond to which output (signals)
    # NOTE: creating a POSITION separation, so a wire input is lower case, and a position
    # in the display is upper case
    i_data = data[0].strip().split(' ')
    o_data = data[1].strip().split(' ')
    i_nums = [-1]*10
    o_nums = [-1,-1,-1,-1]
    w_sets = ['abcdefg']*10
    wires = ['abcdefg']*7
    transforms = {}

    #for i in range(0,len(wires)):
    #    wires[i] = 'abcdefg'
    
    ### process is:
    ### if a signal is for number 1
    ### then there are only 2 letters (wires)
    ### so they must correspond to POSITIONS C and F
    ### so remove everything but C and F for both those letters

    ###  AAAA
    ### B    C
    ### B    C
    ###  DDDD
    ### E    F
    ### E    F
    ###  GGGG

    # CF is 1
    # ACDEG is 2
    # ACDFG is 3
    # BDCF is 4
    # ABDFG is 5
    # ABDEFG is 6
    # ACF is 7
    # ABCDEFG is 8
    # ABCDFG is 9
    # ABCEFG is 0

    # 2 chars: 1
    # 3 chars: 7
    # 4 chars: 4
    # 5 chars: 2,3,5
    # 6 chars: 6,9,0
    # 7 chars: 8

    # so we can always identify 4 numbers with ease
    # only 5 and 6 do not have "C" in them
    # common for 5 chars: ADG
        # 2 adds CE
        # 3 adds CF
        # 5 adds BF
    # common for 6 chars: ABFG
        # 6 adds DE
        # 9 adds CD
        # 0 adds CE

    ### PASS 1 ###
    # place all numbers that we know in the d['input_numbers'] and d['output_numbers']
    for n in range(0,len(i_data)):
        s = i_data[n]
        if len(s) == 2:
            i_nums[n] = 1
            w_sets[1] = s # for number 1, this is the set of wires
        elif len(s) == 3:
            i_nums[n] = 7
            w_sets[7] = s # for number 7, this is the set of wires
        elif len(s) == 4:
            i_nums[n] = 4
            w_sets[4] = s # for number 4, this is the set of wires
        elif len(s) == 7:
            i_nums[n] = 8
            w_sets[8] = s # for number 8, this is the set of wires
        elif len(s) == 5:
            i_nums[n] = [2,3,5]
        elif len(s) == 6:
            i_nums[n] = [0,6,9]

    # if there is a 1 and a 7 we can work out the wire for A
    # and which 2 wires are C and F

    
    if 1 in i_nums and 7 in i_nums:
        p1 = i_nums.index(1)
        w1 = i_data[p1]
        p7 = i_nums.index(7)
        w7 = i_data[p7]
        a_pos = [x for x in w7 if x not in w1]
        wires[0] = a_pos[0]
        wires[2] = w1 # position C
        wires[5] = w1 # position F
        # store these transforms
        transforms[w1] = 'CF'
        transforms[a_pos[0]] = 'A' 
        

    # if we have a 4 and a 1 or a 7 we can work out the wires for B and E

    if 4 in i_nums and ( 7 in i_nums or 1 in i_nums ):
        p4 = i_nums.index(4)
        w4 = i_data[p4]
        p7 = -1
        w = ''
        if 7 in i_nums:
            p7 = i_nums.index(7)
            w = i_data[p7]
        else:
            p1 = i_nums.index(1)
            w = i_data[p1]
        be_pos = [x for x in w4 if x not in w]
        wires[1] = ''.join(be_pos)
        wires[4] = ''.join(be_pos)
        transforms[wires[1]] = 'BE'

    # let's loop over the 6s and 5s separately
    is6 = [False]*len(i_data)
    is5 = [False]*len(i_data)
    for i in range(0,len(i_data)):
        if len(i_data[i]) == 6:
            is6[i] = True
        elif len(i_data[i]) == 5:
            is5[i] = True

    sixes, fives = {}, {}
    for n in range(0,len(i_data)):
        # only work on 6s
        if is6[n]:
            sixes[i_data[n]] = []
        if is5[n]:
            fives[i_data[n]] = []

    # if we have any signals with six letters (from 6 wires)
    # the 6 wire numbers are missing either C, D or E
    if len(sixes) > 0:
        uml = [] # unique missing letters
        letters = 'abcdefg'

        for d in sixes:
            missing = [x for x in letters if x not in d]
            uml.append(missing[0])


        if 4 in i_nums:
            # we can work out what position E is
            p4 = i_nums.index(4)
            w = i_data[p4]
            match = [x for x in uml if x not in w]
            transforms[match[0]] = 'E'
            

        if 7 in i_nums or 1 in i_nums:
            w = ''
            if 1 in i_nums:
                p1 = i_nums.index(1)
                w = i_data[p1]
            else:
                p7 = i_nums.index(7)
                w = i_data[p7]
            # whatever matches that in uml (unique missing letters) is C
            match = [x for x in w if x in uml]
            # remove the F from the CF that likely exists
            keys_to_remove = []
            ks = list(transforms.keys())
            for ws in ks:
                if match[0] in ws:
                    # we know the wire is in there, so remove it
                    k = ws 
                    v = transforms[k]
                    new_k = ws.replace(match[0],'')
                    new_v = transforms[k].replace('C','')
                    transforms[new_k] = new_v
                    keys_to_remove.append(k)
            transforms[match[0]] = 'C'
            for k in keys_to_remove:
                transforms.pop(k)

        # if we know what C and E is (see transforms) then we know what
        # D is because it's the missing one here
        vs = transforms.values()
        if 'C' in vs and 'E' in vs:
            # E must be the missing one
            ce_keys = []
            for k in transforms.keys():
                if transforms[k] == 'C':
                    ce_keys.append(k)
                elif transforms[k] == 'E':
                    ce_keys.append(k)
            # find which uml value is not in ce_keys
            missing = [x for x in uml if x not in ce_keys]
            d_pos = missing[0]
            keys_to_remove = []
            for ws in transforms.keys():
                if d_pos in ws:
                    # we know the wire is in there, so remove it
                    k = ws 
                    v = transforms[k]
                    new_k = ws.replace(d_pos,'')
                    new_v = transforms[k].replace('D','')
                    keys_to_remove.append(k)
            transforms[d_pos] = 'D'
            for k in keys_to_remove:
                transforms.pop(k)

        # check back in with 4 (!) to see if that gives solves any puzzle here
        # because we may have everything (we should have worked out every other
        # position for 4 except 'B')
        if 4 in i_nums:
            # we can work out what position B is
            p4 = i_nums.index(4)
            w = i_data[p4]
            decoded = ''.join(list(transforms.keys()))
            unique = [x for x in w if x not in decoded]
            # unique[0]
            transforms = add_new_transform(transforms, unique[0], 'B')
    

    #output_transform(transforms)

    # now we have transforms at 7 (!) then return the value of the outputs
    digits = decode_output(o_data, transforms)
    return (1000*digits[0]) + (100*digits[1]) + (10*digits[2]) + (digits[3])


def decode_output(o, ts):
    nums = [-1,-1,-1,-1]
    for n in range(0,len(o)):
        s = o[n]
        #print(s)
        if len(s) == 2:
            nums[n] = 1
        elif len(s) == 3:
            nums[n] = 7
        elif len(s) == 4:
            nums[n] = 4
        elif len(s) == 7:
            nums[n] = 8
        elif len(s) == 5:
            #print('DECODE 5 chars:', s)
            sts = {}
            for k in ts.keys():
                if k in s:
                    sts[k] = ts[k]
            #output_transform(sts)
            nums[n] = transform_to_num(s, ts)
        elif len(s) == 6:
            #print('DECODE 6 chars:', s)
            sts = {}
            for k in ts.keys():
                if k in s:
                    sts[k] = ts[k]
            #output_transform(sts)
            nums[n] = transform_to_num(s, ts)
    
    return nums

def transform_to_num(wires, ts):
    # only need to do 5 char and 6 char
    tr = ''
    # put wires into alphabetical order
    w = ''.join(sorted(wires))
    for c in w:
        tr += ts[c]

    tr_sort = ''.join(sorted(tr))

    #print(wires)
    #print(w)
    #print(ts)
    #print(tr_sort)

    if tr_sort == 'ABCEFG':
        return 0
    elif tr_sort == 'ACDFG':
        return 3
    elif tr_sort == 'ACDEG':
        return 2
    elif tr_sort == 'ABCDFG':
        return 9
    elif tr_sort == 'ABDFG':
        return 5
    elif tr_sort == 'ABDEFG':
        return 6

def add_new_transform(ts, wire, pos):
    ks = list(ts.keys())
    keys_to_remove = []
    for ws in ks:
        if wire in ws:
            # we know the wire is in there, so remove it
            k = ws 
            v = ts[k]
            new_k = ws.replace(wire,'')
            new_v = ts[k].replace(pos,'')
            ts[new_k] = new_v
            keys_to_remove.append(k)
    ts[wire] = pos
    for k in keys_to_remove:
        wire.pop(k)

    found_wires = ''
    found_pos = ''
    for key in ts.keys():
        if len(key) == 1:
            found_wires += key
            found_pos += ts[key]

    # if we know we've found 6 of 7 wires (single char transforms)
    # finish it off!
    if len(found_wires) == 6:
        # finish off the last one (!!)
        all_wires = 'abcdefg'
        all_pos = 'ABCDEFG'
        unique_wire = [x for x in all_wires if x not in found_wires]
        unique_pos = [x for x in all_pos if x not in found_pos]
        ts[unique_wire[0]] = unique_pos[0] 

    return ts 

def output_transform(t):

    print('')
    vs = list(t.values())

    if 'A' in vs:
        print(' AAAA ')
    else:
        print(' .... ')

    bc = [False, False]
    if 'B' in vs:
        bc[0] = True
    if 'C' in vs:
        bc[1] = True

    for i in range(0,3):
        if bc[0] and bc[1]:
            print('B    C')
        elif bc[0] and not bc[1]:
            print('B    .')
        elif bc[1] and not bc[0]:
            print('.    C')
        else:
            print('.    .')

    if 'D' in vs:
        print(' DDDD ')
    else:
        print(' .... ')

    ef = [False, False]
    if 'E' in vs:
        ef[0] = True
    if 'F' in vs:
        ef[1] = True

    for i in range(0,3):
        if ef[0] and ef[1]:
            print('E    F')
        elif ef[0] and not ef[1]:
            print('E    .')
        elif ef[1] and not ef[0]:
            print('.    F')
        else:
            print('.    .')
    
    if 'G' in vs:
        print(' GGGG ')
    else:
        print(' .... ')


values = []
for n in range(0,len(value_signals)):
    decoded = (decode_signal(value_signals[n]))
    values.append(decoded)

print(values)

print('sum of all values:',sum(values))

