# `model/` — domain model and pure logic

## Purpose

Holds **types and functions that express business rules** with **no I/O**: no files, databases, network, UI, or hardware drivers.

This is the innermost layer. It should stay **stable** and **easy to test** in isolation.

## What belongs here

- **Dataclasses** (or similar) for domain data, e.g. `Payload`.
- **Pure functions** that transform data, e.g. `normalize`, with no side effects beyond returning a value.

## What does not belong here

- Imports from **`app`**, **`data`**, or any adapter/UI package.
- Code that reads or writes disks, talks to PLCs, opens sockets, or touches Qt/widgets.

## Dependencies

- May use the Python standard library and small, domain-agnostic helpers if you keep the boundary clear.
- **Must not** depend on outer layers (dependency rule: everything else may depend on `model`; `model` depends on nothing in this app).

## In this repo

- `transform.py` — defines `Payload` and `normalize`.
