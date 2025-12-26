from app.ddb_repo.group_ddb_repo import GroupRepositoryDDB


class GroupService:

    @staticmethod
    def create_group(name, created_by, description=None):
        return GroupRepositoryDDB.create(name, created_by, description)

    @staticmethod
    def get_group(group_id):
        return GroupRepositoryDDB.get_by_id(group_id)

    @staticmethod
    def get_user_groups(user_id):
        return GroupRepositoryDDB.get_user_groups(user_id)

    @staticmethod
    def add_member(group_id, user_id):
        return GroupRepositoryDDB.add_member(group_id, user_id)

    @staticmethod
    def get_members(group_id):
        return GroupRepositoryDDB.get_members(group_id)

    @staticmethod
    def is_member(group_id, user_id):
        return GroupRepositoryDDB.is_member(group_id, user_id)
