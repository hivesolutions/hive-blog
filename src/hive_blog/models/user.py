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

import hashlib

import colony.libs.import_util

import root_entity

models = colony.libs.import_util.__import__("models")
mvc_utils = colony.libs.import_util.__import__("mvc_utils")

class User(root_entity.RootEntity):
    """
    The user class, representing the
    user entity.
    """

    username = {
        "data_type" : "string",
        "indexed" : True,
        "index_types" : ("hash", "btree"),
        "mandatory" : True
    }
    """ The username of the user """

    password = {
        "data_type" : "text"
    }
    """ The password of the user """

    name = {
        "data_type" : "text",
        "mandatory" : True
    }
    """ The name of the user """

    email = {
        "data_type" : "text"
    }
    """ The email of the user """

    website = {
        "data_type" : "text"
    }
    """ The website of the user """

    openid_claimed_id = {
        "data_type" : "text"
    }
    """ The user's openid claimed id """

    twitter_username = {
        "data_type" : "text"
    }
    """ The user's twitter username """

    facebook_username = {
        "data_type" : "text"
    }
    """ The user's facebook username """

    posts = {
        "data_type" : "relation",
        "fetch_type" : "lazy",
        "secure" : True,
        "persist_type" : mvc_utils.PERSIST_NONE_TYPE
    }
    """ The posts made by the user """

    comments = {
        "data_type" : "relation",
        "fetch_type" : "lazy",
        "secure" : True,
        "persist_type" : mvc_utils.PERSIST_NONE_TYPE
    }
    """ The comments made by the user """

    def __init__(self):
        """
        Constructor of the class.
        """

        root_entity.RootEntity.__init__(self)

    @staticmethod
    def _relation_posts():
        return {
            "type" : "to-many",
            "target" : models.Post,
            "reverse" : "author"
        }

    @staticmethod
    def _relation_comments():
        return {
            "type" : "to-many",
            "target" : models.Comment,
            "reverse" : "author"
        }

    def set_validation(self):
        """
        Sets the validation structures for the
        current structure.
        """

        # adds the inherited validations
        root_entity.RootEntity.set_validation(self)

        # adds the validation methods to the username attribute
        self.add_validation_method("username", "not_none", True)
        self.add_validation_method("username", "not_empty")
        self.add_validation_method("username", "unique")

        # adds the validation methods to the password attribute
        self.add_validation_method("password", "not_empty")
        self.add_custom_validation_method("password", self.validate_password_match, True)

        # adds the validation methods to the name attribute
        self.add_validation_method("name", "not_none", True)
        self.add_validation_method("name", "not_empty")

        # adds the validation methods to the email attribute
        self.add_validation_method("email", "not_empty")

        # adds the validation methods to the website attribute
        self.add_validation_method("website", "is_url")

        # adds the validation methods to the openid claimed id attribute
        self.add_validation_method("openid_claimed_id", "not_empty")

        # adds the validation methods to the twitter username attribute
        self.add_validation_method("twitter_username", "not_empty")

        # adds the validation methods to the facebook username attribute
        self.add_validation_method("facebook_username", "not_empty")

    def encrypt_password(self, password = None):
        """
        Encrypts the specified password (in sha512) and sets it in the
        user, in the password attribute.

        In case no password is specified, it will be retrieved from
        the parameters map.

        Passwords are encrypted in sha512.

        @type password: String
        @param password: The password to encrypt.
        """

        # retrieves the password to be used, uses the
        # parameters password in case none is provided
        password = password or self._parameters.get("password", None)

        # in case no valid password is found
        if not password:
            # returns immediately since there
            # is no password to encrypt
            return

        # encrypts the password and sets it in the password attribute
        self.password = models.RootEntity.encrypt(password)

    def get_gravatar_hash(self):
        """
        Retrieves the gravatar hash value, according to the email
        defined in the user.

        @rtype: String
        @return: The md5 hash value of the email to be used to
        retrieve the gravatar image.
        """

        # returns in case the email is not defined
        if not self.email:
            # returns immediately
            return

        # creates the md5 value from the email
        email_md5 = hashlib.md5(self.email)

        # generates the md5 email digest
        email_md5_digest = email_md5.hexdigest()

        # returns the md5 email digest
        return email_md5_digest

    def validate_password_match(self, attribute_name, attribute_value, properties):
        """
        Validates the password and password confirmation in the parameters
        are the same.

        The validation is not performed in case either the password and
        password confirmation parameters are not defined.

        @type attribute_name: String
        @param attribute_name: The name of the attribute to be validated.
        @type attribute_value: Object
        @param attribute_value: The value of the attribute to be validated.
        @type properties: Dictionary
        @param properties: The properties for the validation.
        """

        # retrieves the password and its confirmation from the parameters
        password = self._parameters.get("password", None)
        password_confirmation = self._parameters.get("confirm_password", None)

        # in case the required attributes are not defined
        if password == None or password_confirmation == None:
            # returns since the validation
            # cannot be performed
            return

        # in case the password does not match the confirmation
        if not password == password_confirmation:
            # adds an error to the attribute
            self.add_error(attribute_name, "password mismatch")