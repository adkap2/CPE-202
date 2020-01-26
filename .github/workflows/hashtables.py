"""Hash Table
For:
    CPE202
    Sections 7 & 9
    Fall 2019
Author:
    Adam Goldstein
"""
def hash_string(string, capacity):
    """
    Docstring
    """
    hash = 0
    for c in string:
        hash = (hash * 31 + ord(c)) % capacity
    return hash

class HashTableSepchain:
    """Atributes
    """
    def __init__(self):
        self.capacity = 11
        self.slots = [None] * self.capacity
        self.num_items = 0
        self.num_collisions = 0

    def put(self, key, data):
        """
        Docstring
        """
        if self.load_factor() > 1.5:
            self.resize_helper()
        hashvalue = hash_string(key, self.capacity)
        node = NodeQueue(key, data)
        if self.slots[hashvalue] == None:
            self.slots[hashvalue] = node
        else:
            temp_node = self.slots[hashvalue]
            node.next_node = temp_node
            self.slots[hashvalue] = node
        self.num_items += 1

    def resize_helper(self):
        """
        Docstring
        """
        temp_slots = self.slots
        temp_capacity = self.capacity
        self.capacity = (2 * self.capacity) + 1
        self.slots = [None] * self.capacity
        for i in range(temp_capacity):
            node = temp_slots[i]
            if node is not None:
                while node:
                    self.put(node.key, node.data)
                    self.num_items -= 1
                    node = node.next_node

    def get(self, key):
        """
        Docstring
        """
        startslot = hash_string(key, self.capacity)
        if self.slots[startslot] == None:
            return None
        found = False
        node = self.slots[startslot]
        while not found and node:
            if node.key == key:
                found = True
                key, data = node.key, node.data
            node = node.next_node
        if not found:
            raise LookupError()
        return data

    def __getitem__(self, key):
        """
        Docstring
        """
        return self.get(key)

    def __setitem__(self, key, data):
        """
        Docstring
        """
        self.put(key, data)

    def contains(self, key):
        """checks if value is contained at key entry from hash table
        Args:
            table (list) : hash table
            key (int) : the key of an entry to be deleted
        """
        hashvalue = hash_string(key, self.capacity)
        if self.slots[hashvalue] == None:
            return False
        node = self.slots[hashvalue]
        found = False
        while not found and node:
            if node.key == key:
                found = True
            node = node.next_node
        return found

    def remove(self, key):
        """deletes an entry from hash table
        Args:
            key (int) : the key of an entry to be deleted
        """
        hashvalue = hash_string(key, self.capacity)
        if self.slots[hashvalue] == None:
            raise LookupError
        node = self.slots[hashvalue]
        found = False
        if node.key == key:
            found = True
            self.slots[hashvalue] = self.slots[hashvalue].next_node
        node_prev = node
        temp = node
        node = node.next_node
        while not found and node:
            if node.key == key:
                found = True
                temp = node
                node_prev.next_node = node.next_node
            else:
                node = node.next_node
        if found == True:
            return (temp.key, temp.data)
        raise LookupError

    def size(self):
        """
        Docstring
        """
        return self.num_items

    def load_factor(self):
        """
        Docstring
        """
        return self.num_items/self.capacity

    def collisions(self):
        """
        Docstring
        """
        return self.num_collisions

    def __contains__(self, key):
        """
        Docstring
        """
        return self.contains(key)

