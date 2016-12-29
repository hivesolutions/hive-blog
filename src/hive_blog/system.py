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

ENTITY_MANAGER_ARGUMENTS = dict(
    id = "pt.hive.hive_blog.database",
    engine = "sqlite",
    connection_parameters = dict(
        autocommit = False
    )
)
""" The entity manager arguments, these arguments are going
to be used in case no arguments are provided to the system """

ENTITY_MANAGER_PARAMETERS = dict(
    database_prefix = "hive_blog_"
)
""" The entity manager parameters to be used by default in
case they are not overriden by any configuration value """

class HiveBlog(colony.System):
    """
    The hive blog class.
    """

    def load_components(self):
        """
        Loads the main components controller, etc.
        This load should occur only after the dependencies are loaded.
        """

        # retrieves the mvc utils plugin
        mvc_utils_plugin = self.plugin.mvc_utils_plugin

        # retrieves the entity manager arguments
        entity_manager_arguments = self.get_entity_manager_arguments()

        # creates the entity models classes by creating the entity manager
        # and updating the classes, this trigger the loading of the entity
        # manager (and creation of it if necessary) then creates the controllers
        mvc_utils_plugin.assign_models_controllers(self, self.plugin, entity_manager_arguments)

    def unload_components(self):
        """
        Unloads the main components models, controllers, etc.
        This load should occur the earliest possible in the unloading process.
        """

        # retrieves the mvc utils plugin
        mvc_utils_plugin = self.plugin.mvc_utils_plugin

        # retrieves the entity manager arguments
        entity_manager_arguments = self.get_entity_manager_arguments()

        # destroys the entity models, unregistering them from the
        # entity manager instance and then destroy the controllers,
        # unregistering them from the internal structures
        mvc_utils_plugin.unassign_models_controllers(self, entity_manager_arguments)

    def get_patterns(self):
        """
        Retrieves the tuple of regular expressions to be used as patterns,
        to the mvc service. The tuple should relate the route with the handler
        method/function.

        @rtype: Tuple
        @return: The tuple of regular expressions to be used as patterns,
        to the mvc service.
        """

        return (
            (r"hive_blog/?", self.main_controller.index, "get"),
            (r"hive_blog/index", self.main_controller.index, "get"),
            (r"hive_blog/pages/<int:index>", self.page_controller.show, "get"),
            (r"hive_blog/posts/<int:id>", self.post_controller.show, "get"),
            (r"hive_blog/posts/new", self.post_controller.new, "get"),
            (r"hive_blog/posts", self.post_controller.create, "post"),
            (r"hive_blog/comments", self.comment_controller.create, "post"),
            (r"hive_blog/signup", self.main_controller.signup, "get"),
            (r"hive_blog/signup", self.main_controller.signup_create, "post"),
            (r"hive_blog/signin", self.main_controller.signin, "get"),
            (r"hive_blog/signin", self.main_controller.signin_process, "post"),
            (r"hive_blog/openid", self.main_controller.openid, "get"),
            (r"hive_blog/twitter", self.main_controller.twitter),
            (r"hive_blog/facebook", self.main_controller.facebook),
            (r"hive_blog/about", self.main_controller.about, "get"),
            (r"hive_blog/login", self.main_controller.login, "get"),
            (r"hive_blog/logout", self.main_controller.logout, "get"),
            (r"hive_blog/rss", self.main_controller.rss, "get"),
            (r"hive_blog/captcha", self.main_controller.captcha, ("get", "post")),
        )

    def get_resource_patterns(self):
        """
        Retrieves the tuple of regular expressions to be used as resource patterns,
        to the mvc service. The tuple should relate the route with the base
        file system path to be used.

        @rtype: Tuple
        @return: The tuple of regular expressions to be used as resource patterns,
        to the mvc service.
        """

        # retrieves the plugin manager and uses it to retrieve
        # the colony site plugin path
        plugin_manager = self.plugin.manager
        plugin_path = plugin_manager.get_plugin_path_by_id(self.plugin.id)

        return (
            (r"hive_blog/resources/.+", (plugin_path + "/hive_blog/resources/extras", "hive_blog/resources")),
        )

    def get_entity_manager_arguments(self):
        """
        Retrieves the entity manager arguments, this method does not
        take into consideration any kind of configuration and uses
        only static configuration values.

        @rtype: Dictionary
        @return: The entity manager arguments after the resolution
        process for the retrieval of the arguments.
        """

        # retrieves the mvc utils plugin
        mvc_utils_plugin = self.plugin.mvc_utils_plugin

        # generates the entity manager arguments, creating the proper structures
        # using the standard mvc implementation and returns the values
        entity_manager_arguments = mvc_utils_plugin.generate_entity_manager_arguments(
            self.plugin, ENTITY_MANAGER_ARGUMENTS, ENTITY_MANAGER_PARAMETERS
        )
        return entity_manager_arguments

    def require_permissions(self, request, permissions_list = []):
        """
        Requires the permissions in the given permissions list to be set.

        @type request: Request
        @param request: The request to be updated.
        @type permissions_list: List
        @param permissions_list: The list of permission to be validated.
        @rtype: List
        @return: The list of reasons for permission validation failure.
        """

        # casts the permissions list
        permissions_list = self.__cast_list(permissions_list)

        # creates the list that will hold the complete set of reasons
        # for a possible permissions validations failure
        reasons = []

        # retrieves the login session attribute in order to check
        # if the user is currently logged in (as required)
        login = request.get_s(request, "login")

        # in case the login is not set must add the login string
        # to the list of reasons (for failure), then returns the
        # same list to the caller method
        if not login: reasons.append("login")
        return reasons

    def escape_permissions_failed(self, request, reasons_list = []):
        """
        Handler for permission validation failures.
        Displays a message or redirects depending on the encoder name.

        @type request: Request
        @param request: The request object.
        @type reasons_list: List
        @param reasons_list: A list with the reasons for validation failure.
        """

        # retrieves the controller object currently set in the
        # request and that may be used for controller level operations
        controller = request.controller

        # creates the return address from the request path and sets it
        # as a session attribute in the controller, then redirect the
        # user to the signin page so that it can escalate permissions
        return_address = controller._get_path(request)
        request.set_s("return_address", return_address)
        controller.redirect_base_path(request, "signin")

    def __cast_list(self, value):
        """
        Casts the given value to a list, converting it if required.

        @type value: Object
        @param value: The value to be "casted".
        @rtype: List
        @return: The casted list value.
        """

        # in case the value is invalid returns
        # the proper values (fallback)
        if value == None: return value

        # creates the list value from the value and returns
        # the value to the caller method
        list_value = type(value) == list and value or (value,)
        return list_value
