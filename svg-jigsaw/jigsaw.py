#!/usr/bin/env python3

def nub(x0, y0, height, depth, width, midpoint):
    x1 = x0 + depth
    y1 = y0 + height
    return f'''
   <path stroke="red" stroke-width="2" fill="none"
           d="M {x0} {y0}
              L {x0} {midpoint-width}
              C {x0} {midpoint+width}    {x1} {midpoint-2*width}  {x1} {midpoint}
              C {x1} {midpoint+2*width}  {x0} {midpoint-width}    {x0} {midpoint+width}
              L {x0} {y1}"
     />\n'''

with open("/tmp/nub.svg", 'w') as outstream:
    outstream.write('<svg width="1000" height="1000">\n')
    for y in range(10):
        for x in range(10):
            outstream.write('<g transform="translate(%d %d)">\n' % (x*100, y*100))
            outstream.write(nub(x0=10, y0=10,
                                height=80, depth=x*10, width=y*10,
                                midpoint=50))
            outstream.write("</g>")
    outstream.write('<svg/>\n')
