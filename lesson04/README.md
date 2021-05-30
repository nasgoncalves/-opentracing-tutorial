# Notes

* In Lesson 3 we have seen how span context is propagated over the wire between different applications. It is not hard to see that this process can be generalized to passing more than just the tracing context. With OpenTracing instrumentation in place, we can support general purpose distributed context propagation where we associate some metadata with the transaction and make that metadata available anywhere in the distributed call graph. In OpenTracing this metadata is called baggage, to highlight the fact that it is carried over in-band with all RPC requests, just like baggage.
