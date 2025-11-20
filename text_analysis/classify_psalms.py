#!/usr/bin/env python3

"""Make a tree of words to subtrees or Psalm numbers,
in which each level of the tree corresponds to a TF-IDF term.

Thus, the top-level dictionary binds psalm numbers or subtrees
according to their most prominent words; the subtrees within that by
the second-most prominent words, etc.
"""

import csv
import json

from dobishem import storage as s
from orgbookchapterverse.orgbookchapterverse import TextCollection

def emplace(holder, reference, words):
    """Place a reference in a holder according to the associated words."""
    if len(words) > 1:
        first = words[0]
        sub_holder = holder.get(first)
        if not sub_holder:
            sub_holder = dict()
            holder[first] = sub_holder
        emplace(sub_holder, reference, words[1:])
    else:
        holder[words[0]] = reference

def distribute(reference_and_words):
    """Distribute items according to their commonest words."""
    holder = dict()
    for item in reference_and_words:
        emplace(holder, item[0], item[1:])
    return holder

def reduce_tree(tree):
    """Reduce the depth of subtrees by moving up values when the node has only one value."""
    for k, v in tree.items():
        if isinstance(v, dict):
            if len(v) == 1:
                tree[k] = list(v.values())[0]
            reduce_tree(v)

def classify_psalms_main():

    psalms = TextCollection("kj")["Psalms"]

    psalms_tf_idf = psalms.all_chapter_tf_idf()

    with open("/tmp/psalms.csv", 'w') as outstream:
        writer = csv.writer(outstream)
        for p in psalms.all_chapters():
            writer.writerow([p.chapter_number] + ["%s(%f)" % (w[0], w[1]) for w in p.tf_idf()[:12] if w[1] > 0])

    tree = distribute([[p.chapter_number] + [w[0] for w in p.tf_idf()[:3]]
                       for p in psalms.all_chapters()])

    reduce_tree(tree)

    s.save("/tmp/psalms.json", tree)
    s.save("/tmp/psalms.yaml", tree)

if __name__ == "__main__":
    classify_psalms_main()