class HashTableLinear:
    """Attributes
    """
    def __init__(self):
        self.capacity = 11
        self.slots = [None] * self.capacity
        self.num_items = 0
        self.num_collisions = 0

    def __eq__(self, other):
        return isinstance(other, HashTableLinear)\
            and self.capacity == other.capacity\
            and self.num_items == other.num_items\
            and self.slots == other.slots\
            and self.num_collisions == other.num_collisions

    def __repr__(self):
        return "HashTableLinear{capacity: %s, num_items: %s, slots: %s, num_collisions: %s}"\
            % (self.capacity, self.num_items, self.slots, self.num_collisions)

    def put(self, key, data):
        """
        Docstring
        """
        if self.load_factor() > 0.75:
            temp_slots = self.slots
            temp_capacity = self.capacity
            self.capacity = (2 * self.capacity) + 1
            self.slots = [None] * self.capacity
            for i in range(len(temp_slots) - 1):
                if temp_slots[i] != None:
                    self.slots[i] = temp_slots[i]
        hashvalue = hash_string(key, self.capacity)
        if self.slots[hashvalue] == None:
            self.slots[hashvalue] = (key, data)
            self.num_items += 1
        else:
            if self.slots[hashvalue] == key:
                self.slots[hashvalue] = (key, data)  #replace
            else:
                nextslot = self.rehash(hashvalue, len(self.slots))
                while self.slots[nextslot] != None:
                    nextslot = self.rehash(nextslot, len(self.slots))
                    self.num_collisions += 1
                self.slots[nextslot] = (key, data)
                self.num_items += 1

    def rehash(self, oldhash, capacity):
        """
        Docstring
        """
        return (oldhash+1)%capacity

    def get(self, key):
        """
        Docstring
        """
        """startslot = hash_string(key, self.capacity)
        if self.slots[startslot] == None:
            return None
        (key_slot, val_slot) = self.slots[startslot]
        if key_slot != key:
            found = False
        else:
            found = True
            return val_slot
        data = None
        stop = False
        found = False
        position = startslot
        while self.slots[position] != None and  \
                            not found and not stop:
            if self.slots[position][0] == key:
                found = True
                (key, data) = self.slots[position]
            else:
                position = self.rehash(position, self.capacity)
            if position == startslot:
                stop = True
        if not found or data == None:
            raise LookupError()"""
        found = False
        for i in self.slots:
            if i is not None:
                if i[0] == key:
                    found = True
                    return i[1]
        if not found:
            raise LookupError()

    def __getitem__(self, key):
        """
        Docstring
        """
        return self.get(key)

    def __setitem__(self, key, data):
        """
        Docstring
        """
        self.put(key, data)

    def contains(self, key):
        """checks if value is contained at key entry from hash table
        Args:
            table (list) : hash table
            key (int) : the key of an entry to be deleted
        """
        found = False
        for i in self.slots:
            if i is not None:
                if i[0] == key:
                    found = True
        return found

    def remove(self, key):
        """deletes an entry from hash table
        Args:
            key (int) : the key of an entry to be deleted
        """
        found = False
        for i in self.slots:
            if i != None:
                if key == i[0]:
                    found = True
        if found == False:
            raise LookupError()
        position = hash_string(key, self.capacity)
        while key != self.slots[position][0]:
            position = self.rehash(position, len(self.slots))
        (key_ret, data_ret) = self.slots[position][0], self.slots[position][1]
        self.slots[position] = None
        position = self.rehash(position, len(self.slots))
        while self.slots[position]:
            key_to_redo, val_to_redo = self.slots[position][0], self.slots[position][1]
            self.slots[position] = None
            self.put(key_to_redo, val_to_redo)
            position = self.rehash(position, len(self.slots))
        self.num_items -= 1
        return (key_ret, data_ret)

    def size(self):
        """
        Docstring
        """
        return self.num_items

    def load_factor(self):
        """
        Docstring
        """
        return self.num_items/self.capacity

    def collisions(self):
        """
        Docstring
        """
        return self.num_collisions

    def __contains__(self, key):
        """
        Docstring
        """
        return self.contains(key)
    
    def add_keys(self):
        list1 = [None] * self.capacity
        for i in range(len(self.slots)-1):
            if self.slots[i] != None:
                list1[i] = self.slots[i][0]
        """for i in self.slots:
            if i != None:
                list1.append(i[0])"""
        return list1

    def add_vals(self):
        list1 = [None] * self.capacity
        for i in range(len(self.slots)-1):
            if self.slots[i] != None:
                list1[i] = self.slots[i][1]
        return list1


