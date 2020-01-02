#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Solutions Blog
# Copyright (c) 2008-2020 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2020 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Hive Solutions Confidential Usage License (HSCUL)"
""" The license for the module """

import colony

import hive_blog

from .base import BaseController

models = colony.__import__("models")
mvc_utils = colony.__import__("mvc_utils")

class CommentController(BaseController):

    @mvc_utils.serialize
    def create(self, request):
        # retrieves the required controllers
        main_controller = self.system.main_controller

        # validates the captcha, regenerating the captcha and raising
        # an exception in case the validation has failed
        if not main_controller._validate_captcha(request, False):
            raise hive_blog.InvalidCaptcha("invalid captcha value sent")

        # retrieves the comment from the request
        # and applies it to the comment entity
        comment = request.field("comment", {})
        comment = models.Comment.new(map = comment)

        # sets the comment author as the session user in case
        # one is defined or the user specified in the comment
        session_user = request.get_s("user.information")
        comment.author = comment.author or session_user

        # stores the comment and its relations in the data source
        # and then redirects the user to the post show path
        comment.create()
        self.redirect_show(request, comment.post)
