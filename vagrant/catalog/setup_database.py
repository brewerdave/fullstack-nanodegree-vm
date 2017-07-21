#!/usr/bin/env python3

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import create_engine

Base = declarative_base()


class CharacterClass(Base):
    __tablename__ = 'character_class'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False, unique=True)


class GameVersion(Base):
    __tablename__ = 'game_version'

    name = Column(String(5), primary_key=True)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Build(Base):
    __tablename__ = 'build'

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    character_class_name = Column(String(20), ForeignKey("character_class.name"), nullable=False)
    character_class = relationship(CharacterClass)
    short_description = Column(String(500))
    long_description = Column(String(50000))
    url = Column(String(500))
    game_version = Column(String(5), ForeignKey("game_version.name"), nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    author = Column(String(100))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    favorites = relationship('Favorite', cascade='all, delete', backref='build')


class Favorite(Base):
    __tablename__ = 'favorite'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    build_id = Column(Integer, ForeignKey('build.id'))

    __table_args__ = (UniqueConstraint('user_id', 'build_id', name='_user_build_uc'),)

engine = create_engine('sqlite:///pathofexile.db')

Base.metadata.create_all(engine)
