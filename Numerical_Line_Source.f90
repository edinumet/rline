! ----------------------------------------------------------------------------------- !
! The Research LINE source (R-LINE) model is in continuous development by various     !
! groups and is based on information from these groups: Federal Government employees, !
! contractors working within a United States Government contract, and non-Federal     !
! sources including research institutions.  These groups give the Government          !
! permission to use, prepare derivative works of, and distribute copies of their work !
! in the R-LINE model to the public and to permit others to do so.  The United States !
! Environmental Protection Agency therefore grants similar permission to use the      !
! R-LINE model, but users are requested to provide copies of derivative works or      !
! products designed to operate in the R-LINE model to the United States Government    !
! without restrictions as to use by others.  Software that is used with the R-LINE    !
! model but distributed under the GNU General Public License or the GNU Lesser        !
! General Public License is subject to their copyright restrictions.                  !
! ----------------------------------------------------------------------------------- !

      subroutine Numerical_Line_Source(im,ir,Conc_Num,Err)
! -----------------------------------------------------------------------------------
!     Written by AV, MGS and DKH
!     RLINE v1.2, November 2013
!
!     This functions calculates the contribution to concentration 
!     at a receptor due to a line source using Romberg integration 
!
! -----------------------------------------------------------------------------------

      use Line_Source_Data
      implicit none

! External functions:
      real(kind=double)     :: Point_Conc

! Local variables:
      integer, intent(in)             :: im,ir      ! met,receptor indices, respectively
      real(kind=double), intent(out)  :: Conc_Num
      real(kind=double), intent(out)  :: Err        ! The integration is set to an arbitrarily large value before it is reduced

      integer                         :: K=3  ! 2K is the order of Romberg integration.  Nmax needs to be greater than K
                                              ! for Romberg integration to be used. Otherwise trapezoidal integration is used.
      real(kind=double)               :: Xdif,Ydif,Zdif     ! Limits of the integral
      real(kind=double)               :: Disp ! Dummy variable used to store integral
      real(kind=double),Allocatable   :: h(:), Conc(:)  ! Step size, succesive approximations of the concentration 
      real(kind=double)               :: hdum(3), Concdum(3)             ! Step size, succesive approximations of the concentration 
      integer                         :: No_Points, j, is, minj, It_lim  ! Number of points added in eaxh step, Counting index 
      integer                         :: AllocateStatus, AllocError
      real(kind=double)               :: Conc_int               ! Numerical Integrals
      real(kind=double)               :: X, Y,Z,delt,theta,phi
      real(kind=double)               :: t,tmax,cost,sint,sinp,cosp,Xrec,dr
      real(kind=double)               :: Xtemp,Ytemp,Ztemp
      integer                         :: st, fi    ! Starting and finishing indices 

! Parameters
      Real(kind=double)               :: xinterp=0.0

! -----------------------------------------------------------------------------------

! ----Initialize source and receptor variables     
      Conc_Num=0.0

! ----orient the end points so the begining has a lower Y value
      if (Ysend < Ysbegin) then
        Xtemp   = Xsend
        Ytemp   = Ysend
        Ztemp   = Zsend
        Xsend   = Xsbegin
        Ysend   = Ysbegin
        Zsend   = Zsbegin
        Xsbegin = Xtemp
        Ysbegin = Ytemp
        Zsbegin = Ztemp 
      end if

      Xdif  = Xsend-Xsbegin  
      Ydif  = Ysend-Ysbegin
      Zdif  = Zsend-Zsbegin
      theta = datan2(Ydif,Xdif)
      tmax  = sqrt(Xdif*Xdif+Ydif*Ydif+Zdif*Zdif)    
      phi   = asin(Zdif/(tmax+sm_num))  

      sinp  = sin(phi)
      cosp  = cos(phi)
      cost  = cos(theta)
      sint  = sin(theta)

! ----Find x-coord of point on source line directly upwind of receptor
      Xrec = (Xsend -(Ysend-Yr_rot)*(Xsend-Xsbegin)/(Ysend-Ysbegin))
      dr   = abs(Xr_rot- Xrec)
      dr   = max(xd_min, dr)  ! This keeps the user from putting receptor on source

! ----Convergence Criteria: Minimum Iteratons ------------    
      if ((Yr_rot > Ysbegin-tmax/2*abs(cost)) .and. (Yr_rot < Ysend+tmax/2*abs(cost)))then              
        minj = ceiling(log(2.0*tmax/(max(xd_min,dr*abs(sint)))-2.0)/log(2.0))+2
      else 
        minj = 0 ! set minj=0 so if receptor is upwind, the conc will converge quickly
      end if
      if((Xr_rot<Xsbegin).and.(Xr_rot<Xsend)) minj = 0 !True if receptor is upwind of the line

      It_lim = max(10,2*minj)

      if((abs(dr*sint) .le. xd_min).AND. op_warn == 'N')then
        write(*,*) "WARNING: A receptor is within one-meter of a line source; convergence may be incomplete. "
        write(*,*) "Occurance at: met line ", im, " with receptor # ", ir, " and source # ", indq, ". "
      end if

      allocate(h(It_lim),Stat=AllocateStatus)
      allocate(Conc(It_lim),Stat=AllocateStatus)

! ----Compute Concentration at Receptor ------------
      sigmaz0 = Source(indq)%init_sigmaz      
      Conc    = 0.0  ! Initialize concentrations  
      Disp    = (Point_Conc(Xsbegin,Ysbegin,Zsbegin)+ Point_Conc(Xsend,Ysend,Zsend))*0.5
      Conc(1) = Disp*tmax ! This is the first approximation of the integral
      h(1)    = 1.0   ! This is the relative size of the integration interval

! ----Trapezoidal integration 
      do j=2,It_lim                 
        No_Points = 2**(j-2)    
        delt      = tmax/No_Points    
        t         = delt/2
        Disp      = 0.0
        do is=1,No_Points
          X    = t*cost*cosp+Xsbegin
          Y    = t*sint*cosp+Ysbegin
          Z    = t*sinp+Zsbegin
          Disp = Disp+Point_Conc(X,Y,Z)
          t    = t+delt
        end do
        Conc(j) = (Disp*delt+Conc(j-1))/2
        h(j)    = 0.25*h(j-1)  ! See page 134 in "Numerical Receipes" for an explanation
    
! ------Romberg integration is invoked if j>=K
        if (j>=K) then
          st       = j-K+1
          fi       = st+K-1
          hdum     = h(st:fi)
          Concdum  = Conc(st:fi)
          Call polyinterp(Conc_Int,Err,hdum,Concdum,xinterp,K) ! Extrapolates to h=0.0 to  compute integral             
          Conc_Num =abs(Conc_Int)
          
! --------Check convergence criteria          
          if ((abs(Err) < Error_Limit) .and. (j > minj)) then
            deallocate(h,Conc,Stat=AllocError)
            return
          end if
        end if
        Conc_Num = abs(Conc(j))
      end do

      end