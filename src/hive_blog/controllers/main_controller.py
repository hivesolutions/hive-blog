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

import colony.libs.import_util

import hive_blog.exceptions

JPEG_CONTENT_TYPE = "image/jpeg"
""" The jpeg content type """

RSS2_VALUE = "rss2"
""" The rss2 value """

HTTP_PREFIX_VALUE = "http://"
""" The http prefix value """

HTTPS_PREFIX_VALUE = "https://"
""" The https prefix value """

OPENID_SESSION_TYPE = "no-encryption"
""" The openid session type """

OAUTH_CONSUMER_KEY = "JUO1lRFjDMOGnfuuvSSVQ"
""" The oauth consumer key """

OAUTH_CONSUMER_SECRET = "R4rKyklKk2FaUa94B0kHVsrynyqawdxAH75wEprig"
""" The oauth consumer secret """

FACEBOOK_CONSUMER_KEY = "b42e59dee7e7b07258dfc82913648e43"
""" The facebook consumer key """

FACEBOOK_CONSUMER_SECRET = "6fddb2bbaade579798f45b1134865f01"
""" The facebook consumer secret """

DEFAULT_ENCODING = "utf-8"
""" The default encoding value """

RSS_CONTENT_TYPE = "application/rss+xml"
""" The rss content type """

models = colony.libs.import_util.__import__("models")
mvc_utils = colony.libs.import_util.__import__("mvc_utils")
controllers = colony.libs.import_util.__import__("controllers")

