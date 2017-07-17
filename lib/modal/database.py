#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Project: tornado-project-template
@File: database.py
@Author: kehr <kehr.china@gmail.com>
@Date: 2017-07-17 11:28:14
@Last Modified by: kehr
@Last Modified time: 2017-07-17 14:43:01
@Description:
"""
from peewee import MySQLDatabase
from peewee import Model
from peewee import CharField
from peewee import PrimaryKeyField
from peewee import IntegerField
from peewee import FloatField
from peewee import IntegerField
from peewee import DateTimeField


database = MySQLDatabase('db', **{'host': 'localhost', 'password': 'password', 'port': 3306, 'user': 'root'})

# Create your own database modal
