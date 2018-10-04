def sigmaz(xd,zmixed,Lmon):
    sq2pi=0.797885
    xbar       = abs(xd/Lmon)
    xdabs      = abs(xd)
    sigmaz_max = sq2pi*zmixed
    sigmazD    = 0.0
    sigmazB    = 0.0
    utemp      = ueff # use profiled wind speed, Ueff, for Udisp 
    # ignore Barrier and depression induced dispersion for the moment
    #HB         = Source(indq)%hwall
    #dw         = (Source(indq)%dCL_wall - Source(indq)%dCL)

# vertical dispersion curve 
    if (Lmon > 0.0) then     
        sigz = 0.57*(ustar*xdabs/utemp)/(1.0+3.0*(ustar/utemp)*(xbar)**(2.0/3.0))
    else      
        sigz = 0.57*(ustar*xdabs/utemp)*(1.0+1.5*(ustar/utemp*xbar))   

    sigz=sqrt(sigmazD*sigmazD+sigz*sigz+sigmaz0*sigmaz0)+sigmazB
    
    return sigmaz=min(sigz,sigmaz_max)
