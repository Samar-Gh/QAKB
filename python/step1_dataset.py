import json
import requests

from parsing.lc_quad import LC_Qaud
from parsing.lc_quad2 import LC_Qaud2
from parsing.qald import Qald

# Chose data file
data_path = "QALD/8/wikidata"
# data_path = "QALD/8"
# data_path = "QALD/9"
# data_path = "LC-QUAD"
# data_path = "LC-QUAD2"


def prepare_dataset(ds):
    ds.load()
    ds.parse()
    return ds


def ask_query(uri):
    if uri == "<https://www.w3.org/1999/02/22-rdf-syntax-ns#type>":
        return 200, json.loads("{\"boolean\": \"True\"}")
    uri = uri.replace("https://", "http://")
    return query(u'ASK WHERE {{ {} ?u ?x }}'.format(uri))


def query(q):
    q = q.replace("https://", "http://")
    payload = (
        ('query', q),
        ('format', 'application/json'))

    r = requests.get('http://dbpedia.org/sparql', params=payload)
    return r.status_code, r.json()


def has_answer(t):
    if "results" in t and len(t["results"]["bindings"]) > 0:
        return True
    if "boolean" in t:
        return True
    return False


if __name__ == "__main__":
    # opening train dataset
    if data_path == "QALD/8/wikidata":
        with open('data/' + data_path + '/wikidata-train-7.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        print('data len: ', len(data["questions"]))
    else:
        with open('data/' + data_path + '/train-data.json', 'r', encoding='utf-8') as f:
            train = json.load(f)

        with open('data/' + data_path + '/test-data.json', 'r', encoding='utf-8') as f:
            test = json.load(f)

        # total data
        if data_path == "QALD/8":
            data = train["questions"] + test["questions"]
        else:
            data = train + test
        print('data len: ', len(data))

    # saving total data
    with open("data/" + data_path + "/data.json", "w") as write_file:
        json.dump(data, write_file)

    if data_path == "QALD/8/wikidata":
        ds = Qald(path="./data/" + data_path + "/data.json")
    elif data_path == "LC-QUAD2":
        ds = LC_Qaud2(path="./data/" + data_path + "/data.json")
    else:
        ds = LC_Qaud(path="./data/" + data_path + "/data.json")

    tmp = []
    for qapair in prepare_dataset(ds).qapairs:
        raw_row = dict()
        raw_row["id"] = qapair.id.__str__()
        raw_row["question"] = qapair.question.text
        raw_row["sparql_query"] = qapair.sparql.query
        try:
            r = query(qapair.sparql.query)
            raw_row["answers"] = r[1]
        except Exception as e:
            raw_row["answers"] = []

        tmp.append(raw_row)

    with open('data/' + data_path + '/linked_answer.json', 'w') as jsonFile:
        json.dump(tmp, jsonFile)

    print('data len: ', len(tmp))
