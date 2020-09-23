"""Point implementation for the SEQSCAN-D algorithm."""

# Standard modules 
from datetime import datetime
# My modules
from region import Region

class Point(object):
    counter = 0             # id generator
    
    def __init__(self, pzone, time):
        """Constructor.
        
        Args:
            pzone (string) : the zone this point belongs to
            time (datetime) : the observation timestamp

        Note:
            ids are generated using the class counter: this technique is NOT 
            thread-safe.
        """
		
        self.id = Point.counter
        self.pzone = pzone
        self.time = time


        # for labelling convenience
        self.cluster = None
        
        # noise labelling
        self.prev = None
        self.next = None

        Point.counter += 1
        
    def __repr__(self):
        return '( id: %d, pzone: %s, time: %s)' % (
            self.id,
            self.pzone,
            self.time
        )

    def get_time(self):
        return self.time
    def set_time(self,d):
        self.time=d


    def get_pzone(self):
        return self.pzone
    def set_pzone(self,z):
        self.pzone=z

