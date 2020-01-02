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
mvc_utils = colony.__import__("mvc_utils")

class Tag(RootEntity):
    """
    The tag class, representing the tag entity.
    """

    name = dict(
        type = "string",
        indexed = True,
        index_types = ("hash", "btree"),
        mandatory = True
    )
    """ The name of the tag """

    count = dict(
        type = "integer",
        mandatory = True,
        secure = True
    )
    """ The occurrences count of the tag """

    root_entities = dict(
        type = "relation",
        fetch_type = "lazy",
        secure = True,
        persist_type = mvc_utils.PERSIST_NONE
    )
    """ The root entities for this tag """

    def __init__(self):
        """
        Constructor of the class.
        """

        RootEntity.__init__(self)

    @staticmethod
    def _relation_root_entities():
        return dict(
            type = "to-many",
            target = models.RootEntity
        )

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

        # adds the validation methods to the count attribute
        self.add_validation("count", "not_none", True)
        self.add_validation("count", "greater_than_or_equal_to_zero")
