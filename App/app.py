"""Main module for term project - hotel analytics system."""
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
from controller.MostChainReservations import MostChainReservations
from controller.MostClientCapacity import MostClientCapacity
from controller.MostHotelReservations import MostHotelReservations
from controller.login import Login
from controller.chain import Chain
from controller.reserve import Reserve
from controller.room import Room
from controller.HandicapRoom import HandicapRoom
from controller.LeastReserve import LeastReserve
from controller.MostCreditCard import MostCreditCard
from controller.HighestPaid import HighestPaid
from controller.LeastRooms import LeastRooms
from controller.PaymentMethod import PaymentMethod
from controller.MostRevenue import MostRevenue
from controller.client import Client
from controller.hotel import Hotel
from controller.roomunavailable import RoomUnavailable
from controller.MostDiscount import MostDiscount
from controller.RoomType import RoomType
from controller.LeastGuests import LeastGuests
from controller.employee import Employee
from controller.roomdescription import RoomDescription

app = Flask(__name__)
app.json.ensure_ascii = False
CORS(app)




@app.route("/deceptecons/reserve", methods=['GET', 'POST'])
def reservations():
    """Return json object and status code depending on method and success.

    The route is /deceptecons/reserve.
    """
    match request.method:
        case 'GET':
            return Reserve.getAllReservations()
        case 'POST':
            return Reserve.createReservation(request.json)
    return jsonify("Invalid HTTP Verb"), 405


@app.route("/deceptecons/reserve/<int:reid>", methods=['GET', 'PUT', 'DELETE'])
def reservation(reid):
    """Return json object and status code depending on method and success.

    The route is /deceptecons/reserve/<reid>.
    """
    match request.method:
        case 'GET':
            return Reserve.getReservationById(reid)
        case 'PUT':
            return Reserve.updateReservation(reid, request.json)
        case 'DELETE':
            return Reserve.deleteReservation(reid)
    return jsonify("Invalid HTTP Verb"), 405


@app.route("/deceptecons/room", methods=['GET', 'POST'])
def rooms():
    """Return json object and status code depending on method and success.

    The route is /deceptecons/room
    """
    match request.method:
        case 'GET':
            return Room.getAllRooms()
        case 'POST':
            return Room.createRoom(request.json)
    return jsonify("Invalid HTTP Verb"), 405


@app.route("/deceptecons/room/<int:rid>", methods=['GET', 'PUT', 'DELETE'])
def room(rid):
    """Return json object and status code depending on method and success.

    The route is /deceptecons/room/<reid>
    """
    match request.method:
        case 'GET':
            return Room.getRoomById(rid)
        case 'PUT':
            return Room.updateRoom(rid, request.json)
        case 'DELETE':
            return Room.deleteRoom(rid)
    return jsonify("Invalid HTTP Verb"), 405


@app.route("/deceptecons/hotel/<int:hid>/handicaproom", methods=['POST'])
def HandicapRoomAggregate(hid: int):
    """Return json object and status code depending on method and success.

    The route is /deceptecons/hotel/<hid>/handicaproom
    """
    match request.method:
        case 'POST':
            return HandicapRoom.getAggregate(hid, request.json)
    return jsonify("Invalid HTTP Verb"), 405


@app.route("/deceptecons/hotel/<int:hid>/leastreserve", methods=['POST'])
def LeastReserveAggregate(hid: int):
    """Return json object and status code depending on method and success.

    The route is /deceptecons/hotel/<hid>/leastreserve
    """
    match request.method:
        case 'POST':
            return LeastReserve.getAggregate(hid, request.json)
    return jsonify("Invalid HTTP Verb"), 405


@app.route("/deceptecons/hotel/<int:hid>/mostcreditcard", methods=['POST'])
def MostCreditCardAggregate(hid: int):
    """Return json object and status code depending on method and success.

    The route is /deceptecons/hotel/<hid>/mostcreditcard
    """
    match request.method:
        case 'POST':
            return MostCreditCard.getAggregate(hid, request.json)
    return jsonify("Invalid HTTP Verb"), 405


