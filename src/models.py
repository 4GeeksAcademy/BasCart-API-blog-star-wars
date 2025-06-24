from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date

db = SQLAlchemy()

class User(db.Model):

    __tablename__= "users"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(40), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    user_name: Mapped[str] = mapped_column(String(60), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    fecha_creacion: Mapped[date] = mapped_column(Date, default=date.today)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    favorites: Mapped[list["favorite"]] = relationship(back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "user_name": self.user_name,
            "email": self.email 
        }

class People(db.Model):
    __tablename__= "peoples"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    gender: Mapped[str] = mapped_column(String(250), nullable=False)
    skin_color: Mapped[str] = mapped_column(String(250), nullable=False)
    hair_color: Mapped[str] = mapped_column(String(250), nullable=False)
    height: Mapped[str] = mapped_column(String(250), nullable=False)
    eye_color: Mapped[str] = mapped_column(String(250), nullable=False)
    mass: Mapped[str] = mapped_column(String(250), nullable=False)
    homeworld: Mapped[int] = mapped_column(Integer, ForeignKey("planets.id"), nullable=False)
    birth_year: Mapped[str] = mapped_column(String(250), nullable=False)

    def serialize(self):
        return{
        
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "skin_color": self.skin_color,
            "hair_color": self.hair_color,
            "height": self.height,
            "eye_color": self.eye_color,
            "mass": self.mass,
            "homeworld": self.homeworld,
            "birth_year": self.birth_year
        }
    
class Planet(db.Model):
    __tablename__= "planets"

    id: Mapped[int]= mapped_column(primary_key=True, unique=True, autoincrement=True)
    climate: Mapped[str] = mapped_column(String(250), nullable=False)
    surface_water: Mapped[int]= mapped_column(Integer,nullable=False)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    diameter: Mapped[int]= mapped_column(Integer,nullable=False)
    rotation_period: Mapped[int]= mapped_column(Integer,nullable=False)
    terrain: Mapped[str] = mapped_column(String(250), nullable=False)
    gravity: Mapped[str] = mapped_column(String(250), nullable=False)
    orbital_period: Mapped[int]= mapped_column(Integer,nullable=False)
    population: Mapped[int]= mapped_column(Integer,nullable=False)

    def serialize(self):
        return{

            "id": self.id,
            "climate": self.climate,
	    	"surface_water": self.surface_water,
		    "name": self.name,
    		"diameter": self.diameter,
	    	"rotation_period": self.rotation_period,
		    "terrain": self.terrain,
    		"gravity": self.gravity,
	    	"orbital_period": self.orbital_period,
		    "population": self.population,

        }

class Specie(db.Model):
    __tablename__= "species"

    id: Mapped[int]= mapped_column(primary_key=True, unique=True, autoincrement=True)
    classification: Mapped[str]= mapped_column(String(150), nullable=False)
    name: Mapped[str]= mapped_column(String(150), nullable=False)
    designation: Mapped[str]= mapped_column(String(150), nullable=False)
    eye_colors: Mapped[str]= mapped_column(String(150), nullable=False)
    people: Mapped[int]= mapped_column(Integer, ForeignKey("peoples.id"), nullable=False)
    skin_colors: Mapped[str]= mapped_column(String(150), nullable=False)
    language: Mapped[str]= mapped_column(String(150), nullable=False)
    hair_colors: Mapped[str]= mapped_column(String(150), nullable=False)
    homeworld: Mapped[int]= mapped_column(Integer, ForeignKey("planets.id"), nullable=False)
    average_lifespan: Mapped[int]= mapped_column(Integer,nullable=False)
    average_height: Mapped[int]= mapped_column(Integer,nullable=False)
    
    def serialize(self):
        return{

            "classification": self.classification,
            "name": self.name,
            "designation": self.designation,
            "eye_colors": self.eye_colors,
            "people": self.people,
            "skin_colors": self.skin_colors,
            "language": self.language,
            "hair_colors": self.hair_colors,
            "homeworld": self.homeworld,
            "average_lifespan": self.average_lifespan,
            "average_height": self.average_lifespan,
    
        }
        
class Starship(db.Model):
    __tablename__= "starships"

    id: Mapped[int]= mapped_column(primary_key=True, unique=True, autoincrement=True)
    consumables: Mapped[str]= mapped_column(String(150), nullable=False)
    name: Mapped[str]= mapped_column(String(150), nullable=False)
    cargo_capacity: Mapped[int]= mapped_column(Integer,nullable=False)
    passengers: Mapped[int]= mapped_column(Integer,nullable=False)
    max_atmosphering_speed: Mapped[int]= mapped_column(Integer,nullable=False)
    crew: Mapped[str]= mapped_column(String(150), nullable=False)
    length: Mapped[int]= mapped_column(Integer,nullable=False)
    model: Mapped[str]= mapped_column(String(150), nullable=False)
    cost_in_credits: Mapped[int]= mapped_column(Integer,nullable=False)
    manufacturer: Mapped[str]= mapped_column(String(150), nullable=False)
    pilots: Mapped[str]= mapped_column(String(150), nullable=False)
    MGLT: Mapped[int]= mapped_column(Integer,nullable=False)
    starship_class: Mapped[str]= mapped_column(String(150), nullable=False)
    hyperdrive_rating: Mapped[int]= mapped_column(Integer,nullable=False)
    
    def serialize(self):
        return{

            "id": self.id,
            "consumables": self.consumables,
            "name": self.name,
            "cargo_capacity": self.cargo_capacity,
            "passengers": self.passengers,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "crew": self.crew,
            "length": self.length,
            "model": self.model,
            "cost_in_credits": self.cost_in_credits,
            "manufacturer": self.manufacturer,
            "pilots": self.pilots,
            "MGLT": self.MGLT,
            "starship_class": self.starship_class,
            "hyperdrive_rating": self.hyperdrive_rating 
        }
        
class Vehicle(db.Model):
    __tablename__= "vehicles"

    id: Mapped[int]= mapped_column(primary_key=True, unique=True, )
    consumables: Mapped[str]= mapped_column(String(150), nullable=False)
    name: Mapped[str]= mapped_column(String(150), nullable=False)
    cargo_capacity: Mapped[int]= mapped_column(Integer,nullable=False)
    passengers: Mapped[int]= mapped_column(Integer,nullable=False)
    max_atmosphering_speed: Mapped[int]= mapped_column(Integer,nullable=False)
    crew: Mapped[str]= mapped_column(String(150), nullable=False)
    length: Mapped[int]= mapped_column(Integer,nullable=False)
    model: Mapped[str]= mapped_column(String(150), nullable=False)
    cost_in_credits: Mapped[int]= mapped_column(Integer,nullable=False)
    manufacturer: Mapped[str]= mapped_column(String(150), nullable=False)
    vehicle_class: Mapped[str]= mapped_column(String(150), nullable=False)
    pilots: Mapped[str]= mapped_column(String(150), nullable=False)
    
    def serialize(self):
        return{

            "consumables": self.consumables,
	        "name": self.name,
            "cargo_capacity": self.cargo_capacity,
            "passengers": self.passengers,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "crew": self.crew,
            "length": self.length,
            "model": self.model,
            "cost_in_credits": self.cost_in_credits,
            "manufacturer": self.manufacturer,
            "vehicle_class": self.vehicle_class,
            "pilots": self.pilots
    
        }
    
class favorite(db.Model):
    __tablename__= "favorites"

    id: Mapped[int]= mapped_column(primary_key=True, unique=True, autoincrement=True)
    user_id: Mapped[int]= mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    people_id: Mapped[int]= mapped_column(Integer, ForeignKey("peoples.id"), nullable=False)
    planet_id: Mapped[int]= mapped_column(Integer, ForeignKey("planets.id"), nullable=False)
    specie_id: Mapped[int]= mapped_column(Integer, ForeignKey("species.id"), nullable=False)
    starship_id: Mapped[int]= mapped_column(Integer, ForeignKey("starships.id"), nullable=False)
    vehicle_id: Mapped[int]= mapped_column(Integer, ForeignKey("vehicles.id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="favorites")
    peoples: Mapped[list["People"]] = relationship(backref="favorite")
    planets: Mapped[list["Planet"]] = relationship(backref="favorite")
    species: Mapped[list["Specie"]] = relationship(backref="favorite")
    starships: Mapped[list["Starship"]] = relationship(backref="favorite")
    vehicles: Mapped[list["Vehicle"]] = relationship(backref="favorite")

    def serialize(self):
        return{
            "id": self.id,
            "user_id": self.user_id,
            "people_id": self.people_id,
            "planet_id": self.planet_id,
            "specie_id": self.specie_id,
            "starship_id": self.starship_id,
            "vehicles_id":self.vehicle_id
        }