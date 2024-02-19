import streamlit as st
from typing import List, Dict
import math
import pandas as pd
from defaults import DEFAULTS, SETTINGS_MAP
from helpers import list_all, Currency, Settings, FuelUnit, MileageUnit, Distance, Mileage

   
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
    st.write('')
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
                background-color: #A1683A;
                padding: 10px;
                color: white;
                text-align: center;
                top-margin: 0px;
                border-radius: 10px;
            }
            .navbar a {
                color: white;
                text-decoration: none;
                padding: 10px;
            }
        </style>
        <div class="navbar">
            <a href="https://www.example.com">LinkedIn</a>
            <a> | </a>
            <a href="https://www.example.com">Github</a>
            <a> | </a>
            <a href="https://www.example.com">Buy me a coffee</a>
        </div>
    """
    
    st.markdown("<h1  style='color: #FFFFFF; text-align: center; '>Hybrid EV Break Even Calculator</h1>", unsafe_allow_html=True)
    st.markdown(navbar, unsafe_allow_html=True)

def collect_basic_details():
    """Creates the Setup section with currency, mileage unit, fuel price, and distance inputs."""
    # st.markdown("""<h4 style="text-align: center;">Base Info</h4>""", unsafe_allow_html=True)
    st.write("#### General Details")

    # Split setup elements into two columns
    curr, fuel_unit, fuel_price, mileage_unit = st.columns(4)
    
    with curr:
        selected_currency = st.selectbox("Currency:", sorted(list_all(Currency)), index=0)
        selected_currency = Currency(value=selected_currency)
        defaults = SETTINGS_MAP.get(selected_currency.value)

    with fuel_unit:
        # Average fuel price input
        fuel_unit_options = sorted(list_all(FuelUnit))
        selected_fuel_unit = st.selectbox("Fuel Unit:", fuel_unit_options, index=fuel_unit_options.index(defaults.fuel_unit.value))
        selected_fuel_unit = FuelUnit(value=selected_fuel_unit)
        
    with fuel_price:
        # Average fuel price input
        fuel_price_label = f"Avg fuel price / {selected_fuel_unit.name} ({selected_currency.value}):"
        fuel_price = round(st.number_input(fuel_price_label, min_value=0.01, step=0.1, format="%.2f", value=float(defaults.fuel_price)), 2)
        
        # Simulate fuel price increase checkbox
        simulate_fuel_increase = defaults.sim_fuel_price_hike
        simulate_fuel_increase = st.checkbox("Simulate yearly fuel price increase")

        pc_fuel_increase = 0.0
        if simulate_fuel_increase: 
            fuel_increase_label = "Average annual fuel price increase (%)"
            pc_fuel_increase = round(st.number_input(fuel_increase_label, min_value=0.0, max_value=15.0, step=0.1, format="%.1f", key="fuel_increase", value=2.5 if simulate_fuel_increase else None), 2)
        else:
            pc_fuel_increase = 0.0
    
    with mileage_unit:
        # Average fuel price input
        mileage_unit_options = sorted(list_all(MileageUnit))
        selected_mileage_unit = st.selectbox("Mileage Unit:", mileage_unit_options, index=mileage_unit_options.index(defaults.mileage_unit.value))
        selected_mileage_unit = MileageUnit(value=selected_mileage_unit)
        
        # Simulate fuel price increase checkbox
        calculate_at_year_level = st.checkbox("Change average annual distance", value=simulate_fuel_increase, disabled=simulate_fuel_increase)
        
        annual_distance = 15000
        if calculate_at_year_level:
            annual_distance_label = f"Average annual distance driven ({defaults.distance_unit.value})"
            annual_distance = st.number_input(annual_distance_label, min_value=0, step=1000, key="annual_distance", value=int(defaults.annual_distance.get_value_in(defaults.distance_unit)))
        annual_distance = Distance(value=annual_distance, unit=defaults.distance_unit)
    
    settings = Settings(
        currency                = selected_currency,
        fuel_price              = fuel_price,
        sim_fuel_price_hike     = simulate_fuel_increase,
        pct_fuel_price_hike     = pc_fuel_increase,
        mileage_unit            = selected_mileage_unit,
        fuel_unit               = selected_fuel_unit,
        annual_distance         = annual_distance,
        def_hybrid_car_price    = defaults.def_hybrid_car_price,
        def_fuel_car_price      = defaults.def_fuel_car_price,
        car_price_step          = defaults.car_price_step,
        distance_unit           = defaults.distance_unit
    )
    return settings
    
def collect_car_details(car_type: str, settings: Settings) -> List[Dict]:    
    st.write(f"#### {car_type} Car Details")

    if car_type.lower() == 'hybrid_car':
        default_car_price= settings.def_hybrid_car_price
        default_mileage = Mileage(value=4, unit=MileageUnit.L_100KM)
    elif car_type.lower() == 'fuel_car':
        default_car_price= settings.def_fuel_car_price
        default_mileage = Mileage(value=6, unit=MileageUnit.L_100KM)

    price, mileage, normalized_mileage = st.columns(3)
    with price:
        price_label = f"Approx drive-away price ({settings.currency.value}):"
        price = st.number_input(price_label, 
                                step=float(settings.car_price_step),
                                value=float(default_car_price),
                                format="%f",
                                key=f"{car_type}-price")
        price = round(price, 2)
            
    with mileage:
        mileage_label = f"Mileage ({settings.mileage_unit.value}):"
        mileage = st.number_input(mileage_label,
                                  step=0.1, 
                                  value=float(default_mileage.get_value_in(settings.mileage_unit)),
                                  key=f"{car_type}-mileage")
        mileage = Mileage(value=mileage, unit=settings.mileage_unit)

    with normalized_mileage:
        normalized_mileage = mileage.get_value_in(MileageUnit.KMPL)
        normalized_mileage_label = f"Standardized mileage ({MileageUnit.KMPL.value}):"
        st.text_input(normalized_mileage_label, value=f"{normalized_mileage:.2f}", key=f"{car_type}-normmileage", disabled=True)

    return Car(car_type, price, normalized_mileage)


def calculate_distance_fuel_car_could_travel(fuel_car: Car, hybrid_car: Car, settings: Settings):
    price_difference = hybrid_car.price - fuel_car.price
    fuel_could_have_purchased = price_difference/settings.fuel_price
    distance_could_have_travelled = fuel_car.mileage * fuel_could_have_purchased
    
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

def mileage_converter(mileage_in_kmpl, to_unit):
    if to_unit == 'km/L':
        return mileage_in_kmpl
    elif to_unit == 'L/100km':
        return round(100/mileage_in_kmpl)
    elif to_unit == 'MPG':
        return round(mileage_in_kmpl * 2.35214583)
    else:
        ValueError(f'Unrecognized mileage unit: {to_unit}')

def distance_converter(distance, to_unit):
    if to_unit == 'km_to_mi':
        return round(distance * 0.621371, 2)
    if to_unit == 'mi_to_km':
        return round(distance * 1.60934, 2)