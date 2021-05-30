import logging
import sys
import time

import requests
from jaeger_client import Config


def init_tracer(service):
    logging.getLogger("").handlers = []
    logging.basicConfig(format="%(message)s", level=logging.DEBUG)

    config = Config(
        config={
            "sampler": {
                "type": "const",
                "param": 1,
            },
            "logging": True,
        },
        service_name=service,
    )

    # this call also sets opentracing.tracer
    return config.initialize_tracer()


def say_hello(hello_to):
    with tracer.start_active_span("say-hello") as scope:
        scope.span.set_tag("hello-to", hello_to)
        hello_str = format_string(hello_to)
        print_hello(hello_str)


def format_string(hello_to):
    with tracer.start_active_span("format") as scope:
        hello_str = http_get(8081, "format", "helloTo", hello_to)
        scope.span.log_kv({"event": "string-format", "value": hello_str})
        return hello_str


def print_hello(hello_str):
    with tracer.start_active_span("println") as scope:
        http_get(8082, "publish", "helloStr", hello_str)
        scope.span.log_kv({"event": "println"})


def http_get(port, path, param, value):
    url = f"http://localhost:{port}/{path}"
    r = requests.get(url, params={param: value})
    assert r.status_code == 200
    return r.text


# main
assert len(sys.argv) == 2

tracer = init_tracer("hello-world")

hello_to = sys.argv[1]
say_hello(hello_to)

# yield to IOLoop to flush the spans
time.sleep(2)
tracer.close()
