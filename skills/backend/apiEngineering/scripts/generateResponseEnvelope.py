#!/usr/bin/env python3
"""
generateResponseEnvelope.py
Generates type-safe response DTO envelope wrappers for TypeScript and Python (Pydantic v2):
- Top-level { data, meta } success envelope
- RFC 9457 Problem Details model
"""

import sys
import argparse

TS_TEMPLATE = """/**
 * Production API Response Envelopes (RFC 9110 & RFC 9457 Compliant)
 */

export interface ApiResponse<T> {
  data: T;
  meta?: ResponseMeta;
}

export interface ResponseMeta {
  cursor?: string | null;
  hasNextPage?: boolean;
  limit?: number;
  totalCount?: number;
}

export interface ProblemDetails {
  type: string;
  title: string;
  status: number;
  detail?: string;
  instance?: string;
  errors?: FieldValidationError[];
}

export interface FieldValidationError {
  field: string;
  code?: string;
  message: string;
}
"""

PY_TEMPLATE = '''"""
Production API Response Envelopes (Pydantic v2 - RFC 9110 & RFC 9457 Compliant)
"""

from typing import Generic, TypeVar, Optional, List, Any
from pydantic import BaseModel, Field

T = TypeVar("T")

class ResponseMeta(BaseModel):
    cursor: Optional[str] = None
    has_next_page: Optional[bool] = Field(None, alias="hasNextPage")
    limit: Optional[int] = None
    total_count: Optional[int] = Field(None, alias="totalCount")

class ApiResponse(BaseModel, Generic[T]):
    data: T
    meta: Optional[ResponseMeta] = None

class FieldValidationError(BaseModel):
    field: str
    code: Optional[str] = None
    message: str

class ProblemDetails(BaseModel):
    type: str = Field(..., description="Stable URI categorizing problem type")
    title: str = Field(..., description="Short summary of problem")
    status: int = Field(..., description="HTTP status code")
    detail: Optional[str] = Field(None, description="Detailed explanation")
    instance: Optional[str] = Field(None, description="Request URI path")
    errors: Optional[List[FieldValidationError]] = None
'''

def main():
    parser = argparse.ArgumentParser(description="Generate response envelope DTOs")
    parser.add_argument("--lang", choices=["ts", "py"], default="ts", help="Target language (ts or py)")
    args = parser.parse_args()

    if args.lang == "ts":
        print(TS_TEMPLATE)
    else:
        print(PY_TEMPLATE)

if __name__ == "__main__":
    main()
