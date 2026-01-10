"""
API router za odločanje (decision making) na podlagi podatkov - samo comparison-analysis
"""
from fastapi import APIRouter, HTTPException
from app.services.database_service import DatabaseService
from app.models.database import ComparisonAnalysis

router = APIRouter(prefix="/api/decision", tags=["decision"])


@router.get("/comparison-analysis")
async def get_comparison_analysis():
    """
    Vrne analizo primerjav - kateri model je najboljši v primerjavah
    """
    try:
        analysis = await DatabaseService.get_comparison_analysis()
        
        if not analysis:
            raise HTTPException(
                status_code=404,
                detail="Ni podatkov za analizo primerjav. Najprej naredite nekaj primerjav."
            )
        
        fastest = None
        cheapest = None
        if analysis:
            fastest_item = max(analysis, key=lambda x: x.times_fastest)
            cheapest_item = max(analysis, key=lambda x: x.times_cheapest)
            fastest = fastest_item.dict() if fastest_item else None
            cheapest = cheapest_item.dict() if cheapest_item else None
        
        return {
            "analysis": [a.dict() for a in analysis],
            "summary": {
                "total_models": len(analysis),
                "best_performance": {
                    "fastest": fastest,
                    "cheapest": cheapest
                }
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Napaka pri analizi: {str(e)}")
