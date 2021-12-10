import argparse
import time

parser = argparse.ArgumentParser('Provide segments route file path')
parser.add_argument('route', help='A path to a file with route data')

args = parser.parse_args()

initial_data = ''

with open(args.route, 'r') as file:
    initial_data = file.read().strip()

routes = initial_data.splitlines()

# move to AaBbCcDd
data = []
for route in routes:
    s = route
    s = s.replace('{','A')
    s = s.replace('}','a')
    s = s.replace('[','B')
    s = s.replace(']','b')
    s = s.replace('(','C')
    s = s.replace(')','c')
    s = s.replace('<','D')
    s = s.replace('>','d')
    data.append(s)

pairs = {'a':'A', 'b':'B', 'c':'C', 'd':'D'}
scores_pt1 = {'a': 1197, 'b': 57, 'c': 3, 'd': 25137}

r = []
pt1_scores = []

for line in data:
    h = ''
    for c in line:
        if c in 'ABCD':
            h += c
        elif h[-1] == pairs[c]:
            h = h[:-1]
        else:
            print('Illegal Character:',c, end='\r', flush=True)
            time.sleep(0.05)
            pt1_scores.append(scores_pt1[c])
            break
    else:
        r.append(h)

print()
print('total:',sum(pt1_scores))
