import asyncio
import os

from functools import partial
from enum import Enum
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from huggingface_hub import InferenceClient


class LLMProvider(Enum):
    OPENAI = "openai"
    HUGGINGFACE = "huggingface"


class LanguageModelsService:
    """Service to interact with different LLM providers for text summarization."""
    def __init__(self):
        provider = os.getenv("LLM_PROVIDER", "huggingface").lower()
        self.provider = LLMProvider(provider)
        self.model_name = "facebook/bart-large-cnn"
        self.client = InferenceClient(
            api_key=os.getenv("HF_TOKEN"),
            model=self.model_name,
        )
        # TODO read language from domain to choose model accordingly
        # TODO using langchain.llm to manage different providers
        # if self.provider == LLMProvider.OPENAI:
        #     self.llm = ChatOpenAI(
        #         temperature=0,
        #         model_name="gpt-3.5-turbo"
        #     )
        # else:  # HUGGINGFACE
        #     # repo_ptbr = 'neuralmind/bert-base-portuguese-cased'
        #     self.llm = HuggingFaceEndpoint(
        #         repo_id="openai/gpt-oss-20b:groq",
        #         temperature=0.1,
        #         max_new_tokens=512,
        #         huggingfacehub_api_token=os.getenv("HF_TOKEN")
        #     )

    async def summarize_chunk(self, doc):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            partial(self.client.summarization, doc.page_content, truncation='do_not_truncate')
        )

    async def generate_summary(self, text: str, words_limit: int) -> str:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100
        )
        docs = [Document(page_content=text)]
        split_docs = text_splitter.split_documents(docs)

        # For shorter documents, summarize directly
        if len(split_docs) == 1:
                prompt = f"Write a concise summary in approximately {words_limit} words:\n\n{split_docs[0].page_content}"
                response = self.client.summarization(prompt, truncation='do_not_truncate')
                return response.summary_text
        else:
            # Summarize each chunk asynchronously
            tasks = [self.summarize_chunk(doc) for doc in split_docs[:10]]  # Limit to first 10 chunks for performance
            summaries = await asyncio.gather(*tasks)
            chunk_summaries = [s.summary_text for s in summaries]

            # Combine and create final summary
            combined = "\n\n".join(chunk_summaries)
            final_response = self.client.summarization(
                combined,
                truncation='do_not_truncate'
            )
            while len(final_response.summary_text.split()) > words_limit:
                print("Final summary too long, re-summarizing...")
                final_response = self.client.summarization(
                    final_response.summary_text,
                    truncation='only_first'
                )
            return final_response.summary_text
