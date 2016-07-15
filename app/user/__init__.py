#!/usr/bin/env python
# encoding: utf-8

from flask import Blueprint

user = Blueprint('user', __name__)

import views
