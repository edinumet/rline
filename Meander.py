def Meander(X,Y,Z):
#     This function calculates the contribution of a point source at (X,Y,Z)
#     to a receptor at (Xr_rot,Yr_rot,Zrcp) assuming that the material
#     spreads out radially in all directions
#-----------------------------------------------------------------------------------
    R       = sqrt((Xr_rot-X)**2+(Yr_rot-Y)**2) ! This is the radial distance to the receptor   
    R       = max(R,xd_min)
    heff    = Z 
    Effective_Wind(R,heff)
    sz      = sigmaz(R) ! Effective sigmaz
    Vert    = math.sqrt(2.0/pi)*(expx(-0.5*((heff-Zrecep)/sz)**2)+
                expx(-0.5*((heff+Zrecep)/sz)**2))/(2.0*sz*ueff)  
                 # Accounts for source height
    Horz    = 1.0/(2.0*math.pi*R);
    Meander = Vert*Horz;
     
    return Meander
