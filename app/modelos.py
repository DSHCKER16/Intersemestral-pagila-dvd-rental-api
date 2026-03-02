from sqlalchemy import Column, Integer, SmallInteger, String, DateTime, Date, Numeric, Text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.base_datos import Base


class Customer(Base):
    __tablename__ = "customer"
    __table_args__ = {'extend_existing': True}
    
    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    store_id = Column(SmallInteger, ForeignKey("store.store_id"), nullable=False)
    first_name = Column(String(45), nullable=False)
    last_name = Column(String(45), nullable=False)
    email = Column(String(50))
    address_id = Column(SmallInteger, nullable=False)
    activebool = Column(String(1), default='Y')
    create_date = Column(Date, default=datetime.now)
    last_update = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)
    active = Column(Integer)
    
    rentals = relationship("Rental", back_populates="customer")
    payments = relationship("Payment", back_populates="customer")


class Staff(Base):
    __tablename__ = "staff"
    __table_args__ = {'extend_existing': True}
    
    staff_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(45), nullable=False)
    last_name = Column(String(45), nullable=False)
    address_id = Column(SmallInteger, nullable=False)
    email = Column(String(50))
    store_id = Column(SmallInteger, ForeignKey("store.store_id"))
    active = Column(String(1), default='Y')
    username = Column(String(16), nullable=False)
    password = Column(String(40))
    last_update = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)
    picture = Column(Text)
    
    rentals = relationship("Rental", back_populates="staff")
    payments = relationship("Payment", back_populates="staff")


class Store(Base):
    __tablename__ = "store"
    __table_args__ = {'extend_existing': True}
    
    store_id = Column(Integer, primary_key=True, autoincrement=True)
    manager_staff_id = Column(SmallInteger, nullable=False)
    address_id = Column(SmallInteger, nullable=False)
    last_update = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)
    
    inventory_items = relationship("Inventory", back_populates="store")


class Film(Base):
    __tablename__ = "film"
    __table_args__ = {'extend_existing': True}
    
    film_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    release_year = Column(Integer)
    language_id = Column(SmallInteger, nullable=False)
    original_language_id = Column(SmallInteger)
    rental_duration = Column(SmallInteger, default=3, nullable=False)
    rental_rate = Column(Numeric(4, 2), default=4.99, nullable=False)
    length = Column(SmallInteger)
    replacement_cost = Column(Numeric(5, 2), default=19.99, nullable=False)
    rating = Column(String(10), default='G')
    last_update = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)
    special_features = Column(Text)
    fulltext = Column(Text)
    
    inventory_items = relationship("Inventory", back_populates="film")


class Inventory(Base):
    __tablename__ = "inventory"
    __table_args__ = {'extend_existing': True}
    
    inventory_id = Column(Integer, primary_key=True, autoincrement=True)
    film_id = Column(SmallInteger, ForeignKey("film.film_id"), nullable=False)
    store_id = Column(SmallInteger, ForeignKey("store.store_id"), nullable=False)
    last_update = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)
    
    film = relationship("Film", back_populates="inventory_items")
    store = relationship("Store", back_populates="inventory_items")
    rentals = relationship("Rental", back_populates="inventory")


class Rental(Base):
    __tablename__ = "rental"
    __table_args__ = {'extend_existing': True}
    
    rental_id = Column(Integer, primary_key=True, autoincrement=True)
    rental_date = Column(TIMESTAMP, nullable=False, default=datetime.now)
    inventory_id = Column(Integer, ForeignKey("inventory.inventory_id"), nullable=False)
    customer_id = Column(SmallInteger, ForeignKey("customer.customer_id"), nullable=False)
    return_date = Column(TIMESTAMP)
    staff_id = Column(SmallInteger, ForeignKey("staff.staff_id"), nullable=False)
    last_update = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)
    
    customer = relationship("Customer", back_populates="rentals")
    staff = relationship("Staff", back_populates="rentals")
    inventory = relationship("Inventory", back_populates="rentals")
    payments = relationship("Payment", back_populates="rental")


class Payment(Base):
    __tablename__ = "payment"
    __table_args__ = {'extend_existing': True}
    
    payment_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(SmallInteger, ForeignKey("customer.customer_id"), nullable=False)
    staff_id = Column(SmallInteger, ForeignKey("staff.staff_id"), nullable=False)
    rental_id = Column(Integer, ForeignKey("rental.rental_id"))
    amount = Column(Numeric(5, 2), nullable=False)
    payment_date = Column(TIMESTAMP, nullable=False, default=datetime.now)
    
    customer = relationship("Customer", back_populates="payments")
    staff = relationship("Staff", back_populates="payments")
    rental = relationship("Rental", back_populates="payments")
