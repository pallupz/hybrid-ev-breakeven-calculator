import streamlit as st
from typing import List, Dict
import math
import pandas as pd


class Settings:
    def __init__(self, currency, fuel_price, mileage_unit, simulate_fuel_increase, pc_fuel_increase, fuel_unit, annual_distance, calculate_at_year_level):
        self.currency = currency
        self.fuel_price = fuel_price
        self.simulate_fuel_increase = simulate_fuel_increase
        self.pc_fuel_increase = pc_fuel_increase/100
        self.mileage_unit = mileage_unit
        self.fuel_unit = fuel_unit
        self.annual_distance = annual_distance
        self.calculate_at_year_level = calculate_at_year_level

    # def set_values(self, currency, fuel_price, mileage_unit, simulate_fuel_increase, pc_fuel_increase):
    #     self.currency = currency
    #     self.fuel_price = fuel_price
    #     self.simulate_fuel_increase = simulate_fuel_increase
    #     self.pc_fuel_increase = pc_fuel_increase
    #     self.mileage_unit = mileage_unit
    
    def __str__(self):
        """Returns a string representation of the settings."""
        return f"""{vars(self)}"""
   
class Car:
    def __init__(self, type, price, mileage):
        self.type = type
        self.price = price
        self.mileage = mileage

def set_page_header_format():
    st.set_page_config(
    page_title="Hybrid EV Break Even Calculator",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="expanded"
    )

    st.markdown(
        """
            <style>
                .appview-container .main .block-container {{
                    padding-top: {padding_top}rem;
                    padding-bottom: {padding_bottom}rem;
                    }}

            </style>""".format(
            padding_top=0, padding_bottom=1
        ),
        unsafe_allow_html=True,
    )

    navbar = """
        <style>
            .navbar {
                background-color: #333;
                padding: 10px;
                color: white;
                text-align: center;
                top-margin: 0px;
                
            }
            .navbar a {
                color: white;
                text-decoration: none;
                padding: 10px;
            }
        </style>
        <div class="navbar">
            <a href="https://www.example.com">About</a>
            <a href="https://www.example.com">LinkedIn</a>
            <a href="https://www.example.com">Github</a>
            <a href="https://www.example.com">Buy me a coffee</a>
        </div>
    """
    
    st.markdown("<h1 style='text-align: center; '>Hybrid EV Break Even Calculator</h1>", unsafe_allow_html=True)
    st.markdown(navbar, unsafe_allow_html=True)

def collect_basic_details():
    """Creates the Setup section with currency, mileage unit, fuel price, and distance inputs."""
    # st.markdown("""<h4 style="text-align: center;">Base Info</h4>""", unsafe_allow_html=True)
    st.write("#### General Details")

    # Split setup elements into two columns
    curr, fuel_unit, fuel_price, mileage_unit = st.columns(4)
    
    with curr:
        # Currency dropdown
        currency_options = ["AUD", "INR", "USD", "EUR", "GBP", "CAD", "OTHER"]
        selected_currency = st.selectbox("Currency:", currency_options, index=0)

    with fuel_unit:
        # Average fuel price input
        fuel_unit_options = ["Liter", "Gallon"]
        selected_fuel_unit = st.selectbox("Fuel Unit:", fuel_unit_options, index=0)
        fuel_unit = "L" if selected_fuel_unit == "Liter" else "G"
        
    with fuel_price:
        # Average fuel price input
        fuel_price_label = f"Average fuel price / {fuel_unit} ({selected_currency}):"
        fuel_price = round(st.number_input(fuel_price_label, min_value=0.01, step=0.1, format="%.2f", value = 2.00), 2)
        
        # Simulate fuel price increase checkbox
        simulate_fuel_increase = None
        simulate_fuel_increase = st.checkbox("Simulate yearly fuel price increase")

        if simulate_fuel_increase: 
            fuel_increase_label = "Average annual fuel price increase (%)"
            pc_fuel_increase = round(st.number_input(fuel_increase_label, min_value=0.0, max_value=15.0, step=0.1, format="%.1f", key="fuel_increase", value=2.5 if simulate_fuel_increase else None), 2)
        else:
            pc_fuel_increase = 0
    
    with mileage_unit:
        # Average fuel price input
        mileage_unit_options = ["L/100km", "km/L", "MPG"]
        selected_mileage_unit = st.selectbox("Mileage Unit:", mileage_unit_options, index=0)

        # Simulate fuel price increase checkbox
        calculate_at_year_level = st.checkbox("Change average annual distance", value=simulate_fuel_increase, disabled=simulate_fuel_increase)
        
        if calculate_at_year_level:
            annual_distance_label = "Average annual distance driven"
            annual_distance = st.number_input(annual_distance_label, min_value=0, step=1000, key="annual_distance", value=15000 if calculate_at_year_level else None)
        else:
            annual_distance = 15000
    
    return Settings(selected_currency, fuel_price, selected_mileage_unit, simulate_fuel_increase, pc_fuel_increase, fuel_unit, annual_distance, calculate_at_year_level)
    
