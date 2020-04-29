#!/usr/bin/env python3

import json
import re
import requests

known_urls = []
repos = []

USERNAME = 'incanus'

STORE = './data/github_stars.json'

PER_PAGE = 100
URL = 'https://api.github.com/users/' + USERNAME + '/starred?per_page=' + str(PER_PAGE)
HEADERS = {
    'Accept': 'application/vnd.github.v3.star+json'
}

def process_results(project_json):
    global known_urls, repos
    for project in project_json:
        try:
            hit = known_urls.index(project['repo']['html_url'])
            return False
        except:
            if project['repo']['private'] == False:
                repos.append({
                    'name': project['repo']['full_name'],
                    'description': project['repo']['description'],
                    'url': project['repo']['html_url'],
                    'date': project['starred_at']
                })
    return True

def get_next_url(headers):
    match = re.match('.*<(https.*)>; rel="next".*', headers['link'])
    return match.group(1) if match else None

try:
    with open(STORE) as f:
        repos = json.load(f)['projects']
        print(f"Loaded {len(repos)} existing projects")
        for project in repos:
            known_urls.append(project['url'])
except:
    pass

r = requests.get(URL, headers=HEADERS)

if r.status_code >= 200 and r.status_code < 300:
    all_new_results = process_results(r.json())
    print(f"Fetched {len(r.json())} ({len(repos)} now known)")
    next_url = get_next_url(r.headers)
    while next_url and all_new_results:
        r = requests.get(next_url, headers=HEADERS)
        if r.status_code >= 200 and r.status_code < 300:
            all_new_results = process_results(r.json())
            print(f"Fetched {len(r.json())} ({len(repos)} now known)")
            next_url = get_next_url(r.headers)
    sorted_repos = sorted(repos, key=lambda k: k['date'], reverse=True)
    new_count = len(sorted_repos) - len(known_urls)
    if new_count:
        repos = json.dumps({'projects': sorted_repos}, indent=' ' * 4)
        with open(STORE, mode='w') as f:
            f.write(repos)
            print(f"Wrote {new_count} new projects")
    else:
        print('No new projects added')
else:
    print(f"API {r.status_code}")