 # imports
import numpy as np

# class
class Planet(object):

    # -=-=-=- Initialisation methods -=-=-=-

    def __init__(self:object, name:str, mass:float, radius:float, orbit:float, period:float, colour:str) -> None:
        """ Initialise a celestial body given certain parameters """
        self.name = name
        if 'msun' not in mass:
            self.mass = float(mass)
        else:
            self.mass = 1 * float(mass.strip('msun'))
        self.col  = colour.strip()
        # set initial position
        self.rorbit = float(orbit)
        self.position = np.array([orbit, 0.0])

    def InitialiseVelocity(self:object, v:list) -> None:
        """ Initialse object with given velocity """
        self.velocity = v

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
    
    def KineticEnergy(self:object) -> float:
        """ Calculates and returns kinetic energy in Joules """
        return (np.dot(self.velocity, self.velocity)) * self.mass / 2