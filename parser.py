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
    
    #csv
    writer = csv.writer(open("github-colors.csv", "w"))
    for key, value in output.items():
        writer.writerow([key, value])

if __name__ == "__main__":
    main()
