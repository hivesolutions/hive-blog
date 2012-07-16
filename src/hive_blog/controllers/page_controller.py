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

import types

import colony.libs.import_util

# runs the external imports
models = colony.libs.import_util.__import__("models")
mvc_utils = colony.libs.import_util.__import__("mvc_utils")

class PageController:
    """
    The hive blog page controller.
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

    @mvc_utils.serialize_exceptions("all")
    def handle_show(self, rest_request, parameters = {}):
        # retrieves the page index pattern
        page_index = self.get_pattern(parameters, "page_index", types.IntType) or 1

        # retrieves the complete set of posts for the page
        # being requested accessing the data source, then
        # retrieves the number of pages for the blog
        posts = models.Post.find_for_page(page_index)
        number_pages = models.Post.get_number_pages()

        # retrieves the hosts posts path
        host_posts_path = self._get_host_path(rest_request, "/posts/")

        # determines the previous and next page indexes
        previous_page = page_index > 1 and page_index - 1 or None
        next_page = page_index < number_pages and page_index + 1 or None

        # processes the contents of the template file assigning the appropriate values to it
        template_file = self.retrieve_template_file("general.html.tpl", partial_page = "page/page_show_contents.html.tpl")
        template_file.assign("posts", posts)
        template_file.assign("host_posts_path", host_posts_path)
        template_file.assign("previous_page", previous_page)
        template_file.assign("next_page", next_page)
        self.process_set_contents(rest_request, template_file)
