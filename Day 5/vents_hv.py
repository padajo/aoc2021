import argparse

parser = argparse.ArgumentParser('Provide vent data file path')
parser.add_argument('vents', help='A path to a file with vent data')

args = parser.parse_args()

class Vector:
    x, y = 0, 0
    
    def __init__(self, vector):
        x, y = vector.split(',')
        self.x = int(x)
        self.y = int(y)

    def __str__(self):
        return '[' + str(self.x) + ',' + str(self.y) + ']'

class Line:
    start, end = None, None

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __str__(self):
        return str(self.start) + ' to ' + str(self.end)

    def get_all_points_on_line(self):
        a = self.start
        b = self.end
        points = []
        if self.is_horizontal():
            if(a.y > b.y):
                # switch start end end 
                a = self.end
                b = self.start
            # now iterate the x value and create an array and return it
            for y in range(a.y, b.y + 1):
                v = Vector(str(a.x) + ',' + str(y))
                points.append(v)
        elif self.is_vertical():
            if(a.x > b.x):
                # switch start end end 
                a = self.end
                b = self.start
            # now iterate the x value and create an array and return it
            for x in range(a.x, b.x + 1):
                v = Vector(str(x) + ',' + str(a.y))
                points.append(v)
        return points 
        
    def is_horizontal(self):
        if self.start.x == self.end.x:
            return True
        return False

    def is_vertical(self):
        if self.start.y == self.end.y:
            return True
        return False

    def is_horizontal_or_vertical(self):
        return self.is_horizontal() or self.is_vertical()

    def get_max_x(self):
        if self.start.x > self.end.x:
            return self.start.x
        else:
            return self.end.x

    def get_max_y(self):
        if self.start.y > self.end.y:
            return self.start.y
        else:
            return self.end.y

    def get_min_x(self):
        if self.start.x < self.end.x:
            return self.start.x
        else:
            return self.end.x

    def get_min_y(self):
        if self.start.y < self.end.y:
            return self.start.y
        else:
            return self.end.y

class Area:

    minx, miny, maxx, maxy = 0,0,0,0
    area = None

    def __init__(self, minx, maxx, miny, maxy):
        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy
        # ignoring that minx and miny are 0
        # bit of a hack that shouldn't be
        # because there are no minus numbers
        # and the data starts at zero
        area = []
        for n in range(0, self.maxy+1):
            area.append([0]*(self.maxx+1))
        self.area = area

    def __str__(self):
        s = ''
        #for r in range(self.maxy, -1, -1):
        for r in range(0, self.maxy + 1):
            s = s + str(r) + ':' + str(self.area[r]) + '\n'
        s = s + 'x:' + str(list(range(0,self.maxx + 1))) 
        return s

    def get(self, x, y):
        return self.area[y][x]

    def set(self, x, y, value):
        self.area[y][x] = value

    def overlaps_greater_than(self, num=1):
        total = 0
        for r in range(0, self.maxy + 1):
            # get all items greater than num
            total += len([i for i in self.area[r] if i > num])
        return total


def parse_data(vent_data):
    lines = []
    for raw_line in vent_data.splitlines():
        s, e = raw_line.split(' -> ')
        start = Vector(s)
        end = Vector(e)
        line = Line(start, end)
        lines.append(line)
    return lines

raw_data = ''
with open(args.vents, 'r') as file:
    raw_data = file.read().strip()

lines = parse_data(raw_data)

#print('TOTAL lines:', len(lines))

hv_lines = []
def calculate_hv_lines_and_area(lines):
    minx, miny, maxx, maxy = 0,0,0,0
    hvlines = []
    for l in lines:
        if l.is_horizontal_or_vertical():
            hv_lines.append(l)
        if l.get_min_x() < minx:
            minx = l.get_min_x()
        if l.get_min_y() < miny:
            miny = l.get_min_y()
        if l.get_max_x() > maxx:
            maxx = l.get_max_x()
        if l.get_max_y() > maxy:
            maxy = l.get_max_y()
    return hv_lines, minx, miny, maxx, maxy

hv_lines, minx, miny, maxx, maxy = calculate_hv_lines_and_area(lines)

#print('Area:','X',minx,maxx,'Y',miny,maxy)

#print('Horizontal and Vertical lines only:', len(hv_lines))

def calculate_overlaps(line_area, lines):

    for line in lines:
        points = line.get_all_points_on_line()
        for point in points:
            value = line_area.get(point.x, point.y)
            line_area.set(point.x, point.y, value + 1)

area = Area(minx, maxx, miny, maxy)

calculate_overlaps(area, hv_lines)

# area has been filled in
print('GRID:\n',area) 

# how many numbers are greater than or equal to 2?
print('Overlaps:',area.overlaps_greater_than(1))


