# imports
import matplotlib.pyplot as plt
import numpy as np
import astropy.constants as constants
from body import Planet

# simulation class
class Simulation(object):

    def __init__(self:object, path:str) -> None:
        
        # read in input file
        data = np.genfromtxt(path, delimiter='', dtype=str, skip_header=1)
        # set up array of objects
        self.planets = np.array([Planet.Generate(row) for row in data], dtype=object)
        # TODO: worth adding some idea of visualisation rather than radius 
        # set initial velocities
        # set constants
        self.SetConstants()
        # initialise simulation
        self.InitialiseVelocities()

        for p in self.planets:
            print(p.name)

    def SetConstants(self:object) -> None:
        self.Msun = 3
        self.Mearth = 3
        self.G = 1.18638e-4 # AU^3 / Msun / yr^2
        self.dt = 0.01 # or 300? not sure
        self.niter = 100000

    def InitialiseVelocities(self:object) -> None:
        """ initialises the velocities of all objects, assuming that the sun 
            starts off the simulation with zero velocity """
        for p, planet in enumerate(self.planets):
            # assuming sun stays stationary / no 
            if p == 0:
                planet.InitialiseVelocity(np.zeros(2, dtype=float))
            else:
                mag_r = np.linalg.norm(planet.rorbit)
                tan_vel = np.sqrt(self.G * self.planets[0].mass / mag_r)
                planet.InitialiseVelocity(np.array([0., tan_vel]))

            print(planet.velocity)


    def TotalKE(self:object) -> float:
        """ Determines the kinetic energies of all the objects in the sim """
        kinetic_energies = np.array([obj.KineticEnergy() for obj in self.bodies])
        return np.sum(kinetic_energies)
