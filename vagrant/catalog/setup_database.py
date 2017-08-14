#!/usr/bin/env python3

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import create_engine
from flask_login import UserMixin
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
import random
import string

Base = declarative_base()
secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))


class CharacterClass(Base):
    __tablename__ = 'character_class'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False, unique=True)


class GameVersion(Base):
    __tablename__ = 'game_version'

    name = Column(String(5), primary_key=True)


class User(Base, UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False, index=True)
    picture = Column(String(250))

    def generate_auth_token(self, expiration=3600):
        s = Serializer(secret_key, expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            # Valid Token, but expired
            return None
        except BadSignature:
            # Invalid Token
            return None
        user_id = data['id']
        return user_id


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

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'title': self.title,
            'character_class_name': self.character_class_name,
            'short_description': self.short_description,
            'long_description': self.long_description,
            'url': self.url,
            'game_version': self.game_version,
            'time_created': self.time_created,
            'time_updated': self.time_updated,
            'author': self.author
        }


class Favorite(Base):
    __tablename__ = 'favorite'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    build_id = Column(Integer, ForeignKey('build.id'))

    __table_args__ = (UniqueConstraint('user_id', 'build_id', name='_user_build_uc'),)

engine = create_engine('sqlite:///pathofexile.db')

Base.metadata.create_all(engine)
