import os
from typing import Any, Optional, Type
from pydantic.v1 import BaseModel, Field
from crewai_tools import RagTool  # pyright: ignore[reportMissingImports]
from sec_api import QueryApi    # pyright: ignore[reportMissingImports]
from embedchain.models.data_type import DataType  # pyright: ignore[reportMissingImports]
import requests
import html2text  # pyright: ignore[reportMissingImports]
import re

class FixedSEC10KToolSchema(BaseModel):
    """Input schema for FixedSEC10KTool."""

    search_query: str = Field(..., description="Mandatory query you would like to search from the 10-K filing report.")

class SEC10KToolSchema(FixedSEC10KToolSchema):
    """Input schema for SEC10KTool."""
    stock_name: str = Field(..., description="Mandatory valid stock name you would like to search")

class SEC10KTool(RagTool):
    name: str = "Search in the specified 10-K form"
    description: str = "Useful tool to perform semantic search a query from 10-K filing report of a company."
    args_schema: Type[BaseModel] = SEC10KToolSchema

    def __init__(self, stock_name: Optional[str] = None, **kwargs):
        print(f"Initializing SEC10KTool with stock_name: {stock_name}")
        super().__init__(**kwargs)
        if stock_name is not None:
            content = self.get_10k_url_content(stock_name)
            if content:
                self.add(content)
                self.description = f"A tool that can be used to semantic search a query from {stock_name}'s latest 10-K SEC form's content as a txt file."
                self.args_schema = FixedSEC10KToolSchema
                self._generate_description()
    
    def get_10k_url_content(self, stock_name: str) -> Optional[str]:
        """ Fetches the URL content as txt of the latest 10-K form for the given stock""" 
        