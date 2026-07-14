from fastapi import APIRouter

from learning.autonomous_learning import AutonomousLearner

router = APIRouter()


@router.post("/learning/run")
async def run_learning() -> dict:
    learner = AutonomousLearner()
    processed_files = learner.scan_for_new_files()
    return {
        "status": "completed",
        "processed_count": len(processed_files),
        "files": [path.name for path in processed_files],
    }