class HashTableQuadratic:
    def __init__(self):
        self.capacity = 11
        self.slots = [None] * self.capacity
        self.num_items = 0
        self.num_collisions = 0
        self.quad_prob = 1

    def __eq__(self, other):
        return isinstance(other, HashTableLinear)\
            and self.capacity == other.capacity\
            and self.num_items == other.num_items\
            and self.slots == other.slots\
            and self.num_collisions == other.num_collisions\
            and self.quad_prob == other.quad_prob

    def __repr__(self):
        return "HashTableQuadratic{capacity: %s, num_items: %s, slots: %s, num_collisions: %s, self.quad_prob: %s}"\
            % (self.capacity, self.num_items, self.slots, self.num_collisions, self.quad_prob)

    def put(self,key,data):
        """
        Docstring
        """
        if self.load_factor() > 0.75:
            self.resize_helper()
        hashvalue = hash_string(key, self.capacity)
        if self.slots[hashvalue] == None:
            self.slots[hashvalue] = {'key': key, 'data': data}
        else:
            if self.slots[hashvalue]['key'] == key:
                self.slots[hashvalue] = {'key': key, 'data': data}  #replace
            else:
                nextslot = hashvalue
                index = 0
                while self.slots[nextslot] is not None and index < len(self.slots):
                    nextslot = self.rehash(hashvalue, self.quad_prob)
                    self.quad_prob += 1
                    self.num_collisions += 1
                    index += 1
                self.slots[nextslot] = {'key': key, 'data': data}
                self.quad_prob = 1
        self.num_items += 1

    def resize_helper(self):
        """
        Docstring
        """
        temp_slots = self.slots
        temp_capacity = self.capacity
        self.capacity = (2 * self.capacity) + 1
        self.slots = [None] * self.capacity
        for i in range(temp_capacity):
            if temp_slots[i] is not None:
                self.put(temp_slots[i]['key'], temp_slots[i]['data'])
                self.num_items -= 1

    def get(self, key):
        """
        Docstring
        """
        startslot = hash_string(key, self.capacity)
        if self.slots[startslot] == None:
            return None
        (key_slot, val_slot) = self.slots[startslot]
        if key_slot != key:
            found = False
        data = None
        stop = False
        found = False
        position = startslot
        while self.slots[position] != None and  \
                            not found and not stop and position < len(self.slots)-1:
            if self.slots[position]['key'] == key:
                found = True
                (key, data) = self.slots[position]['key'], self.slots[position]['data']
            else:
                position = self.rehash(position, self.quad_prob)
                position = position + 1
            if position == startslot:
                stop = True
        if not found:
            raise LookupError()
        return data

    def __getitem__(self, key):
        """
        Docstring
        """
        return self.get(key)

    def __setitem__(self, key, data):
        """
        Docstring
        """
        self.put(key, data)

    def contains(self, key):
        """checks if value is contained at key entry from hash table
        Args:
            table (list) : hash table
            key (int) : the key of an entry to be deleted
        """
        found = False
        for i in self.slots:
            if i is not None:
                if i['key'] == key:
                    found = True
        return found


    def remove(self, key):
        """deletes an entry from hash table
        Args:
            key (int) : the key of an entry to be deleted
        """
        found = False
        for i in range(len(self.slots)-1):
            if self.slots[i] != None:
                if key == self.slots[i]['key']:
                    found = True
                    break
        if found == False:
            raise LookupError()
        position = i
        while key != self.slots[position]['key']:
            position = self.rehash(position, self.quad_prob)
        (key_ret, data_ret) = self.slots[position]['key'], self.slots[position]['data']
        self.slots[position] = None
        position = self.rehash(position, self.quad_prob)
        while self.slots[position]:
            key_to_redo, val_to_redo = self.slots[position]['key'], self.slots[position]['data']
            self.slots[position] = None
            self.put(key_to_redo, val_to_redo)
            position = self.rehash(position, self.quad_prob)
        self.num_items -= 1
        return (key_ret, data_ret)

    def size(self):
        """
        Docstring
        """
        return self.num_items

    def load_factor(self):
        """
        Docstring
        """
        return self.num_items/self.capacity

    def collisions(self):
        """
        Docstring
        """
        return self.num_collisions

    def __contains__(self, key):
        """
        Docstring
        """
        return self.contains(key)

    def rehash(self, oldhash, i):
        """
        Docstring
        """
        return (oldhash + i**2) % self.capacity

def import_stopwords(filename, hashtable):
    """
    Docstring
    """
    stop_words = []
    with open(filename, "r") as f:
        for line in f:
            stop_words.extend(line.split())
    for word in stop_words:
        hashtable.put(word, 0)
    return hashtable
