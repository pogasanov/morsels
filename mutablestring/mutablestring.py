from collections import UserString, MutableSequence


class MutableString(MutableSequence, UserString):
    def __setitem__(self, key, value):
        list_data = list(self.data)
        list_data[key] = value
        self.data = ''.join(list_data)

    def __delitem__(self, key):
        list_data = list(self.data)
        del list_data[key]
        self.data = ''.join(list_data)

    def insert(self, index, object):
        list_data = list(self.data)
        list_data.insert(index, object)
        self.data = ''.join(list_data)
