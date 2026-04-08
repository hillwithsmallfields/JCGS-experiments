#!/usr/bin/env python3

import googlesearch

def googlesearch_main():
    results = googlesearch.search("archbishop sarah")
    for r in results:
        print("   ", r)

if __name__ == "__main__":
    googlesearch_main()
