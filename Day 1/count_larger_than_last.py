input_text = '''10
12
13
15
14
13
15
16
19
11
14
13
14
15
18
20
'''

# comment out these two lines to test with data above
with open('input.txt', 'r') as file:
    input_text = file.read().strip()

# answer should be 11 with test data above
# get the first number out of the text
data = input_text.partition('\n')
prev_depth = data[0].strip()

larger_measurements = 0
lines_ignored = 0

for next_depth in data[2].split('\n'):
    try:
        diff = int(next_depth) - int(prev_depth)
        #print(prev_depth, '->', next_depth, ': diff =', diff)
        if diff > 0:
            larger_measurements += 1
            #print('\tADD 1 - now', larger_measurements)
        prev_depth = next_depth
    except ValueError:
        lines_ignored += 1
        #print('Invalid value: "', next_depth, '". Ignoring this line.')

print('Number of times a depth was larger than the last?', larger_measurements)
print('Number of lines ignored?', lines_ignored)