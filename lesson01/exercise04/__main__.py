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
        # ref: https://github.com/yurishkuro/opentracing-tutorial/tree/master/python/lesson01#annotate-the-trace-with-tags-and-logs
        # The recommended solution is to annotate spans with tags or logs.
        # A tag is a key-value pair that provides certain metadata about the
        # span. A log is similar to a regular log statement, it contains a
        # timestamp and some data, but it is associated with span from which
        # it was logged.

        # The tags are meant to describe attributes of the span that apply to
        # the whole duration of the span
        span.set_tag('hello-to', hello_to)

        hello_str = f'Hello, {hello_to}!'
        span.log_kv({'event': 'string-format', 'value': hello_str})

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
