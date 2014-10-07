import json

import yaml
import requests


url = 'https://raw.githubusercontent.com/github/linguist/master/lib/linguist/languages.yml'


def main():
    response = requests.get(url, stream=True)
    if not response.ok:
        print "Are you sure the url [%s] is right?" % url

    raw = ""
    for block in response.iter_content(1024):
        if not block:
            break
        raw += block

    languages = yaml.load(raw)
    output = {}

    for key, value in languages.iteritems():
        try:
            output[key] = value['color']
        except KeyError:
            continue

    open("github-colors.json", "w").write(json.dumps(output, indent=4))


if __name__ == "__main__":
    main()