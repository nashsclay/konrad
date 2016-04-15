#!/usr/bin/python
# Simulates airless descent, for Retro

import sim

class RetroSim(sim.RocketSim):
    def simulate(self, booster, hs, vs, alt, throttle, pit, hdg, lat, lon, brad, bgm):
        self.sim_setup(booster, hs, vs, alt, throttle, pit, hdg, lat, lon, brad, bgm)
        self.data = {}
        while not ((
                    (
                     ('h' in self.data and 'v' in self.data)
                     or
                     's' in self.data
                    ) and
                    'b' in self.data
                   ) or
                   self.t > 1200):
            self.step()
            if self.hs <= 0 and 'h' not in self.data:
                self.data['h'] = self.encode()
            if self.vs >= 0 and 'v' not in self.data:
                self.data['v'] = self.encode()
            if self.alt <= self.local_ground_alt and 's' not in self.data:
                self.data['s'] = self.encode()
            if len(self.booster.stages) <= self.stagecap and 'b' not in self.data:
                self.data['b'] = self.encode()
            if self.debug:
                print "time %d"%(self.t,)
                print "(%g, %g) -> (%g, %g)"%(self.downrange, self.alt, self.hs, self.vs)
                print "%s"%(''.join(self.data.keys()),)
        self.has_data = True
