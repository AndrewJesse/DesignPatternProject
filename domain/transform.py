# Domain Layer — the innermost ring of the hexagon.
#
# Domain objects are pure data structures and business rules.
# They have ZERO dependencies on application, adapters, or any framework.
# Every other layer may import from domain, but domain never imports
# from anything outside itself.
from dataclasses import dataclass


@dataclass
class Payload:
    text: str = ""
    date: str | None = None
