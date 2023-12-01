import json
import xmltodict
from typing import Annotated
from typing import Union
from fastapi import FastAPI
from fastapi import Depends
from fastapi import Header
from fastapi import Request
from fastapi import HTTPException
from app import deal_schemas
from app.database import models
from app.database.engine import SessionLocal
from app.deal_processing import postprocess_deal_data

app = FastAPI()

def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/upload-deal/")
async def upload_deal(request: Request, content_type: Annotated[Union[str, None], Header()] = None, db: SessionLocal = Depends(get_db_session)):
    if content_type == 'application/json':
        incoming_data = await request.json()
    elif content_type == 'application/xml':
        xml_data = await request.body()
        parsed_xml_data = xmltodict.parse(xml_data)
        incoming_data = json.loads(json.dumps(parsed_xml_data))
    else:
        raise HTTPException(status_code=400, detail=f'Content type {content_type} not supported')

    if not incoming_data:
        raise HTTPException(status_code=400, detail="Valid deal data not found")

    new_deal = models.PreprocessingDeal(data=incoming_data)
    db.add(new_deal)
    db.commit()
    db.refresh(new_deal)
    return {"id": new_deal.id, "status": "saved"}


@app.get("/deals/preprocessed/")
def list_preprocessed_deals(db: SessionLocal = Depends(get_db_session)):
    deals = db.query(models.PreprocessingDeal).all()
    return deals


@app.post("/process-deal/{deal_id}")
def process_deal(deal_id: int, db: SessionLocal = Depends(get_db_session)):
    deal = db.query(models.PreprocessingDeal).filter(models.PreprocessingDeal.id == deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    postprocessed_data = postprocess_deal_data(deal.data)

    new_processed_deal = models.Deal(data=postprocessed_data)
    db.add(new_processed_deal)
    db.commit()
    db.refresh(new_processed_deal)
    return {"id": new_processed_deal.id, "status": "processed"}


@app.get("/deals/", response_model=list[deal_schemas.DealSchema])
def list_deals(db: SessionLocal = Depends(get_db_session)):
    deals = db.query(models.Deal).all()
    return deals


@app.get("/deal/{deal_id}", response_model=deal_schemas.DealSchema)
def get_deal(deal_id: int, db: SessionLocal = Depends(get_db_session)):
    deal = db.query(models.Deal).filter(models.Deal.id == deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    return deal
