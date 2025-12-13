#!/usr/bin/env python3

def vertical_with_nub(x0, y0, height, nub_depth, nub_breadth, midpoint):
    x1 = x0 + nub_depth
    y1 = y0 + height
    return f'''
   <path stroke="red" stroke-width="2" fill="none"
           d="M {x0} {y0}
              L {x0} {midpoint-nub_breadth}
              C {x0} {midpoint+nub_breadth}    {x1} {midpoint-2*nub_breadth}  {x1} {midpoint}
              C {x1} {midpoint+2*nub_breadth}  {x0} {midpoint-nub_breadth}    {x0} {midpoint+nub_breadth}
              L {x0} {y1}" />\n'''

def horizontal_with_nub(x0, y0, height, nub_depth, nub_breadth, midpoint):
    x1 = x0 + height
    y1 = y0 + nub_depth
    return f'''
   <path stroke="green" stroke-width="2" fill="none"
           d="M {x0}                     {y0}
              L {midpoint-nub_breadth}   {y0}
              C {midpoint+nub_breadth}   {y0}    {midpoint-2*nub_breadth} {y1}     {midpoint}             {y1}
              C {midpoint+2*nub_breadth} {y1}    {midpoint-nub_breadth}   {y0}     {midpoint+nub_breadth} {y0}
              L {x1}                     {y0}" />\n'''

with open("/tmp/nub.svg", 'w') as outstream:
    outstream.write('<svg width="1000" height="1000">\n')
    for y in range(10):
        for x in range(10):
            outstream.write('<g transform="translate(%d %d)">\n' % (x*100, y*100))
            outstream.write(vertical_with_nub(x0=10, y0=10,
                                              height=80, nub_depth=-(2*x+10), nub_breadth=2*y+10,
                                              midpoint=50))
            outstream.write(horizontal_with_nub(x0=10, y0=10,
                                                height=80, nub_depth=-(2*x+10), nub_breadth=2*y+10,
                                                midpoint=50))
            outstream.write("</g>\n")
    outstream.write('</svg>\n')
