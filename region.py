"""Region implementation for the SEQSCAN algorithm."""

# HACK: the recursive version of the lookup function used to smash the stack.
# import sys
# sys.setrecursionlimit(5000)

# Standard modules
from __future__ import division
from collections import defaultdict
from datetime import datetime, timedelta



class Region(object):
    """Region implementation for the SEQSCAN algorithm."""
    
    counter = 0             # instance counter / id generator
    
    def __init__(self, pzone, time_start, time_end, presence, n):
        """Creates an empty region.
        Note:
            ids are generated using the class counter: this technique is NOT 
            thread-safe.
        """
        self.id   = Region.counter      # object id
        self.label=pzone
        self.time_start= time_start
        self.time_end= time_end

        self.points = set([])

        self.noise = 0                  # counter of excursion points
        self.persistent = False         # aggregate persistence flag
        
        self.presence= presence
        self.n=n

        Region.counter += 1
        

    def __repr__(self):
        return "(id:%s, label:%s, time_start:%s, time_end: %s, presence: %d, n: %d )" % (
            self.id,
            self.label,
            self.time_start,
            self.time_end,
            self.presence,
            self.n
        )
        
    def __contains__(self, point):
        """True if this Region contains the specified Point."""

        return point in self.points
        

    def is_persistent(self):
        """Returns the (aggregate) persistence flag."""
        return self.persistent
        
