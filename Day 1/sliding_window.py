input_data = '''199
200
208
210
200
207
240
269
260
263
'''

# comment out these two lines to test with data above
with open('input.txt', 'r') as file:
    input_data = file.read().strip()

# answer should be 5 with test data above
str_data = input_data.strip().splitlines()
data = [int(num) for num in str_data]
print(str_data)

# 'lsm' is 'larger sliding measurements'
lsm = 0
lines_ignored = 0

# calculate 'prev_sdepth'
prev_sdepth = data[0] + data[1] + data[2]

for i in range(3, len(data)):
    next_sdepth = data[i - 2] + data[i - 1] + data[i]
    diff = int(next_sdepth) - int(prev_sdepth)
    print(prev_sdepth, '->', next_sdepth, ': diff =', diff)
    if diff > 0:
        lsm += 1
        print('\tADD 1 - now', lsm)
    prev_sdepth = next_sdepth

print('Number of times a sliding depth was larger than the last?', lsm)
