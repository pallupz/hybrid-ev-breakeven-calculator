from enum import Enum
import pydantic


class Currency(Enum):
    AUD = "AUD"
    INR = "INR"
    USD = "USD"
    GBP = "GBP"


class DistanceUnit(Enum):
    km = "km"
    mi = "mi"


class FuelUnit(Enum):
    L = "Liter"
    USGa = "US Gal"
    UKGa = "UK Gal"


class Fuel(pydantic.BaseModel):
    value: float
    unit: FuelUnit

    def get_value_in(self, target_unit: FuelUnit):
        return convert_fuel(self, target_unit)


class MileageUnit(Enum):
    KMPL = "km/L"
    L_100KM = "L/100km"
    MPG_US = "MPG (US)"
    MPG_UK = "MPG (UK)"


class Distance(pydantic.BaseModel):
    value: float
    unit: DistanceUnit

    def get_value_in(self, target_unit: DistanceUnit):
        if self.unit == target_unit:
            return Distance(value=self.value, unit=target_unit)
        elif self.unit == DistanceUnit.km and target_unit == DistanceUnit.mi:
            return Distance(value=round(self.value / 1.60934, 2), unit=target_unit)
        elif self.unit == DistanceUnit.mi and target_unit == DistanceUnit.km:
            return Distance(round(self.value * 1.60934, 2), unit=target_unit)
        else:
            raise ValueError(f"Unsupported DistanceUnit: {DistanceUnit}")


class Mileage(pydantic.BaseModel):
    value: float
    unit: MileageUnit

    def get_value_in(self, target_unit: MileageUnit):
        return convert_mileage(self, target_unit)
    

class Car(pydantic.BaseModel):
    type: str
    price: int
    mileage: Mileage
    
    @property
    def standardized_mileage(self) -> Mileage:
        return self.mileage.get_value_in(MileageUnit.KMPL)

class Settings(pydantic.BaseModel):
    currency: Currency
    fuel_price: float
    sim_fuel_price_hike: bool
    pct_fuel_price_hike: float
    mileage_unit: MileageUnit
    fuel_unit: FuelUnit
    annual_distance: Distance
    def_hybrid_car_price: float
    def_fuel_car_price: float
    car_price_step: int
    distance_unit: DistanceUnit


def convert_to_litre(fuel: Fuel) -> Fuel:
    if fuel.unit == FuelUnit.L:
        return fuel
    elif fuel.unit == FuelUnit.USGa:
        return Fuel(value=round(fuel.value * 3.785, 2), unit=FuelUnit.L)
    elif fuel.unit == FuelUnit.UKGa:
        return Fuel(value=round(fuel.value * 4.546, 2), unit=FuelUnit.L)
    else:
        raise ValueError(f"Unsupported FuelUnit: {FuelUnit}")
    

def convert_from_litre(fuel: Fuel, target_unit: FuelUnit) -> Fuel:
    if fuel.unit != FuelUnit.L:
        raise TypeError(f"Unsupported unit: {fuel.unit}. Input to this function should have type {FuelUnit.L}") 
    elif target_unit == FuelUnit.L:
        return fuel
    elif target_unit == FuelUnit.USGa:
        return Fuel(value=round(fuel.value / 3.785, 2), unit=target_unit)
    elif target_unit == FuelUnit.UKGa:
        return Fuel(value=round(fuel.value / 4.546, 2), unit=target_unit)
    else:
        raise ValueError(f"Unsupported MileageUnit: {FuelUnit}")


def convert_fuel(fuel: Fuel, target_unit: FuelUnit) -> Fuel:
    if fuel.unit == target_unit:
        return fuel
    return convert_from_litre(convert_to_litre(fuel), target_unit)


def convert_to_kmpl(mileage: Mileage) -> Mileage:
    if mileage.unit == MileageUnit.KMPL:
        return Mileage(value=mileage.value, unit=MileageUnit.KMPL)
    elif mileage.unit == MileageUnit.MPG_US:
        return Mileage(value=round(mileage.value * 0.425144, 2), unit=MileageUnit.KMPL)
    elif mileage.unit == MileageUnit.MPG_UK:
        return Mileage(value=round(mileage.value * 0.354006, 2), unit=MileageUnit.KMPL)
    elif mileage.unit == MileageUnit.L_100KM:
        if mileage.value == 0:
            raise ValueError(f"Value cannot be zero for this conversion")
        return Mileage(value=round(100 / mileage.value, 2), unit=MileageUnit.KMPL)
    else:
        raise ValueError(f"Unsupported MileageUnit: {MileageUnit}")

   
def convert_from_kmpl(mileage: Mileage, target_unit: MileageUnit) -> Mileage:
    if mileage.unit != MileageUnit.KMPL:
        raise TypeError(f"Unsupported unit: {mileage.unit}. Input to this function should have type {MileageUnit.KMPL}") 
    elif target_unit == MileageUnit.KMPL:
        return mileage
    elif target_unit == MileageUnit.MPG_US:
        return Mileage(value=round(mileage.value * 2.352145, 2), unit=target_unit)
    elif target_unit == MileageUnit.MPG_UK:
        return Mileage(value=round(mileage.value * 2.82481, 2), unit=target_unit)
    elif target_unit == MileageUnit.L_100KM:
        return Mileage(value=round(100 / mileage.value, 2), unit=target_unit)
    else:
        raise ValueError(f"Unsupported MileageUnit: {MileageUnit}")


def convert_mileage(mileage: Mileage, target_unit: MileageUnit) -> Mileage:
    if mileage.unit == target_unit:
        return mileage
    return convert_from_kmpl(convert_to_kmpl(mileage), target_unit)


def list_all(Enum):
    return [item.value for item in Enum]



