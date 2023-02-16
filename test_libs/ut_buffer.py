from ftl.buffer.write_buffer import WriteBuffer

def test_buffer_1():
    buffer = WriteBuffer()
    buffer.AddLba(1)
    buffer.AddLba(2)
    assert buffer.GetPage() == None

def test_buffer_2():
    buffer = WriteBuffer()
    buffer.AddLba(1)
    buffer.AddLba(2)
    buffer.AddLba(3)
    buffer.AddLba(4)
    assert buffer.GetPage() == (1,2,3,4)

def test_buffer_3():
    buffer = WriteBuffer()
    buffer.AddLba(1)
    buffer.AddLba(2)
    buffer.AddLba(3)
    buffer.AddLba(4)
    buffer.AddLba(1)
    buffer.AddLba(2)
    assert buffer.GetPage() == (1,2,3,4)
    assert buffer.GetPage() == None