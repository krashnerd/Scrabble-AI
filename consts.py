import string
from dictionary_files.build_dictionary import get_dictionary
# points = {"A": 1, "B": 3, "C": 3, "D": 2, "E": 1, "F": 4, "G": 2, "H": 4, "I": 1, "J": 8, "K": 5, "L": 1, "M": 3, "N": 1, "O": 1, "P": 3, "Q": 10, "R": 1, "S": 1, "T": 1, "U": 1, "V": 4, "W": 4, "X": 8, "Y": 4, "Z": 10}

# distribution = [9,2,2,4,12,2,3,2,9,1,1,4,2,6,8,2,1,6,4,6,4,2,2,1,2,1]
letter_points_amount = [('A', 1, 9), ('B', 3, 2), ('C', 3, 2), ('D', 2, 4), ('E', 1, 12), ('F', 4, 2), ('G', 2, 3), ('H', 4, 2), ('I', 1, 9), ('J', 8, 1), ('K', 5, 1), ('L', 1, 4), ('M', 3, 2), ('N', 1, 6), ('O', 1, 8), ('P', 3, 2), ('Q', 10, 1), ('R', 1, 6), ('S', 1, 4), ('T', 1, 6), ('U', 1, 4), ('V', 4, 2), ('W', 4, 2), ('X', 8, 1), ('Y', 4, 2), ('Z', 10, 1)]
lookup_points_amount = {letter: (points, amount) for letter, points, amount in letter_points_amount}
points = {letter: points for letter, points, _ in letter_points_amount}

dictionary = get_dictionary("dictionary_files/dict.bytesIO")
# letter_info = [(letter, points[letter], distribution[ind]) for ind, letter in enumerate(string.ascii_uppercase)] 

# with open("temp.txt", "w") as outfile:
# 	outfile.write(str(letter_info))

