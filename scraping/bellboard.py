#!/usr/bin/env python3

import os
from collections import defaultdict, namedtuple

from bs4 import BeautifulSoup

with open(os.path.expanduser("~/Downloads/BellBoard-Cambridge-sample.html")) as pagestream:
    soup = BeautifulSoup(pagestream, "lxml")
    performances = soup.find('table', id='performances')
    by_date = defaultdict(list)
    for performance in performances.tbody:
        when = performance.find(class_='date').text
        where = performance.find(class_='place')
        link = where.a['href']
        what = performance.find(class_='title').text
        print("on", when, "at", where.text, "they rang", what, "see", link)
