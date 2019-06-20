import string
from functools import reduce
from pathlib import Path
# EOF = dawg_node(True);
import json
counter = 0
class dawg_node():
    """ Node of a Directed-Acyclic Word Graph, to be used for Scrabble AI"""
    def __init__(self, root, isEOF=False):
        self._paths = {}
        self._followers = [False] * 27
        self._parents = []
        self._root = root
        self._str = ''
        self._string_updated = True

        self._all_list_location = 0
        self.valid_paths = lambda:list(filter(
            lambda x: x in self._paths, (list(string.ascii_uppercase) + ['$'])))
            # self._words_count_found = []

        self._num_words_test_counter = 0

        #Is this node terminal?
        self.term = isEOF     

    def add_parent(self, parent):
        self._parents.append(parent)

    def finalize(self):
        #Switching to a lazy evaluation
        finalized_paths = self.valid_paths()
        self.valid_paths = lambda:finalized_paths

    def path_location(self, path):
        """ Returns the index in all_list of the node that a given character path leads to"""
        return self._paths[path]._all_list_location

    def update_location(self, index):
        # Sets the marker for where it is in the list of all nodex.
        # Will be used to make an easily parseable string representation
        self._all_list_location = index

    def wordcount_test_increment(self):
        self._num_words_test_counter += 1

    def json(self):
        pass


    # def valid_paths(self):
    #   return filter(lambda x: x in self._paths, (list(string.ascii_uppercase) + ['$']))

    def add_node(self, letter):
        #Adds a new node where needed
        self._paths[letter]=dawg_node(self._root)

    def increment_counter(self):
        self._root.size_counter += 1

    def count_words(self, parentStr = ""):
        #Counts the number of possible words that can be made from a given node. Recursive.

        # List of the child nodes' word counts
        
        children_wordcount = reduce((lambda a,b: a+b), 
                list(map(lambda path: self._paths[path].count_words(parentStr + path), 
                    self.valid_paths())) + [0])

        if '$' in self._paths:
            # self.count_found(parentStr)
            return 1 + children_wordcount
        else: 
            return children_wordcount

    def all_words(self):
        return [x + y for y in self._paths[x].all_words() for x in self._valid_paths()]
        # result = [first_letter + for first_letter in self._valid_paths()]
        # for letter in self._valid_paths:


    def add_word(self, word):
        if word == '':
            letter = '$'
        else:
            letter = word[0]

        if letter not in self._paths:
            self.increment_counter()
            self._paths[letter] = dawg_node(self._root)
            self._paths[letter].add_parent(self)        
            self._root._all_nodes.append(self._paths[letter])

        if len(word) > 0:
            self._paths[letter].add_word(word[1:])

        # 
        self._string_updated = False

    def has_path(self, letter):
        return (letter in self._paths)

    def contains_node(self, other):
        if(self == other):
            return False
        for node in self.valid_paths():
            if self._paths[node].contains_node(other):
                return False
        return True
    def contains(self, word):

        #if the word is empty, return true iff the node contains EOS marker
        if(word == ''):
            return '$' in self._paths

        #if the first letter of the word can't go anywhere, return false
        if word[0] not in self._paths:
            return False

        return self._paths[word[0]].contains(word[1:])

    def __ne__(self,other):
        return not (self==other)

    def __eq__(self, other):
        return str(self)==str(other)

    def prettyprint(self, offset = 0):
        #Pretty printing
        #Offset all but the first permutation by 'offset' spaces
        lst_perms = [" " + path  + self._paths[path].prettyprint(offset + 1) for path in self.valid_paths()]
        lst_perms = list(filter(lambda x: x.strip() != "$",lst_perms))
        return ("\n"+"  " * (offset)).join(lst_perms)


    # def __str__(self):
    #   result = ""
    #   for follower in self._valid+paths

    def __str__(self):
        if(self._string_updated):
            return self._str
        result = ""
        valid_paths =list(self.valid_paths())
        if len(valid_paths) == 0:
            return ''
        if(len(valid_paths) == 1):
            result += valid_paths[0] + str(self._paths[valid_paths[0]])
        else:
            result += "("
            for follower in valid_paths:
                if follower == "$":
                    result += "$"
                else: 
                    result += follower + str(self._paths[follower])
                result += "|"
            result = result[:-1] + ")"

        #set string and flags
        self._str = result
        self._string_updated = True
        return result


