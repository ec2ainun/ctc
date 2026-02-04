from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

def configure_logging(app: FastAPI):
    # For now, just logging to console. 
    # In production, you'd likely export to OTLP (e.g. Jaeger, Grafana Tempo, or Opik's collector if applicable)
    
    provider = TracerProvider()
    processor = SimpleSpanProcessor(ConsoleSpanExporter())
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)

    FastAPIInstrumentor.instrument_app(app)

    print("OpenTelemetry instrumentation enabled.")
