import copy


class KeyValueList:
    # python dict clone as key value pair list.
    def __init__(self, name="", input_dict=None):
        self.name = name
        self.pairs = {}
        if isinstance(name, dict) and input_dict is None:
            self.name = "Dictionary"
            self.pairs = name
        if isinstance(input_dict, dict):
            self.pairs = copy.copy(input_dict)

    def set(self, key, value=None):
        if key in self.pairs.keys():
            self.pairs.update({str(key): value})

    def append(self, key, value=None):
        self.pairs.update({str(key): value})

    def update(self, key, value):
        self.pairs.update({str(key): value})

    def get(self, key, ifnotexistreturns=None):
        # this part must be case sensitive
        if key in self.pairs.keys():
            return self.pairs.get(key)
        else:
            return ifnotexistreturns

    def delete(self, key):
        self.pairs.pop(key)

    def parse_input(self, text):
        split = text.split(":", 1)
        self.append(split[0], split[1])

    def keys(self):
        return self.pairs.keys()

    def is_empty(self):
        count = self.pairs.keys().__len__()
        if count == 0:
            return True
        return 0

    def __add__(self, addition):
        if isinstance(addition, KeyValueList):
            keys = addition.keys()
            for k in keys:
                self.append(k, addition.get(k))
            return self

    def __iter__(self):
        return self.pairs.keys()

    def __getitem__(self, item):
        return self.pairs.__getitem__(item)

    def __str__(self):
        ret = f"{self.name} : {{ \n"
        for key in self.pairs:
            value = self.pairs[key]
            key_len = str(key).__len__()
            key_len_max = 20
            if key_len > key_len_max:
                key = str(key)[:key_len_max-2] + ".."
            row = f"{key:{key_len_max}} : {value}"

            ret += row
        return ret

    def __repr__(self):
        return f"KeyValueList {self.name}"
