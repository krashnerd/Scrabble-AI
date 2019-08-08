""" Parsing JSON file and making DAWG """
import time, zlib, json
from base64 import b64encode, b64decode
import pickle
def check_word(word, start):
    if(word[-1] != "$"):
        word += "$"
    curr = start
    for letter in word:
        if letter not in curr or curr[letter] is None:
            return False
        # if letter not in curr or curr[letter] is None:
        #     return False
        curr = curr[letter]
    return True

def uncompress_string(data):
    try:
        j = zlib.decompress(b64decode(data))
    except:
        raise RuntimeError("Could not decode/unzip the contents")
    return j.decode('ascii').replace("\\", "")



def pickle_dawg(infile = "dictionary.json", outfile = "Alphadict.bytesIO"):
    file = open(infile)
    data = file.read()
    file.close()

    data = json.loads(data)

    dawg_nodes = [AlphaDict.AlphaDict() for _ in range(len(data))]

    for idx, node in enumerate(data):
        for path in node['paths']:
            for key in path.keys():
                dawg_nodes[idx][key] = dawg_nodes[path[key]]

    # size = sum([sys.getsizeof(node) for node in dawg_nodes])
    # print("Size:", size)
    with open(outfile, "wb") as file:
        pickle.dump(dawg_nodes, file)

    return dawg_nodes[0]

def get_dictionary(filename = "dict.bytesIO"):
    with open(filename, "rb") as dictfile:
        dawg = pickle.load(dictfile)

    return dawg[0]

def main():
    d1 = get_dictionary("dict.bytesIO")
    d2 = get_dictionary("Alphadict.bytesIO")
    inp = None
    print("Input a word to check in the dictionary, or input 'Q' to quit")
    while inp != "Q":
        if inp is not None:

            t1 = time.time()
            is_word = check_word(inp, d1)
            t2 = time.time()

            mic_seconds = int((t2 - t1) * 1000000)
            print("Time: %d microseconds\n%s is%s a word!\n" % (mic_seconds, inp, "" if is_word else " not"))
        inp = input("Word: ").upper()
    


if __name__ == '__main__':
    main()