from typing import Optional

from fastapi import APIRouter, Request, Response, UploadFile, File, Form
from fastapi import Query

from base.config.logger_config import get_logger
from base.custom_enum.http_enum import SortingOrderEnum
from base.custom_enum.static_enum import StaticVariables
from base.service.country.country_service import CountryService
from base.service.login.login_service import login_required
from base.utils.custom_exception import AppServices

logger = get_logger()

country_router = APIRouter(
    prefix="/country",
    tags=["Country"],
    responses={},
)


@country_router.post("/add")
# @login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
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
    """
    Insert a new country into the system.

    Request:
        - country_name (str): Name of the country (required)
        - country_description (str): Description of the country (required)
        - show_on_homepage_status (bool): Whether to display on homepage (required)
        - country_status (bool): Active status of the country (required)
        - country_currency (str): Currency used in the country (required)
        - country_image (UploadFile): Image file for the country (required)
        - country_flag_image (UploadFile): Flag image file for the country (required)

    Response:
        - Success: Returns the created country details with HTTP 200
        - Error: Returns appropriate error message and status code

    Purpose:
        - Allows administrators to add new countries to the system
        - Stores country information along with images

    Company:
        - Softvan Pvt Ltd
    """
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
        response.status_code=response_payload.get("status_code")
        return response_payload

    except Exception as exception:
        return AppServices.handle_exception(exception)


@country_router.get("/all")
# @login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def get_all_countries(
    request: Request,
    response: Response,
    page_number: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1),
    search_value: str = "",
    sort_by: str = "country_name",
    sort_as: SortingOrderEnum = Query(SortingOrderEnum.ASCENDING),
):
    """
    Retrieve all countries with pagination and filtering options.

    Request:
        - page_number (int): Page number for pagination (default: 1)
        - page_size (int): Number of items per page (default: 10)
        - search_value (str): Value to search in country names/descriptions
        - sort_by (str): Field to sort by (default: country_name)
        - sort_as (SortingOrderEnum): Sorting order (ASCENDING/DESCENDING)

    Response:
        - Success: Returns paginated list of countries with HTTP 200
        - Error: Returns appropriate error message and status code

    Purpose:
        - Provides a way to view all countries with sorting and filtering
        - Supports frontend data tables and grids

    Company:
        - Softvan Pvt Ltd
    """
    try:
        response_payload = CountryService.get_all_categories_service(
            page_number=page_number,
            page_size=page_size,
            search_value=search_value,
            sort_by=sort_by,
            sort_as=sort_as.value,
        )
        response.status_code=response_payload.get("status_code")
        return response_payload
    except Exception as exception:
        return AppServices.handle_exception(exception)


@country_router.delete("/country-id")
# @login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def delete_country_controller(request: Request, response: Response, country_id):
    """
    Delete a specific country by its ID.

    Request:
        - country_id (int): ID of the country to be deleted

    Response:
        - Success: Returns confirmation of deletion with HTTP 200
        - Error: Returns appropriate error message and status code

    Purpose:
        - Allows administrators to remove countries from the system
        - Typically performs soft delete to maintain referential integrity

    Company:
        - Softvan Pvt Ltd
    """
    try:
        response_payload = CountryService.delete_country_service(country_id)
        logger.info(f"Deleted country with ID: {response_payload}")
        response.status_code=response_payload.get("status_code")
        return response_payload
    except Exception as exception:
        return AppServices.handle_exception(exception)


@country_router.get("/country-id")
# @login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def get_country_by_id_controller(request: Request, response: Response, country_id: int):
    """
    Retrieve detailed information about a specific country.

    Request:
        - country_id (int): ID of the country to retrieve

    Response:
        - Success: Returns complete country details with HTTP 200
        - Error: Returns appropriate error message and status code

    Purpose:
        - Provides complete information for viewing/editing a country
        - Used when admin needs to view all details of a specific country

    Company:
        - Softvan Pvt Ltd
    """
    try:
        response_payload = CountryService.get_country_by_id_service(country_id)
        logger.info(f"Fetched country details: {response_payload}")
        response.status_code=response_payload.get("status_code")
        return response_payload
    except Exception as exception:
        return AppServices.handle_exception(exception)


@country_router.put("/update")
# @login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def update_country_controller(
    request: Request,
    response: Response,
    country_id: int = Form(...),
    country_name: Optional[str] = Form(None),
    country_description: Optional[str] = Form(None),
    show_on_homepage_status: Optional[bool] = Form(None),
    country_currency: Optional[str] = Form(None),
    country_status: Optional[bool] = Form(None),
    country_image: Optional[UploadFile] = File(None),
    country_flag_image: Optional[UploadFile] = File(None),
):
    """
    Update an existing country's information.

    Request:
        - country_id (int): ID of the country to update (required)
        - country_name (Optional[str]): New name if updating
        - country_description (Optional[str]): New description if updating
        - show_on_homepage_status (Optional[bool]): New homepage status
        - country_currency (Optional[str]): New currency if updating
        - country_status (Optional[bool]): New active status
        - country_image (Optional[UploadFile]): New image file if updating
        - country_flag_image (Optional[UploadFile]): New flag image if updating

    Response:
        - Success: Returns updated country details with HTTP 200
        - Error: Returns appropriate error message and status code

    Purpose:
        - Allows partial or complete updates to country information
        - Handles both data and image updates

    Company:
        - Softvan Pvt Ltd
    """
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
        response.status_code=response_payload.get("status_code")
        logger.info(f"Updated country with ID: {response_payload}")
        return response_payload
    except Exception as exception:
        return AppServices.handle_exception(exception)
