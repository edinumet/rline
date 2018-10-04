def createexptable():

#     Creates a look-up table based on arguments of the built-in 
#     exponential function to improve computation time.
#
    delexp=20.0/999.0;
    Xexp(1)=-20.0
    ext(1)=exp(Xexp(1))

    for ind in range(2, 1000):
        Xexp(ind)=Xexp(ind-1)+delexp
        ext(ind)=exp(Xexp(ind))

    for ind in range(1, 999):
        Bexp(ind)=(ext(ind+1)-ext(ind))/(Xexp(ind+1)-Xexp(ind))
        Aexp(ind)=ext(ind)-Bexp(ind)*Xexp(ind)

      Bexp(1000)=Bexp(999) 
      Aexp(1000)=Aexp(999)

return Aexp, Bexp



