from dataclasses import dataclass
from typing import Optional


@dataclass
class AdvisResult:
    cpr: str
    navn: str
    haendelse: str
    dato: str
    url_til_advis: Optional[str] = None