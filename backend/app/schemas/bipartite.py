from pydantic import BaseModel

class BipartiteMatchResponse(BaseModel):
    isBipartite: bool
    reason: str = None