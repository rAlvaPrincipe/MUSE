import wikipediaapi

class WikiCategory:
    _id = ""
    status = ""

    def __init__(self, page: wikipediaapi.WikipediaPage, status):
        self._id = page.fullurl
        self.status = status

    def __eq__(self, other):
        if not isinstance(other, WikiCategory):
            return NotImplemented
        return self._id == other._id

    def __hash__(self):
        return hash(self._id)

    def __str__(self):
        return self._id
