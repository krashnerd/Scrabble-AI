import zlib, json
from base64 import b64encode, b64decode


with open("dictionary.json", "r") as dictfile:
	j = dictfile.read()
	print("old length:", len(j))
	encoded_str = b64encode(
            zlib.compress(
                json.dumps(j).encode('utf-8')
            )
        ).decode('ascii')
	print("new length:", len(encoded_str))

with open("dictionary.json.zip", "w") as compressedfile:
	compressedfile.write(encoded_str)





