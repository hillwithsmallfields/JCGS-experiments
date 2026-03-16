#!/usr/bin/env python3

import os

# class DirectoryIter:

#     def __init__(self, directory):
#         self.directory = directory
#         self.filenames = directory.filenames.copy()

#     def __iter__(self):
#         return self

#     def __next__(self):
#         for filename in self.filenames:
#             name = os.path.join(self.directory.dirname, filename)
#             with open(name) as r:
#                 data = r.read()
#             print("__next__ yielding", name, data)
#             yield name, data
#         raise StopIteration

class DirectoryAsDictionary:

    def __init__(self, dirname,
                 readable=True, writable=False):
        self.dirname = dirname
        self.filenames = []
        self.readable = readable
        self.writable = writable
        self.__update__listing__()

    def __update__listing__(self):
        self.filenames = sorted(os.listdir(self.dirname))

    def __next__(self):
        print("in DirectoryAsDictionary.__next__")
        print("iterating over", self.filenames)
        for filename in self.filenames:
            name = os.path.join(self.dirname, filename)
            with open(name) as r:
                data = r.read()
            print("__next__ yielding", name, "and", len(data), "bytes")
            yield name, data

    def __iter__(self):
        print("in DirectoryAsDictionary.__iter__")
        self.__update__listing__()
        return self.__next__()

    def __len__(self):
        self.__update__listing__()
        return len(self.filenames)

    def items(self):
        print("in DirectoryAsDictionary.items iterating over", self.filenames)
        for filename in self.filenames:
            name = os.path.join(self.dirname, filename)
            with open(name) as r:
                data = r.read()
            print("items yielding", name, "and", len(data), "bytes")
            yield name, data
        # return self.__iter__()

    def keys(self):
        self.__update__listing__()
        return self.filenames

    def __contains__(self, key):
        if not self.readable:
            raise TypeError("This DirectoryAsDictionary object is not readable")
        self.__update__listing__()
        print("filenames are", self.filenames)
        return key in self.filenames

    def __getitem__(self, key):
        if not self.readable:
            raise TypeError("This DirectoryAsDictionary object is not readable")
        self.__update__listing__()
        if key not in self.filenames:
            raise FileNotFoundError("No such file or directory: " + key)
        fullname = os.path.join(self.dirname, key)
        with open(fullname) as r:
            return r.read()

d = DirectoryAsDictionary("data")
for k, v in d.items():
    print(k, v)
d = DirectoryAsDictionary("data")
dl = list(d)
print(dl)
d = DirectoryAsDictionary("data")
print(len(d))
d = DirectoryAsDictionary("data")
print(d.keys())
print(d.keys())
print("b" in d)
