import requests
import json

class Item:

    def __init__(self, row, helper):
        self.id = row["item"]
        self.serie = row["serie"]
        self.omroepen = row["omroepen"]
        self.makers = row["makers"]
        self.titel = row["titel"]
        self.omschrijving = row["omschrijving"]
        self.genres = row["genres"]

        self.url = 'https://query.wikidata.org/sparql'
        self.helper = helper

    def get_maker_data(self):
        count = 0
        data = []
        for maker in self.makers:
            try:
                name = maker['given_name'] + " " + maker["family_name"]
                if name not in self.helper.known_persons or self.helper.known_persons[name] == []:
                    output = self.query(name)
                    self.helper.known_persons[name] = output
                    if count % 10 == 0:
                        self.helper.write_to_json('data/known_persons.json', self.helper.known_persons)
                        count += 1
                data.append(self.helper.known_persons[name])
            except TypeError:
                pass
        return data

    def execute_query(self, query):
        """
        Sends a SPARQL query to Wikidata.
        TO DO: Write tests
        """
        try:
            r = requests.get(self.url, params={'format': 'json', 'query': query})
            return r
        except (ConnectionAbortedError, ConnectionError):
            return ConnectionError

    def read_person_response_list(self, response):
        """
        Attempt to retrieve values for each of the value types relevant for people data.
        Leaves value empty in case Wikidata has no information about it.
        """
        try:
            data = response.json()
            occupations = self.read_response(data, 'occupations')
            party = self.read_response(data, 'party')
            positions = self.read_response(data, 'position')
            gender = self.read_response(data, 'gender')
            citizen = self.read_response(data, 'citizen')
            ethnicity = self.read_response(data, 'ethnicity')
            place_of_birth = self.read_response(data, 'place_of_birth')
            sexuality = self.read_response(data, 'sexuality')

            return {'gender': gender, 'occupations': occupations,
                    'party': party, 'positions': positions, 'citizen': citizen, 'ethnicity': ethnicity,
                    'sexuality': sexuality, 'place_of_birth': place_of_birth}
        except json.decoder.JSONDecodeError:
            return []
        except IndexError:
            return []

    @staticmethod
    def read_response(data, label):
        """
        Returns all unique values for a particular label.
        Lowercases occupation data, which is relevant when returning results in English
        """
        output = []
        for x in data['results']['bindings']:
            if label in x:
                if label == 'occupations':
                    output.append(x[label]['value'].lower())
                else:
                    output.append(x[label]['value'])
        return list(set(output))

    def query(self, label):
        try:
            query = """
                SELECT DISTINCT ?s ?occupations ?party ?position ?gender ?citizen ?ethnicity ?place_of_birth ?sexuality WHERE { 
                ?s ?label '""" + label + """'@nl .
              OPTIONAL {
                ?s wdt:P106 ?c .
                ?c rdfs:label ?occupations .
                FILTER(LANG(?occupations) = "" || LANGMATCHES(LANG(?occupations), "en"))
              }
              OPTIONAL {
                ?s wdt:P102 ?d .
                ?d rdfs:label ?party .
                FILTER(LANG(?party) = "" || LANGMATCHES(LANG(?party), "nl"))
              }
              OPTIONAL {
                ?s wdt:P39 ?e .
                ?e rdfs:label ?position .
                FILTER(LANG(?position) = "" || LANGMATCHES(LANG(?position), "en"))
              }
              OPTIONAL {
                ?s wdt:P21 ?f .
                ?f rdfs:label ?gender .
                FILTER(LANG(?gender) = "" || LANGMATCHES(LANG(?gender), "en"))
              }
              OPTIONAL {
                   ?s wdt:P172 ?g . 
                   ?g rdfs:label ?ethnicity .
                   FILTER(LANG(?ethnicity) = "" || LANGMATCHES(LANG(?ethnicity), "en"))
                }
               OPTIONAL {
                   ?s wdt:P19 ?pb . 
                   ?pb wdt:P17 ?country .
                   ?country rdfs:label ?place_of_birth .
                   FILTER(LANG(?place_of_birth) = "" || LANGMATCHES(LANG(?place_of_birth), "en"))
                }
              OPTIONAL {
                ?s wdt:P27 ?h .
                ?h rdfs:label ?citizen
                FILTER(LANG(?citizen) = "" || LANGMATCHES(LANG(?citizen), "en"))
                }
               OPTIONAL {
                ?s wdt:P91 ?i .
                ?i rdfs:label ?sexuality
                FILTER(LANG(?sexuality) = "" || LANGMATCHES(LANG(?sexuality), "en"))
                }
            }"""
            r = self.execute_query(query)
            return self.read_person_response_list(r)
        except (ConnectionAbortedError, requests.exceptions.ChunkedEncodingError):  # in case the connection fails
            return []
