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

__revision__ = "$LastChangedRevision: 421 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 15:16:53 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2010 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Hive Solutions Confidential Usage License (HSCUL)"
""" The license for the module """

import colony.libs.import_util

import hive_blog_main.main.hive_blog_main_exceptions

# runs the external imports
models = colony.libs.import_util.__import__("models")
web_mvc_utils = colony.libs.import_util.__import__("web_mvc_utils")

class CommentController:
    """
    The hive blog comment controller.
    """

    hive_blog_main_plugin = None
    """ The hive blog main plugin """

    hive_blog_main = None
    """ The hive blog main """

    def __init__(self, hive_blog_main_plugin, hive_blog_main):
        """
        Constructor of the class.

        @type hive_blog_main_plugin: HiveBlogMainPlugin
        @param hive_blog_main_plugin: The hive blog main plugin.
        @type hive_blog_main: HiveBlogMain
        @param hive_blog_main: The hive blog main.
        """

        self.hive_blog_main_plugin = hive_blog_main_plugin
        self.hive_blog_main = hive_blog_main

    @web_mvc_utils.serialize_exceptions("all")
    def handle_create(self, rest_request, parameters = {}):
        # retrieves the required controllers
        main_controller = self.hive_blog_main.main_controller

        # validates the captcha, regenerating the captcha
        if not main_controller._validate_captcha(rest_request, False):
            # raises the invalid captcha exception
            raise hive_blog_main.main.hive_blog_main_exceptions.InvalidCaptcha("invalid captcha value sent")

        # retrieves the comment from the rest request
        # and applies it to the comment entity
        comment = self.get_field(rest_request, "comment", {})
        comment_entity = models.Comment.new(comment)

        # sets the comment author as the session user in case
        # one is defined or the user specified in the comment
        session_user_entity = self.get_session_attribute(rest_request, "user.information")
        comment_entity.author = comment_entity.author or session_user_entity

        # stores the comment and its relations in the data source
        comment_entity.store(web_mvc_utils.PERSIST_SAVE_TYPE)

        # redirects to the post show path
        self.redirect_show(rest_request, comment_entity.post)
