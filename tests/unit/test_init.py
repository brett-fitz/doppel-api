import doppel


def test_version():
    assert isinstance(doppel.__version__, str)
    assert doppel.__version__ == "0.1.0"


def test_public_api_exports():
    assert hasattr(doppel, "Doppel")
    assert hasattr(doppel, "AsyncDoppel")
    assert hasattr(doppel, "DoppelError")
    assert hasattr(doppel, "AuthenticationError")
    assert hasattr(doppel, "NotFoundError")
    assert hasattr(doppel, "RateLimitError")
    assert hasattr(doppel, "ValidationError")
