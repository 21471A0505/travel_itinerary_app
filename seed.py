from database import SessionLocal
import models

db = SessionLocal()

def seed():
    db.query(models.Itinerary).delete()

    for region in ['Phuket', 'Krabi']:
        for nights in range(2, 9):
            itinerary = models.Itinerary(name=f"{region} {nights}N Trip", region=region, nights=nights)
            db.add(itinerary)
            db.flush()
            for day_number in range(1, nights+1):
                day = models.Day(itinerary_id=itinerary.id, day_number=day_number)
                db.add(day)
                db.flush()
                db.add(models.HotelStay(day_id=day.id, hotel_name="Hotel XYZ", address=f"{region} Main St"))
                db.add(models.Transfer(day_id=day.id, from_location="Airport", to_location=region, mode="Car"))
                db.add(models.Activity(day_id=day.id, name="Beach Visit", description="Enjoy the local beach"))

    db.commit()
    print("Database seeded.")

if __name__ == "__main__":
    seed()
