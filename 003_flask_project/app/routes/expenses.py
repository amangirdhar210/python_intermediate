from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.services.expense_service import ExpenseService
from app.services.group_service import GroupService

expenses_bp = Blueprint("expenses", __name__)


@expenses_bp.route("/group/<group_id>/create", methods=["GET", "POST"])
@login_required
def create(group_id):
    if not GroupService.is_member(group_id, current_user.id):
        flash("You are not a member of this group", "error")
        return redirect(url_for("groups.list_groups"))

    if request.method == "POST":
        description = request.form.get("description")
        amount = float(request.form.get("amount"))

        expense = ExpenseService.create_expense(
            description=description,
            amount=amount,
            group_id=group_id,
            paid_by=current_user.id,
            split_type="equal",
        )

        flash("Expense added successfully!", "success")
        return redirect(url_for("groups.view", group_id=group_id))

    group = GroupService.get_group(group_id)
    return render_template("expenses/create.html", group=group)


@expenses_bp.route("/group/<group_id>/list")
@login_required
def list_expenses(group_id):
    if not GroupService.is_member(group_id, current_user.id):
        flash("You are not a member of this group", "error")
        return redirect(url_for("groups.list_groups"))

    group = GroupService.get_group(group_id)
    expenses = ExpenseService.get_group_expenses(group_id)

    return render_template("expenses/list.html", group=group, expenses=expenses)
