import json
import warnings


def write(lst, filename='out', encoding="utf-8"):  # write list to textfile line by line
    if type(lst) is dict:
        filename = filename + '.json'
    else:
        filename = filename + '.txt'
    with open(filename, 'w', encoding=encoding) as fp:
        if type(lst) is list:
            fp.write(str('\n'.join(map(str, lst))))
        elif type(lst) is dict:
            fp.write(json.dumps(lst))
        elif type(lst) is str:
            fp.write(lst)
        else:
            warnings.warn("object not recognised!")
            fp.write(str(lst))
        # fp.write(str(words))
    print('Wrote to "' + filename + '"')


def read(filename, encoding="utf-8"):
    with open(filename, encoding=encoding) as f:
        return f.readlines()


def read_json(filename='example.json', encoding="utf-8"):
    with open(filename, 'r', encoding=encoding) as f:
        return json.load(f)


def write_json(obj, filename="out.json", encoding="utf-8"):
    with open(filename, "w", encoding=encoding) as outfile:
        json.dump(obj, outfile)
