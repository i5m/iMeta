import requests


class WikiImagesWrapper:

    def __init__(self):
        self.url = "https://en.wikipedia.org/w/api.php"

    def get_links(self, fl):

        params = {
            "action": "query",
            "format": "json",
            "titles": fl,
            "prop": "imageinfo",
            "iiprop": "url"
        }

        page = requests.get(url = self.url, params = params)
        data = page.json()

        try:
            return data["query"]["pages"]["-1"]["imageinfo"][0]["url"]
        except:
            return ''

    def get_images(self, q):

        params = {
            "action": "query",
            "format": "json",
            "titles": q,
            "prop": "imageinfo|pageimages|images"
        }

        page = requests.get(url = self.url, params = params)
        data = page.json()

        images = []

        for i in data['query']['pages']:

            try:
                images.append(data['query']['pages'][i]["thumbnail"]["source"])
            except:
                pass

            try:
                for j in data['query']['pages'][i]["images"]:
                    lnk = self.get_links(j["title"])
                    if lnk != '':
                        images.append(lnk)
            except:
                pass

        return images

