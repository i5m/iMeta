import requests
from metaphor_python import Metaphor
import os


class MetaphorWrapper:

    def __init__(self):
        self.client = Metaphor(
            api_key = os.environ.get("METAPHOR_API_KEY")
        )

    @staticmethod
    def keyword_or_neural(query):

        page = requests.post("https://dashboard.metaphor.systems/api/keyword-or-neural", json = {
            "query": query
        }).json()

        return page["searchType"]
    
    def search(self, query):

        type_ = self.keyword_or_neural(query)

        response = self.client.search(
            query,
            num_results = 5,
            use_autoprompt = True,
            type = type_
        )

        # title: str
        # url: str
        # id: str
        # score: Optional[float] = None
        # published_date: Optional[str] = None
        # author: Optional[str] = None
        # extract: Optional[str] = None

        return response.results

    def get_content(self, ids):

        response = self.client.get_contents(ids)

        # id: str
        # url: str
        # title: str
        # extract: str

        return response.contents

