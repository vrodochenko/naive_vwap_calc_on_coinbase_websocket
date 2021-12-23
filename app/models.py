from typing import Literal  # noqa: TYP001

from pydantic import BaseModel, confloat, constr


class MatchModel(BaseModel):
    """Let us do very basic sanity-checks to ignore malformed matches."""

    type: Literal["match", "last_match"]
    product_id: constr(  # type: ignore
        max_length=7, regex="[A-Z]{3}-[A-Z]{3}"  # noqa F772
    )
    size: confloat(gt=0, lt=1e9)  # type: ignore
    price: confloat(gt=0, lt=1e7)  # type: ignore
