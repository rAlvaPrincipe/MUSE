import wikipediaapi


class WikiArtist:
    _id = ""
    label = ""
    label_ext = ""
    text = ""
    linked = bool
    linked_inflooenz = bool
    linked_patterns = bool
    linked_ML = bool

    def __init__(self, page: wikipediaapi.WikipediaPage):
        self._id = page.fullurl
        self.label_ext = page.title
        self.text = page.text
        p_title = page.title
        if p_title[-1] == ')':
            index = p_title.rfind(" (")
            self.label = p_title[:index]
        else:
            self.label = p_title
        self.linked = False
        self.linked_inflooenz = False
        self.linked_patterns = False
        self.ML = False

    def __eq__(self, other):
        if not isinstance(other, WikiArtist):
            return NotImplemented
        return self._id == other._id

    def __hash__(self):
        return hash(self._id)

    def __str__(self):
        return self._id
