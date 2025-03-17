def process_data(document):
    document["results"] = document["results"][:-1]
    return document
