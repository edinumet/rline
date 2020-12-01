def Point_Conc(X,Y,Z):

    # Initialize point and meander concentrations
    Conc_p = 0.0
    Conc_m = 0.0
    fran   = 0.0
    sy     = 0.0
    xd     = Xr_rot-X
    heff   = Z  
        
    Effective_Wind(xd,heff)
    
    # Calculate direct plume concentration
    if xd<0.0001:     
        Conc_p = 0.0   
    else
        xd     = max(xd,xd_min)
        yd     = Yr_rot-Y
        sz     = sigmaz(xd) 
        sy     = sigmay(xd)
        vert   = math.sqrt(2.0/pi)*(expx(-0.5*((heff-Zrecep)/sz)**2)&
                 +expx(-0.5*((heff+Zrecep)/sz)**2))/(2.0*sz*ueff)
        horz   = 1/(math.sqrt(2.0*pi)*sy)*expx(-0.5*(yd/sy)**2)
        Conc_p = vert*horz 


    # Calculate meander concentration
    fran   = 2.0*sigmav*sigmav/(ueff*ueff)    
    Conc_m = Meander(X,Y,Z)

    # Combine direct plume and meander contributions
    if op_C =='M':
        Point_Conc = Conc_m*fran
    elif op_C =='P':
        Point_Conc = Conc_p*(1-fran)
    else
        Point_Conc = Conc_p*(1-fran)+Conc_m*fran
     
     return Point_Conc
      
