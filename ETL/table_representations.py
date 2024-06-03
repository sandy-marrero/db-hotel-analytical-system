"""Class representations for database tables using pydantic."""
from pydantic import BaseModel, field_validator
import re


class ReserveTableData(BaseModel):
    """Data class used to represent the records inside of the reserve table.

    This class is used to represent the records inside of the reserve table
    of the reserve.db file given to us as a project resource.

    Construct ReserveTableData.

    :param reid: Auto incremented Primary Key for reserve table
    :param ruid: Foreign key of the Room Unavailable table
    :param clid: Foreign key of the Client table
    :param total_cost: Total cost of a reservation
    :param payment: Payment method
    :param guests: Number of guests in a reservation
    """

    reid: int
    ruid: int
    clid: int
    total_cost: float
    payment: str
    guests: int

    def __str__(self) -> str:
        """Return string representation of ReserveTableData."""
        s = (f"{self.reid}-{self.ruid}-{self.clid}-{self.total_cost}-"
             f"{self.payment}-{self.guests}")
        return s


class RoomTableData(BaseModel):
    """Data class used to represent the records inside of the Room table.

    This class is used to represent the records inside of the reserve table
    of the rooms.db file given to us as a project resource.


    Construct RoomTableData.

    :param rid: Auto incremented Primary Key for Rooms table.
    :param hid: Foreign Key for Hotel Table
    :param rdid: Foreign Key for RoomDescription table
    :param rprice: Price of the room
    """

    rid: int
    hid: int
    rdid: int
    rprice: float

    def __str__(self):
        """Return string representation of RoomTableData."""
        return f"{self.rid}-{self.hid}-{self.rdid}-{self.rprice}"


class RoomDescriptionTableData(BaseModel):
    """Data class represent the records of the RoomDescription table.

    Construct RoomDescriptionData.

    :param rdid: Auto incremented Primary Key for RoomDescription table.
    :param rname: Name of the room.
    :param rtype: Type of room.
    :param capacity: Size of the room.
    :param ishandicap: Checks if room is handicap.
    """

    rdid: int
    rname: str
    rtype: str
    capacity: int
    ishandicap: bool

    def __str__(self):
        """Return string representation of RoomDescriptionTableData."""
        return (f"{self.rdid}-{self.rname}-{self.rtype}"
                f"-{self.capacity}-{self.ishandicap}")


class LoginTableData(BaseModel):
    """Data class used to represent the records inside of the login table.

    Construct LoginTableData.

    :param lid: Auto incremented Primary Key for Login table.
    :param eid: Foreign key for Employee table.
    :param username: String representing the username.
    :param password: String representing the password.
    """

    lid: int
    eid: int
    username: str
    password: str

    def __str__(self):
        """Return string representation of LoginTableData."""
        return f"{self.lid}-{self.eid}-{self.username}-{self.password}"

class LoginTableDataNoPK(BaseModel):
    """Data class used to represent the records inside of the login table.

    Construct LoginTableDataNoPK.

    :param eid: Foreign key for Employee table.
    :param username: String representing the username.
    :param password: String representing the password.
    """

    eid: int
    username: str
    password: str

    def __str__(self):
        """Return string representation of LoginTableDataNoPK."""
        return f"{self.eid}-{self.username}-{self.password}"
    
class ChainsTableData(BaseModel):
    """Data class used to represent the records inside of the chains table.

    Construct ChainsTableData.

    :param chid: Auto incremented Primary Key for Chains table.
    :param cname: String representation of chain name.
    :param springmkup: float representation of spring markup.
    :param summermkup: float representation of summer markup.
    :param fallmkup: float representation of fall markup.
    :param wintermkup: float representation of winter markup.
    """

    chid: int
    cname: str
    springmkup: float
    summermkup: float
    fallmkup: float
    wintermkup: float

    def __str__(self):
        """Return string representation of ChainTableData."""
        return (f"{self.chid}-{self.cname}-{self.springmkup}-{self.summermkup}"
                f"-{self.fallmkup}-{self.wintermkup}")

class ChainsTableDataNoPK(BaseModel):
    """Data class used to represent the records inside of the chains table.

    Construct ChainsTableDataNoPK.

    :param cname: String representation of chain name.
    :param springmkup: float representation of spring markup.
    :param summermkup: float representation of summer markup.
    :param fallmkup: float representation of fall markup.
    :param wintermkup: float representation of winter markup.
    """

    cname: str
    springmkup: float
    summermkup: float
    fallmkup: float
    wintermkup: float

    def __str__(self):
        """Return string representation of ChainTableDataNoPK."""
        return (f"{self.cname}-{self.springmkup}-{self.summermkup}"
                f"-{self.fallmkup}-{self.wintermkup}")

