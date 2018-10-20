#!/usr/bin/env python

from abc import ABC, abstractmethod


#  Abstract timing logic
class Logic(ABC):

    def __init__(self, left_policy):
        self.left_policy = left_policy
        self.last_change = 0

    @abstractmethod
    def get_phase(self, current_phases):
        pass
