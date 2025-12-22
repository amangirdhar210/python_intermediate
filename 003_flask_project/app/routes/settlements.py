from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.services.balance_service import BalanceService
from app.services.group_service import GroupService

settlements_bp = Blueprint("settlements", __name__)


@settlements_bp.route("/group/<group_id>")
@login_required
def view_balances(group_id):
    if not GroupService.is_member(group_id, current_user.id):
        flash("You are not a member of this group", "error")
        return redirect(url_for("groups.list_groups"))

    group = GroupService.get_group(group_id)
    balances = BalanceService.calculate_balances(group_id)
    user_summary = BalanceService.get_user_balance_summary(current_user.id, group_id)

    return render_template(
        "settlements/balances.html",
        group=group,
        balances=balances,
        user_summary=user_summary,
    )


@settlements_bp.route("/group/<group_id>/settle", methods=["POST"])
@login_required
def settle_up(group_id):
    if not GroupService.is_member(group_id, current_user.id):
        flash("You are not a member of this group", "error")
        return redirect(url_for("groups.list_groups"))

    to_user_id = request.form.get("to_user_id")
    amount = float(request.form.get("amount"))

    BalanceService.settle_up(group_id, current_user.id, to_user_id, amount)
    flash("Settlement recorded successfully!", "success")

    return redirect(url_for("settlements.view_balances", group_id=group_id))
