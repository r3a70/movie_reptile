from sqlalchemy import Column, String, Integer, ForeignKey, BigInteger, Text
from sqlalchemy.orm import relationship
from .database import Base


class Movies(Base):
    __tablename__ = 'movies'

    id = Column(BigInteger(), primary_key=True, index=True)
    name = Column(String(255))
    post_url = Column(String(255))
    post_image = Column(String(255))
    tags_id = Column(BigInteger(), ForeignKey("tags.id", ondelete='CASCADE'))
    age = Column(String(255))
    country_id = Column(BigInteger(), ForeignKey("country.id", ondelete='CASCADE'))
    imdb = Column(String(255))
    rating = Column(String(255))
    site_rate = Column(String(255))
    like = Column(Integer())
    dislike = Column(Integer())
    actors_id = Column(BigInteger(), ForeignKey("actors.id", ondelete='CASCADE'))
    director = Column(String(255))
    story = Column(Text())
    links_id = Column(BigInteger(), ForeignKey("links.id", ondelete='CASCADE'))


class Tags(Base):
    __tablename__ = "tags"

    id = Column(BigInteger(), primary_key=True, index=True)
    movie_id = Column(Integer())
    tag = Column(String())


class Country(Base):
    __tablename__ = "country"

    id = Column(BigInteger(), primary_key=True, index=True)
    movie_id = Column(Integer())
    country = Column(String())


class Actors(Base):
    __tablename__ = "actors"

    id = Column(BigInteger(), primary_key=True, index=True)
    movie_id = Column(Integer())
    actor = Column(String())


class Links(Base):
    __tablename__ = "links"

    id = Column(BigInteger(), primary_key=True, index=True)
    movie_id = Column(Integer())
    link = Column(String())




