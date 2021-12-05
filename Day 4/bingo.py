import argparse

parser = argparse.ArgumentParser('Provide bing data file path')
parser.add_argument('bingodata', help='A path to a file with bingo data')

args = parser.parse_args()

def parse_data(data):
    # first line is bingo numbers called in order
    # any blank number means next 5 rows are a bingo card
    bingodata = {'calls':[],'cards':[]} 
    bingocard = []
    for line in data.split('\n'):
        if len(bingodata['calls']) == 0:
            bingodata['calls'] = list(map(int,line.strip().split(',')))
        else:
            if line.strip() == '':
                if len(bingocard) > 0:
                    bingodata['cards'].append(bingocard)
                bingocard = []
            else:
                # add line to bingocard
                bingocard.append(list(map(int,line.strip().replace('  ', ' ').split(' '))))
    # append the last card
    bingodata['cards'].append(bingocard)
    return bingodata

def display_card(card=[], numbers_played=[]):
    print('---------------CARD---------------')
    for row in card:
        output = []
        for num in row:
            if num in numbers_played:
                output.append('*' + str(num))
            else:
                output.append(str(num))
        print('\t'.join(output))
    print('----------------------------------')

raw_data = ''
with open(args.bingodata, 'r') as file:
    raw_data = file.read().strip()

bingodata = parse_data(raw_data)

#print('\n*** BINGO DATA ***\n')
#print(bingodata)

def is_card_a_winner(card, called_numbers):
    for row in card:
        in_called = []
        for num in row:
            if num in called_numbers:
                in_called.append(num)
        if len(in_called) == len(row):
            #print('RETURN TRUE (a)')
            return True
    for colnum in range(0,len(card[0])):
        # check over each row
        in_called = []
        for row in card:
            if row[colnum] in called_numbers:
                in_called.append(row[colnum])
        if len(in_called) == len(card[0]):
            #print('RETURN TRUE (b)')
            return True
    return False

def score_winning_card(card, called_numbers):
    # 1) get sum of all *unmarked numbers*
    unmarked = []
    for row in card:
        for num in row:
            if not num in called_numbers:
                unmarked.append(num)
    #print(unmarked)
    # 2) multiply by the last number called
    last_number = called_numbers[len(called_numbers)-1]

    return sum(unmarked) * last_number

def show_all_cards(bingodata, called_numbers):
    for card in bingodata['cards']:
        display_card(card, called_numbers)

called = []

for n in range(0,len(bingodata['calls'])):
    next_num = bingodata['calls'][n]
    # add next num to numbers called
    called.append(next_num)
    print('**** CALL ****','Number:', next_num)
    # are there any winning cards?
    for card in bingodata['cards']:
        is_winner = is_card_a_winner(card, called)
        #print(is_winner)
        if is_winner:
            #show_all_cards(bingodata, called)
            display_card(card, called)
            print('CARD SCORE:', score_winning_card(card, called))
            exit(0)

