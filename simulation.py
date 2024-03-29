# imports
import matplotlib.pyplot as plt
import numpy as np
import astropy.constants as constants
from body import Planet
from matplotlib.animation import FuncAnimation
import utils
import subprocess, sys

# simulation class
class Simulation(object):

    # -=-=-=- Initialisation Methods

    def __init__(self:object, path:str, pnum:int) -> None:
        
        # read in input file
        data = np.genfromtxt(path, delimiter='', dtype=str, skip_header=1)
        # set up array of objects
        self.planets = np.empty(pnum, dtype=object)
        for r, row in enumerate(data): #limit to inner planets
            self.planets[r] = Planet.Generate(row)
            if r == pnum-1:
                break
        #self.planets = np.array([Planet.Generate(row) for row in data], dtype=object)
        # set constants
        utils.SetConstants(self)
        # initialise simulation
        for planet in self.planets:
            planet.initialise(self.planets[0])

    # -=-=-=- Animation Methods -=-=-=-

    def Anim_init(self:object):
        """ initialises animation """
        return self.patches

    def Update(self:object, i:int):
        """ handles the updates and the animations """
        self.time = (i+1)*self.dt 
        # update all positions TODO: check all attribute labels
        for b, planet in enumerate(self.planets):
            planet.UpdatePosition() 
            self.patches[b].center = planet.position

        # loop through upper triangle excluding diagonal
        if self.experiments['jovian_influence']:
            for j, planet in enumerate(self.planets):
                if j == 0: continue
                planet.UpdateVelocity(self.planets[0])
        else:
            for j, planet in enumerate(self.planets):
                for k in range(0, self.planets.shape[0]):
                    if j != k:
                        planet.UpdateVelocity(self.planets[k])

        for p, planet in enumerate(self.planets):
            if planet.NewYear() and self.experiments['periods']:
                with open('./period_data.txt', 'a') as file:
                    file.write(f'{planet.name.capitalize()} {self.time}\n') 
                if self.options['verbose']:
                    print(f'{planet.name.capitalize()} has entered year {planet.year} [t = {self.time} years]')

        # doomsday experiment
        if self.experiments['alignment'] and i > 10:
            if self.Doomsday():
                if self.alignments == 0:
                    self.ti = self.time
                    self.i = i
                    self.alignments += 1
                elif self.alignments == 1 and i > self.i + 10:
                    with open('./Doomsday.txt', 'a') as file:
                        print(self.time, self.ti)
                        file.write(f'{len(self.planets)} | Alignment t = {self.time - self.ti}\n')
                        sys.exit()

        if i % 100 == 0:
            self.Times.append(self.time)
            self.TotalEnergies.append(self.TotalEnergy())
            if self.options['verbose']:
                print(f't = {self.time:.3f} years | E = {self.TotalEnergies[-1]:.4f} |{(i+1) * 100 / self.niter:.2f} %', end='\r')
            else:
                print(f'Progress: {(i+1) * 100 / self.niter:.2f} %', end='\r')

        return self.patches

    # -=-=-=- Energy Methods -=-=-=-

    def TotalKE(self:object) -> float:
        """ Determines the kinetic energies of all the objects in the sim """
        kinetic_energies = np.array([obj.KineticEnergy() for obj in self.planets])
        return np.sum(kinetic_energies)

    def TotalPE(self:object) -> float:
        potential_energies = np.array([obj.PotentialEnergy(self.planets) for obj in self.planets])
        return np.sum(potential_energies) / 2
    
    def TotalEnergy(self:object) -> float:
        self.KineticEnergies.append(self.TotalKE())
        self.PotentialEnergies.append(self.TotalPE())
        return self.KineticEnergies[-1] + self.PotentialEnergies[-1]

    # -=-=-=- Experiment Methods -=-=-=-

    def Doomsday(self:object) -> bool:
        angles = np.array([np.degrees(planet.Angle()) for planet in self.planets[1:]])
        mean_angle = np.mean(angles)
        angle_mask = (angles <= mean_angle + 2.5) & (angles >= mean_angle - 2.5)
        #print(len(angles))
        #print(len(angles[angle_mask]))
        if len(angles) == len(angles[angle_mask]):
            return True
        else:
            return False

    # -=-=-=- Running Methods -=-=-=-

    def SetOptions(self:object, options:dict) -> None:
       self.options = options

    def SetExperiments(self:object, experiments:dict) -> None:
        self.experiments = experiments
       
        self.alignments = 0 if self.experiments['alignment'] else -999.0
        self.ti = 0 if self.experiments['alignment'] else 0
        
        

    def Run(self:object):

        # set up plotting components
        fig = plt.figure(figsize=(8,8))
        ax  = plt.axes()
        plt.grid()

        # create patches array for bodies
        self.patches = []

        # energy storage arrays
        self.Times = []
        self.KineticEnergies = []
        self.PotentialEnergies = []
        self.TotalEnergies = []

        # get maximum radius for scaling the plot
        radii = [planet.orbit for planet in self.planets]
        maxOrb = np.sqrt(np.power(np.max(radii), 2))

        # add in the planet and moon patches
        for i, planet in enumerate(self.planets):
            factor = 0.005 if i == 0 else 0.005 # makes the sun look larger TODO: update to custom size array and change list to zip
            self.patches.append(ax.add_patch(plt.Circle(planet.position, factor * maxOrb, color=planet.colour, 
                                                        label=planet.name, animated=True)))

        # final plot set up
        limit = 1.1 * maxOrb
        ax.axis('scaled')
        ax.set_xlim(-limit, limit)
        ax.set_ylim(-limit, limit)
        ax.set_xlabel('X [AU]')
        ax.set_ylabel('Y [AU]')
        plt.legend(loc='lower center', bbox_to_anchor=(0.5, -1.0))
        plt.title('Solar System')

        # run animation and show
        if self.options['animate']:
            anim = FuncAnimation(fig, self.Update, init_func=self.Anim_init, frames=self.niter,
                                repeat = False, interval = 1, blit = True)
            plt.show()
        else:
            for iter in range(self.niter):
                self.Update(iter)

        # store for different variables:
        if self.experiments['euler']:
            label = 'euler'
        else:
            label = 'beeman'

        if self.experiments['jovian_influence']:
            label += '_jov'

        energy_table = np.array([self.Times, self.KineticEnergies, self.PotentialEnergies, self.TotalEnergies]).T
        np.savetxt(f'./SimulationEnergies-{label}.dat', energy_table, fmt=('%8.6s', '%20s', '%20s', '%20s'), header=' Time    KE                   PE	                Total')

        plt.figure(figsize=(8,8))
        plt.plot(self.Times, self.KineticEnergies, c='orchid', lw=.5, label='Kinetic', ls='dashed')
        plt.plot(self.Times, self.PotentialEnergies, c='mediumseagreen', lw=.5, label='Potential', ls='dashed')
        plt.plot(self.Times, self.TotalEnergies, c='slategray', lw=.75, label='Total')
        plt.xlabel('Time [years]')
        plt.ylabel('Energy [units]')
        plt.title(f'{label} Integration')
        plt.legend(loc='best')
        plt.savefig(f'./SimulationEnergies_{label}.png')
