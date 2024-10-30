"""
Design a data structure that follows the constraints of a Least Recently Used (LRU) cache.

Implement the LRUCache class:

LRUCache(int capacity) Initialize the LRU cache with positive size capacity.
int get(int key) Return the value of the key if the key exists, otherwise return -1.
void put(int key, int value) Update the value of the key if the key exists. Otherwise, add the key-value pair to the cache.
If the number of keys exceeds the capacity from this operation, evict the least recently used key.


The functions get and put must each run in O(1) average time complexity.

Example 1:

Input
["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"]
[[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]]
Output
[null, null, null, 1, null, -1, null, -1, 3, 4]

Explanation
LRUCache lRUCache = new LRUCache(2);
lRUCache.put(1, 1); // cache is {1=1}
lRUCache.put(2, 2); // cache is {1=1, 2=2}
lRUCache.get(1);    // return 1
lRUCache.put(3, 3); // LRU key was 2, evicts key 2, cache is {1=1, 3=3}
lRUCache.get(2);    // returns -1 (not found)
lRUCache.put(4, 4); // LRU key was 1, evicts key 1, cache is {4=4, 3=3}
lRUCache.get(1);    // return -1 (not found)
lRUCache.get(3);    // return 3
lRUCache.get(4);    // return 4


Constraints:

1 <= capacity <= 3000
0 <= key <= 104
0 <= value <= 105
At most 2 * 105 calls will be made to get and put.

Hints:

Counter implementation
 Every page entry has a counter; every time page is
referenced through this entry, copy the clock into the
counter
 When a page needs to be changed, look at the counters to  find smallest value
 Search through table needed

 Stack implementation
 Keep a stack of page numbers in a double link form:
 Page referenced:
 move it to the top
 requires 6 pointers to be changed
 But each update more expensive
 No search for replacement


"""

v = 'value'
k = 'arrivalTime'
class LRUCache:

    def __init__(self, capacity: int):
        """
        LRUCache(int capacity) Initialize the LRU cache with positive size capacity.
        :param capacity: capacity
        Template structure:
                reference_string = [7,0,1,2,0,3,0,4,2,3,0,3,2,1,2,0,1,7,0,1]
        Example with C = 3 (capacity or number of locations)

        t=0: "7" arrives -> new item :
            self.cache = [{ 'value': 7, 'arrivalTime': 0}]
        t=1: "0" arrives -> new item :
            self.cache = [{ 'value': 7, 'arrivalTime': 0}, { 'value': 0, 'arrivalTime': 1}]
        t=2: "1" arrives -> new item :
            self.cache = [{ 'value': 7, 'arrivalTime': 0}, { 'value': 0, 'arrivalTime': 1}, { 'value': 1, 'arrivalTime': 2}] ==> FULL
        t=3: "2" arrives -> new item : But self.isFull is TRUE
            The least recently used is "7" because t=0 is the minimum between [0,1,2], then:
            self.cache = [{ 'value': 2, 'arrivalTime': 3}, { 'value': 0, 'arrivalTime': 1}, { 'value': 1, 'arrivalTime': 2}]
        """
        self.isFull = False
        self.head = 0
        self.cache = [{v: 0, k: 0}]
        self.idx = []
        self.time = []
        self.mapping = [(0,0)] # (idx_onto_stack , arrivalTime)
        try:
            if capacity > 0:
                self.capacity = capacity
                self._build_cache()
                print(f"\n\n\nCreation of the Cache: {self.cache}\n\n\n")
            else:
                raise ValueError("The LRUcache needs a positive capacity value.")
        except ValueError as e:
            print(f"Error: {e}")

    # helper method
    def _build_cache(self) -> None:
        """
        By the fact:
            cache = [{'v':0, 't':0}]
            cache*=2
            cache
            [{'v': 0, 't': 0}, {'v': 0, 't': 0}]
        :return:
        """
        # self.cache *= self.capacity # THIS IS PROBLEMATIC: unique pointer to all cells (a change reflects in all cells)
        self.cache = [{v: 0, k: 0} for _ in range(self.capacity)]
        self.idx = [0] * self.capacity
        self.time = [0] * self.capacity


    def get(self, key: int) -> bool:
        """
        :param key: element to search in terms of integer contained
        :return: True if the item is present in the positive case or False in the negative case
        """
        for item in self.cache:
            if item[v] == key:
                return True
        return False

    def _replace(self, idx_LRU: int, time_newItem: int, value: int) -> None:
        self.cache[idx_LRU].update({v: value, k: time_newItem})


    def put(self, time: int, value: int) -> None:
        """
        :param key:
        :param value:
        :return:
        """
        # FIFO management until the cache is not Full
        if self.head < self.capacity-1:
            self.cache[self.head][v] = value
            self.cache[self.head][k] = time
            self.head += 1
        else:
            lru_item = min(self.cache, key=lambda x: x[k])
            idx_LRU = self.cache.index(lru_item)
            self._replace(idx_LRU=idx_LRU, time_newItem=time, value=value)



if __name__ == '__main__':
    # Your LRUCache object will be instantiated and called as such:
    reference_string = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
    obj = LRUCache(capacity=3)
    for i, value in enumerate(reference_string):
        obj.put(value=value, time=i)
        print(f"Time {i}: Cache = {obj.cache}")

"""
This code has different problem but the most important is the TIME: the mapping of the time
with the idx in the cache is problematic and needs to be updated too frequently. But the time
for each item is very useless and the get() is problematic. If you require a get, which time
you will need to update (increase by 1) ? All item of the cache?
"""