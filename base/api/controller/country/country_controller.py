from typing import Optional

from fastapi import APIRouter, Request, Response, UploadFile, File, Form
from fastapi import Query

from base.config.logger_config import get_logger
from base.custom_enum.http_enum import SortingOrderEnum
from base.service.country.country_service import CountryService
from base.service.login.login_service import login_required
from base.utils.custom_exception import AppServices

logger = get_logger()

country_router = APIRouter(
    prefix="/country",
    tags=["Country"],
    responses={},
)


# Insert Country
@country_router.post("/add")
# @login_required()
def insert_country_controller(
    response: Response,
    request: Request,
    countryName: str = Form(...),
    countryDescription: str = Form(...),
    showOnHomepageStatus: bool = Form(...),
    countryStatus: bool = Form(...),
    countryCurrency: str = Form(...),
    countryImage: UploadFile = File(...),
    countryFlagImage: UploadFile = File(...),
):
    """insert country controller"""
    try:

        response_payload = CountryService.insert_country_service(
            countryName,
            countryDescription,
            showOnHomepageStatus,
            countryStatus,
            countryCurrency,
            countryImage,
            countryFlagImage,
        )

        logger.info(f"Country inserted: {response_payload}")
        return response_payload
    except Exception as exception:
        logger.exception(f"Error inserting country: {str(exception)}")
        return AppServices.handle_exception(exception)


@country_router.get("/all")
# @login_required()
def view_all_countries(
    request: Request,
    response: Response,
    pageNumber: int = Query(1, ge=1),
    pageSize: int = Query(10, ge=1),
    searchValue: str = "",
    sortBy: str = "countryName",
    sortAs: SortingOrderEnum = Query(SortingOrderEnum.ASCENDING),
):
    try:
        response_payload = CountryService.get_all_categories_service(
            pageNumber=pageNumber,
            pageSize=pageSize,
            searchValue=searchValue,
            sortBy=sortBy,
            sortAs=sortAs.value,
            # Use `.value` to pass the raw string ("asc"/"desc")
        )
        return response_payload
    except Exception as exception:
        logger.exception(f"Error view country: {str(exception)}")
        return AppServices.handle_exception(exception)


@country_router.delete("/{countryId}")
# @login_required()
def delete_country_controller(request: Request, response: Response, countryId):
    try:
        response_payload = CountryService.delete_country_service(countryId)
        logger.info(f"Deleted country with ID: {response_payload}")
        return response_payload
    except Exception as exception:
        logger.exception("Error deleting country")
        return AppServices.handle_exception(exception)


@country_router.get("/{countryId}")
# @login_required()
def get_country_by_id_controller(request: Request, response: Response, countryId: int):
    try:
        response_payload = CountryService.get_country_by_id_service(countryId)
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
    countryId: int = Form(...),
    countryName: Optional[str] = Form(None),
    countryDescription: Optional[str] = Form(None),
    showOnHomepageStatus: Optional[bool] = Form(None),
    countryCurrency: str = Form(None),
    countryStatus: Optional[bool] = Form(None),
    countryImage: Optional[UploadFile] = File(None),
    countryFlagImage: Optional[UploadFile] = File(None),
):
    try:
        response_payload = CountryService.update_country_service(
            countryId=countryId,
            countryName=countryName,
            countryDescription=countryDescription,
            showOnHomepageStatus=showOnHomepageStatus,
            countryCurrency=countryCurrency,
            countryStatus=countryStatus,
            countryImage=countryImage,
            countryFlagImage=countryFlagImage,
        )
        logger.info(f"Updated country with ID: {response_payload}")
        return response_payload
    except Exception as exception:
        logger.exception("Error updating country")
        return AppServices.handle_exception(exception)
