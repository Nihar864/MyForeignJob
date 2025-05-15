from fastapi import APIRouter

from base.api.controller.country import country_controller
from base.api.controller.faq import faq_controller
from base.api.controller.job import job_controller
from base.api.controller.login import login_controller
from base.api.controller.register import register_controller

router = APIRouter()

router.include_router(login_controller.login_router)
router.include_router(register_controller.register_router)
router.include_router(country_controller.country_router)
router.include_router(job_controller.job_router)
router.include_router(faq_controller.faq_router)
