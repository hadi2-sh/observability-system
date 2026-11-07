\
from fastapi import FastAPI, Request
from time import perf_counter
import logging
import json

from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

# OpenTelemetry imports
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = FastAPI()


# Configure OpenTelemetry tracing
resource = Resource.create({
    "service.name": "observability-app"
})

tracer_provider = TracerProvider(resource=resource)

otlp_exporter = OTLPSpanExporter(
    endpoint="tempo:4317",
    insecure=True
)

tracer_provider.add_span_processor(
    BatchSpanProcessor(otlp_exporter)
)

trace.set_tracer_provider(tracer_provider)

FastAPIInstrumentor.instrument_app(app)


# Prometheus metrics
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total number of HTTP requests"
)

REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds"
)


# Middleware: Track requests, duration, and trace ID
@app.middleware("http")
async def track_requests(request: Request, call_next):
    start_time = perf_counter()

    response = await call_next(request)

    duration = perf_counter() - start_time

    REQUEST_COUNT.inc()
    REQUEST_DURATION.observe(duration)

    # Get the current OpenTelemetry trace ID
    current_span = trace.get_current_span()
    span_context = current_span.get_span_context()

    trace_id = (
        format(span_context.trace_id, "032x")
        if span_context.is_valid
        else None
    )

    # Log request details as JSON
    logging.info(json.dumps({
        "method": request.method,
        "path": request.url.path,
        "duration": round(duration, 4),
        "status_code": response.status_code,
        "trace_id": trace_id
    }))

    return response


# Health endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}


# Prometheus metrics endpoint
@app.get("/metrics")
def get_metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )


# Test error endpoint
@app.get("/test-error")
def test_error():
    try:
        result = 10 / 0
        return {"result": result}

    except Exception as error:
        logging.error(f"An error occurred: {error}")
        return {"error": "Something went wrong"}
