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

__author__ = "João Magalhães <joamag@hive.pt>"
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

import colony.base.system
import colony.base.decorators

class HiveBlogPlugin(colony.base.system.Plugin):
    """
    The main class for the Hive Blog Main plugin.
    """

    id = "pt.hive.cronus.plugins.hive_blog"
    name = "Hive Blog"
    description = "The plugin that offers the hive blog"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.system.CPYTHON_ENVIRONMENT
    ]
    capabilities = [
        "mvc_service"
    ]
    dependencies = [
        colony.base.system.PluginDependency("pt.hive.colony.plugins.mvc.utils", "1.x.x"),
        colony.base.system.PluginDependency("pt.hive.colony.plugins.security.captcha", "1.x.x"),
        colony.base.system.PluginDependency("pt.hive.colony.plugins.api.openid", "1.x.x"),
        colony.base.system.PluginDependency("pt.hive.colony.plugins.api.twitter", "1.x.x"),
        colony.base.system.PluginDependency("pt.hive.colony.plugins.api.facebook", "1.x.x")
    ]
    main_modules = [
        "hive_blog.exceptions",
        "hive_blog.system"
    ]

    hive_blog = None
    """ The hive blog """

    mvc_utils_plugin = None
    """ The mvc utils plugin """

    security_captcha_plugin = None
    """ The security captcha plugin """

    api_openid_plugin = None
    """ The api openid plugin """

    api_twitter_plugin = None
    """ The api twitter plugin """

    api_facebook_plugin = None
    """ The api facebook plugin """

    def load_plugin(self):
        colony.base.system.Plugin.load_plugin(self)
        import hive_blog.system
        self.hive_blog = hive_blog.system.HiveBlog(self)

    def end_load_plugin(self):
        colony.base.system.Plugin.end_load_plugin(self)
        self.hive_blog.load_components()

    def unload_plugin(self):
        colony.base.system.Plugin.unload_plugin(self)
        self.hive_blog.unload_components()

    @colony.base.decorators.inject_dependencies
    def dependency_injected(self, plugin):
        colony.base.system.Plugin.dependency_injected(self, plugin)

    def get_patterns(self):
        """
        Retrieves the tuple of regular expressions to be used as patterns,
        to the mvc service. The tuple should relate the route with the handler
        method/function.

        @rtype: Tuple
        @return: The tuple of regular expressions to be used as patterns,
        to the mvc service.
        """

        return self.hive_blog.get_patterns()

    def get_communication_patterns(self):
        """
        Retrieves the tuple of regular expressions to be used as communication patterns,
        to the mvc service. The tuple should relate the route with a tuple
        containing the data handler, the connection changed handler and the name
        of the connection.

        @rtype: Tuple
        @return: The tuple of regular expressions to be used as communication patterns,
        to the mvc service.
        """

        return self.hive_blog.get_communication_patterns()

    def get_resource_patterns(self):
        """
        Retrieves the tuple of regular expressions to be used as resource patterns,
        to the mvc service. The tuple should relate the route with the base
        file system path to be used.

        @rtype: Tuple
        @return: The tuple of regular expressions to be used as resource patterns,
        to the mvc service.
        """

        return self.hive_blog.get_resource_patterns()

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.mvc.utils")
    def set_mvc_utils_plugin(self, mvc_utils_plugin):
        self.mvc_utils_plugin = mvc_utils_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.security.captcha")
    def set_security_captcha_plugin(self, security_captcha_plugin):
        self.security_captcha_plugin = security_captcha_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.api.openid")
    def set_api_openid_plugin(self, api_openid_plugin):
        self.api_openid_plugin = api_openid_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.api.twitter")
    def set_api_twitter_plugin(self, api_twitter_plugin):
        self.api_twitter_plugin = api_twitter_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.api.facebook")
    def set_api_facebook_plugin(self, api_facebook_plugin):
        self.api_facebook_plugin = api_facebook_plugin
