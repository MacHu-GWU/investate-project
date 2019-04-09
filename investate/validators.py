# -*- coding: utf-8 -*-

import six


class Validators(object):
    @staticmethod
    def non_negative_number(instance, attribute, value):
        """
        Value has to greater or equal than 0.
        """
        if value < 0:
            raise ValueError("{} can't less than 0!".format(attribute.name))

    @staticmethod
    def percentage_validator(instance, attribute, value):
        """
        Percentage has to between [0, 1].
        """
        if value > 1:
            raise ValueError("{} can't greater than 1!".format(attribute.name))
        elif value < 0:
            raise ValueError("{} can't less than 0!".format(attribute.name))

    @staticmethod
    def year_validator(instance, attribute, value):
        """
        Year has to be an integer and between [1, 30]
        """
        if not isinstance(value, six.integer_types):
            raise TypeError("{} has to be an integer!".format(attribute.name))
        if value < 1:
            raise ValueError("{} can't less than 1!".format(attribute.name))
        if value > 30:
            raise ValueError("{} can't greater than 30!".format(attribute.name))
