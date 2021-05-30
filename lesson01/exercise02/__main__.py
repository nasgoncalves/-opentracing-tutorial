import sys
import opentracing

tracer = opentracing.tracer

def say_hello(hello_to):
    # span = tracer.start_span('say-hello')
    # hello_str = f"Hello, {hello_to}!"
    # print(hello_str)
    # span.finish()

    with tracer.start_span('say-hello') as span:
        hello_str = f"Hello, {hello_to}!"
        print(hello_str)

assert len(sys.argv) == 2

hello_to = sys.argv[1]
say_hello(hello_to)
