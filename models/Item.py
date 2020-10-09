class Item:

    def __init__(self, row):
        self.id = row["item"]
        self.serie = row["serie"]
        self.omroepen = row["omroepen"]
        self.makers = row["makers"]
        self.titel = row["titel"]
        self.omschrijving = row["omschrijving"]
        self.genres = row["genres"]
