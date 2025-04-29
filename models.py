from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Itinerary(Base):
    __tablename__ = "itineraries"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    region = Column(String, nullable=False)
    nights = Column(Integer, nullable=False)

    days = relationship("Day", back_populates="itinerary", cascade="all, delete")

class Day(Base):
    __tablename__ = "days"
    id = Column(Integer, primary_key=True)
    itinerary_id = Column(Integer, ForeignKey("itineraries.id"))
    day_number = Column(Integer)

    itinerary = relationship("Itinerary", back_populates="days")
    hotels = relationship("HotelStay", back_populates="day", cascade="all, delete")
    transfers = relationship("Transfer", back_populates="day", cascade="all, delete")
    activities = relationship("Activity", back_populates="day", cascade="all, delete")

class HotelStay(Base):
    __tablename__ = "hotel_stays"
    id = Column(Integer, primary_key=True)
    day_id = Column(Integer, ForeignKey("days.id"))
    hotel_name = Column(String)
    address = Column(String)

    day = relationship("Day", back_populates="hotels")

class Transfer(Base):
    __tablename__ = "transfers"
    id = Column(Integer, primary_key=True)
    day_id = Column(Integer, ForeignKey("days.id"))
    from_location = Column(String)
    to_location = Column(String)
    mode = Column(String)

    day = relationship("Day", back_populates="transfers")

class Activity(Base):
    __tablename__ = "activities"
    id = Column(Integer, primary_key=True)
    day_id = Column(Integer, ForeignKey("days.id"))
    name = Column(String)
    description = Column(String)

    day = relationship("Day", back_populates="activities")
