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

import types

import colony

import hive_blog

import base

models = colony.__import__("models")
mvc_utils = colony.__import__("mvc_utils")

class PostController(base.BaseController):

    @mvc_utils.serialize
    @mvc_utils.validated("post.create")
    def new(self, request):
        # processes the contents of the template file assigning the
        # appropriate values to it
        template_file = self.retrieve_template_file(
            "general.html.tpl",
            partial_page = "post/post_new_contents.html.tpl"
        )
        template_file.assign("post", None)
        self.process_set_contents(request, template_file)

    @mvc_utils.serialize
    def create(self, request):
        # retrieves the required controllers
        main_controller = self.system.main_controller

        # retrieves the post from the rest request
        post = self.get_field(request, "post", {})

        # retrieves the preview flag from the post parameters
        post_parameters = self.get_entity_map_parameters(post)
        preview = post_parameters.get("preview", False)

        # validates the captcha, regenerating the captcha and raising
        # an exception in case the validation has failed
        if not preview and not main_controller._validate_captcha(request, False):
            raise hive_blog.InvalidCaptcha("invalid captcha value sent")

        # creates a post entity with the post
        # retrieved from the rest request
        post_entity = models.Post.new(post)

        # sets the post author as the session user
        session_user_entity = self.get_session_attribute(request, "user.information")
        post_entity.author = session_user_entity

        # stores the post and its relations in the data source
        # in case the preview flag is not set
        not preview and post_entity.store(mvc_utils.PERSIST_SAVE)

        # processes the contents of the template file assigning the
        # appropriate values to it
        template_file = self.retrieve_template_file(
            "general.html.tpl",
            partial_page = "post/post_new_contents.html.tpl"
        )
        template_file.assign("preview", True)
        template_file.assign("post", post_entity)
        self.process_set_contents(request, template_file)

    @mvc_utils.serialize
    def show(self, request, id):
        # creates the return address from the request path
        return_address = self._get_path(request)

        # retrieves the hosts posts path
        host_posts_path = self._get_host_path(request, "/posts/")

        # retrieves the posts entity specified in the pattern
        post_object_id = self.get_pattern(parameters, "post_object_id", types.IntType)
        post_entity = models.Post.get_for_show(post_object_id)

        # processes the contents of the template file assigning the
        # appropriate values to it
        template_file = self.retrieve_template_file(
            "general.html.tpl",
            partial_page = "post/post_show_contents.html.tpl"
        )
        template_file.assign("return_address", return_address)
        template_file.assign("host_posts_path", host_posts_path)
        template_file.assign("post", post_entity)
        self.process_set_contents(request, template_file, assign_session = True)
