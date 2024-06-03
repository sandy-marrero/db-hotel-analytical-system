from pydantic import BaseModel

class MostChainReservationsModel(BaseModel):
    """Data class used to represent the results of Global statistics D.


    :param chain_name: Name of the chain.
    :type chain_name: ``str``
    :param reservation_month: Month with the most reservations.
    :type reservation_month: ``int``
    :param reservation_count: Number of reservations in the month.
    :type reservation_count: ``int``
    """

    chain_name: str
    reservation_month: int
    reservation_count: int

class MostClientCapacityModel(BaseModel):
    """Data class used to represent the results of Global statistics E.


    :param hotel_name: Name of the hotel.
    :type hotel_name: ``str``
    :param total_capacity: Total capacity of the hotel.
    :type total_capacity: ``int``
    """

    hotel_name: str
    total_capacity: int

class MostHotelReservationsModel(BaseModel):
    """Data class used to represent the results of Global statistics F.


    :param hotel_name: Name of the hotel.
    :type hotel_name: ``str``
    :param reservation_count: Number of reservations for the hotel.
    :type reservation_count: ``int``
    """

    hotel_name: str
    reservation_count: int