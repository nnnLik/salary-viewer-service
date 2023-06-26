from fastapi import HTTPException, status


class EmployeeInfoExistsError(HTTPException):
    def __init__(self):
        detail = "Employee info already exists"
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class EmployeeInfoNotFoundError(HTTPException):
    def __init__(self):
        detail = "Employee info not found"
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class PositionNotFoundError(HTTPException):
    def __init__(self):
        detail = "Position info not found"
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
