import json
from typing import TypeVar, Generic, Any

import xmltodict
from pydantic import BaseModel
from typing import get_args

T = TypeVar("T", bound=BaseModel)

class ConnectorResponse(Generic[T]):
    def __init__(self, text: str, json_from_xml: bool = False):
        self._text = text
        self._json_from_xml = json_from_xml

    def model(self) -> T:
        """
        Parse and return the response as a Pydantic model.
        """
        orig = getattr(self, "__orig_class__", None)
        if not orig:
            raise ValueError("Pydantic model Type not specified. `.model()` cannot be used for this ConnectorResponse.")
        
        model_cls = get_args(orig)[0]

        if self._json_from_xml:
            data = json.dumps(xmltodict.parse(self._text))
        else:
            data = self._text
        
        return model_cls.model_validate_json(data)

    def json(self) -> dict:
        """
        Parse and return the response as a dict object.
        """
        if self._json_from_xml:
            return xmltodict.parse(self._text)
        return json.loads(self._text)

    def text(self) -> str:
        """Return the raw response text."""
        return self._text
