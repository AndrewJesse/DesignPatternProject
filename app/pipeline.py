from app.ports import DataSource, DataSink
from model.transform import Payload, normalize


def run(source: DataSource, sink: DataSink) -> Payload:
    raw = source.read()
    out = normalize(raw)
    sink.write(out)
    return out
