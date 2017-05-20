import sys
import re
import json
import csv
import requests
import argparse
from datetime import datetime


LOGIN_URL = "https://drafthouse.com/victory/sign-in"
HISTORY_URL = "https://drafthouse.com/austin/victory/history"

def write_csv(filename, data):
    keys = data[0].keys()
    with open(filename, 'wb') as output_file:
        dict_writer = csv.DictWriter(output_file, keys, delimiter=';')
        dict_writer.writeheader()
        dict_writer.writerows(data)

def get_csrf_token(content):
    print "Getting csrf token... ",
    csrf_regex = r'value="296".*name="csrf_token" value="(.*)" />'
    matches = re.search(csrf_regex, content, re.MULTILINE | re.DOTALL)
    if matches:
        token = matches.group(1)
        print "success"
        return token
    print  "failed"
    sys.exit(1)

def fetch_history(session, page_num):
    print "Fetching page {}... ".format(page_num),
    result = session.get("{}/P{}0".format(HISTORY_URL, page_num))
    regex = r'PosterList-heading">(.*?)</h2>.*?u-noMarginBot">(.*?)<br>(.*?)<br>.*?<p>(.*?)</p>.*?u-noPaddingBot">(.*?)<br>'
    matches = re.findall(regex, result.content, re.MULTILINE | re.DOTALL)
    history = []
    if matches:
        for purchase in matches:
            history.append({
                "film": purchase[0].strip(),
                "date": purchase[1].strip(),
                "time": purchase[2].strip(),
                "tickets": purchase[3].strip(),
                "location": purchase[4].strip(),
            })
    print "got {} status code. found {} items".format(result.status_code, len(history))
    return history

def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month

def get_current_visits(total_history):
    current = []
    now = datetime.now()
    next_month_rollover = 0
    for visit in total_history:
        as_date = datetime.strptime(visit["date"], "%A, %b %d %Y")
        diff = diff_month(now, as_date)
        if diff <= 12:
            current.append(visit)
        if diff == 12:
            next_month_rollover += 1
    return current, next_month_rollover

def scrape_history(email, password, csv):
    payload = {
        'email': email,
        'password': password,
        'ACT':296,
        'site_id': 1,
    }

    with requests.Session() as session:
        print "Fetching login page... ",
        result = session.get(LOGIN_URL)
        if result.status_code != 200:
            print "failed. Got {}".format(result.status_code)
            sys.exit(1)
        print "success"

        payload["csrf_token"] = get_csrf_token(result.content)

        print "Logging in... ",
        result = session.post(LOGIN_URL, data=payload)
        if result.status_code != 200:
            print "failed. Got {}".format(result.status_code)
            sys.exit(1)
        print "success"

        valid_page = True
        page_num = 0
        total_history = []
        while valid_page:
            history = fetch_history(session, page_num)
            if history:
                total_history.extend(history)
                page_num += 1
            else:
                valid_page = False

        # print json.dumps(total_history, indent=4, sort_keys=True)
        print
        print "Total Visits: {}".format(len(total_history))
        current_visits, next_month_rollover = get_current_visits(total_history)
        print "Current Visits: {}".format(len(current_visits))
        print "Amount rolling off at the end of the month: {}".format(next_month_rollover)

        write_csv(csv, total_history)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape drafthouse order history')
    parser.add_argument('email', help='Victory email address')
    parser.add_argument('password', help='Victory password')
    parser.add_argument('--csv', default="purchase_history.csv", help='Filename for csv output')
    args = parser.parse_args()
    scrape_history(args.email, args.password, args.csv)
