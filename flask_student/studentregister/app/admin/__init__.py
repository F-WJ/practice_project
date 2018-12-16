# _*_ coding: utf-8 _*_
__author__ = 'FWJ'
__date__ = 2017 / 12 / 24
from flask import Blueprint
admin = Blueprint("admin", __name__)

import app.admin.views


