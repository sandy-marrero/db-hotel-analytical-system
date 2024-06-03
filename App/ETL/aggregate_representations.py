from pydantic import BaseModel


class HandicapRoomModel(BaseModel):
    """Representation of local statistics aggregate A.

    :param rid: Auto incremented Primary Key for Rooms table.
    :type rid: ``int``
    :param hid: Foreign Key for Hotel Table
    :type hid: ``int``
    :param rdid: Foreign Key for RoomDescription table
    :type rdid: ``int``
    :param rprice: Price of the room
    :type rprice: ``float``
    :param reservation_count: Number of reservations for a room
    :type reservation_count: ``int``
    """
    rid: int
    hid: int
    rdid: int
    rprice: float
    reservation_count: int


class LeastReserveModel(BaseModel):
    """Representation of local statistics aggregate A.

    :param rid: Auto incremented Primary Key for Rooms table.
    :type rid: ``int``
    :param hid: Foreign Key for Hotel Table
    :type hid: ``int``
    :param rdid: Foreign Key for RoomDescription table
    :type rdid: ``int``
    :param rprice: Price of the room
    :type rprice: ``float``
    :param days_reserved: Number of days reserved
    :type days_reserved: ``int``
    """
    rid: int
    hid: int
    rdid: int
    rprice: float
    days_reserved: int


class MostCreditCardModel(BaseModel):
    """Class is used to represent the records inside the clients table.


    :param clid: Serial primary key for Client table
    :type clid: ``int``
    :param fname: Varchar of the client's first name
    :type fname: ``str``
    :param lname: Varchar of the client's last name
    :type lname: ``str``
    :param age: Integer of the client's age
    :type age: ``int``
    :param memberyear: Integer of Number of years client
    :type memberyear: ``int``
    has been a member
    :param reservation_count: Number of reservations
    :type reservation_count: ``int``
    """

    clid: int
    fname: str
    lname: str
    age: int
    memberyear: int
    reservation_count: int


class HighestPaidModel(BaseModel):
    """Data class used to represent the records of the Employee table.


    :param eid: Auto incremented Primary Key for Employee table.
    :type eid: ``int``
    :param hid: Foreign Key of the Hotel table.
    :type hid: ``int``
    :param fname: First name of the employee.
    :type fname: ``str``
    :param lname: Last name of the employee.
    :type lname: ``str``
    :param age: Age of employee
    :type age: ``int``
    :param salary: The money that the employee makes.
    :type salary: ``float``
    """

    eid: int
    hid: int
    fname: str
    lname: str
    age: int
    salary: float

class MostRevenueModel(BaseModel):
    """Data class used to represent the results of Global statistics A.


    :param chain_name: Name of the chain.
    :type chain_name: ``str``
    :param total_revenue: Total revenue of the chain.
    :type total_revenue: ``float``
    """

    chain_name: str
    total_revenue: float

class PaymentMethodModel(BaseModel):
    """Data class used to represent the results of Global statistics A.


    :param payment_method: Name of the payment method.
    :type payment_method: ``str``
    :param count_payment: Number of payments.
    :type count_payment: ``int``
    :param payment_percentage: Percentage of payments.
    :type payment_percentage: ``float``
    """

    payment_method: str
    count_payment: int
    payment_percentage: float

class LeastRoomsModel(BaseModel):
    """Data class used to represent the results of Global statistics A.


    :param chain_name: Name of the chain.
    :type chain_name: ``str``
    :param num_rooms: Number of rooms.
    :type num_rooms: ``int``
    """

    chain_name: str
    num_rooms: int
    

class MostDiscountModel(BaseModel):
    """Data class used to represent the results of Global statistics A.

    :param clid: ID of the client
    :type client_name: ``int``
    :param client_name: Name of the client.
    :type client_name: ``str``
    :param discount: discount amount
    :type discount: ``int``
    """
    clid: int
    full_name: str
    discount: float
    # reservation_cost: float
    

class RoomTypeModel(BaseModel):
    """Data class used to represent the results of Global statistics A.

    :param room_type: Type of room.
    :type num_rooms: ``str``
    :param total_reservations: Amount of the reservations of room Type.
    :type hotel_name: ``int``
    """

    room_type: str
    total_reservations: int

class LeastGuestsModel(BaseModel):
    """Data class used to represent the results of Global statistics A.

    :param rid: id of the room.
    :type rid: ``int``
    :param capacity: capacity of the room.
    :type rid: ``int``
    """

    rid: int
    capacity: float
    

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