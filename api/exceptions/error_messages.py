from typing import Any

from starlette import status


class BaseMessage:
    def __init__(self, param: Any | None = None) -> None:
        self.param = param
        
    def __str__(self) -> str:
        return self.__class__.__name__
    
    
class ErrorMessage:
    class INTERNAL_SERVER_ERROR(BaseMessage):
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        text = "システムエラーが発生しました。管理者に問い合わせてください。"

    class ID_NOT_FOUND(BaseMessage):
        status_code = status.HTTP_404_NOT_FOUND
        text = "IDが見つかりません。"
        
    class NOT_FOUND(BaseMessage):
        text = "{}が見つかりません。"
        
    class ALREADY_EXISTS(BaseMessage):
        text = "{}は既に存在します。"