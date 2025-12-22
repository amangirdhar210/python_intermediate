from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.services.group_service import GroupService
from app.services.balance_service import BalanceService

groups_bp = Blueprint("groups", __name__)


@groups_bp.route("/")
@login_required
def list_groups():
    groups = GroupService.get_user_groups(current_user.id)
    return render_template("groups/list.html", groups=groups)


@groups_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")

        group = GroupService.create_group(name, current_user.id, description)
        flash(f'Group "{name}" created successfully!', "success")
        return redirect(url_for("groups.view", group_id=group["id"]))

    return render_template("groups/create.html")


@groups_bp.route("/<group_id>")
@login_required
def view(group_id):
    if not GroupService.is_member(group_id, current_user.id):
        flash("You are not a member of this group", "error")
        return redirect(url_for("groups.list_groups"))

    group = GroupService.get_group(group_id)
    members = GroupService.get_members(group_id)
    balances = BalanceService.calculate_balances(group_id)

    from app.services.expense_service import ExpenseService

    expenses = ExpenseService.get_group_expenses(group_id)

    return render_template(
        "groups/view.html",
        group=group,
        members=members,
        balances=balances,
        expenses=expenses[:5],
    )


@groups_bp.route("/<group_id>/add_member", methods=["POST"])
@login_required
def add_member(group_id):
    if not GroupService.is_member(group_id, current_user.id):
        flash("You are not a member of this group", "error")
        return redirect(url_for("groups.list_groups"))

    username = request.form.get("username")

    from app.repositories.user_repository import UserRepository

    user = UserRepository.get_by_username(username)

    if not user:
        flash(f"User '{username}' not found", "error")
        return redirect(url_for("groups.view", group_id=group_id))

    if GroupService.add_member(group_id, user.id):
        flash(f"Member '{username}' added successfully!", "success")
    else:
        flash(f"User '{username}' is already a member", "error")

    return redirect(url_for("groups.view", group_id=group_id))
