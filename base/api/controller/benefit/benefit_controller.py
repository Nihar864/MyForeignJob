from typing import Optional

from fastapi import APIRouter, Form, Request
from fastapi import Query

from base.config.logger_config import get_logger
from base.custom_enum.http_enum import SortingOrderEnum
from base.custom_enum.static_enum import StaticVariables
from base.service.benefit.benefit_service import BenefitService
from base.service.login.login_service import login_required
from base.utils.custom_exception import AppServices

logger = get_logger()

benefit_router = APIRouter(
    prefix="/benefit",
    tags=["Benefit"],
    responses={},
)


# Insert benefit
@benefit_router.post("/add")
@login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def insert_benefit_controller(
        request: Request,
        country_id: int = Form(...),
        benefit_title: str = Form(...),
        benefit_description: str = Form(...),
        # benefit_image: UploadFile = File(...),
):
    """insert benefit controller"""
    try:

        # response_payload = BenefitService.insert_benefit_service(country_id,
        #                                                          benefit_title,
        #                                                          benefit_description,
        #                                                          benefit_image,)

        response_payload = BenefitService.insert_benefit_service(country_id,
                                                                 benefit_title,
                                                                 benefit_description)

        logger.info(f"benefit inserted: {response_payload}")
        return response_payload
    except Exception as exception:
        logger.exception(f"Error inserting benefit: {str(exception)}")
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
    return BenefitService.get_all_benefit_service(
        page_number=page_number,
        page_size=page_size,
        search_value=search_value,
        sort_by=sort_by,
        sort_as=sort_as,
    )


@benefit_router.delete("/{benefit_id}")
@login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def delete_benefit_controller(request: Request, benefit_id):
    try:
        response_payload = BenefitService.delete_benefit_service(benefit_id)
        logger.info(f"Deleted benefit with ID: {response_payload}")
        return response_payload
    except Exception as exception:
        logger.exception("Error deleting benefit")
        return AppServices.handle_exception(exception, is_raise=True)


@benefit_router.get("/{benefit_id}")
@login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def get_benefit_by_id_controller(request: Request, benefit_id: int):
    try:
        logger.info(f"Fetching benefit details for ID: {benefit_id}")
        response_payload = BenefitService.get_benefit_by_id_service(benefit_id)
        logger.info(f"Fetched benefit details: {response_payload}")
        return response_payload
    except Exception as exception:
        logger.exception("Error fetching benefit details")
        return AppServices.handle_exception(exception, is_raise=True)


@benefit_router.put("/update")
@login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def update_benefit_controller(request: Request,
                              benefit_id: int = Form(...),
                              country_id: Optional[int] = Form(None),
                              benefit_title: Optional[str] = Form(None),
                              benefit_description: Optional[str] = Form(None),
                              # benefit_image: Optional[UploadFile] = File(None),
                              ):
    try:
        # response_payload = BenefitService.update_benefit_service(
        #     country_id=country_id,
        #     benefit_id=benefit_id,
        #     benefit_title=benefit_title,
        #     benefit_description=benefit_description,
        #     benefit_image=benefit_image,)
        response_payload = BenefitService.update_benefit_service(
            country_id=country_id,
            benefit_id=benefit_id,
            benefit_title=benefit_title,
            benefit_description=benefit_description)
        logger.info(f"Updated benefit with ID: {response_payload}")
        return response_payload
    except Exception as exception:
        logger.exception("Error updating benefit")
        return AppServices.handle_exception(exception)
