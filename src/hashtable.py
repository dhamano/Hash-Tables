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
        index = self._hash_mod(key)
        if self.storage[index] is None:
            # print("ERROR: no value to remove")
            return

        current_el = self.storage[index]
        if current_el.next is None:
            self.storage[index] = None
            return

        keep_going = True
        stored_key = current_el.key
        prev_el = self.storage[index]
        while keep_going:
            if stored_key == key:
                if current_el == prev_el:
                    self.storage[index] = current_el.next
                    current_el.next = None
                    keep_going = False
                elif current_el.next is not None:
                    prev_el.next = current_el.next
                    current_el.next = None
                    keep_going = False
                else:
                    stored_key = current_el.next.key
                    prev_el = current_el
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

        for i in range(len(self.storage)):
            new_storage[i] = self.storage[i]

        self.storage = new_storage

"""
ht = HashTable(3)
ht.insert("hello",50)
ht.insert("abacusMAX",2)
ht.insert("world",50)
ht.insert("people",2)
ht.remove("hello")

print(ht.storage)

ht.remove("abacusMAX")

print(ht.storage)

ht.resize()

print(ht.storage)

print(f'retrieve: {ht.retrieve("world")}')

#"""
# """
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

    # Test if data intact after resizing
    print(ht.retrieve("line_1"))
    print(ht.retrieve("line_2"))
    print(ht.retrieve("line_3"))

    print("")
#"""