from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings.huggingface import HuggingFaceInstructEmbeddings
from services.configuration import get_settings
from sklearn.cluster import KMeans
from langchain.schema import Document
import numpy as np


def create_embeddings(documents: list[Document]) -> list[list[float]]:
    """Creates an instance of an embedding model and embeds the documents.If you have a ``OpenAI_API_KEY`` as an env variable, it will use the OpenAIEmbeddings model, otherwise it will use the HuggingFaceInstructEmbeddings model.Specifically the ``hkunlp/instructor-xl`` model.

    Parameters:

    - ``documents``: A list of langchain´s Document object to embed.

    Returns:

    ``embeddings``: A list of lists of floats, where each list of floats is the embedding of a document.

    Raises:

    - ``ValueError``: If the ``OPENAI_API_KEY`` is not set as an env variable or the ``HUGGINGFACEHUB_API_TOKEN`` env variable is not set.
    """
    try:
        settings = get_settings()
        if settings.OPENAI_API_KEY != None:
            embedding = OpenAIEmbeddings(
                openai_api_key=settings.OPENAI_API_KEY)
        else:
            embedding = HuggingFaceInstructEmbeddings(
                model_name="hkunlp/instructor-xl")
        embeddings = embedding.embed_documents(
            [d.page_content for d in documents])
        return embeddings
    except ValueError:
        raise ValueError(
            "You need to set the OPENAI_API_KEY as an env variable or have a HUGGINGFACEHUB_API_TOKEN.")


def cluster_embeddings(embeddings: list[list[float]], num_clusters: int) -> KMeans:
    """Clusters the embeddings using the KMeans algorithm.

    Parameters:
    - ``embeddings``: A list of lists of floats, where each list of floats is the embedding of a document.
    - ``num_clusters``: The number of clusters to create.

    Returns:
    - ``k_means``: A KMeans sklearn object that has been fitted to the embeddings.

    Raises:
    - ``Exception``: If the number of clusters is greater than the number of embeddings.
    """
    try:
        k_means = KMeans(n_clusters=num_clusters).fit(embeddings)
        return k_means
    except Exception:
        raise Exception(
            "The number of clusters is greater than the number of embeddings.")


def get_documents_by_index(indexes: list[int], docs: list[Document]) -> list[Document]:
    """Returns a list of documents picked from the documents provided by the given a list of indexes.

    Parameters

    - ``indexes``: A list of integers that represent the indexes of the documents to pick.

    - ``docs``: A list of langchain´s Document object to pick from.

    Returns

    ``selected_docs``: A list of langchain´s Document object that were picked from the documents provided.

    Raises

    ``IndexError``: If the index is out of range.
    """
    try:
        selected_docs = [docs[doc] for doc in indexes]
        return selected_docs
    except IndexError:
        raise IndexError("The index is out of range.")


def get_relevant_documents_indexes(embeddings: list[list[float]], num_clusters: int):
    """Returns a list of indexes of the documents that are closest to the centroids of the clusters.

    Parameters

    - ``embeddings``: A list of lists of floats, where each list of floats is the embedding of a document.

    - ``num_clusters``: The number of clusters to create.

    Returns

    ``sorted_indices``: A list of integers that represent the indexes of the documents that are closest to the centroids of the clusters.

    Raises

    ``Exception``: If the number of clusters is greater than the number of embeddings.
    """
    try:
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
    except Exception:
        raise Exception(
            "The number of clusters is greater than the number of embeddings.")
