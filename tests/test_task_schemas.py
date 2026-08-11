import pytest
from src.tasks.schemas import STaskResponse

pytestmarker = pytest.mark.unit

class MockTaskResponse:
    task_id = 1
    name = "Купить молоко"
    description = "В магазине у дома"
 
def test_task_response_from_orm_object():
    payload = MockTaskResponse()

    schema = STaskResponse.model_validate(payload)

    assert schema.task_id == payload.task_id
    assert schema.description == payload.description
    assert schema.name == payload.name