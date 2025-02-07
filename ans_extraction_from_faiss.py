from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from transformers import pipeline


class QueryEngine:
    def __init__(self, faiss_index_path="faiss_index"):
        self.faiss_index_path = faiss_index_path
        self.embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.load_vector_store()
        self.llm = pipeline("text-generation", model="gpt2")

    def load_vector_store(self):
        """
        Load FAISS vector store from the local path.
        """
        try:
            self.vector_store = FAISS.load_local(
                self.faiss_index_path,
                self.embeddings_model,
                allow_dangerous_deserialization=True
            )
            print("FAISS index loaded successfully.")
        except Exception as e:
            print(f"Error loading FAISS index: {e}")

    def query_and_generate_response(self, query: str, top_k: int = 5):
        """
        Perform semantic search and generate response using LLM.
        :param query: User query string.
        :param top_k: Number of top results to retrieve.
        :return: Generated response string.
        """
        try:
            # Perform search
            search_results = self.vector_store.similarity_search(query, k=top_k)

            if not search_results:
                return "No relevant information found."

            # Combine relevant text from search results
            context = " ".join([result.page_content for result in search_results])[:1024]
            prompt = f"Context: {context}\nUser Query: {query}\nAnswer:"

            # Generate response using LLM
            response = self.llm(prompt, max_new_tokens=100, num_return_sequences=1)
            print(response)
            # return response[0]["generated_text"]['Answer']
            return response[0]["generated_text"].split("Answer:")[-1].strip()

        except Exception as e:
            print(f"Error during query and response generation: {e}")
            return "An error occurred while processing the query."


def get_answer(query):
# if __name__ == "__main__":
#     # Initialize the query engine
    engine = QueryEngine()
#
#     # Example query
#     query = "What are the key points in the Akzo Nobel presentation?"
    answer = engine.query_and_generate_response(query)
    # print("Answer:", answer)
    return answer
