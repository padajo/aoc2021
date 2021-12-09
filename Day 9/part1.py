import argparse

parser = argparse.ArgumentParser('Provide segments heightmap file path')
parser.add_argument('heightmap', help='A path to a file with signals data')

args = parser.parse_args()

initial_data = ''

with open(args.heightmap, 'r') as file:
    initial_data = file.read().strip()

height_lines = initial_data.splitlines()

m = []
for row in height_lines:
    r = [x for x in row]
    m.append(r)

mheights = []
for x in range(0,len(m[0])):
    for y in range(0,len(m)):
        # identify local minima with 
        n = int(m[y][x])
        a = 1000
        try:
            a = int(m[y+1][x])
        except:
            a = 1000
        b = 1000
        try:
            b = int(m[y-1][x])
        except:
            b = 1000
        c = 1000
        try:
            c = int(m[y][x+1])
        except:
            c = 1000
        d = 1000
        try:
            d = int(m[y][x-1])
        except:
            d = 1000
        if a > n and b > n and c > n and d > n:
            # local minima
            mheights.append(int(n))

print(mheights)
risk = [x + 1 for x in mheights]
print(sum(risk))


