#!/usr/bin/env python3

import json
import os
import random
import shutil
import sqlite3
import urllib.parse

SAMPLE_SIZE_WHILE_EXPERIMENTING = 0

LEAVE_ALONE = set(['yes', 'no', 'OPTOUT', 'true', 'false'])

def scrambled_value(original):
    """Scramble one cookie value element."""
    if isinstance(original, list):
        return [scrambled_value(elt) for elt in original]
    if isinstance(original, int):
        return original + random.randint(-42, 42)
    if not isinstance(original, str):
        return original
    if original in LEAVE_ALONE:
        return original
    for separator in ('-', ':', '.', '/', '&'):
        if separator in original:
            parts = original.split(separator)
            return separator.join(
                [parts[0]]      # the first part often looks like a key, so increase chance of confusion by leaving it alone
                + [scrambled_value(o) for o in parts[1:]])
    chars = list(original)
    random.shuffle(chars)
    return "".join(chars)

def remix_cookie(cookie_text):
    """Scramble a cookie, handling JSON cookies piece-by-piece."""
    if cookie_text.startswith("{") and cookie_text.endswith("}"):
        try:
            cookie_dict = json.loads(cookie_text)
        except:
            print("cookie in curly brackets but not JSON:", cookie_text)
            return scrambled_value(cookie_text)
        return json.dumps({k: scrambled_value(v) for k, v in cookie_dict.items()})
    return scrambled_value(cookie_text)

def crumbler_main():
    """Mix up cookies in your Firefox cookie database.

    Currently works on a copy of the database, while I'm working on it."""
    with open(os.path.expanduser("~/.cookie-safe-sites")) as safe:
        cookie_safe_sites = set(site.strip() for site in safe.readlines())
    cookie_tmp = "/tmp/cookies.sqlite"
    shutil.copy(os.path.expanduser("~/.mozilla/firefox/xvl9uxy0.default-esr/cookies.sqlite"), cookie_tmp)
    connection = sqlite3.connect(cookie_tmp)
    connection.row_factory = lambda cursor, row: {col[0] : row[i] for i,col in enumerate(cursor.description)}
    cursor = connection.cursor()
    # cursor.execute("SELECT * FROM sqlite_master WHERE type='table' AND name='moz_cookies';")
    cursor.execute("SELECT host, name, value from moz_cookies;")
    i = SAMPLE_SIZE_WHILE_EXPERIMENTING
    for row in cursor.fetchall():
        host = row['host']      # TODO: strip down to basic site name, for fast comparison with safe list
        host = host.removeprefix("www.").removeprefix(".")
        if host in cookie_safe_sites:
            continue
        name = row['name']      # TODO: handle "CookieConsent" specially
        if name in ("cookies_policy", "cookies_preferences_set", "CookieConsent"):
            pass
        else:
            old_value = urllib.parse.unquote(row['value'])
            new_value = remix_cookie(old_value)
            print("for", host, "remixed", name, "from", old_value, "to", new_value)
            # https://www.geeksforgeeks.org/python/python-sqlite-update-data/
            new_value = urllib.parse.quote(new_value)
            i -= 1
            if i == 0:
                break

    cursor.close()
    connection.close()

if __name__ == "__main__":
    crumbler_main()
