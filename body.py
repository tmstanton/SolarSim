 # imports
import numpy as np
import sys
import utils

# class
class Planet(object):

    # -=-=-=- Initialisation methods -=-=-=-

    def __init__(self:object, name:str, mass:float, orbit:float, colour:str) -> None:
        """ Initialise a celestial body given certain parameters """
        self.name = name
        self.colour  = colour #.strip()
        # set constants
        utils.SetConstants(self)
        self.orbit = float(orbit) * self.EARTHR
        self.mass = float(mass) * self.EARTHMASS
        self.year = 0

    def initialise(self, p):
        # inital position, initial coords = (orbit radius, 0)
        self.position = np.array([self.orbit, 0])
        # inital velocity, tangential to position
        # speed = sqrt(G*marsmass/r)
        if (self.orbit == 0.0):
            self.velocity = np.array([0, 0])
        else:
            vel = np.sqrt(self.G*p.mass/self.orbit)
            self.velocity = np.array([0, vel])
        # intial accelatation, using gravitational force law
        if (self.orbit == 0.0):
            self.acceleration = np.array([0, 0])
        else:
            self.acceleration = self.UpdateAcceleration(p)
        # set acc_old = acc to start Beeman
        self.acceleration_old = self.acceleration

    def InitialisePosition(self:object) -> None:
        """ Initialise object with a given position """
        self.position = np.array([self.orbit, 0.0])

    def InitialiseVelocity(self:object, v:np.ndarray) -> None:
        """ Initialse object with given velocity """
        self.velocity = np.array(v)

    def InitialiseAcceleration(self:object, a:np.ndarray) -> None:
        """ Initialise the object with a given acceleration """
        self.acceleration = np.array(a)
        self.acceleration_old = np.array(a) # set to initialise beeman

    @staticmethod
    def Generate(row:tuple) -> object:
        # disect row tuple, adjust mass units
        return Planet(*row) 

    # -=-=-=- Euler-Cromer Update Methods -=-=-=- 

    def UpdatePosition_EC(self:object, dt:float) -> None:
        """ Update the position using Euler-Cromer for a given time
            Note: must be done first, as uses current velocity """
        self.position = self.position + self.velocity * dt

    def UpdateVelocity_EC(self:object, a:float, dt:float) -> None:
        """ Update velocity using Euler-Cromer for a given acceleration and time
            Note: Does this second, as uses updated position """
        self.velocity = self.velocity + a * dt

    # -=-=-=- Beeman Update Methods -=-=-=-

    def UpdatePosition(self:object) -> None:
        # keep old position to check for year
        self.position_old = np.copy(self.position)
        
        # update position first: Beeman
        self.position = self.position_old + self.velocity*self.dt + (4*self.acceleration - self.acceleration_old)*self.dt*self.dt/6.0
        

    def UpdateVelocity(self:object, planet:object) -> None:
        # update velocity second: Beeman
        self.acceleration_new = self.UpdateAcceleration(planet)
        self.velocity = self.velocity + (2*self.acceleration_new + 5*self.acceleration - self.acceleration_old)*self.dt/6.0
        # now update acc ready for next iteration
        self.acceleration_old = self.acceleration
        self.acceleration = self.acceleration_new
        
        
    def UpdateAcceleration(self:object, planet:object) -> None:
        # update acc (gravitational force law)
        pos = self.position - planet.position
        self.acceleration = -self.G*planet.mass*pos/np.power(np.linalg.norm(pos),3)
        return self.acceleration

    # -=-=-=- Additonal Methods -=-=-=-

    def KineticEnergy(self:object) -> float:
        """ Calculates and returns kinetic energy in Joules """
        return (np.dot(self.velocity, self.velocity)) * self.mass / 2
    
    def PotentialEnergy(self:object, planet_array:np.ndarray) -> float:
        potential_energies = 0
        for i, planet in enumerate(planet_array):
            if self.name == planet.name:
                continue
            rij = np.linalg.norm(self.position - planet.position)
            potential_energies -= self.G * self.mass * planet.mass / rij
        return potential_energies

    def NewYear(self:object) -> bool:
        """ Determine when the body enters a new year by crossing the 
            x axis """
        if (self.position_old[1] < 0.0) & (self.position[1] >= 0.0):
            self.year += 1
            return True
        else:
            return False
        
    def Angle(self:object) -> float:
        # get angle from x = 0
        return np.arctan2(self.position[1], self.position[0])