class MainController(controllers.Controller):
    """
    The hive blog controller.
    """

    @mvc_utils.serialize_exceptions("all")
    def handle_hive_index(self, rest_request, parameters = {}):
        """
        Handles the given hive index rest request.

        @type rest_request: RestRequest
        @param rest_request: The hive index rest request to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the required controllers
        page_controller = self.system.page_controller

        # retrieves the feed attribute
        feed = self.get_attribute_decoded(rest_request, "feed", DEFAULT_ENCODING)

        # in case the request is for the rss feed
        if feed == RSS2_VALUE:
            # cals the handle rss controller command
            self.handle_hive_rss(rest_request, parameters)
        else:
            # calls the page controller to show the first page
            page_controller.handle_show(rest_request, parameters)

    @mvc_utils.serialize_exceptions("all")
    def handle_hive_about(self, rest_request, parameters = {}):
        """
        Handles the given hive about rest request.

        @type rest_request: RestRequest
        @param rest_request: The hive about rest request to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # processes the contents of the template file assigning the appropriate values to it
        template_file = self.retrieve_template_file("general.html.tpl", partial_page = "main/about_contents.html.tpl")
        self.process_set_contents(rest_request, template_file)

    @mvc_utils.serialize_exceptions("all")
    def handle_hive_signup(self, rest_request, parameters = {}):
        """
        Handles the given hive signup rest request.

        @type rest_request: RestRequest
        @param rest_request: The hive signup rest request to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # processes the contents of the template file assigning the appropriate values to it
        template_file = self.retrieve_template_file("general.html.tpl", partial_page = "main/signup_contents.html.tpl")
        self.process_set_contents(rest_request, template_file, assign_session = True)

    @mvc_utils.serialize_exceptions("all")
    def handle_hive_signup_create(self, rest_request, parameters = {}):
        """
        Handles the given hive signup rest request.

        @type rest_request: RestRequest
        @param rest_request: The hive signup rest request to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # in case the captcha does not validate
        if not self._validate_captcha(rest_request, False):
            # raises the invalid captcha exception
            raise hive_blog.exceptions.InvalidCaptcha("invalid captcha value sent")

        # retrieves the session information attributes
        openid_claimed_id = self.get_session_attribute(rest_request, "openid.claimed_id")
        facebook_username = self.get_session_attribute(rest_request, "facebook.username")
        twitter_username = self.get_session_attribute(rest_request, "twitter.username")

        # retrieves the user from the rest request
        user = self.get_field(rest_request, "user", {})
        user_entity = models.User.new(user)

        # retrieves the authentication information in the user entity
        user_entity.openid_claimed_id = openid_claimed_id
        user_entity.facebook_username = facebook_username
        user_entity.twitter_username = twitter_username

        # stores the user and its relations in the data source
        user_entity.store(mvc_utils.PERSIST_SAVE_TYPE)

        # sets the login username session attribute
        self.set_session_attribute(rest_request, "login.username", user_entity.username)

        # redirects to the login page
        self.redirect_base_path(rest_request, "login")

    @mvc_utils.serialize_exceptions("all")
    def handle_hive_signin(self, rest_request, parameters = {}):
        """
        Handles the given hive signin rest request.

        @type rest_request: RestRequest
        @param rest_request: The hive signin rest request to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # processes the contents of the template file assigning the
        # appropriate values to it
        template_file = self.retrieve_template_file(
            "general.html.tpl",
            partial_page = "main/signin_contents.html.tpl"
        )
        self.process_set_contents(rest_request, template_file)

    @mvc_utils.serialize_exceptions("all")
    def handle_hive_signin_process(self, rest_request, parameters = {}):
        """
        Handles the given hive signin process rest request.

        @type rest_request: RestRequest
        @param rest_request: The hive signin process rest request to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the form data by processing the form
        form_data_map = self.process_form_data(rest_request)

        # retrieves the data from the form data
        login_data = form_data_map.get("login", {})
        openid_data = form_data_map.get("openid", {})
        twitter_data = form_data_map.get("twitter", {})
        facebook_data = form_data_map.get("facebook", {})
        return_address_data = form_data_map.get("return_address", None)

        # retrieves the authentication attributes
        login_username = login_data.get("username", None)
        login_password = login_data.get("password", None)
        openid_value = openid_data.get("value", None)
        twitter_value = twitter_data.get("value", None)
        facebook_value = facebook_data.get("value", None)

        # in case there is a return address data defined (return url)
        if return_address_data:
            # sets the return address in the session
            self.set_session_attribute(rest_request, "return_address", return_address_data)

        # processes a normal signin in case the
        # username and password were specified
        if login_username and login_password:
            # processes a normal signin
            self._process_login_signin(rest_request, login_username, login_password)
        # processes an openid signin in case
        # the open id value was specified
        elif openid_value:
            # processes an openid signin
            self._process_openid_signin(rest_request, openid_value)
        # processes a twitter signin in case
        # the twitter value was specified
        elif twitter_value:
            # processes a twitter signin
            self._process_twitter_signin(rest_request)
        # processes a facebook signin in case
        # the facebook value was specified
        elif facebook_value:
            # processes a facebook signin
            self._process_facebook_signin(rest_request)

    @mvc_utils.serialize_exceptions("all")
    def handle_hive_login(self, rest_request, parameters = {}):
        """
        Handles the given hive login rest request.

        @type rest_request: RestRequest
        @param rest_request: The hive login rest request to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the current session user
        user_entity = self._get_session_user(rest_request)

        # redirects to the signup path in case no user is in the session
        if not user_entity:
            # redirects to the signup path
            self.redirect_base_path(rest_request, "signup")

            # returns immediately
            return

        # retrieves the return address from the session
        # and unsets it from the session
        return_address = self.get_session_attribute(rest_request, "return_address")
        self.unset_session_attribute(rest_request, "return_address")

        # unsets all the session attributes related with registration
        self.unset_session_attribute(rest_request, "user.registration")

        # unsets all the session attributes related with authentication
        self.unset_session_attribute(rest_request, "login.username")
        self.unset_session_attribute(rest_request, "openid.claimed_id")
        self.unset_session_attribute(rest_request, "facebook.username")
        self.unset_session_attribute(rest_request, "twitter.username")

        # sets the user in the session
        self.set_session_attribute(rest_request, "user.information", user_entity)

        # sets the login attribute in the session
        self.set_session_attribute(rest_request, "login", True)

        # redirects to the return address in case it was
        # specified, otherwise redirects to the index
        redirect_path = return_address or "index"
        self.redirect_base_path(rest_request, redirect_path, quote = False)

    @mvc_utils.serialize_exceptions("all")
    def handle_hive_logout(self, rest_request, parameters = {}):
        """
        Handles the given hive logout rest request.

        @type rest_request: RestRequest
        @param rest_request: The hive logout rest request to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # unsets the login attribute from the session
        self.unset_session_attribute(rest_request, "login")

        # unsets the user information from the session
        self.unset_session_attribute(rest_request, "user.information")

        # redirects to the signin page
        self.redirect_base_path(rest_request, "signin")

    @mvc_utils.serialize_exceptions("all")
    def handle_hive_openid(self, rest_request, parameters = {}):
        """
        Handles the given hive openid rest request.

        @type rest_request: RestRequest
        @param rest_request: The hive openid rest request to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the form data by processing the form (in flat format)
        form_data_map = self.process_form_data_flat(rest_request)

        # retrieves the openid data
        openid_data = form_data_map["openid"]

        # tries to retrieve the openid simple registration (sreg) data
        openid_sreg_data = openid_data.get("sreg", {})

        # retrieves the openid remote client from the session
        openid_remote_client = self.get_session_attribute(rest_request, "openid.remote_client")

        # retrieves the openid attributes
        openid_claimed_id = openid_data["claimed_id"]
        openid_identity = openid_data["identity"]
        openid_ns = openid_data["ns"]
        openid_mode = openid_data["mode"]
        openid_provider_url = openid_data["op_endpoint"]
        openid_response_nonce = openid_data["response_nonce"]
        openid_return_to = openid_data["return_to"]
        openid_signature = openid_data["sig"]
        openid_signed = openid_data["signed"]

        # tries to retrieve the optional openid attributes
        openid_invalidate_handle = openid_data.get("invalidate_handle", None)

        # creates the openid return structure
        return_openid_structure = openid_remote_client.generate_openid_structure(openid_provider_url, openid_claimed_id, openid_identity, openid_return_to, None, set_structure = False)

        # sets some of the items of the openid structure
        return_openid_structure.set_signed(openid_signed)
        return_openid_structure.set_signature(openid_signature)
        return_openid_structure.set_response_nonce(openid_response_nonce)
        return_openid_structure.set_ns(openid_ns)
        return_openid_structure.set_mode(openid_mode)
        return_openid_structure.set_invalidate_handle(openid_invalidate_handle)

        # retrieves the attributes list
        attributes_list = rest_request.get_attributes_list()

        # iterates over all the attributes in the attributes list
        for attribute in attributes_list:
            # minimizes the attribute by removing
            # the openid namespace (eg: openid.ns transforms into ns)
            minimized_attribute = attribute[7:]

            # in case the return openid structure does not have
            # the minimizes attribute sets the value of it
            if not hasattr(return_openid_structure, minimized_attribute):
                # retrieves the attribute value from the request
                attribute_value = self.get_attribute_decoded(rest_request, attribute, DEFAULT_ENCODING)

                # sets the attribute value in the return openid structure
                setattr(return_openid_structure, minimized_attribute, attribute_value)

        # verifies the openid return value (in non strict mode)
        openid_remote_client.openid_verify(return_openid_structure, False)

        # retrieves the preferred claimed id
        preferred_claimed_id = openid_remote_client.get_preferred_claimed_id()

        # creates the user registration structure from the openid simple
        # registration (sreg) values
        user_registration = {
            "username" : openid_sreg_data.get("nickname", None),
            "name" : openid_sreg_data.get("fullname", None),
            "email" : openid_sreg_data.get("email", None)
        }

        # sets the openid claimed id attribute
        self.set_session_attribute(rest_request, "openid.claimed_id", preferred_claimed_id)

        # sets the user registration attribute
        self.set_session_attribute(rest_request, "user.registration", user_registration)

        # redirects to the login page
        self.redirect_base_path(rest_request, "login")

    @mvc_utils.serialize_exceptions("all")
    def handle_hive_twitter(self, rest_request, parameters = {}):
        """
        Handles the given hive twitter rest request.

        @type rest_request: RestRequest
        @param rest_request: The hive twitter rest request to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # redirects to the initial page
        self.redirect_base_path(rest_request, "index")

    @mvc_utils.serialize_exceptions("all")
    def handle_hive_facebook(self, rest_request, parameters = {}):
        """
        Handles the given hive facebook rest request.

        @type rest_request: RestRequest
        @param rest_request: The hive facebook rest request to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # redirects to the initial page
        self.redirect_base_path(rest_request, "index")

    @mvc_utils.serialize_exceptions("all")
    def handle_hive_rss(self, rest_request, parameters = {}):
        """
        Handles the given hive rss rest request.

        @type rest_request: RestRequest
        @param rest_request: The hive rss rest request to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the host path then uses it to create
        # the base url from the host path
        host_path = self._get_host_path(rest_request)
        base_url = host_path + "/"

        # retrieves all the posts in the blog
        posts = models.Post.find_for_list(filter)

        # processes the contents of the template file assigning the appropriate values to it
        template_file = self.retrieve_template_file("main/rss.xml.tpl")
        template_file.assign("base_url", base_url)
        template_file.assign("posts", posts)
        self.process_set_contents(rest_request, template_file, content_type = RSS_CONTENT_TYPE)

    @mvc_utils.serialize_exceptions("all")
    def handle_hive_captcha(self, rest_request, parameters = {}):
        """
        Handles the given hive captcha request.

        @type rest_request: RestRequest
        @param rest_request: The hive captcha request to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the security captcha plugin
        security_captcha_plugin = self.plugin.security_captcha_plugin

        # validates the captcha, returning immediately in case
        # the value is valid (expected result)
        if self._validate_captcha(rest_request): return

        # retrieves the captcha session value
        captcha_session = self.get_session_attribute(rest_request, "captcha")

        # in case there is no captcha defined in session
        if not captcha_session:
            # generates a new captcha for session
            captcha_session = self._generate_captcha(rest_request)

        # generates the captcha, retrieving the string value and the string buffer
        _string_value, string_buffer = security_captcha_plugin.generate_captcha(captcha_session, {})

        # retrieves the value from the string buffer
        string_buffer_value = string_buffer.get_value()

        # sets the request contents
        self.set_contents(rest_request, string_buffer_value, JPEG_CONTENT_TYPE)

    def _process_login_signin(self, rest_request, login_username, login_password):
        # validates the captcha, regenerating the captcha
        if not self._validate_captcha(rest_request, True):
            # raises the invalid captcha exception
            raise hive_blog.exceptions.InvalidCaptcha("invalid captcha value sent")

        # encrypts the login password
        encrypted_login_password = models.RootEntity.encrypt(login_password)

        # creates the filter map to be able to filter the users that
        # respect the provided filter (authentication)
        filter = {
            "filters" : (
                {
                    "username" : login_username
                },
                {
                    "password" : encrypted_login_password
                }
            )
        }

        # retrieves all users that match the authentication parameters
        user_entity = models.User.find_one(filter)

        # returns in case the user was not found as it's not possible
        # to login a user that it's not valid
        if not user_entity: return

        # sets the various login related attributes in the current session
        # this is considered the proper login stage
        self.set_session_attribute(rest_request, "login.username", login_username)
        self.set_session_attribute(rest_request, "login", True)
        self.redirect_base_path(rest_request, "login")

    def _process_openid_signin(self, rest_request, openid_value):
        # retrieves the api openid plugin
        api_openid_plugin = self.plugin.api_openid_plugin

        # creates the openid remote client
        openid_remote_client = api_openid_plugin.create_remote_client({})

        # normalizes the openid value
        openid_value_normalized = openid_remote_client.normalize_claimed_id(openid_value)

        # retrieves the host as the openid realm
        openid_realm = self._get_host(rest_request, HTTP_PREFIX_VALUE)

        # retrieves the host path for the openid path as the return to address
        openid_return_to = self._get_host_path(rest_request, "/openid")

        # generates the openid structure by sending all the required data
        openid_remote_client.generate_openid_structure(None, openid_value_normalized, openid_value_normalized, openid_return_to, openid_realm, session_type = OPENID_SESSION_TYPE)

        # runs the openid discovery process to obtains the provider url
        openid_remote_client.openid_discover()

        # associates the server and the provider
        openid_remote_client.openid_associate()

        # sets the openid remote client in the session
        self.set_session_attribute(rest_request, "openid.remote_client", openid_remote_client)

        # retrieves the request url that will be used
        # to forward the user agent
        request_url = openid_remote_client.get_request_url()

        # redirects to the request url page
        self.redirect_base_path(rest_request, request_url, quote = False)

    def _process_twitter_signin(self, rest_request):
        # retrieves the api twitter plugin
        api_twitter_plugin = self.plugin.api_twitter_plugin

        # creates the twitter remote client
        twitter_remote_client = api_twitter_plugin.create_remote_client({})

        # retrieves the callback path from the host
        callback_path = self._get_host_path(rest_request, "/twitter")

        # generates the oauth structure
        twitter_remote_client.generate_oauth_structure(OAUTH_CONSUMER_KEY, OAUTH_CONSUMER_SECRET, oauth_callback = callback_path)

        # retrieves the authenticate url
        twitter_remote_client.open_oauth_request_token()

        # sets the twitter remote client in the session
        self.set_session_attribute(rest_request, "twitter.remote_client", twitter_remote_client)

        # retrieves the oauth authenticate url
        authenticate_url = twitter_remote_client.get_oauth_authenticate_url()

        # redirects to the authenticate url page
        self.redirect_base_path(rest_request, authenticate_url, quote = False)

    def _process_facebook_signin(self, rest_request):
        # retrieves the api facebook plugin
        api_facebook_plugin = self.plugin.api_facebook_plugin

        # creates the facebook remote client
        facebook_remote_client = api_facebook_plugin.create_remote_client({})

        # retrieves the next (callback) from the host
        next = self._get_host_path(rest_request, "/facebook")

        # generates the facebook structure
        facebook_remote_client.generate_facebook_structure(FACEBOOK_CONSUMER_KEY, FACEBOOK_CONSUMER_SECRET, next)

        # sets the facebook remote client in the session
        self.set_session_attribute(rest_request, "facebook.remote_client", facebook_remote_client)

        # retrieves the facebook login url
        login_url = facebook_remote_client.get_login_url()

        # redirects to the login url page
        self.redirect_base_path(rest_request, login_url, quote = False)

    def _get_session_user(self, rest_request):
        # retrieves the session attributes related with authentication
        login_username = self.get_session_attribute(rest_request, "login.username")
        openid_claimed_id = self.get_session_attribute(rest_request, "openid.claimed_id")
        facebook_username = self.get_session_attribute(rest_request, "facebook.username")
        twitter_username = self.get_session_attribute(rest_request, "twitter.username")

        # initializes the login filter
        login_filter = {}

        # in case the login username is defined
        if login_username:
            login_filter["username"] = login_username
        # in case the open id claimed id is defined
        elif openid_claimed_id:
            login_filter["openid_claimed_id"] = openid_claimed_id
        # in case the facebook username is defined
        elif facebook_username:
            login_filter["facebook_username"] = facebook_username
        # in case the twitter username is defined
        elif twitter_username:
            login_filter["twitter_username"] = twitter_username
        # in case no authentication name (method) is defined
        else:
            # raises the invalid authentication information
            raise hive_blog.exceptions.InvalidAuthenticationInformation("missing authentication name")

        # retrieves the user that matches the authentication parameters
        user_entity = models.User.find_one(login_filter)

        # returns the retrieved user
        return user_entity

    def _generate_captcha(self, rest_request):
        # retrieves the security captcha plugin
        security_captcha_plugin = self.plugin.security_captcha_plugin

        # generates a captcha string value
        string_value = security_captcha_plugin.generate_captcha_string_value({})

        # sets the captcha as a session attribute
        self.set_session_attribute(rest_request, "captcha", string_value)

        # returns the generated captcha string value
        return string_value

    def _validate_captcha(self, rest_request, regenerate_on_valid = False):
        # retrieves the form data by processing the form (in flat format)
        form_data_map = self.process_form_data_flat(rest_request)

        # tries to retrieve the captcha validation value
        captcha_validation = form_data_map.get("captcha", None)

        # in case no captcha is meant to be validated, must generate
        # a new one (as this is the initial request)
        if not captcha_validation:
            # generates a new captcha and then returns false, as
            # no validation is being made
            self._generate_captcha(rest_request)
            return False

        # normalizes the captcha validation value
        captcha_validation = captcha_validation.lower()

        # retrieves the captcha session value
        captcha_session = self.get_session_attribute(rest_request, "captcha")

        # in case no valid captcha session is set
        if not captcha_session:
            # raises the invalid captcha exception
            raise hive_blog.exceptions.InvalidCaptcha("invalid captcha session value")

        # in case both captchas match don't match (invalid captcha value)
        if not captcha_validation == captcha_session:
            # raises the invalid captcha exception
            raise hive_blog.exceptions.InvalidCaptcha("non matching captcha value: " + str(captcha_validation))

        # in case the regenerate on valid flag is set, must
        # generate a new captcha for the session
        if regenerate_on_valid: self._generate_captcha(rest_request)

        # validation was successful
        return True
