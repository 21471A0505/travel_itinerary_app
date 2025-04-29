from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import models, schemas

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/itineraries", response_model=schemas.ItineraryOut)
def create_itinerary(itinerary: schemas.ItineraryCreate, db: Session = Depends(get_db)):
    new_itinerary = models.Itinerary(
        name=itinerary.name,
        region=itinerary.region,
        nights=itinerary.nights,
    )
    db.add(new_itinerary)
    db.flush()

    for day_data in itinerary.days:
        day = models.Day(itinerary_id=new_itinerary.id, day_number=day_data.day_number)
        db.add(day)
        db.flush()
        for hotel in day_data.hotels:
            db.add(models.HotelStay(day_id=day.id, **hotel.dict()))
        for transfer in day_data.transfers:
            db.add(models.Transfer(day_id=day.id, **transfer.dict()))
        for activity in day_data.activities:
            db.add(models.Activity(day_id=day.id, **activity.dict()))

    db.commit()
    db.refresh(new_itinerary)
    return new_itinerary

@app.get("/itineraries", response_model=List[schemas.ItineraryOut])
def get_all_itineraries(db: Session = Depends(get_db)):
    return db.query(models.Itinerary).all()

@app.get("/recommendations/{nights}", response_model=List[schemas.ItineraryOut])
def get_recommendations(nights: int, db: Session = Depends(get_db)):
    results = db.query(models.Itinerary).filter(models.Itinerary.nights == nights).all()
    if not results:
        raise HTTPException(status_code=404, detail="No itinerary found for given nights")
    return results
