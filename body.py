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
        # set constants
        self.SetConstants()

    def SetConstants(self:object) -> None:
        self.Msun = 3
        self.Mearth = 3
        self.G = 1.18638e-4 # AU^3 / Msun / yr^2
        self.dt = 0.01 # or 300? not sure
        self.niter = 100000

    def InitialiseVelocity(self:object, v:np.ndarray) -> None:
        """ Initialse object with given velocity """
        self.velocity = v

    def InitialiseAccelerations(self:object,) -> None:
        pass

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
    
    def UpdatePosition(self:object, dt:float) -> None:
        """ Update the position """
        self.radius_old = self.radius
        self.radius = self.radius_old  + self.velocity * dt + \
                      dt ** 2 * (4 * self.acceleration - self.acceleration_old) / 6

    def UpdateVelocity(self:object, dt:float, planet:object) -> None:
        """ Update the velocity """
        self.UpdateAcceleration(dt, planet)
        self.velocity_old = self.velocity + dt ** 2 * \
                            (2 * self.acceleration_new + 5 * self.acceleration \
                             - self.acceleration_old) / 6
        # cycle accelerations
        self.acceleration_old = self.acceleration
        self.acceleration = self.accerelation_new


    def UpdateAcceleration(self:object, planet:object) -> None:
        """ Update the velocity"""
        position = self.radius - planet.radius
        self.acceleration_new = - self.G * planet.mass * position \
                                / np.power(np.linalg.norm(position), 3)

    # -=-=-=- Additonal Methods -=-=-=-
    def KineticEnergy(self:object) -> float:
        """ Calculates and returns kinetic energy in Joules """
        return (np.dot(self.velocity, self.velocity)) * self.mass / 2