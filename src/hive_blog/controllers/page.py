#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Solutions Blog
# Copyright (c) 2008-2019 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2019 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Hive Solutions Confidential Usage License (HSCUL)"
""" The license for the module """

import colony

from .base import BaseController

models = colony.__import__("models")
mvc_utils = colony.__import__("mvc_utils")

class PageController(BaseController):

    @mvc_utils.serialize
    def show(self, request, index = 1):
        # retrieves the complete set of posts for the page
        # being requested accessing the data source, then
        # retrieves the number of pages for the blog
        posts = models.Post.find_for_page(index)
        number_pages = models.Post.get_number_pages()

        # retrieves the hosts posts path
        host_posts_path = self._get_host_path(request, "/posts/")

        # determines the previous and next page indexes
        previous_page = index > 1 and index - 1 or None
        next_page = index < number_pages and index + 1 or None

        # sets the appropriate template structure in order to
        # show the page as it's supposed to be shown
        self._template(
            request = request,
            partial_page = "page/show.html.tpl",
            posts = posts,
            host_posts_path = host_posts_path,
            previous_page = previous_page,
            next_page = next_page
        )
