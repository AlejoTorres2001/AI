from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings.huggingface import HuggingFaceInstructEmbeddings
from services.configuration import get_settings
from sklearn.cluster import KMeans
from langchain.schema import Document
import numpy as np


def create_embeddings(documents: list[Document]) -> list[list[float]]:
    """Creates an instance of an embedding model and embeds the documents"""

    settings = get_settings()
    if settings.OPENAI_API_KEY != None:
        embedding = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)
    else:
        embedding = HuggingFaceInstructEmbeddings(
            model_name="hkunlp/instructor-xl")
    embeddings = embedding.embed_documents([d.page_content for d in documents])
    return embeddings


def cluster_embeddings(embeddings: list[list[float]], num_clusters: int):
    k_means = KMeans(n_clusters=num_clusters).fit(embeddings)
    return k_means


def get_documents_by_index(indexes: list[int], docs: list[Document]):
    selected_docs = [docs[doc] for doc in indexes]
    return selected_docs


def get_relevant_documents_indexes(embeddings: list[list[float]], num_clusters: int):
    # Find the closest embeddings to the centroids
    k_means = cluster_embeddings(embeddings, num_clusters)
# Create an empty list that will hold your closest points
    closest_indices = []

# Loop through the number of clusters you have
    for i in range(num_clusters):

        # Get the list of distances from that particular cluster center
        distances = np.linalg.norm(
            embeddings - k_means.cluster_centers_[i], axis=1)

        # Find the list position of the closest one (using argmin to find the smallest distance)
        closest_index = np.argmin(distances)

        # Append that position to your closest indices list
        closest_indices.append(closest_index)

    sorted_indices = sorted(closest_indices)
    return sorted_indices