def collect_car_details(car_type: str, settings: Settings, defaults: Dict) -> List[Dict]:    
    st.write(f"#### {car_type} Car Details")
    price, mileage, normalized_mileage = st.columns(3)
    with price:
        price_label = f"Approx drive-away price ({settings.currency}):"
        price = st.number_input(price_label, 
                                step=1000,
                                value=defaults.get('price', None),
                                key=f"{car_type}-price")
        price = round(price, 2)
            
    with mileage:
        mileage_label = f"Mileage ({settings.mileage_unit}):"
        mileage = st.number_input(mileage_label,
                                  step=0.1, 
                                  value=defaults.get('mileage', None),
                                  key=f"{car_type}-mileage")
        mileage = round(mileage, 2)

    with normalized_mileage:
        normalized_mileage = calculate_normalized_mileage(mileage, settings.mileage_unit)
        normalized_mileage_label = f"Normalized mileage (km/L):"
        st.text_input(normalized_mileage_label, value=f"{normalized_mileage:.2f}", key=f"{car_type}-normmileage", disabled=True)

    return Car(car_type, price, normalized_mileage)

def calculate_normalized_mileage(mileage, mileage_unit):
    """Returns the appropriate distance unit based on the selected mileage unit."""
    if mileage_unit == "L/100km":
        return 100/mileage
    elif mileage_unit == 'MPG':
        km_per_gallon = mileage * 1.60934
        return km_per_gallon / 3.78541
    elif mileage_unit == 'km/L':
        return mileage
    else:
        ValueError(f'Unrecognized mileage unit: {mileage_unit}')

def calculate_distance_fuel_car_could_travel(fuel: Car, hybrid: Car, settings: Settings):
    price_difference = hybrid.price - fuel.price
    fuel_could_have_purchased = price_difference/settings.fuel_price
    distance_could_have_travelled = fuel.mileage * fuel_could_have_purchased
    
    return distance_could_have_travelled

def calculate_breakeven_distance(fuel: Car, hybrid: Car, settings: Settings):
    price_difference = hybrid.price - fuel.price
    cost_to_run_fuel_car_per_km = (1 / fuel.mileage) * settings.fuel_price
    cost_to_run_hybrid_car_per_km = (1 / hybrid.mileage) * settings.fuel_price
    breakeven_distance = price_difference / (cost_to_run_fuel_car_per_km - cost_to_run_hybrid_car_per_km)
    
    return round(breakeven_distance, 2)

def calculate_detailed_cost(fuel: Car, hybrid: Car, settings: Settings):
    rough_breakeven_distance = calculate_breakeven_distance(fuel, hybrid, settings)
    rough_num_years = math.ceil(rough_breakeven_distance / settings.annual_distance)
    
    fuel_price_df = calculate_yearly_fuel_price(settings.fuel_price, settings.pc_fuel_increase, rough_num_years)

    data = []
    for distance_period in range(1, math.ceil(rough_breakeven_distance)):
        year_period = math.ceil(distance_period / settings.annual_distance)
        data.append((distance_period, year_period))

    df = pd.DataFrame(data, columns=['km', 'year'])
    df = pd.merge(df, fuel_price_df, on='year')
    
    df['hybird_car_running_cost'] = df.km * (1 / hybrid.mileage) * df.fuel_price
    df['fuel_car_running_cost'] = df.km * (1 / fuel.mileage) * df.fuel_price
    df['cost_difference'] = df.fuel_car_running_cost - df.hybird_car_running_cost

    df = df.where(df.cost_difference > hybrid.price - fuel.price).dropna().head(1)
    return (int(df.km.iloc[0]), int(df.year.iloc[0]), df.fuel_price.iloc[0])

def calculate_yearly_fuel_price(fuel_price, pc_increase, num_years):
    data = []
    for period_number in range(1, num_years + 1):
        data.append((period_number, round(fuel_price, 2)))
        fuel_price *= (1 + pc_increase)

    return pd.DataFrame(data, columns=['year', 'fuel_price'])