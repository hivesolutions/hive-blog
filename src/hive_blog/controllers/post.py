#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Solutions Blog
# Copyright (C) 2008-2014 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2014 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Hive Solutions Confidential Usage License (HSCUL)"
""" The license for the module """

import colony

import hive_blog

import base

models = colony.__import__("models")
mvc_utils = colony.__import__("mvc_utils")

class PostController(base.BaseController):

    @mvc_utils.serialize
    @mvc_utils.validated("post.create")
    def new(self, request):
        self._template(
            request = request,
            partial_page = "post/new.html.tpl",
            post = None
        )

    @mvc_utils.serialize
    def create(self, request):
        # retrieves the required controllers and the value for the preview
        # field that defined is the current creation is a preview or not
        main_controller = self.system.main_controller
        preview = request.field("preview", False, cast = bool)

        # validates the captcha, regenerating the captcha and raising
        # an exception in case the validation has failed
        if not preview and not main_controller._validate_captcha(request, False):
            raise hive_blog.InvalidCaptcha("invalid captcha value sent")

        # creates a post entity with the post
        # retrieved from the rest request
        post = request.field("post", {})
        post = models.Post.new(map = post)

        # sets the post author as the session user
        session_user = request.get_s("user.information")
        post.author = session_user

        # stores the post and its relations in the data source
        # in case the preview flag is not set
        not preview and post.create()

        # processes the contents of the template file assigning the
        # appropriate values to it
        self._template(
            request = request,
            partial_page = "post/new.html.tpl",
            preview = True,
            post = post
        )

    @mvc_utils.serialize
    def show(self, request, id):
        return_address = self._get_path(request)
        host_posts_path = self._get_host_path(request, "/posts/")
        post = models.Post.get_for_show(id)
        self._template(
            request = request,
            partial_page = "post/show.html.tpl",
            return_address = return_address,
            host_posts_path = host_posts_path,
            post = post
        )
