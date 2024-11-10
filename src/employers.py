class Employer:
    employers = []
    __slots__ = ("id", "name", "url")

    def __init__(self, id_, name, url):
        self.id = id_
        self.name = name
        self.url = url
        self.employers.append(self)
