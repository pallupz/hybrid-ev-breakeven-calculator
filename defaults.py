from helpers import Settings, Currency, MileageUnit, FuelUnit, Distance, DistanceUnit, FuelPrice

AUD_SETTINGS = Settings(
    currency=Currency.AUD,
    fuel_price=FuelPrice(value=2.0, per_unit=FuelUnit.L),
    fuel_unit=FuelUnit.L,
    sim_fuel_price_hike=True,
    pct_fuel_price_hike=2.5,
    mileage_unit=MileageUnit.L_100KM,
    annual_distance=Distance(value=15_000, unit=DistanceUnit.km),
    def_hybrid_car_price=45_000,
    def_fuel_car_price=40_000,
    car_price_step=1_000,
    distance_unit=DistanceUnit.km,
)

INR_SETTINGS = Settings(
    currency=Currency.INR,
    fuel_price=FuelPrice(value=100.0, per_unit=FuelUnit.L),
    sim_fuel_price_hike=True,
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
    fuel_price=FuelPrice(value=4.4, per_unit=FuelUnit.USGa),
    fuel_unit=FuelUnit.USGa,
    sim_fuel_price_hike=True,
    pct_fuel_price_hike=2.5,
    mileage_unit=MileageUnit.MPG_US,
    annual_distance=Distance(value=13_500, unit=DistanceUnit.mi),
    def_hybrid_car_price=30_000,
    def_fuel_car_price=25_000,
    car_price_step=1_000,
    distance_unit=DistanceUnit.mi,
)

GBP_SETTINGS = Settings(
    currency=Currency.GBP,
    fuel_price=FuelPrice(value=1.7, per_unit=FuelUnit.L),
    fuel_unit=FuelUnit.L,
    sim_fuel_price_hike=True,
    pct_fuel_price_hike=2.5,
    mileage_unit=MileageUnit.MPG_US,
    annual_distance=Distance(value=10_000, unit=DistanceUnit.mi),
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