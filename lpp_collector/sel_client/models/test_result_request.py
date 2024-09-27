from typing import (
    Any,
    Dict,
    Type,
    TypeVar,
    Tuple,
    Optional,
    BinaryIO,
    TextIO,
    TYPE_CHECKING,
)

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field
import json

from ..types import UNSET, Unset

from dateutil.parser import isoparse
import datetime
from typing import Union
from typing import cast, List
from typing import cast
from io import BytesIO
from ..types import UNSET, Unset
from typing import Dict
from ..types import File, FileJsonType

if TYPE_CHECKING:
    from ..models.test_case_result import TestCaseResult


T = TypeVar("T", bound="TestResultRequest")


@_attrs_define
class TestResultRequest:
    """
    Attributes:
        device_time (datetime.datetime):
        test_type (str):
        result (List['TestCaseResult']):
        testcases (Union[Unset, File]):
        source_code (Union[Unset, File]):
    """

    device_time: datetime.datetime
    test_type: str
    result: List["TestCaseResult"]
    testcases: Union[Unset, File] = UNSET
    source_code: Union[Unset, File] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.test_case_result import TestCaseResult

        device_time = self.device_time.isoformat()

        test_type = self.test_type

        result = []
        for result_item_data in self.result:
            result_item = result_item_data.to_dict()
            result.append(result_item)

        testcases: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.testcases, Unset):
            testcases = self.testcases.to_tuple()

        source_code: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.source_code, Unset):
            source_code = self.source_code.to_tuple()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "deviceTime": device_time,
                "testType": test_type,
                "result": result,
            }
        )
        if testcases is not UNSET:
            field_dict["testcases"] = testcases
        if source_code is not UNSET:
            field_dict["sourceCode"] = source_code

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        device_time = self.device_time.strftime("%Y-%m-%dT%H:%M:%SZ").encode()
        device_time = (None, device_time, "text/plain")

        test_type = (None, str(self.test_type).encode(), "text/plain")

        _temp_result = []
        for result_item_data in self.result:
            result_item = result_item_data.to_dict()
            _temp_result.append(result_item)
        result = (None, json.dumps(_temp_result).encode(), "application/json")

        testcases: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.testcases, Unset):
            testcases = self.testcases.to_tuple()

        source_code: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.source_code, Unset):
            source_code = self.source_code.to_tuple()

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict.update(
            {
                "deviceTime": device_time,
                "testType": test_type,
                "result": result,
            }
        )
        if testcases is not UNSET:
            field_dict["testcases"] = testcases
        if source_code is not UNSET:
            field_dict["sourceCode"] = source_code

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.test_case_result import TestCaseResult

        d = src_dict.copy()
        device_time = isoparse(d.pop("deviceTime"))

        test_type = d.pop("testType")

        result = []
        _result = d.pop("result")
        for result_item_data in _result:
            result_item = TestCaseResult.from_dict(result_item_data)

            result.append(result_item)

        _testcases = d.pop("testcases", UNSET)
        testcases: Union[Unset, File]
        if isinstance(_testcases, Unset):
            testcases = UNSET
        else:
            testcases = File(payload=BytesIO(_testcases))

        _source_code = d.pop("sourceCode", UNSET)
        source_code: Union[Unset, File]
        if isinstance(_source_code, Unset):
            source_code = UNSET
        else:
            source_code = File(payload=BytesIO(_source_code))

        test_result_request = cls(
            device_time=device_time,
            test_type=test_type,
            result=result,
            testcases=testcases,
            source_code=source_code,
        )

        test_result_request.additional_properties = d
        return test_result_request

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