class EmployeeTableData(BaseModel):
    """Data class used to represent the records of the Employee table.

    Construct EmployeeData.

    :param eid: Auto incremented Primary Key for Employee table.
    :param hid: Foreign Key of the Hotel table.
    :param fname: First name of the employee.
    :param lname: Last name of the employee.
    :param position: The work position of the employee.
    :param salary: The money that the employee makes.
    """

    eid: int
    hid: int
    fname: str
    lname: str
    age: int
    position: str
    salary: float

    def __str__(self):
        """Return string representation of EmployeeTableData."""
        return (f"{self.eid}-{self.hid}-{self.fname}"
                f"-{self.lname}-{self.position}-{self.salary}")


class ClientTableData(BaseModel):
    """Class is used to represent the records inside the clients table.

    Create ClienTableData class.

    :param clid: (int): Serial primary key for Client table
    :param fname: (str): Varchar of the client's first name
    :param lname: (str): Varchar of the client's last name
    :param age: (int): Integer of the client's age
    :param memberyear: (int): Integer of Number of years client
    has been a member
    """

    clid: int
    fname: str
    lname: str
    age: int
    memberyear: int

    def __str__(self) -> str:
        """Return string representation of the ClientTableData Class."""
        s = (f"{self.clid}-{self.fname}-{self.lname}"
             f"-{self.age}-{self.memberyear}")
        return s


class HotelTableData(BaseModel):
    """Class is used to represent the records inside the Hotel table.

    Create for JotelTableData class.

    :param hid: (int): Serial Primary key for Hotel table
    :param chid: (int): Integer Foreign key from Chains Table
    :param hname: (str): String of the hotel's name
    :param hcity: (str): String of the city's name
    """

    hid: int
    chid: int
    hname: str
    hcity: str

    def __str__(self) -> str:
        """Return string representation of the HotelTableData Class."""
        s = (f"{self.hid}-{self.chid}-{self.hname}-{self.hcity}")
        return s


class RoomUnavailableTableData(BaseModel):
    """Class to represent the records inside the RoomUnavailable table.

    Create for the RoomUnavailable class.

    :param ruid: (int): Serial Primary key for RoomUnavailable table
    :param rid: (int): INteger Foreign key from Room table
    :param startdate: (date): DATE, represents start date of room reservation
    :param enddate: (date): DATE, represents end date of room reservation
    """

    ruid: int
    rid: int
    startdate: str
    enddate: str

    @field_validator("startdate", "enddate")
    @classmethod
    def validate_date(cls, value):
        """Validate that start and end date are valid."""
        if not re.match(r"\d+\/\d+\/\d+", value):
            raise ValueError(f"Invalid date string: {value}")
        month = int(value.split("/")[0])
        day = int(value.split("/")[1])
        year = int(value.split("/")[2])
        if month < 1 or month > 12:
            raise ValueError(f"Invalid month: {month}")
        elif day < 1 or day > 31:
            raise ValueError(f"Invalid day: {day}")
        elif year < 1:
            raise ValueError(f"Invalid year {year}")
        return value
    def __str__(self) -> str:
        """Return string representation of RoomUnavailableTableData Class."""
        s = (f"{self.ruid}-{self.rid}-{self.startdate}-{self.enddate}")
        return s


class RoomUnavailableTableDataNoPK(BaseModel):
    """Class to represent the records inside the RoomUnavailable table.

    Create for the RoomUnavailable class.

    :param ruid: (int): Serial Primary key for RoomUnavailable table
    :param rid: (int): INteger Foreign key from Room table
    :param startdate: (date): DATE, represents start date of room reservation
    :param enddate: (date): DATE, represents end date of room reservation
    """

    rid: int
    startdate: str
    enddate: str

    @field_validator("startdate", "enddate")
    @classmethod
    def validate_date(cls, value):
        """Validate that start and end date are valid."""
        if not re.match(r"\d+\/\d+\/\d+", value):
            raise ValueError(f"Invalid date string: {value}")
        month = int(value.split("/")[0])
        day = int(value.split("/")[1])
        year = int(value.split("/")[2])
        if month < 1 or month > 12:
            raise ValueError(f"Invalid month: {month}")
        elif day < 1 or day > 31:
            raise ValueError(f"Invalid day: {day}")
        elif year < 1:
            raise ValueError(f"Invalid year {year}")
        return value
