# '''
# Linked List hash table key/value pair
# '''
class LinkedPair:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

class HashTable:
    '''
    A hash table that with `capacity` buckets
    that accepts string keys
    '''
    def __init__(self, capacity):
        self.capacity = capacity  # Number of buckets in the hash table
        self.storage = [None] * capacity


    def _hash(self, key):
        '''
        Hash an arbitrary key and return an integer.

        You may replace the Python hash with DJB2 as a stretch goal.
        '''
        return hash(key)


    def _hash_djb2(self, key):
        '''
        Hash an arbitrary key using DJB2 hash

        OPTIONAL STRETCH: Research and implement DJB2
        '''
        hash_value = 33
        key = str.encode(key)
        
        for char in key:
            hash_value = ((hash_value << 5) + hash_value) + char
        
        return hash_value


    def _hash_mod(self, key):
        '''
        Take an arbitrary key and return a valid integer index
        within the storage capacity of the hash table.
        '''
        # return self._hash(key) % self.capacity
        return self._hash_djb2(key) % self.capacity


    def insert(self, key, value):
        '''
        Store the value with the given key.

        Hash collisions should be handled with Linked List Chaining.

        Fill this in.
        '''
        index = self._hash_mod(key)
        el = LinkedPair(key, value)
        if self.storage[index] is not None:
            # print(f"self.storage[index] is: {self.storage[index].key}")
            keep_going = True
            el_for_eval = self.storage[index]
            while keep_going:
                if el_for_eval.key == key:
                    el_for_eval.value = value
                    keep_going = False
                if el_for_eval.next is not None:
                    # print(f"el_for_eval.key: {el_for_eval.key}")
                    # print(f"el_for_eval.next.key: {el_for_eval.next.key}")
                    el_for_eval = el_for_eval.next
                else:
                    # print(f"el_for_eval.next is None: {el_for_eval.next}")
                    el_for_eval.next = el
                    keep_going = False
        else:
            # print(f'no value yet {self.storage[index]}')
            self.storage[index] = el



    def remove(self, key):
        '''
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Fill this in.
        '''
        # print("Remove")
        index = self._hash_mod(key)
        if self.storage[index] is None:
            # print("ERROR: no value to remove")
            return

        current_el = self.storage[index]
        if current_el.next is None:
            # print(f"current_el.next: {current_el.next}")
            self.storage[index] = None
            return

        keep_going = True
        stored_key = current_el.key
        prev_el = self.storage[index]
        while keep_going:
            # print(f"stored_key: {stored_key} | key: {key}")
            if stored_key == key:
                # print('EQUAL!')
                if current_el == prev_el:
                    # print("FIRST ELEMENT")
                    # print(f"current_el: {current_el} | prev_el: {prev_el}")
                    self.storage[index] = current_el.next
                    current_el.next = None
                    keep_going = False
                elif current_el.next is not None:
                    # print("there is a next")
                    # print(f"current_el.next: {current_el.next}")
                    prev_el.next = current_el.next
                    current_el.next = None
                    keep_going = False
                else:
                    # print("ELSE")
                    prev_el.next = current_el.next
                    keep_going = False
                    return
            else:
                stored_key = current_el.next.key
                prev_el = current_el
                # print(f"stored_key: {stored_key} | prev_el.key: {prev_el.key}")
                current_el = current_el.next
                



    def retrieve(self, key):
        '''
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Fill this in.
        '''
        index = self._hash_mod(key)
        # print("RETRIEVE")
        if self.storage[index] is None:
            # print("ERROR: Value DNE")
            return

        current_el = self.storage[index]
        if current_el.next is None:
            # print("only one val")
            # print(f"current_el.key: {current_el.key} | key: {key}")
            return current_el.value

        keep_going = True
        stored_key = current_el.key
        prev_el = self.storage[index]
        while keep_going:
            # print(f"current_el.key: {current_el.key} | key: {key}")
            if current_el.key != key:
                # print('not equal')
                current_el = current_el.next
            else:
                # print('equal')
                return current_el.value


    def resize(self):
        '''
        Doubles the capacity of the hash table and
        rehash all key/value pairs.

        Fill this in.
        '''
        self.capacity *= 2
        new_storage = [None] * self.capacity

        for el in self.storage:
            index = self._hash_djb2(el.key) % self.capacity
            new_storage[index] = el

        # for i in range(0,len(self.storage)):
        #     print(i)
        #     new_storage[i] = self.storage[i]
        #     print(f"self.storage[{i}] : {self.storage[i].key, self.storage[i].value} | new_storage[{i}] : {new_storage[i].key, new_storage[i].value}")

        self.storage = new_storage

        el_list = []
        for el in self.storage:
            if el is not None and el.next is not None:
                keep_going = True
                prev_el = el
                current_el = el
                while keep_going:
                    if current_el.next is not None:
                        el_list.append({"key": current_el.key, "value": current_el.value})
                        current_el = current_el.next
                        prev_el.next = None
                    else:
                        el_list.append({"key": current_el.key, "value": current_el.value})
                        current_el = current_el.next
                        prev_el.next = None
                        keep_going = False
                        
        for i in range(0,len(el_list)):
            self.insert(el_list[i]["key"], el_list[i]["value"])

"""
ht = HashTable(2)
ht.insert("hello",50)
ht.insert("abacusMAX",2)
ht.insert("world",50)
ht.insert("people",2)
ht.remove("hello")
ht.insert("world",100)

print(ht.storage)

ht.remove("abacusMAX")

print(ht.storage)
print(f'retrieve: {ht.retrieve("people")}')
print(f'retrieve: {ht.retrieve("world")}')

ht.resize()

print(ht.storage)

print(f'retrieve: {ht.retrieve("people")}')
print(f'retrieve: {ht.retrieve("world")}')

#"""
"""
ht = HashTable(8)

ht.insert("key-0", "val-0")
ht.insert("key-1", "val-1")
ht.insert("key-2", "val-2")
ht.insert("key-3", "val-3")
ht.insert("key-4", "val-4")
ht.insert("key-5", "val-5")
ht.insert("key-6", "val-6")
ht.insert("key-7", "val-7")
ht.insert("key-8", "val-8")
ht.insert("key-9", "val-9")
print(f"insert: {ht.storage}")

ht.remove("key-9")
ht.remove("key-8")
ht.remove("key-7")
ht.remove("key-6")
ht.remove("key-5")
ht.remove("key-4")
ht.remove("key-3")
ht.remove("key-2")
ht.remove("key-1")
ht.remove("key-0")
print(f"remove: {ht.storage}")
#"""
"""
if __name__ == "__main__":
    ht = HashTable(2)

    ht.insert("line_1", "Tiny hash table")
    ht.insert("line_2", "Filled beyond capacity")
    ht.insert("line_3", "Linked list saves the day!")

    print("")

    # Test storing beyond capacity
    print(ht.retrieve("line_1"))
    print(ht.retrieve("line_2"))
    print(ht.retrieve("line_3"))

    # Test resizing
    old_capacity = len(ht.storage)
    ht.resize()
    new_capacity = len(ht.storage)

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")
    print(f"insert: {ht.storage}")

    # Test if data intact after resizing
    print(ht.retrieve("line_1"))
    print(ht.retrieve("line_2"))
    print(ht.retrieve("line_3"))

    print("")
#"""