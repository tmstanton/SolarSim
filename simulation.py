# imports
import matplotlib.pyplot as plt
import numpy as np
import astropy.constants as constants

# simulation class
class Simulation(object):

    def __init__(self:object, path:str) -> None:
        
        # read in input file
        # set up array of objects
        # set initial velocities
        # set constants
        # initialise simulation
        pass

    def SetConstants(self:object) -> None:
        self.Msun = 3
        self.Mearth = 3
        self.G = constants.G # 1.18638e-4 AU^3 / Msun / yr^2
        self.dt = 0.01 # or 300? not sure
        self.niter = 100000

    def InitialiseVelocities(self:object) -> None:
        pass

    def TotalKE(self:object) -> float:
        """ Determines the kinetic energies of all the objects in the sim """
        kinetic_energies = np.array([obj.KineticEnergy() for obj in self.bodies])
        return np.sum(kinetic_energies)