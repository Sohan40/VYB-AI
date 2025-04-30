from langchain_openai import AzureChatOpenAI

class LLMClient:
    def __init__(self, endpoint, api_key, deployment_name, api_version="2024-02-01"):
        self.llm = AzureChatOpenAI(
            azure_endpoint=endpoint,
            api_key=api_key,
            deployment_name=deployment_name,
            openai_api_version=api_version
        )

    def invoke(self, prompt: str):
        return self.llm.invoke(prompt)
