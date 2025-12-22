from .utils import OpenAIClient, get_timestamp, generate_id, gpt_user_profile_analysis, gpt_knowledge_extraction, ensure_directory_exists
from utils import OpenAIClient, get_timestamp, generate_id, gpt_user_profile_analysis, gpt_knowledge_extraction, ensure_directory_exists

def task_knowledge_extraction():
                    print("Memoryos: Starting parallel knowledge extraction...")
                    return gpt_knowledge_extraction(unanalyzed_pages, self.client, model=self.llm_model)