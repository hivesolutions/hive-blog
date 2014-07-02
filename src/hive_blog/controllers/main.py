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

JPEG_CONTENT_TYPE = "image/jpeg"
""" The jpeg content type """

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

models = colony.__import__("models")
mvc_utils = colony.__import__("mvc_utils")

class MainController(base.BaseController):

    @mvc_utils.serialize
    def index(self, request):
        page_controller = self.system.page_controller
        feed = request.field("feed")
        if feed == "rss2": self.rss(request)
        else: page_controller.show(request)

    @mvc_utils.serialize
    def about(self, request):
        self._template(
            request = request,
            partial_page = "main/about.html.tpl"
        )

    @mvc_utils.serialize
    def signup(self, request):
        self._template(
            request = request,
            partial_page = "main/signup.html.tpl"
        )

    @mvc_utils.serialize
    def signup_create(self, request):
        # validates the captcha, regenerating the captcha and raising
        # an exception in case the validation has failed
        if not self._validate_captcha(request, False):
            raise hive_blog.InvalidCaptcha("invalid captcha value sent")

        # retrieves the session information attributes
        openid_claimed_id = request.get_s("openid.claimed_id")
        facebook_username = request.get_s("facebook.username")
        twitter_username = request.get_s("twitter.username")

        # retrieves the user from the request
        user = request.field("user", {})
        user = models.User.new(user)

        # retrieves the authentication information in the user entity
        user.openid_claimed_id = openid_claimed_id
        user.facebook_username = facebook_username
        user.twitter_username = twitter_username

        # stores the user and its relations in the data source, creating
        # the user as part of the operation
        user.create()

        # sets the login username session attribute
        request.set_s("login.username", user.username)

        # redirects to the login page
        self.redirect_base_path(request, "login")

    @mvc_utils.serialize
    def signin(self, request):
        self._template(
            request = request,
            partial_page = "main/signin.html.tpl"
        )

    @mvc_utils.serialize
    def signin_process(self, request):
        # retrieves the data from the form data
        login_data = request.field("login", {})
        openid_data = request.field("openid", {})
        twitter_data = request.field("twitter", {})
        facebook_data = request.field("facebook", {})
        return_address_data = request.field("return_address", None)

        # retrieves the authentication attributes
        login_username = login_data.get("username", None)
        login_password = login_data.get("password", None)
        openid_value = openid_data.get("value", None)
        twitter_value = twitter_data.get("value", None)
        facebook_value = facebook_data.get("value", None)

        # in case there is a return address data defined (return url)
        # it must be defined in the current session to be used latter
        if return_address_data: request.set_s("return_address", return_address_data)

        # processes a normal signin in case the
        # username and password were specified
        if login_username and login_password:
            self._process_login_signin(request, login_username, login_password)
        # processes an openid signin in case
        # the open id value was specified
        elif openid_value:
            self._process_openid_signin(request, openid_value)
        # processes a twitter signin in case
        # the twitter value was specified
        elif twitter_value:
            self._process_twitter_signin(request)
        # processes a facebook signin in case
        # the facebook value was specified
        elif facebook_value:
            self._process_facebook_signin(request)

    @mvc_utils.serialize
    def login(self, request):
        # retrieves the current session user
        user = self._get_session_user(request)

        # redirects to the signup path in case no user is in the session
        if not user:
            # redirects to the signup path and returns immediately
            self.redirect_base_path(request, "signup")
            return

        # retrieves the return address from the session
        # and unsets it from the session
        return_address = request.get_s("return_address")
        request.unset_s("return_address")

        # unsets all the session attributes related with registration
        request.unset_s("user.registration")

        # unsets all the session attributes related with authentication
        request.unset_s("login.username")
        request.unset_s("openid.claimed_id")
        request.unset_s("facebook.username")
        request.unset_s("twitter.username")

        # sets the user in the session
        request.set_s("user.information", user)

        # sets the login attribute in the session
        request.set_s("login", True)

        # redirects to the return address in case it was
        # specified, otherwise redirects to the index
        redirect_path = return_address or "index"
        self.redirect_base_path(request, redirect_path, quote = False)

    @mvc_utils.serialize
    def logout(self, request):
        # unsets the login attribute from the session and then redirects
        # the user back to the login page so that he can login again
        request.unset_s("login")
        request.unset_s("user.information")
        self.redirect_base_path(request, "signin")

    @mvc_utils.serialize
    def openid(self, request):
        # retrieves the form data by processing the form (in flat format)
        form_data_map = self.process_form_data_flat(request)

        # retrieves the openid data
        openid_data = form_data_map["openid"]

        # tries to retrieve the openid simple registration (sreg) data
        openid_sreg_data = openid_data.get("sreg", {})

        # retrieves the openid remote client from the session
        openid_remote_client = request.get_s("openid.remote_client")

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
        return_openid_structure = openid_remote_client.generate_openid_structure(
            openid_provider_url,
            openid_claimed_id,
            openid_identity,
            openid_return_to,
            None,
            set_structure = False
        )

        # sets some of the items of the openid structure
        return_openid_structure.set_signed(openid_signed)
        return_openid_structure.set_signature(openid_signature)
        return_openid_structure.set_response_nonce(openid_response_nonce)
        return_openid_structure.set_ns(openid_ns)
        return_openid_structure.set_mode(openid_mode)
        return_openid_structure.set_invalidate_handle(openid_invalidate_handle)

        # retrieves the attributes list
        attributes_list = request.get_attributes_list()

        # iterates over all the attributes in the attributes list
        for attribute in attributes_list:
            # minimizes the attribute by removing
            # the openid namespace (eg: openid.ns transforms into ns)
            minimized_attribute = attribute[7:]

            # in case the return openid structure does not have
            # the minimizes attribute sets the value of it
            if not hasattr(return_openid_structure, minimized_attribute):
                # retrieves the attribute value from the request
                attribute_value = self.get_attribute_decoded(request, attribute, "utf-8")

                # sets the attribute value in the return openid structure
                setattr(return_openid_structure, minimized_attribute, attribute_value)

        # verifies the openid return value (in non strict mode)
        openid_remote_client.openid_verify(return_openid_structure, False)

        # retrieves the preferred claimed id
        preferred_claimed_id = openid_remote_client.get_preferred_claimed_id()

        # creates the user registration structure from the openid simple
        # registration (sreg) values
        user_registration = dict(
            username = openid_sreg_data.get("nickname", None),
            name = openid_sreg_data.get("fullname", None),
            email = openid_sreg_data.get("email", None)
        )

        # sets the openid id associate attributes in the current session
        # so that may be used latter in the login process
        request.set_s("openid.claimed_id", preferred_claimed_id)
        request.set_s("user.registration", user_registration)

        # redirects to the login page
        self.redirect_base_path(request, "login")

    @mvc_utils.serialize
    def twitter(self, request):
        self.redirect_base_path(request, "index")

    @mvc_utils.serialize
    def facebook(self, request):
        self.redirect_base_path(request, "index")

    @mvc_utils.serialize
    def rss(self, request):
        # retrieves the host path then uses it to create
        # the base url from the host path
        host_path = self._get_host_path(request)
        base_url = host_path + "/"

        # retrieves all the posts in the blog
        posts = models.Post.find_for_list()

        # processes the contents of the template file assigning the appropriate values to it
        template_file = self.retrieve_template_file("main/rss.xml.tpl")
        template_file.assign("base_url", base_url)
        template_file.assign("posts", posts)
        self.process_set_contents(request, template_file, content_type = "application/rss+xml")

    @mvc_utils.serialize
    def captcha(self, request):
        # retrieves the captcha plugin
        captcha_plugin = self.plugin.captcha_plugin

        # validates the captcha, returning immediately in case
        # the value is valid (expected result)
        if self._validate_captcha(request): return

        # retrieves the captcha session value
        captcha_session = request.get_s("captcha")

        # in case there is no captcha defined in session one must
        # be generated for the current request
        if not captcha_session:
            captcha_session = self._generate_captcha(request)

        # generates the captcha, retrieving the string value and the string buffer
        _string_value, string_buffer = captcha_plugin.generate_captcha(captcha_session, {})

        # retrieves the value from the string buffer
        string_buffer_value = string_buffer.get_value()

        # sets the request contents
        self.set_contents(request, string_buffer_value, JPEG_CONTENT_TYPE)

    def _process_login_signin(self, request, login_username, login_password):
        # validates the captcha, regenerating the captcha and raising
        # an exception in case the validation has failed
        if not self._validate_captcha(request, True):
            raise hive_blog.InvalidCaptcha("invalid captcha value sent")

        # encrypts the login password
        encrypted_login_password = models.RootEntity.encrypt(login_password)

        # creates the filter map to be able to filter the users that
        # respect the provided filter (authentication)
        filter = dict(
            filters = (
                dict(
                    username = login_username
                ),
                dict(
                    password = encrypted_login_password
                )
            )
        )

        # retrieves all users that match the authentication parameters
        user = models.User.find_one(filter)

        # returns in case the user was not found as it's not possible
        # to login a user that it's not valid
        if not user: return

        # sets the various login related attributes in the current session
        # this is considered the proper login stage
        request.set_s("login.username", login_username)
        request.set_s("login", True)
        self.redirect_base_path(request, "login")

    def _process_openid_signin(self, request, openid_value):
        # retrieves the api openid plugin
        api_openid_plugin = self.plugin.api_openid_plugin

        # creates the openid remote client
        openid_remote_client = api_openid_plugin.create_remote_client({})

        # normalizes the openid value
        openid_value_normalized = openid_remote_client.normalize_claimed_id(openid_value)

        # retrieves the host as the openid realm
        openid_realm = self._get_host(request, HTTP_PREFIX_VALUE)

        # retrieves the host path for the openid path as the return to address
        openid_return_to = self._get_host_path(request, "/openid")

        # generates the openid structure by sending all the required data
        openid_remote_client.generate_openid_structure(None, openid_value_normalized, openid_value_normalized, openid_return_to, openid_realm, session_type = OPENID_SESSION_TYPE)

        # runs the openid discovery process to obtains the provider url
        openid_remote_client.openid_discover()

        # associates the server and the provider
        openid_remote_client.openid_associate()

        # sets the openid remote client in the session
        request.set_s("openid.remote_client", openid_remote_client)

        # retrieves the request url that will be used
        # to forward the user agent
        request_url = openid_remote_client.get_request_url()

        # redirects to the request url page
        self.redirect_base_path(request, request_url, quote = False)

    def _process_twitter_signin(self, request):
        # retrieves the api twitter plugin
        api_twitter_plugin = self.plugin.api_twitter_plugin

        # creates the twitter remote client
        twitter_remote_client = api_twitter_plugin.create_remote_client({})

        # retrieves the callback path from the host
        callback_path = self._get_host_path(request, "/twitter")

        # generates the oauth structure
        twitter_remote_client.generate_oauth_structure(OAUTH_CONSUMER_KEY, OAUTH_CONSUMER_SECRET, oauth_callback = callback_path)

        # retrieves the authenticate url
        twitter_remote_client.open_oauth_request_token()

        # sets the twitter remote client in the session
        request.set_s("twitter.remote_client", twitter_remote_client)

        # retrieves the oauth authenticate url
        authenticate_url = twitter_remote_client.get_oauth_authenticate_url()

        # redirects to the authenticate url page
        self.redirect_base_path(request, authenticate_url, quote = False)

    def _process_facebook_signin(self, request):
        api_facebook_plugin = self.plugin.api_facebook_plugin

        # creates the facebook remote client
        facebook_remote_client = api_facebook_plugin.create_remote_client({})

        # retrieves the next (callback) from the host
        next = self._get_host_path(request, "/facebook")

        # generates the facebook structure
        facebook_remote_client.generate_facebook_structure(FACEBOOK_CONSUMER_KEY, FACEBOOK_CONSUMER_SECRET, next)

        # sets the facebook remote client in the session
        request.set_s("facebook.remote_client", facebook_remote_client)

        login_url = facebook_remote_client.get_login_url()
        self.redirect_base_path(request, login_url, quote = False)

    def _get_session_user(self, request):
        login_username = request.get_s("login.username")
        openid_claimed_id = request.get_s("openid.claimed_id")
        facebook_username = request.get_s("facebook.username")
        twitter_username = request.get_s("twitter.username")

        filter = {}

        if login_username: filter["username"] = login_username
        elif openid_claimed_id: filter["openid_claimed_id"] = openid_claimed_id
        elif facebook_username: filter["facebook_username"] = facebook_username
        elif twitter_username: filter["twitter_username"] = twitter_username
        else: raise hive_blog.InvalidAuthenticationInformation("missing authentication name")

        user = models.User.find_one(filter)
        return user

    def _generate_captcha(self, request):
        captcha_plugin = self.plugin.captcha_plugin
        string_value = captcha_plugin.generate_captcha_string_value({})
        request.set_s("captcha", string_value)
        return string_value

    def _validate_captcha(self, request, regenerate_on_valid = False):
        captcha_validation = request.field("captcha", None)
        if not captcha_validation:
            self._generate_captcha(request)
            return False

        captcha_validation = captcha_validation.lower()
        captcha_session = request.get_s("captcha")

        if not captcha_session:
            raise hive_blog.InvalidCaptcha("invalid captcha session value")

        if not captcha_validation == captcha_session:
            raise hive_blog.InvalidCaptcha("non matching captcha value: " + str(captcha_validation))

        if regenerate_on_valid: self._generate_captcha(request)
        return True
