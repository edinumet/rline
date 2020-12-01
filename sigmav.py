
#     This subroutine calculates sigmav using ustar and wstar
def sigmav(ustar,vstar):
    sigmav_calc = sqrt((0.6*wstar)**2+(1.9*ustar)**2) 
    # sigmav calculated from wstar and ustar
    sigmav      = max(sigmav_calc,0.2)  
    angle       = 270.0 - Wdir
    if (angle > 180.0) :            
        angle = angle - 360.0
    return sigmav
    #return thetaw = angle*pi/180.0
