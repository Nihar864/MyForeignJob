from fastapi import APIRouter

from base.api.controller.benefit import benefit_controller
from base.api.controller.country import country_controller
from base.api.controller.faq import faq_controller
from base.api.controller.job import job_controller
from base.api.controller.login import login_controller
from base.api.controller.news import news_controller
from base.api.controller.rules import rules_controller
from base.api.controller.social_media import social_media_controller
from base.api.controller.user import user_controller

router = APIRouter()

router.include_router(login_controller.login_router)
router.include_router(user_controller.user_router)
router.include_router(country_controller.country_router)
router.include_router(job_controller.job_router)
router.include_router(faq_controller.faq_router)
router.include_router(benefit_controller.benefit_router)
router.include_router(rules_controller.rule_router)
router.include_router(social_media_controller.social_media_router)
router.include_router(news_controller.news_router)
