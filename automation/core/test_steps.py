from contextlib import contextmanager


@contextmanager
def step(description: str):
    print(f"\nSTEP: {description}")
    yield