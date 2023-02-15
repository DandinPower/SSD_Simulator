from collections import deque

class BufferQueue:
    def __init__(self):
        self.buffer = deque()
    
    def add_data(self, data):
        self.buffer.append(data)
    
    def get_data(self):
        if len(self.buffer) < 4:
            return None
        data = tuple(self.buffer.popleft() for _ in range(4))
        return data