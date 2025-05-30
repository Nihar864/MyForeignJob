from typing import Optional

from fastapi import APIRouter, Form, Query, Response, Request

from base.config.logger_config import get_logger
from base.custom_enum.http_enum import SortingOrderEnum
from base.service.benefit.benefit_service import BenefitService
from base.utils.custom_exception import AppServices

logger = get_logger()

benefit_router = APIRouter(
    prefix="/benefit",
    tags=["Benefit"],
    responses={},
)


# Insert benefit
@benefit_router.post("/add")
# @login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def insert_benefit_controller(
    response: Response,
    request: Request,
    country_id: int = Form(...),
    benefit_title: str = Form(...),
    benefit_description: str = Form(...),
    # benefit_image: UploadFile = File(...),
):
    """
    Insert a new benefit into the system.

    Request:
        - country_id (int): ID of the country associated with the benefit
        - benefit_title (str): Title of the benefit
        - benefit_description (str): Description of the benefit
        # - benefit_image (UploadFile): Image file for the benefit

    Response:
        - Success: Returns the created benefit details
        - Error: Returns appropriate error message and status code

    Purpose:
        - Allows admin to add new benefits to the system

    Company:
        - Softvan Pvt Ltd
    """
    try:
        response_payload = BenefitService.insert_benefit_service(
            country_id, benefit_title, benefit_description
        )
        response.status_code = response_payload.get("status_code")
        print(">>>>>>>>", response.status_code)
        logger.info(f"benefit inserted: {response_payload}")
        return response_payload
    except Exception as exception:
        return AppServices.handle_exception(exception)


@benefit_router.get("/all")
# @login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def view_benefit_controller(
    request: Request,
    page_number: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1),
    search_value: str = "",
    sort_by: str = "benefit_title",
    sort_as: SortingOrderEnum = Query(SortingOrderEnum.ASCENDING),
):
    """
    Retrieve all benefits with pagination and filtering options.

    Request:
        - page_number (int): Page number for pagination (default: 1)
        - page_size (int): Number of items per page (default: 10)
        - search_value (str): Value to search in benefit titles/descriptions
        - sort_by (str): Field to sort by (default: benefit_title)
        - sort_as (SortingOrderEnum): Sorting order (ASCENDING/DESCENDING)

    Response:
        - Success: Returns paginated list of benefits
        - Error: Returns appropriate error message and status code

    Purpose:
        - Provides a way to view all benefits with sorting and filtering capabilities

    Company:
        - Softvan Pvt Ltd
    """

    return BenefitService.get_all_benefit_service(
        page_number=page_number,
        page_size=page_size,
        search_value=search_value,
        sort_by=sort_by,
        sort_as=sort_as,
    )


@benefit_router.delete("/benefit-id")
# @login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def delete_benefit_controller(response: Response, request: Request, benefit_id):
    """
    Delete a specific benefit by its ID.

    Request:
        - benefit_id (int): ID of the benefit to be deleted

    Response:
        - Success: Returns confirmation of deletion
        - Error: Returns appropriate error message and status code

    Purpose:
        - Allows admin to remove benefits from the system

    Company:
        - Softvan Pvt Ltd
    """
    try:
        response_payload = BenefitService.delete_benefit_service(benefit_id)
        response.status_code = response_payload.get("status_code")
        logger.info(f"Deleted benefit with ID: {response_payload}")
        return response_payload
    except Exception as exception:
        return AppServices.handle_exception(exception, is_raise=True)


@benefit_router.get("/benefit-id")
# @login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def get_benefit_by_id_controller(response: Response, request: Request, benefit_id: int):
    """
    Retrieve a specific benefit by its ID.

    Request:
        - benefit_id (int): ID of the benefit to retrieve

    Response:
        - Success: Returns the benefit details
        - Error: Returns appropriate error message and status code

    Purpose:
        - Provides detailed information about a specific benefit

    Company:
        - Softvan Pvt Ltd
    """
    try:
        logger.info(f"Fetching benefit details for ID: {benefit_id}")
        response_payload = BenefitService.get_benefit_by_id_service(benefit_id)
        response.status_code = response_payload.get("status_code")
        logger.info(f"Fetched benefit details: {response_payload}")
        return response_payload
    except Exception as exception:
        return AppServices.handle_exception(exception, is_raise=True)


@benefit_router.put("/update")
# @login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def update_benefit_controller(
    response: Response,
    request: Request,
    benefit_id: int = Form(...),
    country_id: Optional[int] = Form(None),
    benefit_title: Optional[str] = Form(None),
    benefit_description: Optional[str] = Form(None),
    # benefit_image: Optional[UploadFile] = File(None),
):
    """
    Update an existing benefit's information.

    Request:
        - benefit_id (int): ID of the benefit to update
        - country_id (Optional[int]): New country ID if updating
        - benefit_title (Optional[str]): New title if updating
        - benefit_description (Optional[str]): New description if updating
        # - benefit_image (Optional[UploadFile]): New image if updating

    Response:
        - Success: Returns the updated benefit details
        - Error: Returns appropriate error message and status code

    Purpose:
        - Allows admin to modify existing benefit information

    Company:
        - Softvan Pvt Ltd
    """
    try:
        response_payload = BenefitService.update_benefit_service(
            country_id=country_id,
            benefit_id=benefit_id,
            benefit_title=benefit_title,
            benefit_description=benefit_description,
        )
        response.status_code = response_payload.get("status_code")
        logger.info(f"Updated benefit with ID: {response_payload}")
        return response_payload
    except Exception as exception:
        return AppServices.handle_exception(exception)
