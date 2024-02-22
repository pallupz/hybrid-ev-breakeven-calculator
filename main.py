import streamlit as st
from streamlit.logger import get_logger
from utils import set_page_header_format, collect_basic_details, \
                  collect_car_details, calculate_distance_fuel_car_could_travel, \
                  calculate_breakeven_distance, calculate_detailed_cost
from helpers import Distance, DistanceUnit

LOGGER = get_logger(__name__)


def run():
    set_page_header_format()
    st.write('')

    with st.container(border=True):
        settings = collect_basic_details()

    with st.container(border=True):
        hybrid_car = collect_car_details('Hybrid_Car', settings)
        fuel_car = collect_car_details('Fuel_Car', settings)
    
    with st.container(border=True):
        st.write("### Comparison Outcome")
        if hybrid_car.price <= fuel_car.price or hybrid_car.standardized_mileage.value <= fuel_car.standardized_mileage.value:
            st.write("Are you sure the numbers are correct? If yes, great news! You are already in the green!")
            return

        no_hybrid_distance, no_hybrid_fuel = calculate_distance_fuel_car_could_travel(fuel_car, hybrid_car, settings)
        breakeven_distance = calculate_breakeven_distance(fuel_car, hybrid_car, settings)
        
        cost_difference_per_km = round(fuel_car.cost_per_km - hybrid_car.cost_per_km, 2)
        cost_difference_per_distance = round(cost_difference_per_km / Distance(value=1, unit=DistanceUnit.km).get_value_in(settings.distance_unit).value, 2)

        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Fuel car is cheaper by :", 
                      value=f"{settings.currency.name} {int(hybrid_car.price - fuel_car.price):,}")
            
        with col2:
            st.metric(label=f"At {settings.currency.name} {settings.fuel_price.value} / {settings.fuel_price.per_unit.name}, enough to buy {round(no_hybrid_fuel.value)} {settings.fuel_unit.value}s of fuel for :",
                      value=f"{round(no_hybrid_distance.get_value_in(settings.distance_unit).value):,} {settings.distance_unit.value}")

        st.divider()
        
        st.write(f"If the average fuel price remains unchanged at {settings.currency.name} {settings.fuel_price.value:.2f} / {settings.fuel_price.per_unit.name} :")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label=f"Break-even at:", 
                      value=f"{round(breakeven_distance.get_value_in(settings.distance_unit).value):,} {settings.distance_unit.value}")
            
        with col2:
            st.metric(label=f"At {int(settings.annual_distance.get_value_in(settings.distance_unit).value):,} {settings.distance_unit.value} per year, break-even in:", 
                      value=f"{round(breakeven_distance.get_value_in(settings.distance_unit).value / settings.annual_distance.get_value_in(settings.distance_unit).value, 1)} years")
        
        with col3:
            st.metric(label=f"Diff of {settings.currency.name} {cost_difference_per_distance} per {settings.distance_unit.name}, saves you:", 
                      value=f"{settings.currency.name} {round(settings.annual_distance.value * cost_difference_per_distance):,} / year")

        if not settings.sim_fuel_price_hike:
            st.caption("""To simulate yearly fuel price increase, enable the "_Simulate yearly fuel price increase_" option in General Details section above.""")

        if settings.sim_fuel_price_hike:
            st.divider()
            df, inc_breakeven_distance, inc_years, inc_fuel_price = calculate_detailed_cost(fuel_car, hybrid_car, settings)
            
            st.write(f"If the average fuel price increases {settings.pct_fuel_price_hike}% per year :")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label=f"Break-even at:", 
                          value=f"{int(inc_breakeven_distance.get_value_in(settings.distance_unit).value):,} {settings.distance_unit.value}")
                
            with col2:
                st.metric(label=f"At {int(settings.annual_distance.get_value_in(settings.distance_unit).value):,} {settings.distance_unit.value} per year, break-even in:", 
                          value=f"{inc_years} years")

            with col3:
                st.metric(label=f"After {int(inc_years)} years, fuel would be:", 
                          value=f"{settings.currency.value} {inc_fuel_price.get_value_per(settings.fuel_unit).value} / {settings.fuel_unit.name}")

    st.caption("""Note: Above calculations do not take into consideration other factors such as Cost of Ownership""")
    st.write(' ')
    st.write(' ')
    


if __name__ == "__main__":
    run()
