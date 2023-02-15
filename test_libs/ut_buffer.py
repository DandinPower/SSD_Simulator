from ftl.buffer import BufferQueue

def test_buffer_1():
    buffer = BufferQueue()
    buffer.add_data(1)
    buffer.add_data(2)
    assert buffer.get_data() == None