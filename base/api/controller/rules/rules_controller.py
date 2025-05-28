from fastapi import APIRouter, Response, Query, Request

from base.config.logger_config import get_logger
from base.custom_enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
from base.custom_enum.http_enum import SortingOrderEnum
from base.custom_enum.static_enum import StaticVariables
from base.dto.rules.rules_dto import RuleDTO, UpdateRuleDTO
from base.service.login.login_service import login_required
from base.service.rules.rules_service import RuleService
from base.utils.custom_exception import AppServices

logger = get_logger()

rule_router = APIRouter(
    prefix="/rule",
    tags=["Rule"],
    responses={},
)


@rule_router.post("/add")
# @login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def insert_rule_controller(
    request: Request,
    rule_dto: RuleDTO,
    response: Response,
):
    """
    Request: Accepts RuleDTO object containing rule information.

    Response: JSON object indicating success or failure of rule insertion.

    Purpose: To insert a new rule record into the system.

    Company Name: Softvan Pvt. Ltd.
    """
    try:
        if not rule_dto:
            response.status_code = HttpStatusCodeEnum.BAD_REQUEST

            return AppServices.app_response(
                HttpStatusCodeEnum.BAD_REQUEST.value,
                ResponseMessageEnum.NOT_FOUND.value,
                success=False,
            )

        response_payload = RuleService.insert_rule_service(rule_dto)

        logger.info(f"rule inserted: {response_payload}")
        return response_payload

    except Exception as exception:
        return AppServices.handle_exception(exception, is_raise=True)


@rule_router.get("/all")
# @login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def view_rule_controller(
    request: Request,
    page_number: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1),
    search_value: str = "",
    sort_by: str = "rule_title",
    sort_as: SortingOrderEnum = Query(SortingOrderEnum.ASCENDING),
):
    """
    Request: Query parameters for page_number, page_size, search_value, sort_by, and sort_as.

    Response: Paginated list of rules based on the specified filters and sorting.

    Purpose: To retrieve all rule records with support for pagination, search, and sorting.

    Company Name: Softvan Pvt. Ltd.
    """
    return RuleService.get_all_rule_service(
        page_number=page_number,
        page_size=page_size,
        search_value=search_value,
        sort_by=sort_by,
        sort_as=sort_as,
    )


@rule_router.delete("/{rule-id}")
# @login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def delete_rule_controller(response: Response, request: Request, rule_id):
    """
    Request: Path parameter rule_id representing the ID of the rule to be deleted.

    Response: JSON object confirming success or failure of the deletion process.

    Purpose: To delete a specific rule based on its unique identifier.

    Company Name: Softvan Pvt. Ltd.
    """
    try:
        response_payload = RuleService.delete_rule_service(rule_id)
        response.status_code = response_payload.get("status_code")
        logger.info(f"Deleted rule with ID: {response_payload}")
        return response_payload
    except Exception as exception:
        return AppServices.handle_exception(exception, is_raise=True)


@rule_router.get("/{rule-id}")
# @login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def get_rule_by_id_controller(response: Response, request: Request, rule_id: int):
    """
    Request: Path parameter rule_id to fetch the corresponding rule.

    Response: JSON object containing rule details if found, else error message.

    Purpose: To fetch details of a single rule based on its unique identifier.

    Company Name: Softvan Pvt. Ltd.
    """
    try:
        logger.info(f"Fetching rule details for ID: {rule_id}")
        response_payload = RuleService.get_rule_by_id_service(rule_id)
        response.status_code = response_payload.get("status_code")
        logger.info(f"Fetched rule details: {response_payload}")
        return response_payload
    except Exception as exception:
        return AppServices.handle_exception(exception, is_raise=True)


@rule_router.put("/update")
# @login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def update_rule_controller(
    response: Response,
    request: Request,
    rule_dto: UpdateRuleDTO,
):
    """
    Request: Accepts UpdateRuleDTO containing updated rule information.

    Response: JSON object indicating success or failure of the update operation.

    Purpose: To update an existing rule with new data.

    Company Name: Softvan Pvt. Ltd.
    """
    try:
        response_payload = RuleService.update_rule_service(rule_dto)
        response.status_code = response_payload.get("status_code")
        logger.info(f"Updated job with ID: {response_payload}")
        return response_payload
    except Exception as exception:
        return AppServices.handle_exception(exception, is_raise=True)
