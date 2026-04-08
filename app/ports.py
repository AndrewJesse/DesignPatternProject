from typing import Protocol

from model.transform import Payload


class DataSource(Protocol):
    def read(self) -> Payload: ...


class DataSink(Protocol):
    def write(self, data: Payload) -> None: ...
