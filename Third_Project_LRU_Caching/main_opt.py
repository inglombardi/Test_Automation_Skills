class LRUCache:

    def __init__(self, capacity: int):
        """
        LRUCache(int capacity) Initialize the LRU cache with positive size capacity.
        :param capacity: capacity
        """
        self.capacity = capacity
        self.cache = []  # Stores elements as dictionaries with value and arrival time
        self.time = 0  # Global counter for keeping track of time
        # The cost of a push or replace or get is the same.
        try:
            if capacity > 0:
                self.capacity = capacity
            else:
                raise ValueError("The LRUcache needs a positive capacity value.")
        except ValueError as e:
            print(f"Error: {e}")
    def get(self, key: int) -> int:
        """
        :param key: The value to search for in the cache.
        :return: The value if found, otherwise -1.
        """
        found = False
        for item in self.cache:
            if item['value'] == key:
                # Update the arrival time since this key was just accessed
                item['arrivalTime'] = self.time
                self.time += 1
                found = True
                return key
            else:
                # NO - OP -> pass
                self.time += 1
        # here the list is finished
        if not found:
            # raise ValueError(f"The LRUcache does not contain {key}")
            return -1


    def _replace(self, value: int) -> None:
        """
        Why use lambda?
        The lambda function is useful here because it allows you to create a function inline, without
        having to define a separate function. It is a compact shortcut for simple operations that
        need to be performed only at that point.

        Replace the least recently used item in the cache.
        :param value: The new value to insert.
        """
        # Find the item with the smallest arrivalTime (least recently used)
        lru_item = min(self.cache, key=lambda x: x['arrivalTime'])
        self.cache.remove(lru_item)  # Remove the LRU item
        # Insert the new item with the current time
        self.cache.append({'value': value, 'arrivalTime': self.time})
        self.time += 1

    def put(self, value: int) -> None:
        """
        Add a new value to the cache or replace the least recently used one if full.
        :param value: The value to insert.
        """
        # Check if the item is already in the cache
        if self.get(value) == -1:
            if len(self.cache) < self.capacity:
                # Cache is not full, just add the new item
                self._push(value=value)
            else:
                # Cache is full, replace the least recently used (LRU) item
                self._replace(value)

    def _push(self, value: int) -> None:
        self.cache.append({'value': value, 'arrivalTime': self.time})
        self.time += 1

if __name__ == '__main__':
    reference_string = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
    capacity = 3  # Set the cache capacity
    obj = LRUCache(capacity)

    for i, value in enumerate(reference_string):
        obj.put(value)
        print(f"Time {i}: Cache = {obj.cache}")
