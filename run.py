from simulation import Simulation
import sys
import argparse

if __name__=="__main__":

    # experiments
    experiment_list = ['mars_satellite', 'jupiter_satellite', 'asteroids', 'euler', 'alignment', 'jovian_influence', 'periods']

    # handle command line inputs
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--planets', choices=range(2, 10), required=True, type=int,
                        help='input number of planets')
    parser.add_argument('-e', '--experiments', choices=experiment_list, nargs='+', required=False,
                        help='input list of experiments to run', default='NONE')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='verbose output')
    parser.add_argument('-a', '--animate', action='store_true',
                        help='animation output')
    args = parser.parse_args()

    # generate simulation object
    solar_system = Simulation('planets.txt', args.planets)

    # this is where you will practise argparser to set options and experiments

    # this is where you can change the options
    options = {
            'animate'  : args.animate,
            'verbose'  : args.verbose,
            'anim_save': False,
               } 
    solar_system.SetOptions(options)

    # this is where you can alter the experiments
    experiments = {
            'mars_satellite'   : False,
            'jupiter_satellite': False,
            'asteroids'        : False,
            'euler'            : False,
            'alignment'        : False,
            'jovian_influence' : False,
            'periods'          : False,
            'NONE'             : False
        }
    for experiment in args.experiments:
        experiments[experiment] = True
    solar_system.SetExperiments(experiments)

    # run the simulation    
    solar_system.Run()

    # extract plots