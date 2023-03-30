# handle imports
import numpy as np
import matplotlib.pyplot as plt

# main method
if __name__ == "__main__":

    # set up storage
    data = {
        'mercury': [],
        'venus'  : [],
        'earth'  : [],
        'mars'   : [],
        'jupiter': [],
        'saturn' : [],
        'uranus' : [],
        'neptune': []
    }

    new_years = {
        'mercury': [],
        'venus'  : [],
        'earth'  : [],
        'mars'   : [],
        'jupiter': [],
        'saturn' : [],
        'uranus' : [],
        'neptune': []
    }

    # read in data
    names, periods = np.genfromtxt('../period_data.txt', dtype=str).T
    
    for name, period, i in zip(names, periods, range(len(periods))):
        data[name.lower()].append(period)

    # cast periods as float
    periods = periods.astype(float)
        
    print(f'No: {len(periods)}')

    ticks, labels = [], []
    for k, key in enumerate(data):
        ticks.append(k)
        labels.append(key.capitalize())

    # compare to theoretical
    planet_radii = np.genfromtxt('../planets.txt', dtype=float).T[2][1:]
    sun_mass = 332946. * 5.972e24 # kg
    planet_radii *= 1.495978707e11 # m
    p_t = 2 * np.pi * np.power(planet_radii, 1.5) / np.sqrt(sun_mass * 6.6743e-11)

    col = np.genfromtxt('../planets.txt', dtype=str).T[-1][1:]

    plt.figure(figsize=(8,8))
    # perform fitting
    residuals = np.zeros(len(data))
    errors = np.zeros(len(data))
    lab = np.zeros(len(data), dtype='U8')
    pers = np.zeros(len(data))
    for k, key in enumerate(data):
        onum = np.arange(1, len(data[key]), dtype=int)
        periods = np.diff(np.array(data[key]).astype(float)[np.array(data[key]).astype(float) > 0.])
        print(key, np.min(periods), np.max(periods))
        l, m, h = np.percentile(periods, [0.16, 0.50, 0.84])
        E = max(m-l, h-m)
        errors[k] = E
        pers[k] = m
        lab[k] = key.capitalize()
        plt.errorbar(k, m, yerr=E, label=f'{key.capitalize()} | T = {m:.2f} ± {E:.2e}', marker='.', capsize=5, ls='', c=col[k])
        plt.plot(k, p_t[k] / (60 * 60 * 24 * 365.25), marker='x', c=col[k])
        residuals[k] = m - p_t[k] / (60 * 60 * 24 * 365.25)

    # TODO: change storage of periods to individual files, write out etc 

    #plt.xlim(0, 100)
    plt.xticks(ticks, labels)
    plt.legend()
    plt.xlabel('Planet')
    plt.ylabel('Period [years]')
    plt.title('Planet vs Period')
    plt.savefig('../figures/periods.png')    

    plt.figure(figsize=(8,8))   
    for k, residual in enumerate(residuals):
        plt.errorbar(k, residual / pers[k], yerr = errors[k], ls='', marker='.', c=col[k], label=lab[k], capsize=5)
    plt.axhline(0.0, ls='dashed', c='gray', lw='.5')
    plt.xticks(ticks, labels) 
    plt.legend()
    plt.xlabel('Planet')
    plt.ylabel('Residual / Measured Period')
    plt.savefig('../figures/periods_residuals.png')  