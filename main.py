import os
import logging
from enum import Enum, auto

from service import ChatService
from repository import OpenAIRepository, LocalLLMRepository, DDGSearchRepository

logging.basicConfig(level=logging.ERROR, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

class LLMType(Enum):
    OPENAI = auto()
    LOCAL = auto()

class ChatCLI:
    def __init__(self):
        self.service = None
        self.llm_type = None
        self.search_repo = DDGSearchRepository()
        
    def configure_llm(self):
        print("\n=== LLM Configuration ===")
        print("1. OpenAI")
        print("2. Local LLM")
        print("3. Back to main menu")
        
        choice = input("Select LLM provider: ").strip()
        
        if choice == "1":
            api_key = os.environ.get("OPENAI_API_KEY")
            if not api_key:
                api_key = input("Enter OpenAI API key: ").strip()
                os.environ["OPENAI_API_KEY"] = api_key
            self.llm_type = LLMType.OPENAI
            self.service = ChatService(OpenAIRepository(), self.search_repo, logger=logger)
            print("OpenAI configured successfully!")
        elif choice == "2":
            base_url = input("Enter Local LLM base URL [http://localhost:8000]: ").strip() or "http://localhost:8000"
            self.llm_type = LLMType.LOCAL
            self.service = ChatService(LocalLLMRepository(base_url=base_url), self.search_repo, logger=logger)
            print(f"Local LLM configured at {base_url}!")
        elif choice == "3":
            return
        else:
            print("Invalid selection. Please try again.")
            self.configure_llm()
    
    def chat_loop(self):
        if not self.service:
            print("LLM not configured. Please configure first.")
            self.configure_llm()
            if not self.service:
                return
                
        print("\n=== Chat Mode ===")
        print("Type 'menu' to return to configuration")
        print("Type 'exit' to quit\n")
        
        while True:
            question = input("Ask me anything: ").strip()
            
            if question.lower() == 'exit':
                return True  # Signal to exit completely
            elif question.lower() == 'menu':
                return False  # Signal to return to menu
                
            search_toggle = input("Perform web search? (y/n): ").strip().lower() == 'y'
            response = self.service.ask_question(question, perform_search=search_toggle)
            print(f"\nAssistant:\n{response}\n")

    def run(self):
        print("=== AI Assistant CLI ===")
        print("Configure your LLM provider first\n")
        
        self.configure_llm()
        
        while True:
            should_exit = self.chat_loop()
            if should_exit:
                print("Goodbye!")
                break
                
            # If we get here, user selected 'menu'
            print("\nReturning to main menu...")
            self.configure_llm()

def main():
    cli = ChatCLI()
    cli.run()

if __name__ == "__main__":
    main()