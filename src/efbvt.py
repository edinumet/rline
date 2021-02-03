import pandas as pd
import math

def sre(v, alpha, beta, gamma, delta, epsilon, zita, hta):
        """COPERT 5 polynomial to return the emission factor (g/km)
            influenced by the traffic speed """
        return (alpha * math.pow(v,2) + beta * v + gamma + delta/v) / (epsilon * math.pow(v,2) + zita * v + hta)

def efbvt(fleetmix_2020, trafficstats, TomTom_congestion):
    """ Need to extract the emission factor information for the correct % of the 
     vehicle fleet.
     This information comes from rtp_fleet_projection_NAEI_2017_Base2019r_v1_1.xlsx
     available from: https://naei.beis.gov.uk/data/ef-transport
     For the moment, just select 2020 data for testing purposes
     Eventually, it'd be nice to read the Excel sheets directly so when they are 
     up-dated, this projection can easily be modified.
    """
    vs = trafficstats["vs"]
    hour = trafficstats["hour"]
    AADT = trafficstats["AADT"]
    print(AADT, vs, hour)
    # Passenger Cars #################################################
    # Within that overall breakdown, we need to know what % of each category 
    # uses diesel and in what Euro category they are
    # Full Hybrid and Plug-in Hybrid are essentially 0 at the mo.
    # Assume that Euro 6_1 = Euro 6 a/b/c
    #             Euro 6_2 = Euro 6 d-temp
    #             Euro 6_3 = Euro 6 d
    # so we can align fleet % with emissions factors

    frac_petrol_car = {"Euro 3": 0.03, "Euro 4": 0.10, "Euro 5": 0.23,
             "Euro 6 a/b/c": 0.14, "Euro 6 d-temp": 0.32, "Euro 6 d": 0.11}
    frac_diesel_car =  {"Euro 3": 0.02, "Euro 4": 0.11, "Euro 5": 0.33,
             "Euro 6 a/b/c": 0.19, "Euro 6 d-temp": 0.27, "Euro 6 d": 0.08}        
    
    # We will use selection boxes and sliders to control the simulation eventually
    # to allow students to change the fleet mix and traffic speed
    
    # Loop through the vehicle fleet mix by fuel type and EuroStandard.
    
    # Start by finding the emissions from petrol driven passenger cars
    # Read in the traffic emission factors
    efis_df = pd.read_excel("Passenger Cars.xlsx")   

    weighted_PM_emission_petrol_cars = 0.0    # keep a running total
    weighted_PM_emission_diesel_cars = 0.0
    weighted_NOx_emission_petrol_cars = 0.0
    weighted_NOx_emission_diesel_cars = 0.0

    segment_list = ['Mini','Small','Medium','Large-SUV-Executive']
    fuel_list = ['Petrol', 'Diesel', 'Petrol Hybrid']
    euro_list = ['Euro 3', 'Euro 4', 'Euro 5', 'Euro 6 a/b/c', 'Euro 6 d-temp','Euro 6 d']
    poll_list = ["PM Exhaust", "NOx"]
    tech_list = ["PFI", "GDI", "DPF"]
    
    for vehicle_type in segment_list:
        for fuel_type in fuel_list:
            for euro_type in euro_list:
                for tech_type in tech_list:
                    for poll_type in poll_list:
                        dfen = efis_df.loc[efis_df['Fuel'].eq(fuel_type) &
                            efis_df['Segment'].eq(vehicle_type) &
                            efis_df['Euro Standard'].eq(euro_type) &
                            efis_df['Technology'].eq(tech_type) &
                            efis_df['Mode'].isnull() &
                            efis_df['Pollutant'].eq(poll_type)]
                        if not dfen.empty:
                        # This will return a dataframe of 1 entry with the speed-related parameters 
                        # for this class of vehicle
                        # Now modify it by passing in vehicle speed
                            emis = sre(vs, dfen['Alpha'],
                                        dfen['Beta'], dfen['Gamma'], dfen['Delta'],
                                        dfen['Epsilon'], dfen['Zita'], dfen['Hta'])
                        # Now weight the emissions by % Euro Standard in the whole fleet
                        # Will also need to weight by ratio GDI:PFI for petrol vehicles - luckily 50:50 split
                            if poll_type=="PM Exhaust" and fuel_type=="Petrol":
                                weighted_PM_emission_petrol_cars = weighted_PM_emission_petrol_cars \
                                 + emis.values * frac_petrol_car[euro_type]
                            if poll_type=="PM Exhaust" and fuel_type=="Diesel":
                                weighted_PM_emission_diesel_cars = weighted_PM_emission_diesel_cars \
                                + emis.values * frac_diesel_car[euro_type]
                            if poll_type=="NOx" and fuel_type=="Petrol":
                                weighted_NOx_emission_petrol_cars = weighted_NOx_emission_petrol_cars \
                                + emis.values * frac_petrol_car[euro_type]
                            if poll_type=="NOx" and fuel_type=="Diesel":
                                weighted_NOx_emission_diesel_cars = weighted_NOx_emission_diesel_cars \
                                 + emis.values * frac_diesel_car[euro_type]
    
    #  Light Commercial Vehicles ############################################

    # Start by finding the emissions from petrol driven LGVs
    # Read in the traffic emission factors
    efis_df = pd.read_excel("Light Commercial Vehicles.xlsx")   

    weighted_PM_emission_petrol_lgv = 0.0    # keep a running total
    weighted_PM_emission_diesel_lgv = 0.0
    weighted_NOx_emission_petrol_lgv = 0.0
    weighted_NOx_emission_diesel_lgv = 0.0
    frac_petrol_lgv =  {"Euro 3": 0.04, "Euro 4": 0.12, "Euro 5": 0.27,
             "Euro 6 a/b/c": 0.20, "Euro 6 d-temp": 0.35, "Euro 6 d": 0.01}
    frac_diesel_lgv =  {"Euro 3": 0.02, "Euro 4": 0.10, "Euro 5": 0.26,
             "Euro 6 a/b/c": 0.17, "Euro 6 d-temp": 0.44, "Euro 6 d": 0.01}
    segment_list = ["N1-1", "N1-II", "N1-III"]
    euro_list = ["Euro 3", "Euro 4", "Euro 5", "Euro 6 a/b/c", "Euro 6 d-temp", "Euro 6 d"]
    fuel_list = ["Petrol", "Diesel"]
    poll_list = ["PM Exhaust", "NOx"]
    tech_list = ["PFI", "GDI", "DPF", "GDI+GPF"]
    
    for vehicle_type in segment_list:
        for fuel_type in fuel_list:
            for euro_type in euro_list:
                for tech_type in tech_list:
                    for poll_type in poll_list:
                        dfen = efis_df.loc[efis_df['Fuel'].eq(fuel_type) &
                            efis_df['Segment'].eq(vehicle_type) &
                            efis_df['Euro Standard'].eq(euro_type) &
                            efis_df['Technology'].eq(tech_type) &
                            efis_df['Mode'].isnull() &
                            efis_df['Pollutant'].eq(poll_type)]
                        if not dfen.empty:
                        # This will return a dataframe of 1 entry with the speed-related parameters 
                        # for this class of vehicle
                        # Now modify it by passing in vehicle speed
                            emis = sre(vs, dfen['Alpha'],
                                        dfen['Beta'], dfen['Gamma'], dfen['Delta'],
                                        dfen['Epsilon'], dfen['Zita'], dfen['Hta'])
                        # Now weight the emissions by % Euro Standard in the whole fleet
                        # Will also need to weight by ratio GDI:PFI for petrol vehicles - luckily 50:50 split
                            if poll_type=="PM Exhaust" and fuel_type=="Petrol":
                                weighted_PM_emission_petrol_lgv = weighted_PM_emission_petrol_lgv \
                                 + emis.values * frac_petrol_lgv[euro_type]
                            if poll_type=="PM Exhaust" and fuel_type=="Diesel":
                                weighted_PM_emission_diesel_lgv = weighted_PM_emission_diesel_lgv \
                                  + emis.values * frac_diesel_lgv[euro_type]
                            if poll_type=="NOx" and fuel_type=="Petrol":
                                weighted_NOx_emission_petrol_lgv = weighted_NOx_emission_petrol_lgv \
                                  + emis.values * frac_petrol_lgv[euro_type]
                            if poll_type=="NOx" and fuel_type=="Diesel":
                                weighted_NOx_emission_diesel_lgv = weighted_NOx_emission_diesel_lgv \
                                  + emis.values * frac_diesel_lgv[euro_type]


    # Rigid Trucks ###########################################################

    # Start by finding the emissions from rigid trucks
    # Read in the traffic emission factors
    efis_df = pd.read_excel("Heavy Trucks.xlsx")   
    frac_hgv =  {"Euro III": 0.03, "Euro IV": 0.03, "Euro V": 0.15,
             "Euro VI A/B/C": 0.39, "Euro VI D/E": 0.39}
    # ToDo 9999 Need to allow for weights
    frac_hgv_by_weight =  {"3,5 - 7,5 t": 0.247, "7,5 - 12 t": 0.055, "12 - 14 t": 0.022,
             "14 - 20 t": 0.116, "20 - 26 t": 0.167, "26 - 28 t": 0.112,
             "28 - 32 t": 0.225, ">32 t": 0.056}  
    # keep a running total
    weighted_PM_emission_rigid_diesel_trucks = 0.0
    weighted_NOx_emission_rigid_diesel_trucks = 0.0
    segment_list = [">3,5 t", "Rigid <=7,5 t","Rigid 7,5 - 12 t", "Rigid 12 -14 t", 
           "Rigid 14 - 20 t", "Rigid 20 - 26 t", "Rigid 26 - 28 t", "Rigid 28 - 32 t",
           "Rigid >32 t"]
    euro_list = ["Conventional","Euro III", "Euro IV", "Euro V", "Euro VI A/B/C", "Euro VI D/E"]
    tech_list = ["EGR", "SCR", "DPF+SCR"]
    poll_list = ["PM Exhaust", "NOx"]
    fuel_list = ["Diesel"]
    
    for vehicle_type in segment_list:
        for fuel_type in fuel_list:
            for euro_type in euro_list:
                for tech_type in tech_list:
                    for poll_type in poll_list:
                        dfen = efis_df.loc[efis_df['Fuel'].eq(fuel_type) &
                            efis_df['Segment'].eq(vehicle_type) &
                            efis_df['Euro Standard'].eq(euro_type) &
                            efis_df['Technology'].eq(tech_type) &
                            efis_df['Mode'].isnull() &
                            efis_df['Pollutant'].eq(poll_type)]
                        if not dfen.empty:
                        # This will return a dataframe of 1 entry with the speed-related parameters 
                        # for this class of vehicle
                        # Now modify it by passing in vehicle speed
                            emis = sre(vs, dfen['Alpha'],
                                        dfen['Beta'], dfen['Gamma'], dfen['Delta'],
                                        dfen['Epsilon'], dfen['Zita'], dfen['Hta'])
                        # Now weight the emissions by % Euro Standard in the whole fleet
                        # ToDo 9999  Sort out weighting by fleet type, weight etc.
                            if poll_type=="PM Exhaust" and fuel_type=="Diesel":
                                weighted_PM_emission_rigid_diesel_trucks = weighted_PM_emission_rigid_diesel_trucks \
                                + emis.values * frac_hgv[euro_type]
                            if poll_type=="NOx" and fuel_type=="Diesel":
                                weighted_NOx_emission_rigid_diesel_trucks = weighted_NOx_emission_rigid_diesel_trucks \
                                + emis.values * frac_hgv[euro_type]
    
    
    # Articulated Trucks ###########################################################

    # Start by finding the emissions from articulated trucks
    # Read in the traffic emission factors
    efis_df = pd.read_excel("Heavy Trucks.xlsx")   
    frac_artic =  {"Euro III": 0.0, "Euro IV": 0.01, "Euro V": 0.09,
             "Euro VI A/B/C": 0.45, "Euro VI D/E": 0.45}
    frac_artic_by_weight =  {"14 - 20 t": 0.018, "20 - 28 t": 0.024, "28 - 34 t": 0.018,
             "34 - 40 t": 0.115, ">32 t": 0.824}
    # keep a running total
    weighted_PM_emission_artic_diesel_trucks = 0.0
    weighted_NOx_emission_artic_diesel_trucks = 0.0
    segment_list = ["Articulated 14 - 20 t", "Articulated 20 - 28 t",
           "Articulated 28 - 34 t", "Articulated 34 - 40 t", "Articulated 40 - 50 t",
           "Articulated 50 - 60 t"]
    euro_list = ["Conventional","Euro III", "Euro IV", "Euro V", "Euro VI A/B/C", "Euro VI D/E"]
    tech_list = ["EGR", "SCR", "DPF+SCR"]
    poll_list = ["PM Exhaust", "NOx"]
    fuel_list = ["Diesel"]
    
    for vehicle_type in segment_list:
        for fuel_type in fuel_list:
            for euro_type in euro_list:
                for tech_type in tech_list:
                    for poll_type in poll_list:
                        dfen = efis_df.loc[efis_df['Fuel'].eq(fuel_type) &
                            efis_df['Segment'].eq(vehicle_type) &
                            efis_df['Euro Standard'].eq(euro_type) &
                            efis_df['Technology'].eq(tech_type) &
                            efis_df['Mode'].isnull() &
                            efis_df['Pollutant'].eq(poll_type)]
                        if not dfen.empty:
                        # This will return a dataframe of 1 entry with the speed-related parameters 
                        # for this class of vehicle
                        # Now modify it by passing in vehicle speed
                            emis = sre(vs, dfen['Alpha'],
                                        dfen['Beta'], dfen['Gamma'], dfen['Delta'],
                                        dfen['Epsilon'], dfen['Zita'], dfen['Hta'])
                        # Now weight the emissions by % Euro Standard in the whole fleet
                        # ToDo 9999  Sort out weighting by fleet type, weight etc.
                            if poll_type=="PM Exhaust" and fuel_type=="Diesel":
                                weighted_PM_emission_artic_diesel_trucks = weighted_PM_emission_artic_diesel_trucks \
                                + emis.values * frac_artic[euro_type]
                            if poll_type=="NOx" and fuel_type=="Diesel":
                                weighted_NOx_emission_artic_diesel_trucks = weighted_NOx_emission_artic_diesel_trucks \
                                + emis.values * frac_hgv[euro_type]
    

    # Buses ################################################################
    # Start by finding the emissions from petrol driven passenger cars
    # Read in the traffic emission factors
    efis_df = pd.read_excel("Buses.xlsx")   
    frac_bus =  {"Euro III": 0.0, "Euro IV": 0.01, "Euro V": 0.09,
             "Euro VI A/B/C": 0.88, "Euro VI D/E": 0.02}   # 9999 Check Euro VI figs
    frac_bus_coach =  {"bus": 0.72, "coach": 0.28}
    frac_bus_size = {"Urban Buses Midi <=15 t"": 0.314, Urban Buses Standard 15 -18 t": 0.686}
    frac_coach = {"Coaches Standard <=18 t": 0.50, "Coaches Articulated >18 t": 0.50}
    # keep a running total
    weighted_PM_emission_diesel_buses = 0.0
    weighted_NOx_emission_diesel_buses = 0.0
    weighted_PM_emission_biodiesel_buses = 0.0
    weighted_NOx_emission_biodiesel_buses = 0.0
    segment_list = ["Urban Buses Midi <= 15 t", "Urban Buses Standard 15 - 18 t",
           "Urban Buses Articulated >18 t", "Coaches Standard <=18 t",
           "Coaches Articulated >18 t", "Urban Buses Diesel Hybrid",
           "Urban CNG Buses", "Urban Biodiesel Buses"]
    euro_list = ["Conventional","Euro III", "Euro IV", "Euro V", "Euro VI A/B/C", "Euro VI D/E"]
    tech_list = ["EGR", "SCR", "DPF+SCR"]
    poll_list = ["PM Exhaust", "NOx"]
    fuel_list = ["Diesel", "Diesel Hybrid ~ Diesel", "CNG", "Biodiesel"]

    for vehicle_type in segment_list:
        for fuel_type in fuel_list:
            for euro_type in euro_list:
                for tech_type in tech_list:
                    for poll_type in poll_list:
                        dfen = efis_df.loc[efis_df['Fuel'].eq(fuel_type) &
                            efis_df['Segment'].eq(vehicle_type) &
                            efis_df['Euro Standard'].eq(euro_type) &
                            efis_df['Technology'].eq(tech_type) &
                            efis_df['Mode'].isnull() &
                            efis_df['Pollutant'].eq(poll_type)]
                        if not dfen.empty:
                        # This will return a dataframe of 1 entry with the speed-related parameters 
                        # for this class of vehicle
                        # Now modify it by passing in vehicle speed
                            emis = sre(vs, dfen['Alpha'],
                                        dfen['Beta'], dfen['Gamma'], dfen['Delta'],
                                        dfen['Epsilon'], dfen['Zita'], dfen['Hta'])
                        # Now weight the emissions by % Euro Standard in the whole fleet
                        # Will also need to weight by ratio GDI:PFI for petrol vehicles - luckily 50:50 split
                            if poll_type=="PM Exhaust" and fuel_type=="Biodiesel":
                                weighted_PM_emission_biodiesel_buses = weighted_PM_emission_biodiesel_buses \
                                 + emis.values * frac_bus[euro_type]
                            if poll_type=="PM Exhaust" and fuel_type=="Diesel":
                                weighted_PM_emission_diesel_buses = weighted_PM_emission_diesel_buses \
                                 + emis.values * frac_bus[euro_type]
                            if poll_type=="NOx" and fuel_type=="Biodiesel":
                                weighted_NOx_emission_biodiesel_buses = weighted_NOx_emission_biodiesel_buses \
                                 + emis.values * frac_bus[euro_type]
                            if poll_type=="NOx" and fuel_type=="Diesel":
                                weighted_NOx_emission_diesel_buses = weighted_NOx_emission_diesel_buses \
                                 + emis.values * frac_bus[euro_type]

    
    # Need to scale by Annual Average Daily Traffic (AADT)
    # and scale for hour of day
    
    hourly_AADT = [(x * AADT) / sum(TomTom_congestion) for x in TomTom_congestion]
    # print(hourly_AADT)
