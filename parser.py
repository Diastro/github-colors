import re
import csv
import json
import unicodedata

import yaml
import requests


url = 'https://raw.githubusercontent.com/github/linguist/master/lib/linguist/languages.yml'

def slugify(str):
    # From <http://yashchandra.com/2014/05/08/how-to-generate-clean-url-or-a-slug-in-python/>
    slug = unicodedata.normalize("NFKD",unicode(str)).encode("ascii", "ignore")
    slug = re.sub(r"[^\w]+", " ", slug)
    slug = "-".join(slug.lower().strip().split())
    return slug

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
    
    # less.js
    with open("github-colors.less", 'w') as f:
        for key, value in output.items():
            f.write('@github-color-%s: %s;\n' % (slugify(key), value.upper()))
    
    # sass
    with open("github-colors.scss", 'w') as f:
        for key, value in output.items():
            f.write('$github-color-%s: %s;\n' % (slugify(key), value.upper()))

    # json
    with open("github-colors.json", 'w') as f:
        f.write(json.dumps(output, indent=4))
    
    # csv
    writer = csv.writer(open("github-colors.csv", "w"))
    writer.writerow(["language", "color"])
    for key, value in output.items():
        writer.writerow([key, value])
    
    # colors
    # insipired by : https://github.com/ozh/github-colors [which isn't being updated]
    with open("colors.md", "w") as f:
        for key, value in output.items():
            f.write("[![](http://www.placehold.it/150/" + value.replace("#", "") + "/ffffff&text=" + key + ")](https://github.com/trending?l=" + key + ")")

if __name__ == "__main__":
    main()
