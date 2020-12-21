from powersimdata.scenario.scenario import Scenario
import uuid

def test_scenario_1712_analysis():
    scenario = Scenario('1712')
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
    # get power flow profile for AC lines
    pf_ac = scenario.state.get_pf()
    # get locational marginal price profile for each bus
    lmp = scenario.state.get_lmp()
    # get congestion (upper power flow limit) profile for AC lines
    congu = scenario.state.get_congu()
    # get congestion (lower power flow limit) profile for AC lines
    congl = scenario.state.get_congl()
    # get time averaged congestion (lower and power flow limits) for AC lines
    avg_cong = scenario.state.get_averaged_cong()
    # get generation profile for storage units (if present in scenario)
    pg_storage = scenario.state.get_storage_pg()
    # get energy state of charge of storage units (if present in scenario)
    e_storage = scenario.state.get_storage_e()

    # missing for scenario 1712
    # # get load shed profile for each load bus
    # load_shed = scenario.state.get_load_shed()
    # # get power flow profile for DC lines
    # pf_dc = scenario.state.get_dcline_pf()

def test_scenario_1712_regression():
    # The scenario info for 1712 is:
    # --------------------
    # SCENARIO INFORMATION
    # --------------------
    # id: 1712
    # plan: test
    # name: new_bus
    # state: analyze
    # interconnect: Texas
    # base_demand: ercot
    # base_hydro: v2
    # base_solar: v4.1
    # base_wind: v5.1
    # change_table: Yes
    # start_date: 2016-01-01 00:00:00
    # end_date: 2016-01-03 23:00:00
    # interval: 24H
    # engine: REISE.jl
    # runtime: 0:01
    # infeasibilities: 

    # # The change table for scenario 1712 is:
    # ct = {'new_bus': [{'lat': 30, 'lon': -95, 'zone_id': 308, 'Pd': 0, 'baseKV': 230}],
    # 'storage': {3008161: 100},
    # 'new_plant': [{'type': 'wind','bus_id': 3008161,'Pmax': 400,'Pmin': 0}],
    # 'new_branch': [{'from_bus_id': 3008160, 'to_bus_id': 3008161,'capacity': 300}]}

    scenario = Scenario('')
    scenario.state.set_builder(["Texas"])
    scenario.state.builder.set_name("1712_regression_test" + '_' + str(uuid.uuid1()), 
        "1712_regression_test" + '_' + str(uuid.uuid1()))
    scenario.state.builder.set_time("2016-01-01 00:00:00","2016-01-03 23:00:00","24H")

    scenario.state.builder.set_base_profile("demand", "ercot")
    scenario.state.builder.set_base_profile("hydro", "v2")
    scenario.state.builder.set_base_profile("solar", "v4.1")
    scenario.state.builder.set_base_profile("wind", "v5.1")

    # scenario.state.builder.change_table.add_bus(ct['new_bus'])
    # scenario.state.builder.change_table.add_plant(ct['new_plant'])
    # scenario.state.builder.change_table.add_storage_capacity(ct['storage'])
    # scenario.state.builder.change_table.add_branch(ct['new_branch'])

    new_bus_id = scenario.state.get_grid().bus.index.max() + 1
    scenario.state.builder.change_table.add_bus(
        [{"lat": 30, "lon": -95, "zone_id": 308}]
    )
    scenario.state.builder.change_table.add_storage_capacity(
        bus_id={new_bus_id: 100}
    )
    scenario.state.builder.change_table.add_plant(
        [{"type": "wind", "bus_id": new_bus_id, "Pmax": 400}]
    )
    scenario.state.builder.change_table.add_branch(
        [{"from_bus_id": (new_bus_id - 1), "to_bus_id": new_bus_id, "capacity": 300}]
    )

    # scenario.state.builder.change_table.scale_renewable_stubs()
    
    earlier_scenario = Scenario('1712')

    # scenario.state.builder.change_table.ct = earlier_scenario.state.get_ct()

    scenario.state.print_scenario_info()
    scenario.state.create_scenario()
    scenario.state.print_scenario_status()
    scenario.print_scenario_info()
    scenario.state.prepare_simulation_input()

    # earlier_ct = earlier_scenario.state.get_ct()
    # new_ct = scenario.state.get_ct()
    # assert(earlier_ct == new_ct)

    previous_grid = earlier_scenario.state.get_grid()
    new_grid = scenario.state.get_grid()
    previous_grid == new_grid
    assert(previous_grid == new_grid)

def test_create_and_upload_Texas_scenario():
    scenario = Scenario('')

    scenario.state.set_builder(["Texas"])
    scenario.state.builder.set_name("test" + '_' + str(uuid.uuid1()), "dummy" + '_' + str(uuid.uuid1()))
    scenario.state.builder.set_time("2016-08-01 00:00:00","2016-08-31 23:00:00","24H")

    scenario.state.builder.set_base_profile("demand", "ercot")
    scenario.state.builder.set_base_profile("hydro", "v2")
    scenario.state.builder.set_base_profile("solar", "v4.1")
    scenario.state.builder.set_base_profile("wind", "v5.1")

    scenario.state.builder.change_table.scale_plant_capacity("solar", zone_name={"Far West": 5, 'West': 2.5})
    scenario.state.builder.change_table.scale_plant_capacity("wind", zone_name={"South": 1.5, "North Central": 2})
    scenario.state.builder.change_table.scale_branch_capacity(zone_name={"South": 2, "North Central": 2})

    new_bus_id = scenario.state.get_grid().bus.index.max() + 1
    scenario.state.builder.change_table.add_bus([{"lat": 30, "lon": -95, "zone_id": 308}])
    scenario.state.builder.change_table.add_storage_capacity(bus_id={new_bus_id: 100})
    scenario.state.builder.change_table.add_plant([{"type": "wind", "bus_id": new_bus_id, "Pmax": 400}])
    scenario.state.builder.change_table.add_branch([{"from_bus_id": (new_bus_id - 1),
     "to_bus_id": new_bus_id, "capacity": 300}]
    )

    ct = scenario.state.get_ct()

    scenario.state.builder.change_table.scale_renewable_stubs()
    
    scenario.state.print_scenario_info()
    scenario.state.create_scenario()
    scenario.state.print_scenario_status()
    scenario.print_scenario_info()
    scenario.state.prepare_simulation_input()
    # launch simulation
    process_run = scenario.state.launch_simulation()

    # Get simulation status
    scenario.state.print_scenario_status()