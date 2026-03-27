from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.kildarestreet import get_politician_id, get_debates
from app.claude import analyse_promise
from app.promises import get_all_promises

router = APIRouter()


class CheckRequest(BaseModel):
    politician_name: str
    promise: str
    promise_source: str = ""


@router.post("/check")
async def check_promise(req: CheckRequest):
    politician_id = await get_politician_id(req.politician_name)
    if not politician_id:
        raise HTTPException(status_code=404, detail=f"Politician '{req.politician_name}' not found in KildareStreet")

    speeches = await get_debates(politician_id)
    if not speeches:
        raise HTTPException(status_code=404, detail="No Dáil debate records found for this politician")

    result = await analyse_promise(
        politician_name=req.politician_name,
        promise=req.promise,
        promise_source=req.promise_source,
        speeches=speeches,
    )
    return result


@router.get("/promises")
async def list_promises():
    return get_all_promises()
