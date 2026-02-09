#!/usr/bin/env python3

"""Fetch performances from BellBoard.

Not actually needed, as there's a CSV download available, but it was a
handy exercise in reminding myself of how to use BeautifulSoup.

"""

import os
import datetime
from collections import defaultdict, namedtuple

import requests
from bs4 import BeautifulSoup

Performance = namedtuple('Performance', ['when', 'where', 'what', 'link'])

def parse_performance_list(data):
    soup = BeautifulSoup(data, "lxml")
    performances = soup.find('table', id='performances')
    by_date = defaultdict(list)
    for performance in performances:
        when = datetime.datetime.strptime(performance.find(class_='date').text, "%A, %d %B %Y").date().isoformat()
        where = performance.find(class_='place')
        link = where.a['href']
        what = performance.find(class_='title').text
        by_date[when].append(Performance(
            when=when,
            where=where.text,
            what=performance.find(class_='title').text,
            link=where.a['href']))
    return by_date

def parse_performance_list_file(filename):
    with open(os.path.expanduser(filename)) as pagestream:
        return parse_performance_list(pagestream)

def get_recent_performances(placename):
    response = requests.get("https://bb.ringingworld.co.uk/search.php", {'place': placename})
    return (parse_performance_list(str(response.content))
            if response.status_code == 200
            else None)

c = get_recent_performances("Histon")

for datestring, perf in c.items():
    print(datestring, perf)
