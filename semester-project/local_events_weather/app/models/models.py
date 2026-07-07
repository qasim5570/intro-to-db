from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.postgres import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    plans = relationship("UserEventPlan", back_populates="user")


class City(Base):
    __tablename__ = "cities"

    city_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)

    venues = relationship("Venue", back_populates="city")


class Venue(Base):
    __tablename__ = "venues"

    venue_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    address = Column(String(255))
    city_id = Column(Integer, ForeignKey("cities.city_id"), nullable=False)

    city = relationship("City", back_populates="venues")
    events = relationship("Event", back_populates="venue")


class Category(Base):
    __tablename__ = "categories"

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)

    events = relationship("Event", back_populates="category")


class Event(Base):
    __tablename__ = "events"

    event_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    venue_id = Column(Integer, ForeignKey("venues.venue_id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.category_id"), nullable=False)
    source_event_id = Column(String(100))

    venue = relationship("Venue", back_populates="events")
    category = relationship("Category", back_populates="events")
    plans = relationship("UserEventPlan", back_populates="event")


class UserEventPlan(Base):
    __tablename__ = "user_event_plans"

    plan_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.event_id"), nullable=False)
    status = Column(String(50), nullable=False)  # e.g., "interested", "going"
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="plans")
    event = relationship("Event", back_populates="plans")
