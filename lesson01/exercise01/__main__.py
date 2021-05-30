import sys

def say_hello(hello_to):
    hello_str = f"Hello, {hello_to}!"
    print(hello_str)

assert len(sys.argv) == 2

hello_to = sys.argv[1]
say_hello(hello_to)
