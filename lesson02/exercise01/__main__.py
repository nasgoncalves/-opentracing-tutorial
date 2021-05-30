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
        span.set_tag('hello-to', hello_to)
        hello_str = format_string(span, hello_to)
        print_hello(span, hello_str)

def format_string(root_span, hello_to):
    with tracer.start_span('format', child_of=root_span) as span:
        hello_str = 'Hello, %s!' % hello_to
        span.log_kv({'event': 'string-format', 'value': hello_str})
        return hello_str

def print_hello(root_span, hello_str):
    with tracer.start_span('println', child_of=root_span) as span:
        print(hello_str)
        span.log_kv({'event': 'println'})

assert len(sys.argv) == 2

hello_to = sys.argv[1]
say_hello(hello_to)

# Jaeger Tracer is primarily designed for long-running server processes,
# so it has an internal buffer of spans that is flushed by a background thread.
# Since our program exits immediately, it may not have time to flush the spans
# to Jaeger backend

time.sleep(2)
tracer.close()
