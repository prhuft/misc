# pseudocode here

atoms = ensemble(size) # generate atom dist with x,v,|c_i|^2
dt ~ lifetime
steps = 100

# first, some sanity checks
vstd = std(atoms.v)
xstd = std(atoms.x)

vavg = empty(len(steps),object)
xavg = empty(len(steps),object)

for a in atoms:
    
    vlist = empty(steps) 
    xlist = empty(steps)
    
    for i in range(steps):
        
        cg,ce,v,x = a.state # the current atom state

        tlist = linspace(0,dt,100) # dt ~ pi time
        solg,sole = master_eq(a.state,v,x) # the population dist
        plot(tlist,sol) # sanity check

        cg = accept_reject({tlist,solg},dt) # 1 or 0
        ce = 1-c_g

        x = v*dt
        k_eff = (omega+k*v)/c
        v = v-(hbar*k_eff/mRb)*c_e
        
        xlist[i]=x
        vlist[i]=v
        
        # update the atom state
        a.state = [cg,ce,v,x]
    
    # sanity checks
    plot(range(steps),xlist) 
    plot(range(steps),vlist)
    
    # update the lists to-be-averaged, el-wise addition
    xavg += xlist #
    vavg += vlist
    
# finish the averages
xavg /= len(atoms)
vavg /= len(atoms)

# plot temp 
temps = [(.5*mRb*v**2)/kB for v in vavg]
plot(range(steps),temps/1e-6)