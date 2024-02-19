import streamlit as st
from streamlit.logger import get_logger
from utils import set_page_header_format, collect_basic_details, \
                  collect_car_details, calculate_distance_fuel_car_could_travel, \
                  calculate_breakeven_distance, calculate_detailed_cost

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
        st.write("### Outcome")
        if hybrid_car.price <= fuel_car.price or hybrid_car.standardized_mileage.value <= fuel_car.standardized_mileage.value:
            st.write("Are you sure the numbers are correct? If yes, you are already in the green!")
            return

        no_hybrid_distance, no_hybrid_fuel = calculate_distance_fuel_car_could_travel(fuel_car, hybrid_car, settings)
        breakeven_distance = calculate_breakeven_distance(fuel_car, hybrid_car, settings)
        
        if settings.sim_fuel_price_hike:
            inc_breakeven_distance, inc_years, inc_fuel_price = calculate_detailed_cost(fuel_car, hybrid_car, settings)

        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Price difference :", value=f"{settings.currency.name} {int(hybrid_car.price - fuel_car.price):,}")
            
        with col2:
            st.metric(label=f"Enough to buy {round(no_hybrid_fuel.value)} {settings.fuel_unit.value}s of fuel to drive :", value=f"{round(no_hybrid_distance.get_value_in(settings.distance_unit).value):,} {settings.distance_unit.value}")

        st.divider()
        
        st.write(f"If fuel price remains unchanged at {settings.currency.name} {settings.fuel_price:.2f} / {settings.fuel_unit.name} :")
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label=f"Break-even at:", value=f"{round(breakeven_distance.get_value_in(settings.distance_unit).value):,} {settings.distance_unit.value}")
            
        with col2:
            st.metric(label=f"At {int(settings.annual_distance.get_value_in(settings.distance_unit).value):,} {settings.distance_unit.value} per year, break-even in:", value=f"{round(breakeven_distance.get_value_in(settings.distance_unit).value / settings.annual_distance.get_value_in(settings.distance_unit).value, 1)} years")

        if settings.sim_fuel_price_hike:
            st.divider()
            
            st.write(f"If fuel price increases {settings.pct_fuel_price_hike}% per year :")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label=f"Break-even at:", value=f"{int(inc_breakeven_distance.get_value_in(settings.distance_unit).value):,} {settings.distance_unit.value}")
                
            with col2:
                st.metric(label=f"At {int(settings.annual_distance.get_value_in(settings.distance_unit).value):,} {settings.distance_unit.value} per year, break-even in:", value=f"{inc_years} years")

            with col3:
                st.metric(label=f"After {inc_years} years, fuel would be:", value=f"{settings.currency.value} {inc_fuel_price} / {settings.fuel_unit.name}")

    st.write(' ')
    st.write(' ') 

if __name__ == "__main__":
    run()
