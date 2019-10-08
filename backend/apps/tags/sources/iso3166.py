from pycountry import countries

from . import BaseSource


def get_country(ref):
    return countries.get(alpha_3=ref)


class Source(BaseSource):

    def country_to_output(self, country):
        return self.get_value(country.alpha_3), country.name

    def get_all(self):
        return map(self.country_to_output, countries)

    def get(self, ref):
        return self.country_to_output(get_country(ref))

    def search(self, query):
        return map(self.country_to_output, countries.search_fuzzy(query))

