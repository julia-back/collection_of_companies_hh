from re import sub


class Vacancy:
    vacancies = []
    __slots__ = ("id_", "name", "area", "salary_from", "salary_to", "currency",
                 "address", "url", "responsibility", "experience")

    def __init__(self, id_, name, area, salary_from, salary_to, currency, url, responsibility, experience):
        """Метод инизиализации объектов класса"""
        self.id_ = id_
        self.name = name
        self.area = area
        self.salary_from = salary_from if salary_from is not None else 0
        self.salary_to = salary_to if salary_to is not None else 0
        self.currency = currency if currency is not None else "RUR"
        self.url = url
        self.responsibility = sub(r"<([a-z]|/)+>", "", responsibility) \
            if responsibility is not None else responsibility
        self.experience = experience
