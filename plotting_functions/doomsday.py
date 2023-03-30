# imports
import numpy as np
import matplotlib.pyplot as plt

# main method
if __name__=="__main__":

    # read in doomsday data
    doomsday = np.genfromtxt('../Doomsday.txt', dtype=float).T

    # get ticks
    ticks, labels = [], []
    planets = ['mercury', 'venus', 'earth', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune']
    for i in range(len(doomsday[0]) + 1):
        ticks.append(i+1)
        labels.append(planets[i].capitalize())
        
    # add in some log fit or something 
    logs = np.log(doomsday[1])
    cov = np.polyfit(doomsday[0].astype(int)-1, logs, 1)
    #print(cov)
    #theoretical_nep = np.exp(cov[0] + 9. * cov[1])

    plt.figure(figsize=(8,8))
    plt.semilogy(doomsday[0].astype(int) - 1, doomsday[1], 'o', ls='', c='mediumseagreen')
    #plt.plot(9, theoretical_nep, 'o', ls='', c='orchid')
    plt.xticks(ticks, labels) 
    plt.xlabel('Number of Planets')
    plt.ylabel('log Years between Alignments')
    plt.savefig('../figures/doomsday_alignments.png')