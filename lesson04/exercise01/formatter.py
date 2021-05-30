import logging

from flask import Flask, request
from jaeger_client import Config
from opentracing.ext import tags
from opentracing.propagation import Format


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


app = Flask(__name__)
tracer = init_tracer("formatter")


@app.route("/format")
def format():
    # https://github.com/yurishkuro/opentracing-tutorial/tree/master/python/lesson04#read-baggage-in-formatter
    span_ctx = tracer.extract(Format.HTTP_HEADERS, request.headers)
    span_tags = {tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER}

    with tracer.start_active_span("format", child_of=span_ctx, tags=span_tags) as scope:

        # https://github.com/yurishkuro/opentracing-tutorial/tree/master/python/lesson04#whats-the-big-deal
        greeting = scope.span.get_baggage_item("greeting")

        if not greeting:
            greeting = "Hello"

        hello_to = request.args.get("helloTo")
        return f"{greeting} {hello_to}!"


if __name__ == "__main__":
    app.run(port=8081)
