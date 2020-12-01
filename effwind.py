def Effective_Wind(xd,heff):

    sq2pi = 0.797885
    sz=sigmaz(xd)
    err=10
    iter=1
    uref = MOST_Wind(refht,zrough,dispht,ustar,Lmon)
    ueff=MOST_Wind(heff,zrough,dispht,ustar,Lmon)*Wspd/uref
   
    while ((err>1.0e-02) and (iter<20)):
        zbar = sq2pi*sz*exp(-0.5*(heff/sz)**2)+heff*erf(heff/(sqrt(2.0)*sz))
        ueff=MOST_Wind(max(zbar,heff),zrough,dispht,ustar,Lmon)*Wspd/uref
        ueff=sqrt(2*sigmav**2+ueff**2)
        sz_new=sigmaz(xd)
        err=abs((sz_new-sz)/sz)
        sz=sz_new; iter=iter+1
    return ueff

  
