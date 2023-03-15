def SetConstants(object:object) -> None:
    object.G = 1.18638e-4 #6.67e-11 #1.18638e-4 # AU^3 / Msun / yr^2
    object.dt = 0.001 #60 * 60 * 24 # or 300? not sure
    object.niter = 100000
    object.EARTHR = 1 #1.496e11
    object.EARTHMASS = 1 #5.972e24
    object.SUNMASS = 2e30
    object.MASSRATIO = 1 #self.SUNMASS / self.EARTHMASS