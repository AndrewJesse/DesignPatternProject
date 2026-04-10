# Adapters Layer (aka Infrastructure) — the outermost ring of the hexagon.
#
# Adapters are concrete implementations of the port interfaces defined in
# the application layer. They handle real-world I/O: databases, files,
# APIs, message queues, etc.
#
# Adapters depend INWARD on domain objects and port interfaces.
# The application layer never imports from adapters — only the
# composition root (main.py) wires them together.
