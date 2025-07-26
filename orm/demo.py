from sqlalchemy import create_engine

connection = create_engine("mysql+mysqlconnector://root:password@localhost:3306/demo")

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import (
    DeclarativeBase, 
    Mapped, 
    Session, 
    mapped_column, 
    relationship
)

class Base(DeclarativeBase):
    pass

class Animal(Base):
    __tablename__ = "animals"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    name: Mapped[str] = mapped_column(String(255))

    food: Mapped["Food"] = relationship(back_populates="animal")

class Food(Base):
    __tablename__ = "food"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    name: Mapped[str] = mapped_column(String(255))
    
    animal_id: Mapped[int] = mapped_column(ForeignKey("animals.id"))

    animal: Mapped["Animal"] = relationship(back_populates="food")

with Session(connection) as session:
    dog = Animal(
        name="Dog",
        food=Food(name="Bone")
    )

    bird = Animal(
        name="Bird",
        food=Food(name="Seed")
    )

    chicken = Animal(name="Chicken")

    session.add_all([dog, bird, chicken])

    session.commit()

from sqlalchemy import select

with Session(connection) as session:
    stmt = select(Animal.name, Food.name).join(Food.animal)

    results = session.execute(stmt).all()

    print(results)