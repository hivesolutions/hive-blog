#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Solutions Blog
# Copyright (c) 2008-2020 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2020 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Hive Solutions Confidential Usage License (HSCUL)"
""" The license for the module """

import colony

from .root_entity import RootEntity

models = colony.__import__("models")

class Setting(RootEntity):
    """
    The setting class, representing the
    setting entity.
    """

    name = dict(
        type = "string",
        indexed = True,
        index_types = ("hash", "btree"),
        mandatory = True
    )
    """ The name for the setting """

    value = dict(
        type = "text",
        mandatory = True
    )
    """ The value for the setting """

    def __init__(self):
        """
        Constructor of the class.
        """

        RootEntity.__init__(self)

    def set_validation(self):
        """
        Sets the validation structures for the
        current structure.
        """

        # adds the inherited validations
        RootEntity.set_validation(self)

        # adds the validation methods to the name attribute
        self.add_validation("name", "not_none", True)
        self.add_validation("name", "not_empty")
        self.add_validation("name", "unique")

        # adds the validation methods to the value attribute
        self.add_validation("value", "not_none", True)
        self.add_validation("value", "not_empty")
