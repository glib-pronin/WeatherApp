from .database_config import City, EngPrefix, UaPrefix, Country, Session
from sqlalchemy import select, and_, or_

def get_city_for_completer(lang, prefix):
    with Session() as session:
        stmt = select(EngPrefix).where(EngPrefix.name == prefix) if lang == "eng" else select(UaPrefix).where(UaPrefix.name == prefix)
        result = session.execute(stmt).scalars().first()
        if result:
            cities =  [city.name_eng if lang == "eng" else city.name_ua for city in result.cities]
            return cities
        
def get_countries(lang):
    with Session() as session:
        stmt = select(Country)
        result = session.execute(stmt).scalars().all()
        res_dict = {}
        for country in result:
            res_dict[country.id] = country.name_eng if lang == "eng" else country.name_ua
        return res_dict
    
def get_cities_by_country_id(lang, country_id):
    with Session() as session:
        result = session.get(Country, country_id)
        cities =  [city.name_eng if lang == "eng" else city.name_ua for city in result.cities]
        return cities
    
def get_eng_city_country(country_id, city_ua):
    with Session() as session:
        country = session.get(Country, country_id)
        city = session.execute(select(City.name_eng).where(and_(City.name_ua == city_ua, City.country_id == country_id))).scalars().first()
        return [country.name_eng, city]
    
def get_city_eng_ua_names(city_name):
    with Session() as session:
        city = session.execute(select(City).where(or_(City.name_eng == city_name, City.name_ua == city_name))).scalars().first()
        return [city.name_eng, city.name_ua]