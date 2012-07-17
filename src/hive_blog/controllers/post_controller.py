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

import types

import colony.libs.import_util

import hive_blog.main.hive_blog_exceptions

models = colony.libs.import_util.__import__("models")
mvc_utils = colony.libs.import_util.__import__("mvc_utils")

class PostController:
    """
    The hive blog post controller.
    """

    hive_blog_plugin = None
    """ The hive blog plugin """

    hive_blog = None
    """ The hive blog """

    def __init__(self, hive_blog_plugin, hive_blog):
        """
        Constructor of the class.

        @type hive_blog_plugin: HiveBlogPlugin
        @param hive_blog_plugin: The hive blog plugin.
        @type hive_blog: HiveBlog
        @param hive_blog: The hive blog.
        """

        self.hive_blog_plugin = hive_blog_plugin
        self.hive_blog = hive_blog

    def validate(self, rest_request, parameters, validation_parameters):
        # returns the result of the require permission call
        return self.hive_blog.require_permissions(self, rest_request, validation_parameters)

    @mvc_utils.serialize_exceptions("all")
    @mvc_utils.validated_method("post.create")
    def handle_new(self, rest_request, parameters = {}):
        # processes the contents of the template file assigning the appropriate values to it
        template_file = self.retrieve_template_file("general.html.tpl", partial_page = "post/post_new_contents.html.tpl")
        template_file.assign("post", None)
        self.process_set_contents(rest_request, template_file)

    @mvc_utils.serialize_exceptions("all")
    def handle_create(self, rest_request, parameters = {}):
        # retrieves the required controllers
        main_controller = self.hive_blog.main_controller

        # retrieves the post from the rest request
        post = self.get_field(rest_request, "post", {})

        # retrieves the preview flag from the post parameters
        post_parameters = self.get_entity_map_parameters(post)
        preview = post_parameters.get("preview", False)

        # in case this is not a preview validates the captcha,
        # regenerating the captcha if invalid
        if not preview and not main_controller._validate_captcha(rest_request, False):
            # raises the invalid captcha exception
            raise hive_blog.main.hive_blog_exceptions.InvalidCaptcha("invalid captcha value sent")

        # creates a post entity with the post
        # retrieved from the rest request
        post_entity = models.Post.new(post)

        # sets the post author as the session user
        session_user_entity = self.get_session_attribute(rest_request, "user.information")
        post_entity.author = session_user_entity

        # stores the post and its relations in the data source
        # in case the preview flag is not set
        not preview and post_entity.store(mvc_utils.PERSIST_SAVE_TYPE)

        # processes the contents of the template file assigning the appropriate values to it
        template_file = self.retrieve_template_file("general.html.tpl", partial_page = "post/post_new_contents.html.tpl")
        template_file.assign("preview", True)
        template_file.assign("post", post_entity)
        self.process_set_contents(rest_request, template_file)

    @mvc_utils.serialize_exceptions("all")
    def handle_show(self, rest_request, parameters = {}):
        # creates the return address from the request path
        return_address = self._get_path(rest_request)

        # retrieves the hosts posts path
        host_posts_path = self._get_host_path(rest_request, "/posts/")

        # retrieves the posts entity specified in the pattern
        post_object_id = self.get_pattern(parameters, "post_object_id", types.IntType)
        post_entity = models.Post.get_for_show(post_object_id)

        # processes the contents of the template file assigning the appropriate values to it
        template_file = self.retrieve_template_file("general.html.tpl", partial_page = "post/post_show_contents.html.tpl")
        template_file.assign("return_address", return_address)
        template_file.assign("host_posts_path", host_posts_path)
        template_file.assign("post", post_entity)
        self.process_set_contents(rest_request, template_file, assign_session = True)
