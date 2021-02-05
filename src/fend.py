import ipywidgets as widgets


class fend():
    # Should now scale for the time of day effect
    # TAF - Temporal Allocation Factor
    #  Get from up-to-date Tom Tom web site: 
    #      https://www.tomtom.com/en_gb/traffic-index/edinburgh-traffic/
    #  For a typical Wednesday since that seems to be the eveing rush-hour with most    congestion
    # TAF list has % congestion by hour starting at hour 0, midnight
    # In Jupyter Notebook make this a Figure
    TomTom_congestion = [2, 0, 0, 0, 0, 0, 13, 54, 80, 50, 38, 38, 40, \
        40, 42, 55, 81, 86, 54, 30, 20, 16, 14, 8]
    #print(sum(TomTom_congestion))
    trafficstats = {"AADT": 10000,
                "hour": 12,
                "vs": 15
               }
    # Now adjust for fleet Mix and AADT and Time
    # Defaults -  get from spreadsheet for 2020
    # Urban split for England in 2020 below since that's likely to be the most relevant
    # Use a selection box for this
    fleetmix_2020 = {"electric": 0.5, 
                     "petrol": 47.8, 
                     "diesel":33.1,
                     "petrol_lgv": 0.4,
                     "diesel_lgv": 15.0,
                     "rigid": 0.9,
                     "artic": 0.4,
                     "biodiesel": 0.1,
                     "buses": 0.7,
                     "motorcycle": 1.1
                    }
    sumt=0.0
    #for x in fleetmix_2020.values():
    #  sumt=sumt+x
    #sumtt=(str(int(sumt)))
    #print(sumtt)

    # All this to go into separate python code to be imported
    bft_electric = widgets.BoundedFloatText(value = fleetmix_2020["electric"], min=0.1,     max=90, step=1, 
                                     description="electric %", width=50)
    bft_petrol_cars = widgets.BoundedFloatText(value = fleetmix_2020["petrol"], min=5, max=75, step=0.5, 
                                        description="petrol cars %", width=50)
    bft_diesel_cars = widgets.BoundedFloatText(value =fleetmix_2020["diesel"],  min=5, max=75, step=0.5, 
                                        description="diesel cars %", width=50)
    bft_petrol_lgv = widgets.BoundedFloatText(value =fleetmix_2020["petrol_lgv"], min=0.1, max=0.8, step=0.1, 
                                       description="petrol lgv %", width=50)
    bft_diesel_lgv = widgets.BoundedFloatText(value=fleetmix_2020["diesel_lgv"], min=3, max=18, step=1, 
                                       description="diesel lgv %", width=50)
    bft_rigid_truck = widgets.BoundedFloatText(value=fleetmix_2020["rigid"],min=0.1, max=1.0, step=0.1, 
                                        description="rigid truck %", width=50)
    bft_artic_truck = widgets.BoundedFloatText(value=fleetmix_2020["artic"], min=0.1, max=0.6, step=0.1, 
                                        description="artic truck %", width=50)  
    bft_biodiesel = widgets.BoundedFloatText(value=fleetmix_2020["biodiesel"], min=0.1, max=1.0,step=0.1, 
                                      description="biodiesel %", width=50)
    bft_buses = widgets.BoundedFloatText(value=fleetmix_2020["buses"], min=0.1, max=1.5, step=0.1, 
                                  description="buses %", width=50)
    bft_motorcycles = widgets.BoundedFloatText(value=fleetmix_2020["motorcycle"], min=0.5, max=1.5, step=0.1, 
                                        description="motorcycles %", width=50)
    sumtotal = widgets.Text(value=sumtt,description="Total should be 100%", width=50, color='red')

    def checksum():
        sum=0.0
        for x in fleetmix_2020.values():
            sum=sum+x
        sumt=sum
        sumtt=(str(int(sumt))) # make it an integer so students don't chase getting exactly 100.0
        sumtotal.value = sumtt
           
    def bft_electric_eventhandler(change):
        bft_electric.observe(bft_electric_eventhandler, names='value')
        fleetmix_2020["electric"]=bft_electric.value
        checksum()

    def bft_petrol_cars_eventhandler(change):
        bft_petrol_cars.observe(bft_petrol_cars_eventhandler, names='value')
        fleetmix_2020["petrol"]=bft_petrol_cars.value
        checksum()

    def bft_diesel_cars_eventhandler(change):
        bft_diesel_cars.observe(bft_diesel_cars_eventhandler, names='value')
        fleetmix_2020["diesel"]=bft_diesel_cars.value
        checksum()

    def bft_petrol_lgv_eventhandler(change):
        bft_petrol_lgv.observe(bft_petrol_lgv_eventhandler, names='value')
        fleetmix_2020["petrol_lgv"]=bft_petrol_lgv.value
        checksum()

    def bft_diesel_lgv_eventhandler(change):
        bft_diesel_lgv.observe(bft_diesel_lgv_eventhandler, names='value')
        fleetmix_2020["diesel_lgv"]=bft_diesel_lgv.value
        checksum()

    def bft_rigid_truck_eventhandler(change):
        bft_rigid_truck.observe(bft_rigid_truck_eventhandler, names='value')
        fleetmix_2020["rigid"]=bft_rigid_truck.value
        checksum()

    def bft_artic_truck_eventhandler(change):
        bft_artic_truck.observe(bft_artic_truck_eventhandler, names='value')
        fleetmix_2020["artic"]=bft_artic_truck.value
        checksum()

    def bft_biodiesel_eventhandler(change):
        bft_biodiesel.observe(bft_biodiesel_eventhandler, names='value')
        fleetmix_2020["biodiesel"]=bft_biodiesel.value
        checksum()

    def bft_buses_eventhandler(change):
        bft_buses.observe(bft_buses_eventhandler, names='value')
        fleetmix_2020["buses"]=bft_buses.value
        checksum()

    def bft_motorcycles_eventhandler(change):
        bft_motorcycles.observe(bft_motorcycles_eventhandler, names='value')
        fleetmix_2020["motorcycle"]=bft_motorcycles.value
        checksum()

    #sumtotal.observe(sumtotal_eventhandler, names='value')
    bft_electric.observe(bft_electric_eventhandler, names='value')
    bft_petrol_cars.observe(bft_petrol_cars_eventhandler, names='value')
    bft_diesel_cars.observe(bft_diesel_cars_eventhandler, names='value')
    bft_petrol_lgv.observe(bft_petrol_lgv_eventhandler, names='value')
    bft_diesel_lgv.observe(bft_diesel_lgv_eventhandler, names='value')
    bft_rigid_truck.observe(bft_rigid_truck_eventhandler, names='value')
    bft_artic_truck.observe(bft_artic_truck_eventhandler, names='value')
    bft_biodiesel.observe(bft_biodiesel_eventhandler, names='value')
    bft_buses.observe(bft_buses_eventhandler, names='value')
    bft_motorcycles.observe(bft_motorcycles_eventhandler, names='value')

    h1 = widgets.HBox(children=[bft_electric, bft_petrol_cars, bft_diesel_cars])
    h2 = widgets.HBox(children=[bft_petrol_lgv, bft_diesel_lgv, bft_rigid_truck])
    h3 = widgets.HBox(children=[bft_artic_truck, bft_biodiesel, bft_buses])
    h4 = widgets.HBox(children=[bft_motorcycles,sumtotal])

    widgets.VBox(children=[h1,h2,h3,h4])
