from powersimdata.scenario.scenario import Scenario

def test_scenario_88_analysis():
    scenario = Scenario('88')
    print(scenario.state.name)

    # print scenario information
    scenario.state.print_scenario_info()

    # get change table
    ct = scenario.state.get_ct()
    # get grid
    grid = scenario.state.get_grid()

    # get demand profile
    demand = scenario.state.get_demand()
    # get hydro profile
    hydro = scenario.state.get_hydro()
    # get solar profile
    solar = scenario.state.get_solar()
    # get wind profile
    wind = scenario.state.get_wind()

    # get generation profile for generators
    pg = scenario.state.get_pg()
    # get generation profile for storage units (if present in scenario)
    pg_storage = scenario.state.get_storage_pg()
    # get energy state of charge of storage units (if present in scenario)
    e_storage = scenario.state.get_storage_e()
    # get power flow profile for AC lines
    pf_ac = scenario.state.get_pf()
    # get power flow profile for DC lines
    pf_dc = scenario.state.get_dcline_pf()
    # get locational marginal price profile for each bus
    lmp = scenario.state.get_lmp()
    # get congestion (upper power flow limit) profile for AC lines
    congu = scenario.state.get_congu()
    # get congestion (lower power flow limit) profile for AC lines
    congl = scenario.state.get_congl()
    # get time averaged congestion (lower and power flow limits) for AC lines
    avg_cong = scenario.state.get_averaged_cong()
    # get load shed profile for each load bus
    load_shed = scenario.state.get_load_shed()

def create_and_upload_Texas_scenario():
    scenario = Scenario('')

    scenario.state.set_builder(["Texas"])
    scenario.state.builder.set_name("test", "dummy")
    scenario.state.builder.set_time("2016-08-01 00:00:00","2016-08-31 23:00:00","24H")

    scenario.state.builder.set_base_profile("demand", "ercot")
    scenario.state.builder.set_base_profile("hydro", "v2")
    scenario.state.builder.set_base_profile("solar", "v4.1")
    scenario.state.builder.set_base_profile("wind", "v5.1")

    scenario.state.builder.change_table.scale_plant_capacity("solar", zone_name={"Far West": 5, 'West': 2.5})
    scenario.state.builder.change_table.scale_plant_capacity("wind", zone_name={"South": 1.5, "North Central": 2})
    scenario.state.builder.change_table.scale_branch_capacity(zone_name={"South": 2, "North Central": 2})

    ct = scenario.state.get_ct()

    scenario.state.builder.change_table.scale_renewable_stubs()
    
    scenario.state.print_scenario_info()
    scenario.state.create_scenario()