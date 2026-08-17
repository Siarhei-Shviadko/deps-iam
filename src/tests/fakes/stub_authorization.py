import contextlib
import json

from deps_iam.domain.exceptions import UserNotFoundError
from deps_iam.domain.services.registration import RegistrationService
from deps_iam.domain.services.user import UserService

HARDCODED_SUBJECT = "00000000-0000-0000-0000-000000000001"
HARDCODED_ORGANISATION = "Local Organisation"

_PAYLOAD = {
    "email": "local@deps.local",
    "first_name": "Local",
    "last_name": "User",
    "roles": [],
    "groups": ["deprecated_field"],
    "subject": HARDCODED_SUBJECT,
    "organisation": HARDCODED_ORGANISATION,
}


class StubAuthorizationService:
    def __init__(self, user_service: UserService, register_service: RegistrationService):
        self._user_service = user_service
        self._register_service = register_service

    def authorize(self, request_headers) -> str:
        payload = dict(_PAYLOAD)
        self._ensure_stub_user_exists(payload)
        token = json.dumps(payload)
        payload["deps_token"] = token
        return json.dumps(payload)

    def _ensure_stub_user_exists(self, payload: dict) -> None:
        with contextlib.suppress(UserNotFoundError):
            self._user_service.get(user_pk=HARDCODED_SUBJECT)
            return
        self._register_service.register_user(payload, is_personal=False)
