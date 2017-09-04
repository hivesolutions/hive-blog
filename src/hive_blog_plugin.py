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

__author__ = "João Magalhães <joamag@hive.pt>"
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

import colony

class HiveBlogPlugin(colony.Plugin):
    """
    The main class for the Hive Blog Main plugin.
    """

    id = "pt.hive.cronus.plugins.hive_blog"
    name = "Hive Blog"
    description = "The plugin that offers the hive blog"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.CPYTHON_ENVIRONMENT
    ]
    capabilities = [
        "mvc_service"
    ]
    dependencies = [
        colony.PluginDependency("pt.hive.colony.plugins.mvc.utils"),
        colony.PluginDependency("pt.hive.colony.plugins.security.captcha"),
        colony.PluginDependency("pt.hive.colony.plugins.api.openid"),
        colony.PluginDependency("pt.hive.colony.plugins.api.twitter"),
        colony.PluginDependency("pt.hive.colony.plugins.api.facebook")
    ]
    main_modules = [
        "hive_blog"
    ]

    def load_plugin(self):
        colony.Plugin.load_plugin(self)
        import hive_blog
        self.system = hive_blog.HiveBlog(self)

    def end_load_plugin(self):
        colony.Plugin.end_load_plugin(self)
        self.system.load_components()

    def unload_plugin(self):
        colony.Plugin.unload_plugin(self)
        self.system.unload_components()

    def get_patterns(self):
        """
        Retrieves the tuple of regular expressions to be used as patterns,
        to the mvc service. The tuple should relate the route with the handler
        method/function.

        :rtype: Tuple
        :return: The tuple of regular expressions to be used as patterns,
        to the mvc service.
        """

        return self.system.get_patterns()

    def get_resource_patterns(self):
        """
        Retrieves the tuple of regular expressions to be used as resource patterns,
        to the mvc service. The tuple should relate the route with the base
        file system path to be used.

        :rtype: Tuple
        :return: The tuple of regular expressions to be used as resource patterns,
        to the mvc service.
        """

        return self.system.get_resource_patterns()
