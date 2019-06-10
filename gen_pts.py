"""
File to generate N random points on a 2-D grid of bounds x in (-180, 180) and y in (-90,90)
Output is a csv with all of the points; first column is a unique ID, second is x value, third is y value
"""

import random as r
import uuid

N = 10000
fname = 'trash.csv'

with open(fname, 'w') as f:
    f.write('id,x,y\n')
    for i in range(N):
        id = uuid.uuid4().hex
        xpos = r.uniform(-180, 180)
        ypos = r.uniform(-90, 90)
        row = '{}, {:.5}, {:.5}\n'.format(id, xpos, ypos)
        f.write(row)

print('Wrote {} random locations to {}'.format(N, fname))