@app.route("/deceptecons/hotel/<int:hid>/highestpaid", methods=['POST'])
def HighestPaidAggregate(hid: int):
    """Return json object and status code depending on method and success.

    The route is /deceptecons/hotel/<hid>/highestpaid
    """
    match request.method:
        case 'POST':
            return HighestPaid.getAggregate(hid, request.json)
    return jsonify("Invalid HTTP Verb"), 405


def create_app():
    """Use by gunnicorn to serve application.

    :rtype: Flask App
    """
    return app


@app.route("/deceptecons/login", methods=['GET', 'POST'])
def login():
    """
    Route to get all of the login records or create a new record from the JSON body provided.

    Returns:
        If the HTTP method is GET:
            A JSON response containing all logins.
        If the HTTP method is POST:
            A JSON response containing the newly created login.
        If the HTTP method is neither GET nor POST:
            A JSON response with an error message indicating an invalid HTTP verb.
    """
    match request.method:
        case 'GET':
            login_controller = Login()
            loginsAll = login_controller.getAll()
            return loginsAll
        case 'POST':
            login_controller = Login()
            login_data = request.json
            new_login = login_controller.createLogin(login_data)
            print(new_login)
            return new_login
    return jsonify("Invalid HTTP Verb"), 405


@app.route("/deceptecons/login/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def login_crud(id):
    """
    Perform CRUD operations for login based on the HTTP verb used.

    Args:
        id (int): The ID of the login.

    Returns:
        JSON: The response in JSON format.
    """
    match request.method:
        case 'GET':
            login_controller = Login()
            login = login_controller.getById(id)
            return login
        case 'PUT':
            login_controller = Login()
            login_data = request.json
            updated_login = login_controller.updateLogin(id, login_data)
            return updated_login
        case 'DELETE':
            login_controller = Login()
            deleted_login = login_controller.deleteLogin(id)
            return deleted_login
    return jsonify("Invalid HTTP Verb"), 405


@app.route("/deceptecons/chains", methods=['GET', 'POST'])
def chains():
    """
    Handles GET and POST requests related to chains.

    GET: Retrieves all chains from the database and returns them as JSON.
    POST: Creates a new chain based on the provided JSON data and returns the newly created chid as JSON.

    Returns:
        JSON: The response in JSON format.

    """
    match request.method:
        case 'GET':
            chains_controller = Chain()
            chains = chains_controller.getAll()
            return chains
        case 'POST':
            chains_controller = Chain()
            chain_data = request.json
            new_chain = chains_controller.createChain(chain_data)
            return new_chain
    return jsonify("Invalid HTTP Verb"), 405


@app.route("/deceptecons/chains/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def chains_crud(id):
    """
    Perform CRUD operations on chains.

    Args:
        id (int): The ID of the chain.

    Returns:
        Flask.Response: The response containing the result of the operation.
    """
    match request.method:
        case 'GET':
            chains_controller = Chain()
            chain = chains_controller.getById(id)
            return chain
        case 'PUT':
            chains_controller = Chain()
            chain_data = request.json
            updated_chain = chains_controller.updateChain(id, chain_data)
            return updated_chain
        case 'DELETE':
            chains_controller = Chain()
            deleted_chain = chains_controller.deleteChain(id)
            return deleted_chain
    return jsonify("Invalid HTTP Verb"), 405


@app.route("/deceptecons/most/revenue", methods=['POST'])
def most_revenue():
    """
    Retrieves the top three chains with the most revenue.

    Returns:
        JSON: A JSON object containing the top three chains with the most revenue. The object contains the following keys:
            - chain_name : str Chain name.
            - total_revenue : double Revenue.

    """
    match request.method:
        case 'POST':
            most_revenue_controller = MostRevenue()
            most_revenue = most_revenue_controller.getAggregate(request.json)
            return most_revenue
    return jsonify("Invalid HTTP Verb"), 405


@app.route("/deceptecons/paymentmethod", methods=['POST'])
def payment_method():
    """
    Retrieves the payment method statistics.

    Returns:
        JSON: A JSON object containing the payment method statistics. The object contains the following keys: 
            - Amount of times the payment method has been used.
            - Payment method name.
            - Percentage of the payment method used. 
    """
    match request.method:
        case 'POST':
            payment_method_controller = PaymentMethod()
            payment_method = payment_method_controller.getPaymentMethod(
                request.json)
            return payment_method
    return jsonify("Invalid HTTP Verb"), 405


@app.route("/deceptecons/least/rooms", methods=['POST'])
def least_rooms():
    """
    Retrieves the companies with the least number of rooms.

    Returns:
        JSON: A JSON object containing the companies with the least number of rooms.
    """
    match request.method:
        case 'POST':
            least_rooms_controller = LeastRooms()
            least_rooms = least_rooms_controller.getLeastRooms(request.json)
            return least_rooms
    return jsonify("Invalid HTTP Verb"), 405


@app.route("/deceptecons/most/capacity", methods=['POST'])
def most_capacity():
    """
    Retrieves the top five hotels with the most client capacity.

    Returns:
        JSON: A JSON object containing the top five hotels with the most capacity. The object contains the following keys:
            - hotel_name : str Hotel name.
            - total_capacity : int Capacity.

    """
    match request.method:
        case 'POST':
            most_capacity_controller = MostClientCapacity()
            most_capacity = most_capacity_controller.getMostClientCapacity(
                request.json)
            return most_capacity
    return jsonify("Invalid HTTP Verb"), 405


@app.route("/deceptecons/most/reservation", methods=['POST'])
def most_reservation():
    """
    Retrieves the top ten perfect of hotels that had the most reservations.

    Returns:
        JSON: A JSON object containing the top ten perfect of hotels that had the most reservations. The object contains the following keys:
            - hotel_name : str Hotel name.
            - reservation_count : int Reservations.

    """
    match request.method:
        case 'POST':
            most_reservations_controller = MostHotelReservations()
            most_reservations = most_reservations_controller.getMostHotelReservations(
                request.json)
            return most_reservations
    return jsonify("Invalid HTTP Verb"), 405


@app.route("/deceptecons/most/profitmonth", methods=['POST'])
def most_profitmonth():
    """
    Retrieves the top three months with the most reservation by chain.

    Returns:
        JSON: A JSON object containing the top three months with the most reservation by chain. The object contains the following keys:
            - chain_name : str Chain name.
            - reservation_month : int Month.
            - reservation_count : int Reservations.

    """
    match request.method:
        case 'POST':
            most_profitmonth_controller = MostChainReservations()
            most_profitmonth = most_profitmonth_controller.getMostChainReservations(
                request.json)
            return most_profitmonth
    return jsonify("Invalid HTTP Verb"), 405


@app.route("/deceptecons/client", methods=['GET', 'POST'])
def client():
    controller = Client()
    match request.method:
        case 'GET':
            return controller.getAll()
        case 'POST':
            return controller.createClient(request.json)
    return jsonify("Invalid HTTP Verb"), 405


@app.route("/deceptecons/client/<int:clid>", methods=['GET', 'PUT', 'DELETE'])
def client_crud(clid):
    controller = Client()
    match request.method:
        case 'GET':
            return controller.getById(clid)
        case 'PUT':
            return controller.updateClient(clid, request.json)
        case 'DELETE':
            return controller.deleteClient(clid)
    return jsonify("Invalid HTTP Verb"), 405


@app.route("/deceptecons/hotel", methods=['GET', 'POST'])
def hotel():
    controller = Hotel()
    match request.method:
        case 'GET':
            return controller.getAll()
        case 'POST':
            return controller.createHotel(request.json)
    return jsonify("Invalid HTTP Verb"), 405


@app.route("/deceptecons/hotel/<int:hid>", methods=['GET', 'PUT', 'DELETE'])
def hotel_crud(hid):
    controller = Hotel()
    match request.method:
        case 'GET':
            return controller.getById(hid)
        case 'PUT':
            return controller.updateHotel(hid, request.json)
        case 'DELETE':
            return controller.deleteHotel(hid)
    return jsonify("Invalid HTTP Verb"), 405


@app.route("/deceptecons/roomunavailable", methods=['GET', 'POST'])
def roomunavailable():
    controller = RoomUnavailable()
    match request.method:
        case 'GET':
            return controller.getAll()
        case 'POST':
            return controller.createRoomUnavailable(request.json)
    return jsonify("Invalid HTTP Verb"), 405


@app.route("/deceptecons/roomunavailable/<int:ruid>",
           methods=['GET', 'PUT', 'DELETE'])
def roomunavailable_crud(ruid):
    controller = RoomUnavailable()
    match request.method:
        case 'GET':
            return controller.getById(ruid)
        case 'PUT':
            return controller.updateRoomUnavailable(ruid, request.json)
        case 'DELETE':
            return controller.deleteRoomUnavailable(ruid)
    return jsonify("Invalid HTTP Verb"), 405


@app.route("/deceptecons/hotel/<int:hid>/mostdiscount", methods=['POST'])
def MostDiscountAggregate(hid: int):
    match request.method:
        case 'POST':
            return MostDiscount.getMostDiscount(hid, request.json)
    return jsonify("Invalid HTTP Verb"), 405


@app.route("/deceptecons/hotel/<int:hid>/roomtype", methods=['POST'])
def RoomTypeAggregate(hid: int):
    match request.method:
        case 'POST':
            return RoomType.getRoomType(hid, request.json)
    return jsonify("Invalid HTTP Verb"), 405


@app.route("/deceptecons/hotel/<int:hid>/leastguests", methods=['POST'])
def LeastguestsAggregate(hid: int):
    match request.method:
        case 'POST':
            return LeastGuests.getLeastGuests(hid, request.json)
    return jsonify("Invalid HTTP Verb"), 405


@app.route("/deceptecons/employee", methods=['GET', 'POST'])
def employee():
    controller = Employee()
    match request.method:
        case 'GET':
            return controller.getAll()
        case 'POST':
            return controller.createEmployee(request.json)
    return jsonify("Invalid HTTP Verb"), 405


@app.route("/deceptecons/employee/<int:eid>", methods=['GET', 'PUT', 'DELETE'])
def employee_crud(eid):
    controller = Employee()
    match request.method:
        case 'GET':
            return controller.getById(eid)
        case 'PUT':
            return controller.updateEmployee(eid, request.json)
        case 'DELETE':
            return controller.deleteEmployee(eid)
    return jsonify("Invalid HTTP Verb"), 405


@app.route("/deceptecons/roomdescription", methods=['GET', 'POST'])
def roomDescription():
    controller = RoomDescription()
    match request.method:
        case 'GET':
            return controller.getAll()
        case 'POST':
            return controller.createRoomDescription(request.json)
    return jsonify("Invalid HTTP Verb"), 405


@app.route("/deceptecons/roomdescription/<int:rdid>",
           methods=['GET', 'PUT', 'DELETE'])
def roomDescription_crud(rdid):
    controller = RoomDescription()
    match request.method:
        case 'GET':
            return controller.getById(rdid)
        case 'PUT':
            return controller.updateRoomDescription(rdid, request.json)
        case 'DELETE':
            return controller.delete_roomDescription(rdid)
    return jsonify("Invalid HTTP Verb"), 405


if not ("gunicorn" in sys.modules):
    app.run(debug=True)
