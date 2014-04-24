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

__author__ = "João Magalhães <joamag@hive.pt>"
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

import colony.base.system

ENTITY_MANAGER_ARGUMENTS = {
    "id" : "pt.hive.hive_blog.database",
    "engine" : "sqlite",
    "connection_parameters" : {
        "autocommit" : False
    }
}
""" The entity manager arguments """

ENTITY_MANAGER_PARAMETERS = {
    "default_database_prefix" : "hive_blog_"
}
""" The entity manager parameters """

AJAX_ENCODER_NAME = "ajx"
""" The ajax encoder name """

class HiveBlog(colony.base.system.System):
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
            (r"^hive_blog/?$", self.main_controller.handle_hive_index, "get"),
            (r"^hive_blog/index$", self.main_controller.handle_hive_index, "get"),
            (r"^hive_blog/pages/(?P<page_index>[0-9]+)$", self.page_controller.handle_show, "get"),
            (r"^hive_blog/posts/(?P<post_object_id>[0-9]+)$", self.post_controller.handle_show, "get"),
            (r"^hive_blog/posts/new$", self.post_controller.handle_new, "get"),
            (r"^hive_blog/posts$", self.post_controller.handle_create, "post"),
            (r"^hive_blog/comments$", self.comment_controller.handle_create, "post"),
            (r"^hive_blog/signup$", self.main_controller.handle_hive_signup, "get"),
            (r"^hive_blog/signup$", self.main_controller.handle_hive_signup_create, "post"),
            (r"^hive_blog/signin$", self.main_controller.handle_hive_signin, "get"),
            (r"^hive_blog/signin$", self.main_controller.handle_hive_signin_process, "post"),
            (r"^hive_blog/openid$", self.main_controller.handle_hive_openid, "get"),
            (r"^hive_blog/twitter$", self.main_controller.handle_hive_twitter),
            (r"^hive_blog/facebook$", self.main_controller.handle_hive_facebook),
            (r"^hive_blog/about$", self.main_controller.handle_hive_about, "get"),
            (r"^hive_blog/login$", self.main_controller.handle_hive_login, "get"),
            (r"^hive_blog/logout$", self.main_controller.handle_hive_logout, "get"),
            (r"^hive_blog/rss$", self.main_controller.handle_hive_rss, "get"),
            (r"^hive_blog/captcha$", self.main_controller.handle_hive_captcha, ("get", "post")),
        )

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

        return ()

    def get_resource_patterns(self):
        """
        Retrieves the tuple of regular expressions to be used as resource patterns,
        to the mvc service. The tuple should relate the route with the base
        file system path to be used.

        @rtype: Tuple
        @return: The tuple of regular expressions to be used as resource patterns,
        to the mvc service.
        """

        # retrieves the plugin manager
        plugin_manager = self.plugin.manager

        # retrieves the plugin path
        plugin_path = plugin_manager.get_plugin_path_by_id(self.plugin.id)

        return (
            (r"^hive_blog/resources/.+$", (plugin_path + "/hive_blog/resources/extras", "hive_blog/resources")),
        )

    def get_entity_manager_arguments(self):
        """
        Retrieves the entity manager arguments.

        @rtype: Dictionary
        @return: The entity manager arguments.
        """

        # retrieves the mvc utils plugin
        mvc_utils_plugin = self.plugin.mvc_utils_plugin

        # generates the entity manager arguments
        entity_manager_arguments = mvc_utils_plugin.generate_entity_manager_arguments(
            self.plugin, ENTITY_MANAGER_ARGUMENTS, ENTITY_MANAGER_PARAMETERS
        )

        # returns the entity manager arguments
        return entity_manager_arguments

    def require_permissions(self, rest_request, permissions_list = []):
        """
        Requires the permissions in the given permissions list to be set.

        @type rest_request: RestRequest
        @param rest_request: The rest request to be updated.
        @type permissions_list: List
        @param permissions_list: The list of permission to be validated.
        @rtype: List
        @return: The list of reasons for permission validation failure.
        """

        # retrieves the controller object currently set in the rest
        # request and that may be used for controller level operations
        controller = rest_request.controller

        # casts the permissions list
        permissions_list = self.__cast_list(permissions_list)

        # creates the list that will hold the complete set of reasons
        # for a possible permissions validations failure
        reasons = []

        # retrieves the login session attribute in order to check
        # if the user is currently logged in (as required)
        login = controller.get_session_attribute(rest_request, "login")

        # in case the login is not set must add the login string
        # to the list of reasons (for failure), then returns the
        # same list to the caller method
        if not login: reasons.append("login")
        return reasons

    def escape_permissions_failed(self, rest_request, reasons_list = []):
        """
        Handler for permission validation failures.
        Displays a message or redirects depending on the encoder name.

        @type rest_request: RestRequest
        @param rest_request: The rest request object.
        @type reasons_list: List
        @param reasons_list: A list with the reasons for validation failure.
        """

        # retrieves the controller object currently set in the rest
        # request and that may be used for controller level operations
        controller = rest_request.controller

        # creates the return address from the request path
        return_address = controller._get_path(rest_request)

        # sets the return address to the new post
        controller.set_session_attribute(rest_request, "return_address", return_address)

        # in case the encoder name is ajax
        if rest_request.encoder_name == AJAX_ENCODER_NAME:
            # sets the contents
            controller.set_contents(rest_request, "not enough permissions - access denied")
        else:
            # redirects to the signin page
            controller.redirect_base_path(rest_request, "signin")

    def __cast_list(self, value):
        """
        Casts the given value to a list,
        converting it if required.

        @type value: Object
        @param value: The value to be "casted".
        @rtype: List
        @return: The casted list value.
        """

        # in case the value is invalid returns
        # the proper values (fallback)
        if value == None: return value

        # creates the list value from the value
        list_value = type(value) == types.ListType and value or (value,)

        # returns the list value
        return list_value
