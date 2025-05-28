from base.config.logger_config import get_logger
from base.custom_enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
from base.dao.country.country_dao import CountryDAO
from base.dao.rules.rules_dao import RuleDAO
from base.utils.custom_exception import AppServices
from base.vo.rules_vo import RuleVO

logger = get_logger()


class RuleService:
    """
    RuleService Layer

    Company: Softvan Pvt Ltd
    """

    @staticmethod
    def insert_rule_service(rule_dto):
        """
        Request: rule_dto (includes rule_title, rule_description, country_id)
        Response: JSON response with inserted rule data or error
        Purpose: Insert a new rule after validating the provided country_id
        Company: Softvan Pvt Ltd
        """
        try:
            existing_rule = RuleDAO.check_existing_rule(rule_dto.rule_title)
            if existing_rule:
                return AppServices.app_response(
                    HttpStatusCodeEnum.NOT_FOUND,
                    f"The rule Title '{rule_dto.rule_title}' is already in use. "
                    f"Please choose a different Title.",
                    success=False,
                    data={},
                )

            country_vo = CountryDAO.get_country_by_id_dao(rule_dto.country_id)
            if not country_vo:
                return AppServices.app_response(
                    HttpStatusCodeEnum.NOT_FOUND,
                    "try another country",
                    success=False,
                    data={},
                )

            rule_vo = RuleVO()
            rule_vo.rule_country_id = country_vo.country_id
            rule_vo.rule_country_name = country_vo.country_name
            rule_vo.rule_title = rule_dto.rule_title
            rule_vo.rule_description = rule_dto.rule_description

            rule_insert_data = RuleDAO.insert_rule_dao(rule_vo)

            if not rule_insert_data:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                    data={},
                )

            logger.info("Inserted rule: %s", rule_vo.rule_title)
            return AppServices.app_response(
                HttpStatusCodeEnum.OK.value,
                ResponseMessageEnum.INSERT_DATA.value,
                success=True,
                data=rule_insert_data,
            )

        except Exception as exception:
            return AppServices.handle_exception(exception, is_raise=True)

    @staticmethod
    def get_all_rule_service(page_number, page_size, search_value, sort_by, sort_as):
        """
        Request: page_number, page_size, search_value, sort_by, sort_as
        Response: Paginated JSON response with list of rules or error
        Purpose: Retrieve all rules with search, pagination, and sorting support
        Company: Softvan Pvt Ltd
        """
        try:
            result = RuleDAO.get_all_rule_dao(
                page_number=page_number,
                page_size=page_size,
                search_value=search_value,
                sort_by=sort_by,
                sort_as=sort_as,
            )

            if not result["items"]:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                    data={},
                )

            return AppServices.app_response(
                HttpStatusCodeEnum.OK.value,
                ResponseMessageEnum.GET_DATA.value,
                success=True,
                data=result,
            )

        except Exception as exception:
            return AppServices.handle_exception(exception, is_raise=True)

    @staticmethod
    def delete_rule_service(rule_id):
        """
        Request: rule_id
        Response: JSON response confirming soft deletion or failure
        Purpose: Perform soft delete of a rule by marking `is_deleted` as True
        Company: Softvan Pvt Ltd
        """
        try:
            delete_rule_data = RuleDAO.delete_rule_dao(rule_id)

            if not delete_rule_data:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                    data={},
                )

            delete_rule_data.is_deleted = True  # Soft delete

            logger.info("Deleted rule with ID: %s", rule_id)
            return AppServices.app_response(
                HttpStatusCodeEnum.ACCEPTED.value,
                ResponseMessageEnum.DELETE_DATA.value,
                success=True,
                data=delete_rule_data,
            )

        except Exception as exception:
            return AppServices.handle_exception(exception, is_raise=True)

    @staticmethod
    def get_rule_by_id_service(rule_id):
        """
        Request: rule_id
        Response: JSON response with rule detail or error
        Purpose: Fetch specific rule detail using unique rule ID
        Company: Softvan Pvt Ltd
        """
        try:
            rule_detail = RuleDAO.get_rule_by_id_dao(rule_id)

            if not rule_detail:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                    data={},
                )

            logger.info("Fetched rule detail for ID: %s", rule_id)
            return AppServices.app_response(
                HttpStatusCodeEnum.ACCEPTED.value,
                ResponseMessageEnum.GET_DATA.value,
                success=True,
                data=rule_detail,
            )

        except Exception as exception:
            return AppServices.handle_exception(exception, is_raise=True)

    @staticmethod
    def update_rule_service(rule_dto):
        """
        Request: rule_dto (includes rule_id, updated title/description/country_id)
        Response: JSON response with updated rule data or error
        Purpose: Update an existing rule with new details and country mapping
        Company: Softvan Pvt Ltd
        """
        try:
            existing_rule = RuleDAO.check_existing_rule(rule_dto.rule_title)
            if existing_rule:
                return AppServices.app_response(
                    HttpStatusCodeEnum.NOT_FOUND,
                    f"The rule Title '{rule_dto.rule_title}' is already in use. "
                    f"Please choose a different Title.",
                    success=False,
                    data={},
                )

            if rule_dto.rule_id is not None:
                existing_rule.rule_id = rule_dto.rule_id

            if rule_dto.country_id is not None:
                country_vo = CountryDAO.get_country_by_id_dao(rule_dto.country_id)
                if not country_vo:
                    return AppServices.app_response(
                        HttpStatusCodeEnum.NOT_FOUND,
                        "try another country",
                        success=False,
                        data={},
                    )
                existing_rule.rule_country_id = country_vo.country_id
                existing_rule.rule_country_name = country_vo.country_name

            if rule_dto.rule_title is not None:
                existing_rule.rule_title = rule_dto.rule_title

            if rule_dto.rule_description is not None:
                existing_rule.rule_description = rule_dto.rule_description

            updated_rule = RuleDAO.update_rule_dao(existing_rule)

            if not updated_rule:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.UPDATE_FAILED.value,
                    success=False,
                    data={},
                )

            logger.info("Updated rule with ID: %s", rule_dto.rule_id)
            return AppServices.app_response(
                HttpStatusCodeEnum.ACCEPTED.value,
                ResponseMessageEnum.UPDATE_DATA.value,
                success=True,
                data=updated_rule,
            )

        except Exception as exception:
            return AppServices.handle_exception(exception, is_raise=True)
