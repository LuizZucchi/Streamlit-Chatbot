import logging
from repository import IRepository, ISearchRepository

class ChatService:
    def __init__(self, llm_repo: IRepository, search_repo: ISearchRepository, logger: logging.Logger = None):
        self.llm_repo = llm_repo
        self.search_repo = search_repo
        self.logger = logger or logging.getLogger(__name__)

    def ask_question(self, question: str, perform_search: bool = False) -> str:
        search_results = ""
        
        if perform_search:
            self.logger.info(f"🔎 Performing web search for: '{question}'")
            search_results = self.search_repo.web_search(question)
            if search_results:
                self.logger.info(f"Search results found: {search_results}")
            else:
                self.logger.warning("No search results found.")
        
        self.logger.info(f"🤖 Generating response with LLM for question: '{question}'")
        response = self.llm_repo.query(question, search_results)
        
        self.logger.info(f"✅ Response received: {response}")
        
        return response
