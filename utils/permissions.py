class Permissions:
    def __init__(self, is_host_management: bool = False, 
                       is_bot_management: bool = False,
                       is_database_view: bool = False):
        self._permissions = (is_host_management, is_bot_management, is_database_view)
        
    def get_host_permission(self) -> bool:
        return self._permissions[0]
    

    def get_bot_permission(self) -> bool:
        return self._permissions[1]
    
    
    def get_database_permission(self) -> bool:
        return self._permissions[2]
    