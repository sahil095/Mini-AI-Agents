import os
from typing import Any, Optional, Type
from pydantic import BaseModel, Field
from crewai_tools import RagTool  # pyright: ignore[reportMissingImports]
from sec_api import QueryApi    # pyright: ignore[reportMissingImports]
from crewai_tools.rag.data_types import DataType  # pyright: ignore[reportMissingImports]
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
        """ Initialize the SEC10KTool with the given stock name"""
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
        try:
            query_api = QueryApi(api_key=os.getenv("SEC_API_API_KEY"))
            query = {
                "query": {
                    "query_string": {
                            "query": f"ticker:{stock_name} AND formType:\"10-K\"",
                        }
                    },
                    "from": 0,
                    "size": 1,
                    "sort": [
                        {
                            "filedAt": {
                                "order": "desc"
                            }
                        }
                    ]
                }
            filings = query_api.get_filings(query=query)['filings']
            if len(filings) == 0:
                print("No filings found for this stock")
                return None
            
            url = filings[0]['linkToFilingDetails']

            headers = {
                "User-Agent": "sehgal.sahil0786@gmail.com",
                "Accept-Encoding": "gzip, deflate",
                "Host": "www.sec.gov"
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            h = html2text.HTML2Text()
            h.ignore_links = False
            text = h.handle(response.content.decode('utf-8'))

            text = re.sub(r"[^a-zA-Z0-9\s\n]", "", text)
            return text
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error occurred: {e}")
            return None
        except Exception as e:
            print(f"Error fetching 10-K content for {stock_name}: {e}")
            return None
    
    def add(self, *args:Any, **kwargs: Any)-> None:
        """ Add the 10-K content to the tool"""
        kwargs["data_type"] = DataType.TEXT
        super().add(*args, **kwargs)

    def _run(self, search_query: str, **kwargs: Any) -> Any:
        """ Perform semantic search on the 10-K content for the given query"""
        return super()._run(search_query, **kwargs)


class FixedSEC10QToolSchema(BaseModel):
    """Input schema for FixedSEC10QTool."""

    search_query: str = Field(..., description="Mandatory query you would like to search from the 10-Q filing report.")


class SEC10QToolSchema(FixedSEC10QToolSchema):
    """Input schema for SEC10QTool."""
    stock_name: str = Field(..., description="Mandatory valid stock name you would like to search")


class SEC10QTool(RagTool):
    name: str = "Search in the specified 10-Q form"
    description: str = "Useful tool to perform semantic search a query from 10-Q filing report of a company."
    args_schema: Type[BaseModel] = SEC10QToolSchema

    def __init__(self, stock_name: Optional[str] = None, **kwargs):
        """ Initialize the SEC10QTool with the given stock name"""
        print(f"Initializing SEC10QTool with stock_name: {stock_name}")
        super().__init__(**kwargs)
        if stock_name is not None:
            content = self.get_10q_url_content(stock_name)
            if content:
                self.add(content)
                self.description = f"A tool that can be used to semantic search a query from {stock_name}'s latest 10-Q SEC form's content as a txt file."
                self.args_schema = FixedSEC10QToolSchema
                self._generate_description()
    
    def get_10q_url_content(self, stock_name: str) -> Optional[str]:
        """ Fetches the URL content as txt of the latest 10-Q form for the given stock""" 
        try:
            query_api = QueryApi(api_key=os.getenv("SEC_API_API_KEY"))
            query = {
                "query": {
                    "query_string": {
                            "query": f"ticker:{stock_name} AND formType:\"10-Q\"",
                        }
                    },
                    "from": 0,
                    "size": 1,
                    "sort": [
                        {
                            "filedAt": {
                                "order": "desc"
                            }
                        }
                    ]
                }
            filings = query_api.get_filings(query=query)['filings']
            if len(filings) == 0:
                print("No filings found for this stock")
                return None
            
            url = filings[0]['linkToFilingDetails']

            headers = {
                "User-Agent": "sehgal.sahil0786@gmail.com",
                "Accept-Encoding": "gzip, deflate",
                "Host": "www.sec.gov"
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            h = html2text.HTML2Text()
            h.ignore_links = False
            text = h.handle(response.content.decode('utf-8'))

            text = re.sub(r"[^a-zA-Z0-9\s\n]", "", text)
            return text
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error occurred: {e}")
            return None
        except Exception as e:
            print(f"Error fetching 10-Q content for {stock_name}: {e}")
            return None
    
    def add(self, *args:Any, **kwargs: Any)-> None:
        """ Add the 10-Q content to the tool"""
        kwargs["data_type"] = DataType.TEXT
        super().add(*args, **kwargs)

    def _run(self, search_query: str, **kwargs: Any) -> Any:
        """ Perform semantic search on the 10-Q content for the given query"""
        return super()._run(search_query, **kwargs)
