def mostwind():

kappa=0.4
if (dh .ge. z):
    MOST_Wind = sqrt(2.0)*sigmav
else
    if (L>0.0):
        psi1=-17.0*(1-exp(-0.29*(z-dh)/L))  
        psi2=-17.0*(1-exp(-0.29*z0/L))    
    else     
        x1=(1.0-16.0*(z-dh)/L)**0.25; x2=(1.0-16.0*z0/L)**0.25     
        psi1=2.0*log((1.0+x1)/2.0)+log((1.0+x1*x1)/2.0)-2.0*atan(x1)+pi/2.0     
        psi2=2.0*log((1.0+x2)/2.0)+log((1.0+x2*x2)/2.0)-2.0*atan(x2)+pi/2.0     
    endif
    MOST_Wind=ust*(log((z-dh)/z0)-psi1+psi2)/kappa

return MOST_Wind
