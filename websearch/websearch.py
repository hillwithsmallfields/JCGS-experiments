#!/usr/bin/env python3

import requests
from search_engines import bing_search

def websearch_main():
    search_url = bing_search.get_search_url("archbishop sarah")
    resp = requests.get(search_url)
    if resp.status_code == 200:
        results, next_page_url = bing_search.extract_search_results(resp.text, search_url)
        if not(any(results)):
            print("all results were empty")
            print("raw result text:", resp.text)
        print("got", len(results), "results:")
        for index, item in enumerate(results):
            print("  ", index)
            for k in sorted(item.keys()):
                print("    ", k, item[k])
    else:
        print("got status code", resp.status_code)

if __name__ == "__main__":
    websearch_main()
