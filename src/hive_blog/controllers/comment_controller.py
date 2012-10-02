#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Solutions Blog
# Copyright (C) 2010-2012 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2010-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Hive Solutions Confidential Usage License (HSCUL)"
""" The license for the module """

import colony.libs.import_util

import hive_blog.exceptions

models = colony.libs.import_util.__import__("models")
mvc_utils = colony.libs.import_util.__import__("mvc_utils")
controllers = colony.libs.import_util.__import__("controllers")

class CommentController(controllers.Controller):
    """
    The hive blog comment controller.
    """

    @mvc_utils.serialize_exceptions("all")
    def handle_create(self, rest_request, parameters = {}):
        # retrieves the required controllers
        main_controller = self.system.main_controller

        # validates the captcha, regenerating the captcha
        if not main_controller._validate_captcha(rest_request, False):
            # raises the invalid captcha exception
            raise hive_blog.exceptions.InvalidCaptcha("invalid captcha value sent")

        # retrieves the comment from the rest request
        # and applies it to the comment entity
        comment = self.get_field(rest_request, "comment", {})
        comment_entity = models.Comment.new(comment)

        # sets the comment author as the session user in case
        # one is defined or the user specified in the comment
        session_user_entity = self.get_session_attribute(rest_request, "user.information")
        comment_entity.author = comment_entity.author or session_user_entity

        # stores the comment and its relations in the data source
        comment_entity.store(mvc_utils.PERSIST_SAVE_TYPE)

        # redirects to the post show path
        self.redirect_show(rest_request, comment_entity.post)
