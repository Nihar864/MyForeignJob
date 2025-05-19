from typing import Optional

from fastapi import APIRouter, Request, Response, UploadFile, File, Form, Security
from fastapi import Query

from base.config.logger_config import get_logger
from base.custom_enum.http_enum import SortingOrderEnum
from base.custom_enum.static_enum import StaticVariables
from base.dto.country.country_dto import CountryDTO
from base.service.country.country_service import CountryService
from base.service.login.login_service import LoginService, login_required
from base.utils.custom_exception import AppServices

logger = get_logger()

country_router = APIRouter(
    prefix="/country",
    tags=["Country"],
    responses={},
)


# Insert Country


@country_router.post("/add")
@login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
async def insert_country_controller(
    response: Response,
    request: Request,
    country_name: str = Form(...),
    country_description: str = Form(...),
    show_on_homepage_status: bool = Form(...),
    country_status: bool = Form(...),
    country_currency: str = Form(...),
    country_image: UploadFile = File(...),
    country_flag_image: UploadFile = File(...),
):
    """Insert country controller (requires admin scope)"""
    try:
        response_payload = CountryService.insert_country_service(
            country_name,
            country_description,
            show_on_homepage_status,
            country_status,
            country_currency,
            country_image,
            country_flag_image,
        )
        return response_payload

    except Exception as exception:
        logger.exception(f"Error inserting country: {str(exception)}")
        return AppServices.handle_exception(exception)


@country_router.get("/all")
@login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def get_all_countries(
    request: Request,
    response: Response,
    page_number: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1),
    search_value: str = "",
    sort_by: str = "country_name",
    sort_as: SortingOrderEnum = Query(SortingOrderEnum.ASCENDING),
):
    try:

        response_payload = CountryService.get_all_categories_service(
            page_number=page_number,
            page_size=page_size,
            search_value=search_value,
            sort_by=sort_by,
            sort_as=sort_as.value,
        )
        return response_payload
    except Exception as exception:
        logger.exception(f"Error view country: {str(exception)}")
        return AppServices.handle_exception(exception)


@country_router.delete("/{country_id}")
# @login_required()
def delete_country_controller(request: Request, response: Response, country_id):
    try:
        response_payload = CountryService.delete_country_service(country_id)
        logger.info(f"Deleted country with ID: {response_payload}")
        return response_payload
    except Exception as exception:
        logger.exception("Error deleting country")
        return AppServices.handle_exception(exception)


@country_router.get("/{country_id}")
# @login_required()
def get_country_by_id_controller(request: Request, response: Response, country_id: int):
    try:
        response_payload = CountryService.get_country_by_id_service(country_id)
        logger.info(f"Fetched country details: {response_payload}")
        return response_payload
    except Exception as exception:
        logger.exception("Error fetching country details")
        return AppServices.handle_exception(exception)


@country_router.put("/update")
# @login_required()
def update_country_controller(
    request: Request,
    response: Response,
    country_id: int = Form(...),
    country_name: Optional[str] = Form(None),
    country_description: Optional[str] = Form(None),
    show_on_homepage_status: Optional[bool] = Form(None),
    country_currency: str = Form(None),
    country_status: Optional[bool] = Form(None),
    country_image: Optional[UploadFile] = File(None),
    country_flag_image: Optional[UploadFile] = File(None),
):
    try:
        response_payload = CountryService.update_country_service(
            country_id=country_id,
            country_name=country_name,
            country_description=country_description,
            show_on_homepage_status=show_on_homepage_status,
            country_status=country_status,
            country_currency=country_currency,
            country_image=country_image,
            country_flag_image=country_flag_image,
        )
        logger.info(f"Updated country with ID: {response_payload}")
        return response_payload
    except Exception as exception:
        logger.exception("Error updating country")
        return AppServices.handle_exception(exception)
