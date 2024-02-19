from helpers import Settings, Currency, MileageUnit, FuelUnit, Distance, DistanceUnit

DEFAULTS = {
    'AUD' : {
        'fuel_unit': 'Liter',
        'distance_unit': 'km',
        'fuel_price': 2,
        'fuel_price_step': 0.1,
        'mileage_unit': 'L/100km',
        'hybrid_car_price': 45000,
        'fuel_car_price': 40000,
        'car_price_step': 500,
        },
    'INR' : {
        'fuel_unit': 'Liter',
        'distance_unit': 'mi',
        'fuel_price': 105,
        'fuel_price_step': 2,
        'mileage_unit': 'km/L',
        'hybrid_car_price': 1300000,
        'fuel_car_price': 1050000,
        'car_price_step': 50000,
        }
}

AUD_SETTINGS = Settings(
    currency=Currency.AUD,
    fuel_price=2.0,
    sim_fuel_price_hike=False,
    pct_fuel_price_hike=2.5,
    mileage_unit=MileageUnit.L_100KM,
    fuel_unit=FuelUnit.L,
    annual_distance=Distance(value=15_000, unit=DistanceUnit.km),
    def_hybrid_car_price=45_000,
    def_fuel_car_price=40_000,
    car_price_step=1_000,
    distance_unit=DistanceUnit.km,
)

INR_SETTINGS = Settings(
    currency=Currency.INR,
    fuel_price=101.0,
    sim_fuel_price_hike=False,
    pct_fuel_price_hike=2.5,
    mileage_unit=MileageUnit.KMPL,
    fuel_unit=FuelUnit.L,
    annual_distance=Distance(value=15_000, unit=DistanceUnit.km),
    def_hybrid_car_price=12_50_000,
    def_fuel_car_price=10_00_000,
    car_price_step=50_000,
    distance_unit=DistanceUnit.km,
)

USD_SETTINGS = Settings(
    currency=Currency.USD,
    fuel_price=3.1,
    sim_fuel_price_hike=False,
    pct_fuel_price_hike=2.5,
    mileage_unit=MileageUnit.MPG_US,
    fuel_unit=FuelUnit.USGa,
    annual_distance=Distance(value=15_000, unit=DistanceUnit.mi),
    def_hybrid_car_price=35_000,
    def_fuel_car_price=30_000,
    car_price_step=1_000,
    distance_unit=DistanceUnit.mi,
)

GBP_SETTINGS = Settings(
    currency=Currency.GBP,
    fuel_price=1.7,
    sim_fuel_price_hike=False,
    pct_fuel_price_hike=2.5,
    mileage_unit=MileageUnit.MPG_US,
    fuel_unit=FuelUnit.L,
    annual_distance=Distance(value=15_000, unit=DistanceUnit.mi),
    def_hybrid_car_price=40_000,
    def_fuel_car_price=35_000,
    car_price_step=1_000,
    distance_unit=DistanceUnit.mi,
)



# print(UK_SETTINGS.dict())

SETTINGS_MAP = {
    Currency.AUD.value: AUD_SETTINGS,
    Currency.USD.value: USD_SETTINGS,
    Currency.INR.value: INR_SETTINGS,
    Currency.GBP.value: GBP_SETTINGS,
}