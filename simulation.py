# imports
import matplotlib.pyplot as plt
import numpy as np
import astropy.constants as constants
from body import Planet
from matplotlib.animation import FuncAnimation

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
        self.dt = 300 # or 300? not sure
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

    def Anim_init(self:object):
        """ initialises animation """
        return self.patches

    def Update(self:object, i:int):
        """ handles the updates and the animations """
        self.time = (i+1)*self.dt
        
        # update all positions TODO: check all attribute labels
        for b, planet in enumerate(self.planets):
            planet.UpdatePosition(...) # TODO: add arguments
            self.patches[b].center = planet.radius

        # loop through upper triangle excluding diagonal
        for j, planet in enumerate(self.planets):
            for k in range(j+1, self.planets.shape[0]):
                planet.UpdateVelocity(self.dt, self.planets[k])

        # add in year calculation here I guess?
        return self.patches

    def TotalKE(self:object) -> float:
        """ Determines the kinetic energies of all the objects in the sim """
        kinetic_energies = np.array([obj.KineticEnergy() for obj in self.bodies])
        return np.sum(kinetic_energies)

    def Run(self:object):

        # set up plotting components
        fig = plt.figure()
        ax  = plt.axes()

        # create patches array for bodies
        self.patches = []

        # get maximum radius for scaling the plot
        radii = [planet.radius for planet in self.planets]
        maxOrb = np.sqrt(np.power(np.max(radii), 2))

        # add in the planet and moon patches
        for i, planet in enumerate(self.planets):
            factor = 0.05 if i == 0 else 0.02 # makes the sun look larger TODO: update to custom size array and change list to zip
            self.patches.append(ax.add_patch(plt.Circle(planet.radius, factor * maxOrb, color=planet.colour, animated=True)))

        # final plot set up
        limit = 1.2 * maxOrb
        ax.axis('scaled')
        ax.set_xlim(-limit, limit)
        ax.set_ylim(-limit, limit)

        # run animation and show
        anim = FuncAnimation(fig, self.Update, init_func=self.Anim_init, frames=self.niter,
                             repeat = False, interval = 1, blit = True)
        plt.show()