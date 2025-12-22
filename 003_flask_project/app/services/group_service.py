from app.repositories.group_repository import GroupRepository
from app.repositories.user_repository import UserRepository


class GroupService:

    @staticmethod
    def create_group(name, created_by, description=None):
        return GroupRepository.create(name, created_by, description)

    @staticmethod
    def get_group(group_id):
        return GroupRepository.get_by_id(group_id)

    @staticmethod
    def get_user_groups(user_id):
        return GroupRepository.get_user_groups(user_id)

    @staticmethod
    def add_member(group_id, user_id):
        return GroupRepository.add_member(group_id, user_id)

    @staticmethod
    def get_members(group_id):
        return GroupRepository.get_members(group_id)

    @staticmethod
    def is_member(group_id, user_id):
        return GroupRepository.is_member(group_id, user_id)

    @staticmethod
    def search_users(query):
        return UserRepository.search(query)
