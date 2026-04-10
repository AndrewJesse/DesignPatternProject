# Application Layer — Use Cases (Services).
#
# Use cases orchestrate the flow of data to and from domain entities
# through ports. They answer "WHAT does the app do?" but not "HOW is
# data stored or retrieved?" — that detail is behind the port.
#
# Use cases depend on:
#   - domain objects (Payload)
#   - port interfaces (PayloadWriter)
# They NEVER depend on concrete adapters.
from datetime import datetime

from ..ports import PayloadWriter
from domain.transform import Payload


def write_user_input(writer: PayloadWriter, user_text: str) -> Payload:
    payload = Payload(
        text=user_text.strip(),
        date=datetime.now().isoformat(timespec="seconds"),
    )
    writer.write(payload)
    return payload
