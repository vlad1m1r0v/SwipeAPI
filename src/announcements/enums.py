import enum


class Colour(str, enum.Enum):
    RED = "red"
    GREEN = "green"


class Phrase(str, enum.Enum):
    PURCHASE_GIFT = "purchase_gift"
    BARGAIN_IS_POSSIBLE = "bargain_is_possible"
    NEAR_THE_SEA = "near_the_sea"
    IN_RESIDENTIAL_AREA = "in_residential_area"
    LUCKY_WITH_THE_PRICE = "lucky_with_the_price"
    FOR_A_LARGE_FAMILY = "for_a_large_family"
    FAMILY_HOME = "family_home"
    PRIVATE_PARKING = "private_parking"
