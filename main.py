from libs.trace_iterator import TraceIterator

def main():
    iterator = TraceIterator()
    iterator.Load('trace/test.csv', 10)
    print(len(iterator))

if __name__ == "__main__":
    main()