import logging
import sys
import time

from jaeger_client import Config


def init_tracer(service):
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)

    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
        },
        service_name=service,
    )

    # this call also sets opentracing.tracer
    return config.initialize_tracer()

tracer = init_tracer('hello-world')


def say_hello(hello_to):
    with tracer.start_span('say-hello') as span:
        hello_str = f"Hello, {hello_to}!"
        print(hello_str)

assert len(sys.argv) == 2

hello_to = sys.argv[1]
say_hello(hello_to)

time.sleep(2)
tracer.close()
