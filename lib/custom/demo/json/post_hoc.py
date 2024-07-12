def process_data(document):
    document["prop_c"] = document["prop_a"] + document["prop_b"]
    return document
