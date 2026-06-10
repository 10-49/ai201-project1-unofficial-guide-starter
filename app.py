import os
import chromadb
from chromadb.utils import embedding_functions
from groq import Groq
from dotenv import load_dotenv

# load environment variables from our hidden .env file
load_dotenv()

def run_rag_pipeline(question: str, db_path: str = "./chroma_db", top_k: int = 4):
    # 1. connect to our local vector database
    client = chromadb.PersistentClient(path=db_path)
    emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    collection = client.get_collection(
        name="kean_cs_professors",
        embedding_function=emb_fn
    )
    
    # 2. query the vector database for relevant chunks
    results = collection.query(
        query_texts=[question],
        n_results=top_k
    )
    
    retrieved_docs = results['documents'][0]
    retrieved_metadatas = results['metadatas'][0]
    
    # gather unique source filenames to append at the very end
    sources = list(set([meta.get('source', 'Unknown') for meta in retrieved_metadatas]))
    
    # 3. compile the chunks into a single context string for the llm
    context = "\n\n".join(retrieved_docs)
    
    # 4. set up the rigid grounding system prompt
    system_prompt = (
        "You are an assistant that answers questions about professors using ONLY the provided text context.\n"
        "Strict rules:\n"
        "1. Answer the question using ONLY the facts explicitly mentioned in the context.\n"
        "2. Do NOT use any outside training knowledge or make assumptions.\n"
        "3. If the context does not contain enough concrete information to fully answer, say exactly: "
        "'I do not have enough information in my database to answer this.'\n"
        "4. Keep your answer brief, factual, and direct."
    )
    
    user_prompt = f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
    
    # 5. initialize groq client and send payload
    groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    completion = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.0 # zero means deterministic, no creative guessing
    )
    
    answer = completion.choices[0].message.content
    
    # if the model admitted it doesn't know, we don't list sources
    if "I do not have enough information" in answer:
        sources = []
        
    return {
        "answer": answer,
        "sources": sources
    }

if __name__ == "__main__":
    # simple interactive command line interface loop
    print("=" * 60)
    # quick check to ensure key loaded properly
    if not os.getenv("GROQ_API_KEY"):
        print("error: GROQ_API_KEY is missing from your .env file.")
        exit(1)
        
    print("kean cs professor rag interface active.")
    print("type 'exit' or 'quit' to close the program.")
    print("=" * 60)
    
    while True:
        user_input = input("\nAsk a question: ").strip()
        if user_input.lower() in ['exit', 'quit']:
            print("closing pipeline.")
            break
            
        if not user_input:
            continue
            
        print("searching database and generating grounded answer...")
        output = run_rag_pipeline(user_input)
        
        print("\nAnswer:")
        print(output["answer"])
        
        if output["sources"]:
            print("\nRetrieved From:")
            for source in output["sources"]:
                print(f" - {source}")
        print("-" * 60)