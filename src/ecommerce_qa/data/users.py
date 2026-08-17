"""Demo accounts published by SauceDemo."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class User:
    username: str
    password: str = "secret_sauce"


STANDARD_USER = User(username="standard_user")
LOCKED_OUT_USER = User(username="locked_out_user")
