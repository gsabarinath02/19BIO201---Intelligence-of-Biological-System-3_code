import os


def get_suffixes(string):
    return [string[i:] + "$" for i in range(len(string) + 1)]


def shared_prefix(string_a, string_b):
    return os.path.commonprefix([string_a, string_b])


def construct_suffix_tree(string):
    tree = {}
    for i in range(len(string) + 1):
        suffix = string[i:] + "$"
        insert_suffix(suffix, tree)
    return tree


def insert_suffix(string, suffix_tree):
    if len(suffix_tree) == 0:
        suffix_tree[string] = []
        return suffix_tree

    found_match = False
    for key in list(suffix_tree):
        prefix = shared_prefix(string, key)
        n = len(prefix)
        if len(prefix) > 0:
            found_match = True
            key_suffix = key[n:]
            string_suffix = string[n:]
            del suffix_tree[key]
            suffix_tree[prefix] = [key_suffix, string_suffix]

    if not found_match:
        suffix_tree[string] = []
    return suffix_tree


print("\n\t\t\t\t\t19BIO201 - Intelligence of Biological System 3"
      "\n\t\t\t\tSuffix Trees and their Applications in Bioinformatics"
      "\n\t\t-----------------------------------------------------------------------"
      "\n\t\tAdithya R(005), Advaith A J(006), Aiswarya Mahesh(007), G Sabarinath(026)")
my_string = input("\n\tEnter the String: ")
print(construct_suffix_tree(my_string))
