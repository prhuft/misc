"""
	Arbitrary random dists, April 2019
	Preston Huft
	
	Accept-reject method for a desired distribution f(x). Originally used in my
	mot simulation code. Simply edit f0, and f in lines 18 and 24 below to be a 
	the desired distribution. 
"""

def gaussian_dist(n,mean,sigma,domain,showplot=False):
    """return a 1D array of randoms with a gaussian pdf. 
       mean: the average value
       sigma: the std
       domain: the dist's domain. e.g. domain = 100 would
       generate a gaussian dist f(x) for x on (mean-domain/2,mean+domain/2)
    """
    var = sigma**2
    f0 = (1/m.sqrt(2*m.pi*var)) # the normalization const
    y_dist = np.empty(n) # the
    f_dist = np.empty(n) 
    x_dist = np.empty(n) # this is the distribution we want
    j = 0 # dist index
    while j < n:
        x = domain*(rand()-.5)+mean # rand val on domain of f(x)
        f = f0*m.exp(-(x-mean)**2/(2*var))
        y = rand()*f0 # rand val on range of f(x)
        if y <= f:
            y_dist[j]=y
            f_dist[j]=f
            x_dist[j]=x # x vals with desired pdf
            j+=1
            
    # plot distribution as a check:
    if showplot is not False:
        plt.scatter(x_dist,y_dist,c='red',s=10)
        plt.scatter(x_dist,f_dist,c='blue',s=10)
        plt.show()
    
    return x_dist

