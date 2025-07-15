import enum


class Status(str, enum.Enum):
    UNDER_CONSTRUCTION = "under_construction"
    BUILT = "built"
    COMMISSIONED = "commissioned"


class Type(str, enum.Enum):
    MULTI_APARTMENT = "multi_apartment"
    TOWNHOUSE = "townhouse"
    COTTAGE = "cottage"
    VILLA = "villa"


class Class(str, enum.Enum):
    ECONOMY = "economy"
    COMFORT = "comfort"
    BUSINESS = "business"
    PREMIUM = "premium"
    ELITE = "elite"


class Technology(str, enum.Enum):
    BRICK = "brick"
    PANEL = "panel"
    AERATED_CONCRETE = "aerated_concrete"
    FRAME = "frame"


class Territory(str, enum.Enum):
    CLOSED_GUARDED = "closed_guarded"
    CLOSED = "closed"
    GUARDED = "guarded"
    OPEN = "open"


class UtilityBills(str, enum.Enum):
    INDIVIDUAL_METERS = "individual_meters"
    FIXED_RATE = "fixed_rate"
    INCLUDED_IN_RENT = "included_in_rent"
    SEPARATE_RECEIPTS = "separate_receipts"
    CENTRALIZED = "centralized"


class Heating(str, enum.Enum):
    CENTRAL = "central"
    INDIVIDUAL_GAS = "individual_gas"
    INDIVIDUAL_ELECTRIC = "individual_electric"
    AUTONOMOUS = "autonomous"


class Sewerage(str, enum.Enum):
    CENTRAL = "central"
    SEPTIC_TANK = "septic_tank"
    AUTONOMOUS = "autonomous"


class WaterSupply(str, enum.Enum):
    CENTRAL = "central"
    WELL = "well"


class Formalization(str, enum.Enum):
    NOTARY = "notary"
    LEGAL_AGREEMENT = "legal_agreement"
    STATE_REGISTRATION = "state_registration"
    PRIVATE_AGREEMENT = "private_aggregation"


class BillingOptions(str, enum.Enum):
    MORTGAGE = "mortgage"
    CASH = "cash"
    INSTALLMENT = "installment"
    LEASING = "leasing"
    STATE_PROGRAM = "state_program"


class PropertyType(str, enum.Enum):
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"
    INDUSTRIAL = "industrial"
    LAND = "land"


class SumInContract(str, enum.Enum):
    FULL = "full"
    PARTIAL = "partial"
