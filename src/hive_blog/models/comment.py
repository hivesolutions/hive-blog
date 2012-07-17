#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Solutions Blog
# Copyright (C) 2010 Hive Solutions Lda.
#
# This file is part of Hive Solutions Blog.
#
# Hive Solutions Blog is confidential and property of Hive Solutions Lda.,
# its usage is constrained by the terms of the Hive Solutions
# Confidential Usage License.
#
# Hive Solutions Blog should not be distributed under any circumstances,
# violation of this may imply legal action.
#
# If you have any questions regarding the terms of this license please
# refer to <http://www.hive.pt/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt> & Tiago Silva <tsilva@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2010 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Hive Solutions Confidential Usage License (HSCUL)"
""" The license for the module """

import datetime

import colony.libs.import_util

import root_entity

MONTH_NUMBER_MAP = {
    1 : "Jan",
    2 : "Feb",
    3 : "Mar",
    4 : "Apr",
    5 : "May",
    6 : "Jun",
    7 : "Jul",
    8: "Aug",
    9 : "Sep",
    10 : "Oct",
    11 : "Nov",
    12 : "Dec"
}
""" The map relating the month number with the "mini" month name """

models = colony.libs.import_util.__import__("models")
mvc_utils = colony.libs.import_util.__import__("mvc_utils")

class Comment(root_entity.RootEntity):
    """
    The comment class, representing the comment entity.
    """

    date = {
        "data_type" : "date",
        "mandatory" : True,
        "secure" : True
    }
    """ The date of the comment """

    contents = {
        "data_type" : "text",
        "mandatory" : True
    }
    """ The contents of the comment """

    author = {
        "data_type" : "relation",
        "fetch_type" : "lazy",
        "mandatory" : True,
        "persist_type" : mvc_utils.PERSIST_SAVE_TYPE | mvc_utils.PERSIST_ASSOCIATE_TYPE
    }
    """ The author of the comment """

    post = {
        "data_type" : "relation",
        "fetch_type" : "lazy",
        "mandatory" : True,
        "persist_type" : mvc_utils.PERSIST_ASSOCIATE_TYPE
    }
    """ The post that contains the comment """

    in_reply_to = {
        "data_type" : "relation",
        "fetch_type" : "lazy",
        "mandatory" : True,
        "secure" : True,
        "persist_type" : mvc_utils.PERSIST_ASSOCIATE_TYPE
    }
    """ The comment for which this comment is a reply """

    replies = {
        "data_type" : "relation",
        "fetch_type" : "lazy",
        "secure" : True,
        "persist_type" : mvc_utils.PERSIST_NONE_TYPE
    }
    """ The comment replies to the comment """

    def __init__(self):
        """
        Constructor of the class.
        """

        root_entity.RootEntity.__init__(self)
        self.date = datetime.datetime.utcnow()

    @staticmethod
    def _relation_author():
        return {
            "type" : "to-one",
            "target" : models.User,
            "reverse" : "comments",
            "is_mapper" : True
        }

    @staticmethod
    def _relation_post():
        return {
            "type" : "to-one",
            "target" : models.Post,
            "reverse" : "posts",
            "is_mapper" : True
        }

    @staticmethod
    def _relation_in_reply_to():
        return {
            "type" : "to-one",
            "target" : models.Comment,
            "reverse" : "replies",
            "is_mapper" : True
        }

    @staticmethod
    def _relation_replies():
        return {
            "type" : "to-many",
            "target" : models.Comment,
            "reverse" : "in_reply_to"
        }

    def set_validation(self):
        """
        Sets the validation structures for the current structure.
        """

        # adds the inherited validations
        root_entity.RootEntity.set_validation(self)

        # adds the validation methods to the date attribute
        self.add_validation_method("date", "not_none", True)

        # adds the validation methods to the contents attribute
        self.add_validation_method("contents", "not_none", True)
        self.add_validation_method("contents", "not_empty")

    def get_day(self):
        """
        Retrieves the day when the comment was made.

        @rtype: int
        @return: The day when the comment was made.
        """

        # in case there is no date set
        if not self.date:
            # returns invalid
            return None

        # returns the date day
        return self.date.day

    def get_month(self):
        """
        Retrieves the month when the comment was made
        (represented in abbreviated text, eg: "January"
        is represented as "Jan").

        @rtype: String
        @return: The month when the comment was made.
        """

        # in case there is no date set
        if not self.date:
            # returns invalid
            return None

        # returns the data month abbreviated
        return MONTH_NUMBER_MAP[self.date.month]
