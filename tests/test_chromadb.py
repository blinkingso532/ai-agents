"""Vector Database > ChromaDB"""

import chromadb
import asyncio

from chromadb.api import AsyncClientAPI


async def get_client() -> AsyncClientAPI:
    return await chromadb.AsyncHttpClient(host="localhost", port=8853)


async def main():
    client = await get_client()
    collection = await client.get_or_create_collection(name="readme_collection")
    await collection.add(documents=["hello world"], ids=["readme01"])


# asyncio.run(main())

client = chromadb.HttpClient(host="localhost", port=8853)
collection = client.get_or_create_collection(name="readme_collection")

from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
import os
from datetime import datetime
from dotenv import load_dotenv

if not load_dotenv():
    print("Failed to load dotenv file")


openai_embedding_function = OpenAIEmbeddingFunction(
    api_base=os.getenv("DASHSCOPE_BASE_URL"),
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model_name="text-embedding-v3",
    dimensions=1024,
)


def test_custom_embedding_function():
    """Customer embedding function"""
    my_collection = client.get_or_create_collection(
        name="my_collection",
        embedding_function=openai_embedding_function,
        metadata={
            "description": "A collection of documents with custom embeddings",
            "created": str(datetime.now()),
        },
    )
    my_collection.add(documents=["hello world"], ids=["my01"])
    print(my_collection.get())


test_custom_embedding_function()
