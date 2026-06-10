import os
import chromadb
from chromadb.utils import embedding_functions

# import the chunk loader
from chunk_builder import load_and_validate_chunks

def build_vector_store(cleaned_dir: str, db_path: str = "./chroma_db"):
    print("loading chunks and metadata from disk")
    # <--- CATCH BOTH LISTS HERE
    chunks, metadatas = load_and_validate_chunks(cleaned_dir) 
    
    if not chunks:
        print("error: no chunks found. aborting.")
        return

    # setup chroma to save locally so we don't have to re-embed every time we run the app
    print(f"setting up chroma db at {db_path}")
    client = chromadb.PersistentClient(path=db_path)
    
    # load the sentence transformer model (might take a sec to download on the first run)
    print("loading the embedding model")
    emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    
    # create the collection or grab it 
    collection = client.get_or_create_collection(
        name="kean_cs_professors",
        embedding_function=emb_fn
    )
    
    # chroma needs string ids for everything, so just number them sequentially
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    
    # shove everything into the db
    print("embedding and adding chunks")
    collection.add(
        documents=chunks,
        ids=ids,
        metadatas=metadatas  # <--- ADD METADATAS HERE
    )
    
    # sanity check to make sure they all actually saved
    stored_count = collection.count()
    print("=" * 60)
    print(f"done! total chunks saved in db: {stored_count}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # build the absolute path to data/cleaned
    cleaned_directory = os.path.join(base_dir, "data", "cleaned")
    build_vector_store(cleaned_directory)