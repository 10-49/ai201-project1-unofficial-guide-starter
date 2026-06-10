import chromadb
from chromadb.utils import embedding_functions

def query_database(question: str, db_path: str = "./chroma_db", top_k: int = 5):
    # point to the local database we built in the last script
    client = chromadb.PersistentClient(path=db_path)
    
    # load the exact same embedding model we used to save the chunks
    # so the math matches up when it searches
    emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    
    # grab the collection
    collection = client.get_collection(
        name="kean_cs_professors",
        embedding_function=emb_fn
    )
    
    # run the actual semantic search
    # chroma embeds our question and finds the closest matches
    print(f"\n--- searching for: '{question}' ---")
    results = collection.query(
        query_texts=[question],
        n_results=top_k
    )
    
    # unpack the results. chroma returns arrays inside arrays
    documents = results['documents'][0]
    metadatas = results['metadatas'][0]
    distances = results['distances'][0]
    
    # print everything out clearly so we can check if it worked
    for i in range(len(documents)):
        print(f"\n[Result {i+1}]")
        print(f"Source: {metadatas[i].get('source', 'Unknown')}")
        print(f"Distance Score: {distances[i]:.4f}")
        print(f"Text: {documents[i]}")
        print("-" * 50)

if __name__ == "__main__":
    # here are the specific questions from our planning.md evaluation section
    
    q1 = "Which professor is known for making students copy code without explaining the underlying concepts?"
    q2 = "What is the common consensus on Daehan Kwak's exams and study materials?"
    q3 = "Does Professor Subramanian curve grades for CPS2231?"
    
    # test them one by one
    query_database(q1)
    query_database(q2)
    query_database(q3)