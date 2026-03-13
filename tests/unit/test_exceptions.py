from doppel.exceptions import (
    AuthenticationError,
    ConflictError,
    DoppelError,
    ForbiddenError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
    exception_for_status,
)


class TestExceptionHierarchy:
    def test_all_inherit_from_doppel_error(self):
        for cls in (
            ValidationError,
            AuthenticationError,
            ForbiddenError,
            NotFoundError,
            ConflictError,
            RateLimitError,
            ServerError,
        ):
            assert issubclass(cls, DoppelError)

    def test_doppel_error_attributes(self):
        exc = DoppelError(
            "test",
            status_code=400,
            errors={"field": "bad"},
            error_messages=["oops"],
            response_body={"detail": "oops"},
        )
        assert str(exc) == "test"
        assert exc.status_code == 400
        assert exc.errors == {"field": "bad"}
        assert exc.error_messages == ["oops"]
        assert exc.response_body == {"detail": "oops"}

    def test_doppel_error_defaults(self):
        exc = DoppelError("bare")
        assert exc.status_code is None
        assert exc.errors == {}
        assert exc.error_messages == []
        assert exc.response_body is None

    def test_rate_limit_error_retry_after(self):
        exc = RateLimitError("slow down", retry_after=60.0, status_code=429)
        assert exc.retry_after == 60.0
        assert exc.status_code == 429


class TestExceptionForStatus:
    def test_known_codes(self):
        assert exception_for_status(400) is ValidationError
        assert exception_for_status(401) is AuthenticationError
        assert exception_for_status(403) is ForbiddenError
        assert exception_for_status(404) is NotFoundError
        assert exception_for_status(409) is ConflictError
        assert exception_for_status(429) is RateLimitError

    def test_5xx_returns_server_error(self):
        assert exception_for_status(500) is ServerError
        assert exception_for_status(502) is ServerError
        assert exception_for_status(503) is ServerError

    def test_unknown_returns_doppel_error(self):
        assert exception_for_status(418) is DoppelError
        assert exception_for_status(422) is DoppelError
