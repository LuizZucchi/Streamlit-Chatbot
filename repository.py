import logging
import os
from typing import Any, Mapping, Optional
import requests

from langchain_community.tools import DuckDuckGoSearchResults
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.llms.base import LLM 

import os
from abc import ABC, abstractmethod


class IRepository(ABC):
    @abstractmethod
    def query(self, question: str, search_results: str, logger: logging.Logger) -> str:
        """Queries the model with the provided question and search results."""
        pass

class ISearchRepository(ABC):
    @abstractmethod
    def web_search(self, query: str, logger: logging.Logger) -> str:
        """Performs a web search and returns the results."""
        pass
    
class OpenAIRepository(IRepository):
    def __init__(self, api_key=None, model="gpt-4.1", logger: logging.Logger = None):
        api_key = os.environ.get("OPENAI_API_KEY", api_key) 
        self.logger = logger or logging.getLogger(__name__)
        
        if not api_key:
            self.logger.critical("OpenAI API key not provided. Exiting initialization.")
            raise ValueError("OpenAI API key must be provided either as parameter or through OPENAI_API_KEY environment variable")
        
        self.logger.info(f"Using OpenAI API key: {api_key}")
        
        self.llm = ChatOpenAI(openai_api_key=api_key, model_name=model)
        self.prompt = PromptTemplate(
            input_variables=["question", "search_results"],
            template="Question: {question}\n{search_results}\nAnswer concisely with references if available."
        )
        self.chain = self.prompt | self.llm

    def query(self, question: str, search_results: str) -> str:
        self.logger.info(f"🔎 Querying OpenAI with question: '{question}'")
        try:
            response = self.chain.invoke({"question": question, "search_results": search_results})
            self.logger.info(f"✅ Response received from OpenAI: {response.content}")
            return response.content
        except Exception as e:
            self.logger.error(f"❌ OpenAI query failed: {str(e)}")
            return "An error occurred while querying OpenAI."


class LocalLLMRepository(IRepository, LLM):
    base_url: str = "http://localhost:8000"
    
    def __init__(self, base_url: str = "http://localhost:8000", logger: logging.Logger = None):
        super().__init__()
        self.base_url = base_url
        self.logger = logger or logging.getLogger(__name__)

    def query(self, question: str, search_results: str) -> str:
        prompt = f"Question: {question}\n{search_results}\nAnswer concisely with references if available."
        self.logger.info(f"🔎 Querying Local LLM at {self.base_url} with prompt: '{prompt}'")
        return self._call(prompt)
    
    def _call(self, prompt: str, stop: Optional[list[str]] = None) -> str:
        payload = {"question": prompt}
        try:
            response = requests.post(
                f"{self.base_url}/generate",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 200:
                self.logger.info("✅ Local LLM returned a successful response.")
                return response.json().get("answer", "No answer found.")
            elif response.status_code == 422:
                self.logger.warning("⚠️ Validation error. Check the format of the payload.")
                self.logger.debug(f"Request payload: {payload}")
                self.logger.debug(f"Response: {response.text}")
                return "Error: Invalid request format"
            else:
                self.logger.error(f"❌ Error {response.status_code}: {response.text}")
                return f"Error: {response.status_code} - {response.text}"
        except requests.exceptions.RequestException as e:
            self.logger.critical(f"🔥 Request to Local LLM failed: {str(e)}")
            return f"Request failed: {str(e)}"

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        return {"base_url": self.base_url}
    
    @property
    def _llm_type(self) -> str:
        return "local_llm_repository"


class DDGSearchRepository(ISearchRepository):
    def __init__(self, logger: logging.Logger = None):
        self.search = DuckDuckGoSearchResults()
        self.logger = logger or logging.getLogger(__name__)

    def web_search(self, query: str) -> str:
        self.logger.info(f"🔎 Performing web search for: '{query}'")
        try:
            search_results = self.search.run(query)
            if search_results:
                self.logger.info(f"✅ Search results found: {search_results}")
                return search_results
            else:
                self.logger.warning("⚠️ No search results found.")
                return "No search results found."
        except Exception as e:
            self.logger.error(f"❌ Web search failed: {str(e)}")
            return "An error occurred during the web search."
