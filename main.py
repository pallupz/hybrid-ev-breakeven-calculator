import streamlit as st
from streamlit.logger import get_logger
from utils import set_page_header_format, collect_basic_details, \
                  collect_car_details, calculate_distance_fuel_car_could_travel, \
                  calculate_breakeven_distance, calculate_detailed_cost

LOGGER = get_logger(__name__)


def run():
    set_page_header_format()
    with st.container(border=True):
        settings = collect_basic_details()

    with st.container(border=True):
        hybrid = collect_car_details('Hybrid', settings, defaults={'price': 45000, 'mileage': 4.0})
        fuel = collect_car_details('Fuel', settings, defaults={'price': 40000, 'mileage': 6.0})
    
    with st.container(border=True):
        st.write("### Outcome")
        if hybrid.price <= fuel.price or hybrid.mileage <= fuel.mileage:
            st.write("Are you sure the numbers are correct? If yes, you are already in the green!")
            return

        no_hybrid_distance = calculate_distance_fuel_car_could_travel(fuel, hybrid, settings)
        breakeven_distance = calculate_breakeven_distance(fuel, hybrid, settings)
        
        if settings.simulate_fuel_increase:
            km, year, fuel_price = calculate_detailed_cost(fuel, hybrid, settings)

        st.markdown(f""" 
                    - The Hybrid car costs {settings.currency} {(hybrid.price - fuel.price):,} more than the Fuel-only car.
                    - If all of it was used to purchase fuel at the provided rate, the fuel car can drive around {round(no_hybrid_distance):,} km.
                    - If the fuel price remained unchanged at {settings.currency} {settings.fuel_price:.2f}, you'd break-even at around {round(breakeven_distance):,} km.
                        - {"Assuming" if not settings.calculate_at_year_level else "At"} driving {settings.annual_distance:,} km per year, you'd break-even in {round(breakeven_distance / settings.annual_distance, 1)} years.
                    """)
        if settings.simulate_fuel_increase:
            st.markdown(f"""
                        - If fuel price were to increase at a rate of {settings.pc_fuel_increase*100}% per year, you'd break-even at around {km:,} km 
                            - {"Assuming" if not settings.calculate_at_year_level else "At"} driving {settings.annual_distance:,} km per year, you'd break-even in {year} years when the average fuel price would be {settings.currency} {fuel_price}.
                        """)

if __name__ == "__main__":
    run()
