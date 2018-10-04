def sigmay(xd):
    sz=sigmaz(xd)
    sz = sqrt(sz**2-sigmaz0**2)
    if (Lmon > 0) then     # stable
        sigmay = 1.6*sigmav/ustar*sz*(1.0+2.5*sz/abs(Lmon)) 
    else # convective
        sigmay = 1.6*sigmav/ustar*sz*(1.0+1.0*sz/abs(Lmon))**(-1.0/2.0) 

    return sigmay = sqrt(sigmay**2+sigmay0**2)
