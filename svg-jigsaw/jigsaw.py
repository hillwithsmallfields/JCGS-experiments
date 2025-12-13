#!/usr/bin/env python3

import nubs

with open("/tmp/nub.svg", 'w') as outstream:
    outstream.write('<svg width="1000" height="1000">\n')
    for y in range(10):
        for x in range(10):
            outstream.write('<g transform="translate(%d %d)">\n' % (x*100, y*100))
            outstream.write(nubs.vertical_with_nub(x0=10, y0=10,
                                                   height=80, nub_depth=-(2*x+10), nub_breadth=2*y+10,
                                                   midpoint=50))
            outstream.write(nubs.horizontal_with_nub(x0=10, y0=10,
                                                     height=80, nub_depth=-(2*x+10), nub_breadth=2*y+10,
                                                     midpoint=50))
            outstream.write("</g>\n")
    outstream.write('</svg>\n')
