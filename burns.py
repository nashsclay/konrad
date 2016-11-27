#!/usr/bin/python
# Simulates (airless) maneuver burn, for Astrogation console

import sim

class ManeuverSim(sim.RocketSim3D):
    orbitals = True
    UT = 0
    burnUT = 0
    def simulate(self, booster, throttle, pit, hdg, brad, bgm, inc, lan, tan, ape, ecc, sma):
        self.sim_setup(booster, 0, pit, hdg, brad, bgm, inc, lan, tan, ape, ecc, sma)
        burnT = self.burnUT - self.UT
        if burnT > 1200:
            self.data = {'0': {'time': burnT}}
            return
        while (self.t < burnT):
            if self.step():
                return
        self.data = {'0': self.encode()}
        self.throttle = throttle
        self.point(pit, hdg)
        while not ('b' in self.data or self.t > 1200):
            if self.step():
                return
            if len(self.booster.stages) <= self.stagecap and 'b' not in self.data:
                self.data['b'] = self.encode()
            if self.debug:
                print "time %d"%(self.t,)
                print "(%g, %g) -> (%g, %g)"%(self.downrange, self.alt, self.hs, self.vs)
                print "%s"%(''.join(self.data.keys()),)

# notes:
# burnsim should offer 'start' and 'rotating' frames for 'fixed' mode, and also have 'prograde' mode
