from typing import Any, Dict, Type, TypeVar, Tuple, Optional, BinaryIO, TextIO, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.test_case_result_passed import TestCaseResultPassed






T = TypeVar("T", bound="TestCaseResult")


@_attrs_define
class TestCaseResult:
    """ 
        Attributes:
            name (str):
            passed (TestCaseResultPassed):
            message (str):
     """

    name: str
    passed: TestCaseResultPassed
    message: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        passed = self.passed.value

        message = self.message


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "passed": passed,
            "message": message,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        passed = TestCaseResultPassed(d.pop("passed"))




        message = d.pop("message")

        test_case_result = cls(
            name=name,
            passed=passed,
            message=message,
        )


        test_case_result.additional_properties = d
        return test_case_result

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
