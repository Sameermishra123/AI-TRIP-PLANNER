import os
from dotenv import load_dotenv
from typing import Literal, Optional, Any
from pydantic import BaseModel, Field
from utils.config_loader import load_config
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

# Load environment variables from .env
load_dotenv()

class ConfigLoader:
    """Load configuration from a file or dict."""
    def __init__(self):
        print("Loaded config...")
        self.config = load_config()
    
    def __getitem__(self, key):
        return self.config[key]

class ModelLoader(BaseModel):
    model_provider: Literal["groq", "openai"] = "groq"
    config: Optional[ConfigLoader] = Field(default=None, exclude=True)

    def model_post_init(self, __context: Any) -> None:
        # Initialize config after model creation
        self.config = ConfigLoader()

    class Config:
        arbitrary_types_allowed = True

    def load_llm(self, model_name: Optional[str] = None):
        """
        Load and return the LLM model.
        If model_name is provided, it overrides the config default.
        """
        print("LLM loading...")
        print(f"Loading model from provider: {self.model_provider}")

        if self.model_provider == "groq":
            print("Loading LLM from Groq...")
            groq_api_key = os.getenv("GROQ_API_KEY")
            if groq_api_key is None:
                raise ValueError("GROQ_API_KEY not found in environment variables!")

            # Use provided model_name or fallback to config
            if model_name is None:
                model_name = self.config["llm"]["groq"]["model_name"]
            
            llm = ChatGroq(model=model_name, api_key=groq_api_key)

        elif self.model_provider == "openai":
            print("Loading LLM from OpenAI...")
            openai_api_key = os.getenv("OPENAI_API_KEY")
            if openai_api_key is None:
                raise ValueError("OPENAI_API_KEY not found in environment variables!")

            if model_name is None:
                model_name = self.config["llm"]["openai"]["model_name"]
            
            llm = ChatOpenAI(model_name=model_name, api_key=openai_api_key)

        else:
            raise ValueError(f"Unsupported model provider: {self.model_provider}")

        print(f"LLM loaded successfully: {model_name}")
        return llm
