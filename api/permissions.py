from rest_framework.permissions import BasePermission


class IsStaff(BasePermission):
    """
    *** Authorization for executing dangerous commands ***
    *** Only staff members are allowed ***
    """

    def has_permission(self, request, view):
        dangerous_commands = ["shutdown", "reboot", "poweroff", "attrib", "diskpart", "del", "rd"]

        # authorize user for executing dangerous commands
        # commands can contain multiple parts e.g., shutdown -s, attrib -r -s -h
        if request.data['command'].split()[0] in dangerous_commands:
            return bool(request.user and request.user.is_staff)
        else:
            return True
