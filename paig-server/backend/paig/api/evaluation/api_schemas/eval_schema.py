import os
from pydantic import BaseModel, Field, ConfigDict
from typing import Literal, List, Optional
from core.factory.database_initiator import BaseAPIFilter
from fastapi import Query
from datetime import datetime
from api.evaluation.api_schemas.eval_config_schema import ConfigCreateRequest

REPORT_URL = os.environ.get('REPORT_SERVER_BASE_URL', 'http://localhost:15500')

class GetCategories(BaseModel):
    purpose: str = Field(..., max_length=1024)

class SaveAndRunRequest(ConfigCreateRequest):
    report_name: str = Field(..., max_length=1024)

class RunRequest(BaseModel):
    report_name: str = Field(..., max_length=1024)

class BaseEvaluationView(BaseModel):
    name: str = Field(..., max_length=1024)
    application_names: str = Field(..., max_length=1024)
    config_name: str = Field(..., max_length=1024)
    purpose: str = Field(..., max_length=1024)
    eval_id: str = Field(..., max_length=1024)
    config_id: int
    status: str = Field(..., max_length=1024)
    owner: Optional[str] = Field(None, description="The User ID", alias="owner")
    passed: str
    failed: str
    id: int
    create_time: Optional[datetime]
    report_url: str = Field(default=REPORT_URL)
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )


class QueryParamsBase(BaseAPIFilter):
    owner: Optional[str] = Field(None, description="The User ID", alias="owner")
    application_names: Optional[str] = Field(None, description="The Application name", alias="application_names")
    config_name: Optional[str] = Field(None, description="The Config name", alias="config_name")
    purpose: Optional[str] = Field(None, description="The Purpose", alias="purpose")
    name: Optional[str] = Field(None, description="The Name", alias="name")
    status: Optional[str] = Field(None, description="The Status", alias="status")



class IncludeQueryParams(QueryParamsBase):
    pass

def include_query_params(
        include_query_application_names: Optional[str] = Query(None, alias="includeQuery.application_names"),
        include_query_owner: Optional[str] = Query(None, alias="includeQuery.owner"),
        include_query_config_name: Optional[str] = Query(None, alias="includeQuery.config_name"),
        include_query_purpose: Optional[str] = Query(None, alias="includeQuery.purpose"),
        include_query_name: Optional[str] = Query(None, alias="includeQuery.name"),
        include_query_status: Optional[str] = Query(None, alias="includeQuery.status"),
) -> IncludeQueryParams:
    return IncludeQueryParams(
        application_names=include_query_application_names,
        owner=include_query_owner,
        config_name=include_query_config_name,
        purpose=include_query_purpose,
        name=include_query_name,
        status=include_query_status
    )


def exclude_query_params(
        exclude_query_application_names: Optional[str] = Query(None, alias="excludeQuery.application_names"),
        exclude_query_owner: Optional[str] = Query(None, alias="excludeQuery.owner"),
        exclude_query_config_name: Optional[str] = Query(None, alias="excludeQuery.config_name"),
        exclude_query_purpose: Optional[str] = Query(None, alias="excludeQuery.purpose"),
        exclude_query_name: Optional[str] = Query(None, alias="excludeQuery.name"),
        exclude_query_status: Optional[str] = Query(None, alias="excludeQuery.status"),
) -> QueryParamsBase:
    return QueryParamsBase(
        application_names=exclude_query_application_names,
        owner=exclude_query_owner,
        config_name=exclude_query_config_name,
        purpose=exclude_query_purpose,
        name=exclude_query_name,
        status=exclude_query_status
    )


def extract_include_query_params(params):
    params_dict = params.model_dump(exclude=BaseAPIFilter.model_fields.keys(), by_alias=False, exclude_none=True)

    # Extract only the required fields
    filtered_params = {params.model_fields[field].alias: value for field, value in params_dict.items() if
                       value is not None}

    return filtered_params