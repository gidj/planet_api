# -*- coding: utf-8 -*-

import re

from flask import url_for
from sqlalchemy.orm import validates

from . import db
from errors import InvalidNameError, InvalidAssetTypeError, InvalidAssetClassError

import itertools

class Asset(db.Model):
    VALID_TYPES = {
        u'satellite': (u'dove', u'rapideye'),
        u'antenna'  : (u'dish', u'yagi'),
    }
    VALID_CLASSES = list(itertools.chain.from_iterable(VALID_TYPES.values()))

    __tablename__ = u"assets"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    asset_type = db.Column(db.String(64))
    asset_class = db.Column(db.String(64))

    def __init__(self, name, asset_type, asset_class):
        self.name=name
        self.asset_type=asset_type
        self.asset_class=asset_class

    def __repr__(self):
        return u'<Asset: {} - {}[{}]>'.format(self.name, self.asset_type, self.asset_class)

    def __unicode__(self):
        return u'Asset: {}'.format(self.name)

    @validates('name')
    def validate_name(self, key, name):
        if not self.valid_name(name):
            raise InvalidNameError
        return name

    @validates('asset_type')
    def validate_asset_type(self, key, asset_type):
        if asset_type not in self.VALID_TYPES:
            raise InvalidAssetTypeError
        return asset_type

    @validates('asset_class')
    def validate_asset_class(self, key, asset_class):
        if asset_class not in self.VALID_TYPES.get(self.asset_type, ()):
            raise InvalidAssetClassError
        return asset_class

    def to_json(self):
        json_asset = {
            u'name': self.name,
            u'type': self.asset_type,
            u'class': self.asset_class,
            u'link': url_for('api.assets', asset_name=self.name, _external=True),
        }
        return json_asset

    @classmethod
    def from_json(cls, json_post):
        name = json_post.get('name')
        asset_type = json_post.get('type')
        asset_class = json_post.get('class')

        if cls.query.filter_by(name=name).count() > 0:
            from api_v1.errors import ResourceExistsError
            raise ResourceExistsError

        instance = cls(name=name, asset_type=asset_type, asset_class=asset_class)
        db.session.add(instance)
        db.session.commit()
        return instance

    @staticmethod
    def valid_name(name):
        NAME_REGEX = r'^[a-zA-Z0-9][a-zA-Z0-9_-]{3,63}$'
        return bool(re.compile(NAME_REGEX).match(name))



