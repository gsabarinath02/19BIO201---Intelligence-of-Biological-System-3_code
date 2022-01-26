from math import inf


def longestCommonSubstring(s, t):
    """Return the length of the longest substring that appears in both s and t.
    This function builds a suffix tree of a combination of s and t using
    Ukkonen's algorithm. It assumes that the symbols $ and # appear in neither s
    nor t.
    """

    len_s = len(s)
    string = s + '#' + t + '$'
    len_string = len(string)
    max_len = 0

    class LeafNode():

        def __init__(self, from_first_word):
            self.from_first_word = from_first_word

        @property
        def has_s_leaves(self):
            return self.from_first_word

        @property
        def has_t_leaves(self):
            return not self.from_first_word

    class InternalNode():

        def __init__(self, root_length):
            self.edges = {}  # dictionary of edges keyed by first letter of edge
            self.link = None
            self.root_length = root_length
            self.has_s_leaves = False
            self.has_t_leaves = False
            self.already_counted = False

        def __getitem__(self, key):
            return self.edges[key]

        def __setitem__(self, key, edge):
            self.edges[key] = edge
            # Update leaf identity based on new child leaves
            # Using "or" is faster than "|=" (I guess |= doesn't short circuit)
            self.has_s_leaves = self.has_s_leaves or edge.dest.has_s_leaves
            self.has_t_leaves = self.has_t_leaves or edge.dest.has_t_leaves

        def __contains__(self, key):
            return key in self.edges

    class Edge():

        def __init__(self, dest, start, end):
            self.dest = dest
            self.start = start
            self.end = end
            self.length = self.end - self.start

    root = InternalNode(0)

    class Cursor:

        def __init__(self):
            self.node = root
            self.edge = None
            self.idx = 0
            self.lag = -1

        def is_followed_by(self, letter):
            if self.idx == 0:
                return letter in self.node
            return letter == string[self.node[self.edge].start + self.idx]

        def defer(self, letter):
            """When we defer the insertion of a letter,
            we need to advance the cursor one position.
            """
            self.idx += 1
            # We never want to leave the cursor at the end of an explicit edge.
            # If this is the case, move it to the beginning of the next edge.
            if self.edge is None:
                self.edge = letter
            edge = self.node[self.edge]
            if self.idx == edge.length:
                self.node = edge.dest
                self.edge = None
                self.idx = 0

        def post_insert(self, i):
            """When we are finished inserting a letter, we can pop
            it off the front of our queue and prepare the cursor for the
            next letter.
            """
            self.lag -= 1
            # Only when the current node is the root is the first letter (which
            # we must remove) part of the cursor edge and index. Otherwise it is
            # implicitly determined by the current node.
            if self.node is root:
                if self.idx > 1:
                    self.edge = string[i - self.lag]
                    self.idx -= 1
                else:
                    self.idx = 0
                    self.edge = None
            # Following an insert, we move the active node to the node
            # linked from our current active_node or root if there is none.
            self.node = self.node.link if self.node.link else root
            # When following a suffix link, even to root, it is possible to
            # end up with a cursor index that points past the end of the current
            # edge. When that happens, follow the edges to a valid cursor
            # position. Note that self.idx might be zero and self.edge None.
            while self.edge and self.idx >= self.node[self.edge].length:
                edge = self.node[self.edge]
                self.node = edge.dest
                if self.idx == edge.length:
                    self.idx = 0
                    self.edge = None
                else:
                    self.idx -= edge.length
                    self.edge = string[i - self.lag + self.node.root_length]

        def split_edge(self):
            edge = self.node[self.edge]
            # Create a new node and edge
            middle_node = InternalNode(self.node.root_length + self.idx)
            midpoint = edge.start + self.idx
            next_edge = Edge(edge.dest, midpoint, edge.end)
            middle_node[string[midpoint]] = next_edge
            # Update the current edge to end at the new node
            edge.dest = middle_node
            edge.end = midpoint
            edge.length = midpoint - edge.start
            return middle_node

    cursor = Cursor()
    from_first_word = True
    dummy = InternalNode(0)

    for i, letter in enumerate(string):

        if from_first_word and i > len_s:
            from_first_word = False

        cursor.lag += 1
        prev = dummy  # dummy node to make suffix linking easier the first time

        while cursor.lag >= 0:

            if cursor.is_followed_by(letter):  # Suffix already exists in tree
                prev.link = cursor.node
                cursor.defer(letter)
                break

            elif cursor.idx != 0:  # We are part-way along an edge
                stem = cursor.split_edge()
            else:
                stem = cursor.node
            # Now we have an explicit node and can insert our new edge there.
            stem[letter] = Edge(LeafNode(from_first_word), i, inf)
            # Whenever we update an internal node, we check for a new max_len
            # But not until we have started into the second input string
            if (i > len_s and not stem.already_counted
                    and stem.has_s_leaves and stem.has_t_leaves):
                stem.already_counted = True
                if stem.root_length > max_len:
                    max_len = stem.root_length
            # Link the previously altered internal node to the new node and make
            # the new node prev.
            prev.link = prev = stem
            cursor.post_insert(i)

    print(max_len)


print("\n\t\t\t\t\t19BIO201 - Intelligence of Biological System 3"
      "\n\t\t\t\tSuffix Trees and their Applications in Bioinformatics"
      "\n\t\t-----------------------------------------------------------------------"
      "\n\t\tAdithya R(005), Advaith A J(006), Aiswarya Mahesh(007), G Sabarinath(026)"
      "\n\n\t\tthe length of the longest substring using Ukkonen's algorithm")

s = input("\n\nEnter the String: ")
t = input("Enter the Text: ")
longestCommonSubstring(s, t)
