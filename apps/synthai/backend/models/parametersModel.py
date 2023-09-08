from typing import Literal
from pydantic import BaseModel


class Parameters(BaseModel):
    language: Literal["EN", "SP"]
    max_sequence_length: int
    temperature: float
    top_k: float
    top_p: float
    clusters_number: int
    chunk_size: int
    chunk_overlap: int
    from_page: int = 0
    to_page: int = -1
