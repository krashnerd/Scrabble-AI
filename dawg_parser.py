""" Parsing JSON file and making DAWG """
import time, zlib, json
from base64 import b64encode, b64decode

def check_word(word, start):
    if(word[-1] != "$"):
        word += "$"
    curr = start
    for letter in word:
        if letter not in curr:
            return False
        curr = curr[letter]
    return True

def uncompress_string(data):
    try:
        j = zlib.decompress(b64decode(data))
    except:
        raise RuntimeError("Could not decode/unzip the contents")
    return j.decode('ascii').replace("\\", "")

def get_dawg(filename):
    file = open(filename)
    data = file.read()
    file.close()

    types = filename.split(".")
    if types[-1] == "zip64":
        data = uncompress_string(data)
        print(data[:50])

    data = json.loads(data)

    dawg_nodes = [dict() for _ in range(len(data))]


    for idx, node in enumerate(data):
        for path in node['paths']:
            for key in path.keys():
                dawg_nodes[idx][key] = dawg_nodes[path[key]]

    return dawg_nodes[0]

def main():
    dictionary = get_dawg("dictionary.json")
    inp = None
    print("Input a word to check in the dictionary, or input 'Q' to quit")
    while inp != "Q":
        if inp:
            t1 = time.time()
            is_word = check_word(inp, dictionary)
            t2 = time.time()
            mic_seconds = int((t2 - t1) * 1000000)
            print("Time: %d microseconds\n%s is%s a word!\n" % (mic_seconds, inp, "" if is_word else " not"))
        inp = input("Word: ").upper()

def read(filename):
    pass
    


if __name__ == '__main__':
    main()