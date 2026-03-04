#!/usr/bin/env python3
"""Security helper utilities for Star Office backend.

P1 step: extraction without behavior change.
"""

from __future__ import annotations

import hmac
import os


def is_production_mode() -> bool:
    env = (os.getenv("STAR_OFFICE_ENV") or os.getenv("FLASK_ENV") or "").strip().lower()
    return env in {"prod", "production"}


def is_strong_secret(secret: str) -> bool:
    if not secret:
        return False
    secret = secret.strip()
    if len(secret) < 24:
        return False
    weak_markers = {"change-me", "dev", "example", "test", "default"}
    low = secret.lower()
    return not any(m in low for m in weak_markers)


def is_strong_drawer_pass(pwd: str) -> bool:
    if not pwd:
        return False
    pwd = pwd.strip()
    if pwd == "1234":
        return False
    return len(pwd) >= 8


def parse_csv_set(value: str | None) -> set[str]:
    if not value:
        return set()
    return {x.strip() for x in str(value).split(",") if x and x.strip()}


def feature_enabled(name: str, default: bool = False) -> bool:
    v = os.getenv(name)
    if v is None:
        return default
    return str(v).strip().lower() in {"1", "true", "yes", "on"}


def is_valid_bearer(token: str, accepted_tokens: set[str]) -> bool:
    t = (token or "").strip()
    if not t or not accepted_tokens:
        return False
    for at in accepted_tokens:
        if hmac.compare_digest(t, at):
            return True
    return False