#     print(sum(hourly_AADT))
#     print(hour)
    # For the chosen hour, what is the traffic count?
    traffic_count = hourly_AADT[hour]
    # print("Number of vehicles at {:.0f}".format(hour),": ","{:.0f}".format(traffic_count))
#     
#     print("Particulate matter")
#     print("weighted_PM_emission_petrol_cars = ", weighted_PM_emission_petrol_cars * traffic_count * fleetmix_2020["petrol"]/100)
#     print("weighted_PM_emission_diesel_cars = ", weighted_PM_emission_diesel_cars * traffic_count * fleetmix_2020["diesel"]/100)
#     print("weighted_PM_emission_petrol_lgv = ", weighted_PM_emission_petrol_lgv * traffic_count * fleetmix_2020["petrol_lgv"]/100)
#     print("weighted_PM_emission_diesel_lgv = ", weighted_PM_emission_diesel_lgv * traffic_count * fleetmix_2020["diesel_lgv"]/100)
#     print("weighted_PM_emission_rigid_diesel_trucks = ", weighted_PM_emission_rigid_diesel_trucks * traffic_count * fleetmix_2020["rigid"]/100)
#     print("weighted_PM_emission_artic_diesel_trucks = ", weighted_PM_emission_artic_diesel_trucks * traffic_count * fleetmix_2020["artic"]/100)
#     print("weighted_PM_emission_diesel_buses = ", weighted_PM_emission_diesel_buses * traffic_count * fleetmix_2020["buses"]/100)
#     print("weighted_PM_emission_biodiesel_buses = ", weighted_PM_emission_biodiesel_buses * traffic_count * fleetmix_2020["biodiesel"]/100)
#     print("NOx")
#     print("weighted_NOx_emission_petrol_cars = ", weighted_NOx_emission_petrol_cars * traffic_count * fleetmix_2020["petrol"]/100)
#     print("weighted_NOx_emission_diesel_cars = ", weighted_NOx_emission_diesel_cars * traffic_count * fleetmix_2020["diesel"]/100)
#     print("weighted_NOx_emission_petrol_lgv = ", weighted_NOx_emission_petrol_lgv * traffic_count * fleetmix_2020["petrol_lgv"]/100)
#     print("weighted_NOx_emission_diesel_lgv = ", weighted_NOx_emission_diesel_lgv * traffic_count * fleetmix_2020["diesel_lgv"]/100)
#     print("weighted_NOx_emission_rigid_diesel_trucks = ", weighted_NOx_emission_rigid_diesel_trucks * traffic_count * fleetmix_2020["rigid"]/100)
#     print("weighted_NOx_emission_artic_diesel_trucks = ", weighted_NOx_emission_artic_diesel_trucks * traffic_count * fleetmix_2020["artic"]/100)
#     print("weighted_NOx_emission_diesel_buses = ", weighted_NOx_emission_diesel_buses * traffic_count * fleetmix_2020["buses"]/100)
#     print("weighted_NOx_emission_biodiesel_buses = ", weighted_NOx_emission_biodiesel_buses * traffic_count * fleetmix_2020["biodiesel"]/100)
#         
    
    
    
    hourly_weighted_PM_emission = weighted_PM_emission_petrol_cars * traffic_count * fleetmix_2020["petrol"]/100 + \
                               weighted_PM_emission_diesel_cars * traffic_count * fleetmix_2020["diesel"]/100 + \
                               weighted_PM_emission_petrol_lgv * traffic_count * fleetmix_2020["petrol_lgv"]/100 + \
                               weighted_PM_emission_diesel_lgv * traffic_count * fleetmix_2020["diesel_lgv"]/100 + \
                               weighted_PM_emission_rigid_diesel_trucks * traffic_count * fleetmix_2020["rigid"]/100 + \
                               weighted_PM_emission_artic_diesel_trucks * traffic_count * fleetmix_2020["artic"]/100 + \
                               weighted_PM_emission_biodiesel_buses * traffic_count * fleetmix_2020["biodiesel"]/100 + \
                               weighted_PM_emission_diesel_buses * traffic_count * fleetmix_2020["buses"]
    
    hourly_weighted_NOx_emission = weighted_NOx_emission_petrol_cars * traffic_count * fleetmix_2020["petrol"]/100 + \
                               weighted_NOx_emission_diesel_cars * traffic_count * fleetmix_2020["diesel"]/100 + \
                               weighted_NOx_emission_petrol_lgv * traffic_count * fleetmix_2020["petrol_lgv"]/100 + \
                               weighted_NOx_emission_diesel_lgv * traffic_count * fleetmix_2020["diesel_lgv"]/100 + \
                               weighted_NOx_emission_rigid_diesel_trucks * traffic_count * fleetmix_2020["rigid"]/100 + \
                               weighted_NOx_emission_artic_diesel_trucks * traffic_count * fleetmix_2020["artic"]/100 + \
                               weighted_NOx_emission_biodiesel_buses * traffic_count * fleetmix_2020["biodiesel"]/100 + \
                               weighted_NOx_emission_diesel_buses * traffic_count * fleetmix_2020["buses"]/100                           
    
    print("PM Emission (g/m/s) = ", hourly_weighted_PM_emission/3600000)
    print("NOx Emission (g/m/s) = ", hourly_weighted_NOx_emission/3600000)
    # returns in g/m/s ready for RLine
    return(hourly_weighted_PM_emission/3600000, hourly_weighted_NOx_emission/3600000, traffic_count)
    
    
