from fastapi import APIRouter, Depends, HTTPException

from api.services.learner import LearnerService, get_learner_service

router = APIRouter()


@router.get("/knowledge")
async def get_knowledge(service: LearnerService = Depends(get_learner_service)) -> list[dict]:
    return service.list_knowledge()


@router.get("/stats")
async def get_stats(service: LearnerService = Depends(get_learner_service)) -> dict:
    return service.get_stats()


@router.post("/learn")
async def learn_concept(payload: dict, service: LearnerService = Depends(get_learner_service)) -> dict:
    try:
        concept_id = service.learn_concept(
            name=payload.get("name", ""),
            category=payload.get("category", ""),
            description=payload.get("description", ""),
            source=payload.get("source", ""),
            confidence=float(payload.get("confidence", 0.0)),
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return {"success": True, "concept_id": concept_id}
