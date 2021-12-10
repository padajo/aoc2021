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

def get_minima_and_heights(m):
    mheights = []
    minima = []
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
                minima.append([x,y])
                mheights.append(int(n))

    return minima, mheights

minima, mheights = get_minima_and_heights(m)
print(minima)

def fill_basin_positions(kp, m):
    # kp = known positions
    # m = map

    added_positions = []

    basin = len(kp.keys())

    for pos in kp.keys():
        # get x and y
        xy = pos.split('-')
        x,y = int(xy[0]), int(xy[1])
        # depth n
        n = int(m[y][x])
        # default depth to 9
        a,b,c,d = 9, 9, 9, 9
        try:
            if (y+1) < len(m):
                a = int(m[y+1][x])
        except:
            a = 9
        try:
            if (y-1) > -1:
                b = int(m[y-1][x])
        except:
            b = 9
        try:
            if (x+1) < len(m[y]):
                c = int(m[y][x+1])
        except:
            c = 9
        try:
            if (x-1) > -1:
                d = int(m[y][x-1])
        except:
            d = 9
        if a < 9:
            added_positions.append([x,y+1])
        if b < 9:
            added_positions.append([x,y-1])
        if c < 9:
            added_positions.append([x+1,y])
        if d < 9:
            added_positions.append([x-1,y])
        
    for p in added_positions:
        x,y = p[0], p[1]
        k = '{0}-{1}'.format(x,y)
        if k not in kp:
            kp[k] = m[y][x]

    if len(kp.keys()) > basin:
        fill_basin_positions(kp, m)


def get_basin_size(m, minimum):
    # kp = known positions
    kp = {}
    x,y = minimum[0],minimum[1]
    k = '{0}-{1}'.format(x,y)
    # store the value against the key
    kp[k] = m[y][x]
    # now get all the basin positions nearby
    # send the known positions
    # send the map
    fill_basin_positions(kp, m)
    return len(kp.keys())

sizes = []
for minimum in minima:
    # m = map
    # m = local minimum
    sizes.append(get_basin_size(m, minimum))

print(sizes)

# find 3 largest
sizes.sort()

top3 = sizes[-3:]

print('Top 3 multipled together:', top3[0]*top3[1]*top3[2])


