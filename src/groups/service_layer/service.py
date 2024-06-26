from typing import Optional, List, Set

from src.groups.domain.models import GroupModel, GroupMemberModel
from src.groups.interfaces.units_of_work import GroupsUnitOfWork
from src.groups.exceptions import GroupNotFoundError


class GroupsService:
    """
    Service layer core according to DDD, which using a unit of work, will perform operations on the domain model.
    """

    def __init__(self, uow: GroupsUnitOfWork) -> None:
        self._uow: GroupsUnitOfWork = uow

    async def get_group_by_id(self, id: int) -> GroupModel:
        async with self._uow as uow:
            group: Optional[GroupModel] = await uow.groups.get(id=id)
            if not group:
                raise GroupNotFoundError

            return group

    async def create_group(self, group: GroupModel) -> GroupModel:
        async with self._uow as uow:
            group = await uow.groups.add(model=group)
            await uow.commit()
            return group

    async def check_group_existence(self, owner_id: int, name: str) -> bool:
        async with self._uow as uow:
            group: Optional[GroupModel] = await uow.groups.get_by_owner_and_name(name=name, owner_id=owner_id)
            if group:
                return True

        return False

    async def delete_group(self, id: int) -> None:
        async with self._uow as uow:
            await uow.groups.delete(id=id)
            await uow.commit()

    async def get_user_groups(self, user_id: int) -> List[GroupModel]:
        async with self._uow as uow:
            groups: List[GroupModel] = await uow.groups.get_user_groups(user_id=user_id)
            return groups

    async def add_group_members(self, id: int, members: Set[GroupMemberModel]) -> GroupModel:
        async with self._uow as uow:
            group: Optional[GroupModel] = await uow.groups.get(id=id)
            if not group:
                raise GroupNotFoundError

            group.members.update(members)
            await uow.commit()
            return group

    async def remove_group_members(self, id: int, members: Set[GroupMemberModel]) -> GroupModel:
        async with self._uow as uow:
            group: Optional[GroupModel] = await uow.groups.get(id=id)
            if not group:
                raise GroupNotFoundError

            for member in members:
                group.members.remove(member)

            await uow.commit()
            return group

    async def update_group(self, id: int, group: GroupModel) -> GroupModel:
        async with self._uow as uow:
            if not await uow.groups.get(id=id):
                raise GroupNotFoundError

            group = await uow.groups.update(id=id, model=group)
            await uow.commit()
            return group
