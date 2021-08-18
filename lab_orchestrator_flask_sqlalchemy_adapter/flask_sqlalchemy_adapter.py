"""
Warning: Untested. This is just an example.
"""

from typing import Type, Optional

import sqlalchemy as sql
from flask_sqlalchemy import SQLAlchemy

from lab_orchestrator_lib.database.adapter import Adapter


_DB: Optional[SQLAlchemy] = None


def get_db() -> SQLAlchemy:
    if _DB is None:
        raise Exception("_DB is None. SQLAlchemy is not configured correctly.")
    return _DB


def config_flask_sqlalchemy(db: SQLAlchemy):
    global _DB
    _DB = db


class FlaskSQLAlchemyAdapter(Adapter):
    @classmethod
    def filter(cls, **kwargs):
        return cls.get_cls().filter_by(**kwargs).all()

    @classmethod
    def get_by_attr(cls, attr, value):
        return cls.get_cls().filter_by(**{attr: value}).first()

    @classmethod
    def save(cls, obj):
        """Warning: Saves all updated items."""
        get_db().session.commit()

    @staticmethod
    def get_cls() -> get_db().Model:
        raise NotImplementedError()

    @classmethod
    def create(cls, **kwargs):
        obj = cls.get_cls()(**kwargs)
        get_db().session.add(obj)
        get_db().session.commit()
        return obj

    @classmethod
    def get_all(cls):
        return cls.get_cls().query.all()

    @classmethod
    def get(cls, identifier):
        return cls.get_cls().query.get(identifier)

    @classmethod
    def delete(cls, identifier):
        obj = cls.get_cls().objects.get(identifier)
        get_db().session.delete(obj)
        get_db().session.commit()


def flask_sqlalchemy_adapter_factory(cls):
    class Intern(FlaskSQLAlchemyAdapter):
        @staticmethod
        def get_cls():
            return cls
    Intern.__name__ = f"{cls.__name__}FlaskSQLAlchemyAdapter"
    return Intern


class DockerImage(get_db().Model):
    __tablename__ = 'docker_image'
    id = sql.Column(sql.Integer, primary_key=True)
    name = sql.Column(sql.String(32), unique=True)
    description = sql.Column(sql.String(128))
    url = sql.Column(sql.String(256))


class Lab(get_db().Model):
    __tablename__ = 'lab'
    id = sql.Column(sql.Integer, primary_key=True)
    name = sql.Column(sql.String(32), unique=True)
    namespace_prefix = sql.Column(sql.String(32), unique=True)
    description = sql.Column(sql.String(128))
    docker_image_id = sql.Column(sql.Integer, sql.ForeignKey('docker_image.id'))
    docker_image_name = sql.Column(sql.String(32))


class LabInstance(get_db().Model):
    __tablename__ = 'lab_instance'
    id = sql.Column(sql.Integer, primary_key=True)
    lab_id = sql.Column(sql.Integer, sql.ForeignKey('lab.id'))
    user_id = sql.Column(sql.Integer, sql.ForeignKey('users.id'))


DockerImageFlaskSQLAlchemyAdapter = flask_sqlalchemy_adapter_factory(DockerImage)
LabFlaskSQLAlchemyAdapter = flask_sqlalchemy_adapter_factory(Lab)
LabInstanceFlaskSQLAlchemyAdapter = flask_sqlalchemy_adapter_factory(LabInstance)
