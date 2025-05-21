from base.config.logger_config import get_logger
from base.custom_enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
from base.dao.country.country_dao import CountryDAO
from base.dao.rules.rules_dao import RuleDAO
from base.utils.custom_exception import AppServices
from base.vo.rules_vo import RuleVO

logger = get_logger()


class RuleService:

    @staticmethod
    def insert_rule_service(rule_dto):

        try:
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
            logger.exception("Error inserting rule")
            return AppServices.handle_exception(exception, is_raise=True)

    @staticmethod
    def get_all_rule_service(page_number, page_size, search_value, sort_by,
                             sort_as):
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
            logger.exception("Error fetching all rule")
            return AppServices.handle_exception(exception, is_raise=True)

    @staticmethod
    def delete_rule_service(rule_id):
        """Soft delete a rule by ID."""
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
            logger.exception("Error deleting rule with ID: %s", rule_id)
            return AppServices.handle_exception(exception, is_raise=True)

    @staticmethod
    def get_rule_by_id_service(rule_id):
        """Retrieve rule details for a given ID."""
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
            logger.exception("Error retrieving rule with ID: %s", rule_id)
            return AppServices.handle_exception(exception, is_raise=True)

    @staticmethod
    def update_rule_service(rule_dto):
        try:
            existing_rule = RuleDAO.get_rule_by_id_dao(rule_dto.rule_id)

            if not existing_rule:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                    data={},
                )

            if rule_dto.rule_id is not None:
                existing_rule.rule_id = rule_dto.rule_id

            if rule_dto.country_id is not None:
                country_vo = CountryDAO.get_country_by_id_dao(
                    rule_dto.country_id)
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

            # Step 3: Persist updated data
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
            logger.exception("Error updating rule")
            return AppServices.handle_exception(exception, is_raise=True)