class Dawg(dawg_node):
    def __init__(self):
        dawg_node.__init__(self, self)
        self.size_counter = 1
        self._root = self
        self._all_nodes = [self]

    def construct_dawg(self, word_list):
        self.add_words(word_list)
        #self.finalize_paths()
        self.update_indices()
        self.remove_dupes()
        self.update_indices()

    def finalize_paths(self):
        # Updates self.valid_paths function to return a definite string instead of filtering
        for node in self._all_nodes:
            node.finalize()


    def update_indices(self, start = 0):
        for node_index in range(start, len(self._all_nodes)):
            self._all_nodes[node_index].update_location(node_index)

    def test_export(self, filename):

        #adding .dwg extension to filename if it isn't already there
        if len(filename) < 4 or filename[-4:] != ".dwg":
            filename = filename + ".dwg"

        out_file = Path(filename)
        # if(out_file.is_file()):
        #   confirm = input("Overwrite %s y/n?" % filename)
        #   if(confirm.lower() != "y"):
        #       return

        f = open(filename,'w')
        f.write("%d\r\n" % len(self._all_nodes))
        for node in self._all_nodes:
            path_lst = []
            for path in node.valid_paths():
                path_lst.append("%s:%d" % (path, node.path_location(path)))
            str1 = "%d   %s" % (node._all_list_location, ",".join(path_lst))
            str1 += " " * (50 - len(str1))
            str1 += "%s\r\n" % str(node)

            f.write(str1)

    def json_export(self):
        filename = input("filename?")
        if len(filename) < 4 or filename[-4:] != ".json":
            filename = filename + ".json"

        all_attr = lambda d_node: {'len':len(d_node.valid_paths()), 'paths':[{path: d_node._paths[path]._all_list_location} for path in d_node.valid_paths()]}
        return json.dumps([all_attr(node) for node in self._all_nodes],separators=(',', ':'))




        

    def remove_dupes(self):
        
        """ Get rid of duplicate nodes by iterating through list of all nodes. 
        Time inefficient but it's a one time thing."""

        def get_path(child, parent = None):
            """Returns the letter of the child's parent that paths the 
            parent to the child"""
            
            if(parent == None): 
                parent = child._parents[0]

            for letter in parent.valid_paths():
                if(parent._paths[letter] is child):
                    return letter

        num_nodes = len(self._all_nodes)
        original_node = 0
        # Want to go to the second-to-last node, since by the time 
        # it gets to the last node that one must be unique
        while(original_node < num_nodes - 1):
            print("\rOn node %d of %d, %0.2f%% complete %s" % (original_node + 1, num_nodes, (100*original_node/num_nodes), (" " * 20)), end = '')
            dupe_node_indices = []

            # Generate a list of all the indices of duplicate nodes.
            for possible_dupe_index in range(original_node + 1, num_nodes):
                
                if self._all_nodes[original_node] == self._all_nodes[possible_dupe_index]:
                    dupe_node_indices.append(possible_dupe_index)
                    assert(self._all_nodes[original_node] is not self._all_nodes[possible_dupe_index])

            num_dupes = len(dupe_node_indices)

            for offset in range(num_dupes):

                #Because the nodes are getting removed from the list, have to subtract offset
                dupe_node_index = dupe_node_indices[offset] - offset

                dead = self._all_nodes[dupe_node_index]

                parent = dead._parents[0]
                
                path = get_path(dead, parent)
                
                #Instead of pointing to dupe node, points to original node
                parent._paths[path] = self._all_nodes[original_node]
                self._all_nodes[original_node].add_parent(parent)
                self._all_nodes.pop(dupe_node_index)

            num_nodes -= num_dupes
            original_node += 1
        print("\ncomplete %s\n" % (" " * 60))

    def add_words(self, word_list):
        for word in word_list:
            self.add_word(word) 

                #for parent in self._all_nodes[dupe_node_index]:

            # num_nodes -= 1
        


