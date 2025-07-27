
from opta_read.auxiliares.f28_aux_funct import possesion

class F28:

    def __init__(self, path):
        self.path=path
    
    def get_possesion(self,possesion_type, interval_length):
        return possesion(path=self.path,possesion_type=possesion_type, interval_length=interval_length)

    
        
    

