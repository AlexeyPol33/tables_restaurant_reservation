from fastapi import APIRouter
from app.models.schemas import TableCreate, ReservationCreate
from .views import create_table, tables_list, delete_table
from .views import create_reservations, reservations_list, delete_reservations


router = APIRouter()

router.add_api_route(
    path='/tables/', endpoint=tables_list,
    methods=['GET'], tags=['Tables'])
router.add_api_route(
    path='/tables/', endpoint=create_table,
    methods=['POST'], tags=['Tables'])
router.add_api_route(
    path='/tables/{id}', endpoint=delete_table,
    methods=['DELETE'], tags=['Tables'])


router.add_api_route(
    path='/reservations/', endpoint=reservations_list,
    methods=['GET'], tags=['Reservations'])
router.add_api_route(
    path='/reservations/', endpoint=create_reservations,
    methods=['POST'], tags=['Reservations'])
router.add_api_route(
    path='/reservations/{id}', endpoint=delete_reservations,
    methods=['DELETE'], tags=['Reservations'])