from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, select
from sqlalchemy.orm import DeclarativeBase, sessionmaker, relationship

engine = create_engine("sqlite:///weather_app.db")

class Base(DeclarativeBase):
    pass

class Country(Base):
    __tablename__ = "countries"
    id = Column(Integer, primary_key=True)
    name_ua = Column(String, nullable=False)
    name_eng = Column(String, nullable=False)

    cities = relationship("City", back_populates="country", cascade="all, delete")

class UaPrefix(Base):
    __tablename__ = "ua_prefixes"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    cities = relationship("City", back_populates="ua_prefix", cascade="all, delete")


class EngPrefix(Base):
    __tablename__ = "eng_prefixes"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    cities = relationship("City", back_populates="eng_prefix", cascade="all, delete")

class City(Base):
    __tablename__ = "cities"
    id = Column(Integer, primary_key=True)
    name_ua = Column(String, nullable=False)
    name_eng = Column(String, nullable=False)
    country_id = Column(Integer, ForeignKey("countries.id"))
    ua_prefix_id = Column(Integer, ForeignKey("ua_prefixes.id"))
    eng_prefix_id = Column(Integer, ForeignKey("eng_prefixes.id"))

    country = relationship("Country", back_populates="cities")
    ua_prefix = relationship("UaPrefix", back_populates="cities")
    eng_prefix = relationship("EngPrefix", back_populates="cities")

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)

# import json 

# with open("static/configs/grouped_cities.json", mode="r", encoding="utf-8") as f:
#     data = json.load(f)

# with Session() as session:
#     for prefix, cities in data["eng"].items():
#         p = EngPrefix(name=prefix)
#         session.add(p)
#         for city in cities:
#             stmt = select(City).where(City.name_eng == city)
#             c = session.execute(stmt).scalars().first()
#             if c:
#                 p.cities.append(c)
#     session.commit()
        

# with Session() as session:
#     for country in data:
#         c= Country(name_ua = country["name"]["ua"], name_eng = country["name"]["eng"])
#         city_arr = []
#         for city_ua, city_eng in zip(country["cities"]["ua"], country["cities"]["eng"]):
#             city = City(name_ua = city_ua, name_eng = city_eng)
#             city_arr.append(city)
#         c.cities = city_arr
#         session.add(c)
#     session.commit()
