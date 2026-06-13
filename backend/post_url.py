from fastapi import APIRouter, HTTPException, status
from backend.schema import BrochureRequest
from AI import brochure


router = APIRouter(
    prefix="/brochure",
    tags = ["brochure"]
    )

@router.post("")
def create_brochure(request: BrochureRequest):
    try:
        result = brochure.create_brochure(
            company_name=request.company_name, 
            url=request.url
            )
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=str(e))
