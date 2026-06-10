import os
import random

#slight logic change: i was wrong, 
#there were not empty lines between each chunk but instead 
#a large line of spaces. as a temp workaround
#we filter for the word Professor which starts each chunk entry anyway.
#this is another oversight and can be addressed in the future.

import os
import random

def load_and_validate_chunks(cleaned_dir: str):
    all_chunks = []
    all_metadatas = [] # <--- NEW: Array to hold the metadata dictionaries
    
    for filename in os.listdir(cleaned_dir):
        if filename.endswith(".txt"):
            filepath = os.path.join(cleaned_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                
                lines = content.split('\n')
                
                for line in lines:
                    if line.strip().startswith("Professor:"):
                        all_chunks.append(line.strip())
                        # <--- NEW: Map the exact filename to this specific chunk
                        all_metadatas.append({"source": filename}) 
                        
    return all_chunks, all_metadatas # Return both lists

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # build the absolute path to data/cleaned
    cleaned_directory = os.path.join(base_dir, "data", "cleaned")
    chunks, metadatas = load_and_validate_chunks(cleaned_directory)

    total_chunks = len(chunks)
    print(f"Total chunks loaded: {total_chunks}")
    print("=" * 60)
    
    if total_chunks >= 5:
        sample_chunks = random.sample(chunks, 5)
        for i, chunk in enumerate(sample_chunks):
            print(f"Sample {i+1}:\n{chunk}")
            print("-" * 60)
    else:
        print("Error: Insufficient chunks generated.")