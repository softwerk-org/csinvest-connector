import httpx
import pydantic


HTTPStatusError = httpx.HTTPStatusError
RequestError = httpx.RequestError
ValidationError = pydantic.ValidationError


class AuthParamsError(Exception):
    pass
