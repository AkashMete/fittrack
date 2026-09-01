from datetime import date

from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource, fields

from ....common.errors import ForbiddenError, NotFoundError
from ....common.pagination import get_page_args, paginate
from ....common.responses import success
from ....models import DietLog, DietPlan, User
from . import services
from .schemas import (
    diet_log_entry_schema,
    diet_log_entry_update_schema,
    diet_log_notes_schema,
    diet_plan_schema,
    diet_plan_update_schema,
)

diet_ns = Namespace("diet", description="Diet plans and daily tracking")


def _current_user() -> User:
    u = User.objects(id=get_jwt_identity()).first()
    if not u:
        raise NotFoundError("User not found")
    return u


def _get_plan(plan_id: str, user: User) -> DietPlan:
    plan = DietPlan.objects(id=plan_id, user=user).first()
    if not plan:
        raise NotFoundError(f"Diet plan {plan_id} not found")
    return plan


def _parse_date(date_str: str) -> date:
    try:
        return date.fromisoformat(date_str)
    except ValueError:
        from ....common.errors import BadRequestError
        raise BadRequestError("Date must be YYYY-MM-DD format")


# ── Plans ─────────────────────────────────────────────────────────────────────

@diet_ns.route("/plans")
class PlanList(Resource):
    @jwt_required()
    def get(self):
        """List own diet plans"""
        user = _current_user()
        page, per_page = get_page_args()
        qs = DietPlan.objects(user=user).order_by("-created_at")
        items, meta = paginate(qs, page, per_page)
        return success([p.to_dict() for p in items], meta=meta)

    @jwt_required()
    @diet_ns.response(201, "Plan created")
    def post(self):
        """Create a diet plan"""
        user = _current_user()
        data = diet_plan_schema.load(diet_ns.payload or {})
        plan = services.create_plan(user, data)
        return success(plan.to_dict(), status_code=201)


@diet_ns.route("/plans/<string:plan_id>")
class PlanDetail(Resource):
    @jwt_required()
    def get(self, plan_id: str):
        """Get diet plan with all meals"""
        return success(_get_plan(plan_id, _current_user()).to_dict())

    @jwt_required()
    def patch(self, plan_id: str):
        """Update plan name / meals"""
        user = _current_user()
        plan = _get_plan(plan_id, user)
        data = diet_plan_update_schema.load(diet_ns.payload or {})
        plan = services.update_plan(plan, data)
        return success(plan.to_dict())

    @jwt_required()
    def delete(self, plan_id: str):
        """Delete a diet plan"""
        user = _current_user()
        _get_plan(plan_id, user).delete()
        return success({"message": "Plan deleted"})


@diet_ns.route("/plans/<string:plan_id>/activate")
class PlanActivate(Resource):
    @jwt_required()
    def patch(self, plan_id: str):
        """Set this plan as the active plan (deactivates all others)"""
        user = _current_user()
        plan = services.activate_plan(user, _get_plan(plan_id, user))
        return success(plan.to_dict())


@diet_ns.route("/plans/<string:plan_id>/duplicate")
class PlanDuplicate(Resource):
    @jwt_required()
    def post(self, plan_id: str):
        """Duplicate a plan as a new starting template"""
        user = _current_user()
        new_plan = services.duplicate_plan(user, _get_plan(plan_id, user))
        return success(new_plan.to_dict(), status_code=201)


# ── Daily log ─────────────────────────────────────────────────────────────────

@diet_ns.route("/logs")
class LogList(Resource):
    @jwt_required()
    @diet_ns.param("start_date", "YYYY-MM-DD")
    @diet_ns.param("end_date", "YYYY-MM-DD")
    def get(self):
        """List diet logs in a date range"""
        user = _current_user()
        filters = {"user": user}
        if request.args.get("start_date"):
            filters["date__gte"] = _parse_date(request.args["start_date"])
        if request.args.get("end_date"):
            filters["date__lte"] = _parse_date(request.args["end_date"])
        page, per_page = get_page_args()
        qs = DietLog.objects(**filters).order_by("-date")
        items, meta = paginate(qs, page, per_page)
        return success([l.to_dict() for l in items], meta=meta)


@diet_ns.route("/logs/<string:log_date>")
class LogDay(Resource):
    @jwt_required()
    def get(self, log_date: str):
        """Get (or create empty) log for YYYY-MM-DD"""
        user = _current_user()
        log = services.get_or_create_log(user, _parse_date(log_date))
        return success(log.to_dict())

    @jwt_required()
    def patch(self, log_date: str):
        """Update day notes"""
        user = _current_user()
        data = diet_log_notes_schema.load(diet_ns.payload or {})
        log = services.get_or_create_log(user, _parse_date(log_date))
        log.notes = data.get("notes")
        log.save()
        return success(log.to_dict())


@diet_ns.route("/logs/<string:log_date>/entries")
class LogEntries(Resource):
    @jwt_required()
    @diet_ns.response(201, "Entry added")
    def post(self, log_date: str):
        """Add a food entry to a daily log"""
        user = _current_user()
        data = diet_log_entry_schema.load(diet_ns.payload or {})
        log, _ = services.add_entry(user, _parse_date(log_date), data)
        return success(log.to_dict(), status_code=201)


@diet_ns.route("/logs/<string:log_date>/entries/<string:entry_id>")
class LogEntry(Resource):
    @jwt_required()
    def patch(self, log_date: str, entry_id: str):
        """Edit quantity or meal type of an existing entry"""
        user = _current_user()
        data = diet_log_entry_update_schema.load(diet_ns.payload or {})
        log = services.update_entry(user, _parse_date(log_date), entry_id, data)
        return success(log.to_dict())

    @jwt_required()
    def delete(self, log_date: str, entry_id: str):
        """Remove an entry from a log"""
        user = _current_user()
        log = services.delete_entry(user, _parse_date(log_date), entry_id)
        return success(log.to_dict())


@diet_ns.route("/logs/<string:log_date>/import-plan")
class LogImportPlan(Resource):
    @jwt_required()
    def post(self, log_date: str):
        """Quick-import entries from the active diet plan into today's log"""
        user = _current_user()
        log = services.import_from_plan(user, _parse_date(log_date))
        return success(log.to_dict())


# ── Monthly report ────────────────────────────────────────────────────────────

@diet_ns.route("/reports/monthly")
class DietMonthlyReport(Resource):
    @jwt_required()
    @diet_ns.param("year", "4-digit year")
    @diet_ns.param("month", "1-12")
    def get(self):
        """Monthly diet summary — averages, trend, compliance"""
        user = _current_user()
        try:
            year = int(request.args.get("year", date.today().year))
            month = int(request.args.get("month", date.today().month))
            if not (1 <= month <= 12):
                raise ValueError
        except ValueError:
            from ....common.errors import BadRequestError
            raise BadRequestError("year and month must be valid integers")
        return success(services.monthly_report(user, year, month))
