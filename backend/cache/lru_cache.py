import time

class Node:
    def __init__(self,key,value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:

    def __init__(self, capacity:int):
        self.capacity = capacity
        self.cache = {}
        self.size = 0

        self.head = Node(0,0)
        self.tail = Node(0,0)
        self.head.next = self.tail
        self.tail.prev = self.head

        self.hits = 0
        self.misses = 0

        self.evictions = []

    def _add_node(self,node):
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self,node):
        prev = node.prev
        nxt = node.next
        prev.next = nxt
        nxt.prev = prev

    def _move_to_front(self,node):
        self._remove_node(node)
        self._add_node(node)

    def get(self,key):
        node = self.cache.get(key)

        if not node:
            self.misses += 1
            return None

        self.hits += 1
        self._move_to_front(node)
        return node.value

    def get_eviction_candidate(self):
        if self.size == 0:
            return None
        return self.tail.prev.key

    def put(self,key,value):

        node = self.cache.get(key)

        if node:
            node.value = value
            self._move_to_front(node)
            return

        new_node = Node(key,value)
        self.cache[key] = new_node
        self._add_node(new_node)
        self.size += 1

        if self.size > self.capacity:

            lru = self.tail.prev

            self.evictions.append({
                "key": lru.key,
                "reason": "Least Recently Used",
                "time": time.time()
            })

            self._remove_node(lru)
            del self.cache[lru.key]
            self.size -= 1

    def stats(self):
        return {
            "hits": self.hits,
            "misses": self.misses,
            "current_size": self.size
        }
