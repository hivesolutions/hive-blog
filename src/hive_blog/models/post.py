#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Solutions Blog
# Copyright (c) 2008-2017 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2017 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Hive Solutions Confidential Usage License (HSCUL)"
""" The license for the module """

import math
import datetime

import colony

from .root_entity import RootEntity

DEFAULT_DATE_FORMAT = "%Y-%m-%d"
""" The default date format """

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

models = colony.__import__("models")
mvc_utils = colony.__import__("mvc_utils")

class Post(RootEntity):
    """
    The post class, representing the
    post entity.
    """

    date = dict(
        type = "date",
        mandatory = True
    )
    """ The date of the post """

    title = dict(
        type = "text",
        mandatory = True
    )
    """ The title of the post """

    contents = dict(
        type = "text",
        mandatory = True
    )
    """ The contents of the post """

    contents_abstract = dict(
        type = "text"
    )
    """ The contents of the abstract of the post """

    author = dict(
        type = "relation",
        fetch_type = "lazy",
        mandatory = True,
        secure = True,
        persist_type = mvc_utils.PERSIST_ASSOCIATE
    )
    """ The author of the post """

    comments = dict(
        type = "relation",
        fetch_type = "lazy",
        secure = True,
        persist_type = mvc_utils.PERSIST_NONE
    )
    """ The comment for the post """

    def __init__(self):
        """
        Constructor of the class.
        """

        RootEntity.__init__(self)
        self.date = datetime.datetime.utcnow()

    @staticmethod
    def _relation_author():
        return dict(
            type = "to-one",
            target = models.User,
            reverse = "posts",
            is_mapper = True
        )

    @staticmethod
    def _relation_comments():
        return dict(
            type = "to-many",
            target = models.Comment,
            reverse = "post"
        )

    def set_validation(self):
        """
        Sets the validation structures for the current structure.
        """

        # adds the inherited validations
        RootEntity.set_validation(self)

        # adds the validation methods to the date attribute
        self.add_validation("date", "not_none", True)

        # adds the validation methods to the title attribute
        self.add_validation("title", "not_none", True)
        self.add_validation("title", "not_empty")

        # adds the validation methods to the contents attribute
        self.add_validation("contents", "not_none", True)
        self.add_validation("contents", "not_empty")

        # adds the validation methods to the contents abstract attribute
        self.add_validation("contents_abstract", "not_empty")

    @staticmethod
    def get_for_show(post_object_id, *args, **kwargs):
        """
        Retrieves the specified instance with the necessary relations
        loaded for its usage in a context where it is being shown.

        :type post_object_id: int
        :param post_object_id: The post object id.
        :rtype: Post
        :return: The post.
        """

        # defines the filter to retrieve the post with
        filter = dict(
            eager = dict(
                author = dict(),
                tags = dict(),
                comments = dict(
                    eager = (
                        "author",
                    )
                )
            )
        )

        # retrieves the post and then returns it to the
        # caller method (as requested by the method)
        post = Post.get(post_object_id, filter, *args, **kwargs)
        return post

    @staticmethod
    def find_for_list():
        """
        Retrieves all the posts in the blog with the necessary relations
        loaded for its usage in a context where they are being listed.

        :rtype: List
        :return: The blog posts.
        """

        # creates the filter map
        filter = dict(
            order_by = "date",
            eager = dict(
                author = dict(),
                tags = dict(),
                comments = dict(
                    eager = (
                        "author",
                    )
                )
            )
        )

        # retrieves the posts in the blog
        posts = models.Post.find(filter)

        # returns the posts
        return posts

    @staticmethod
    def find_for_page(page_index, number_records_page = 3):
        """
        Retrieves the posts that belong to the requested page, using the
        specified page size.

        :type page_index: int
        :param page_index: The number of the page being requested.
        :type number_records_page: int
        :param number_records_page: Number of posts in a page.
        :rtype: List
        :return: The posts that belong to the specified page.
        """

        # calculates the start record from the current page index and
        # the number of records
        start_record = (page_index - 1) * number_records_page

        # creates the filter map
        filter = dict(
            range = (start_record, number_records_page),
            order_by = "date",
            eager = dict(
                author = dict(),
                tags = dict(),
                comments = dict(
                    eager = (
                        "author",
                    )
                )
            )
        )

        # retrieves the posts for the given page
        posts = models.Post.find(filter)

        # returns the posts
        return posts

    @staticmethod
    def get_number_pages(number_records_page = 3):
        """
        Retrieves the number of pages in the blog by counting the number
        of blog posts in the data source and dividing it by the specified
        page size.

        :type number_records_page: int
        :param number_records_page: Number of posts in a page.
        :rtype: int
        :return: The number of pages.
        """

        # retrieves the post count and uses it to calculate
        # the number of pages in the blog
        post_count = models.Post.count()
        number_pages = int(math.ceil(float(post_count) / number_records_page))

        # returns the number of pages
        return number_pages

    def get_day(self):
        """
        Retrieves the day when the comment was made.

        :rtype: int
        :return: The day when the comment was made.
        """

        # in case there is no date set, must return
        # immediately with invalid value
        if not self.date: return None

        # returns the date day
        return self.date.day

    def get_month(self):
        """
        Retrieves the month when the comment was made
        (represented in abbreviated text, eg: "January"
        is represented as "Jan").

        :rtype: String
        :return: The month when the comment was made.
        """

        # in case there is no date set, must return
        # immediately with invalid value
        if not self.date: return None

        # returns the data month abbreviated
        return MONTH_NUMBER_MAP[self.date.month]

    def get_date_formatted(self):
        """
        Retrieves the data formatted to a string
        in the "YYYY-MM-DD" representation.

        :rtype: String
        :return: The formatted date.
        """

        # formats the date using the default format
        date_formatted = self.date.strftime(DEFAULT_DATE_FORMAT)

        # returns the date formatted
        return date_formatted
