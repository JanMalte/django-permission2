"""
Permission logic module
"""

from permission.logics.author import AuthorPermissionLogic as AuthorPermissionLogic
from permission.logics.base import PermissionLogic as PermissionLogic
from permission.logics.collaborators import CollaboratorsPermissionLogic as CollaboratorsPermissionLogic
from permission.logics.groupin import GroupInPermissionLogic as GroupInPermissionLogic
from permission.logics.oneself import OneselfPermissionLogic as OneselfPermissionLogic
from permission.logics.staff import StaffPermissionLogic as StaffPermissionLogic
