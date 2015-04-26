import csv
import json

import yaml
import requests


url = 'https://raw.githubusercontent.com/github/linguist/master/lib/linguist/languages.yml'


def main():
    response = requests.get(url, stream=True)
    if not response.ok:
        print "Are you sure the url [%s] is right?" % url

    languages = yaml.load(response.text)
    output = {}

    for key, value in languages.iteritems():
        try:
            output[key] = value['color']
        except KeyError:
            continue

    # json
    open("github-colors.json", "w").write(json.dumps(output, indent=4))

    # csv
    writer = csv.writer(open("github-colors.csv", "w"))
    writer.writerow(["language", "color"])
    for key, value in output.items():
        writer.writerow([key, value])

    # colors
    # insipired by : https://github.com/ozh/github-colors [which isn't being updated]
    f = open("colors.md", "w")
    for key, value in output.items():
        f.write("[![](http://www.placehold.it/150/" + value.replace("#", "") + "/ffffff&text=" + key + ")](https://github.com/trending?l=" + key + ")")
if __name__ == "__main__":
    main()
