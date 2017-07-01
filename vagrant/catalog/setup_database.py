import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class WeaponType(Base):
    __tablename__ = 'weaponType'

    name = Column(String(80), nullable=False, unique=True)
    id = Column(Integer, primary_key=True)


class ArmorType(Base):
    __tablename__ = 'armorType'

    name = Column(String(80), nullable=False, unique=True)
    id = Column(Integer, primary_key=True)


class Weapon(Base):
    __tablename__ = 'weapon'

    name = Column(String(80), nullable=False, unique=True)
    id = Column(Integer, primary_key=True)
    weaponTypeID = Column(Integer, ForeignKey('weaponType.id'))
    weaponType = relationship(WeaponType)
    reqLevel = Column(Integer)
    minDamage = Column(Integer)
    maxDamage = Column(Integer)
    attacksPerSecond = Column(Float)
    damagePerSecond = Column(Float)
    reqStrength = Column(Integer)
    reqDexterity = Column(Integer)
    reqIntelligence = Column(Integer)


class Armor(Base):
    __tablename__ = 'armor'

    name = Column(String(80), nullable=False, unique=True)
    id = Column(Integer, primary_key=True)
    armorTypeID = Column(Integer, ForeignKey('armorType.id'))
    armorType = relationship(ArmorType)
    reqLevel = Column(Integer)
    armorAmount = Column(Integer)
    evasionRating = Column(Integer)
    energyShield = Column(Integer)
    reqStrength = Column(Integer)
    reqDexterity = Column(Integer)
    reqIntelligence = Column(Integer)

engine = create_engine('sqlite:///pathofexile.db')

Base.metadata.create_all(engine)