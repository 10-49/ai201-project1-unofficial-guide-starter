import os
import random

#slight logic change: i was wrong, 
#there were not empty lines between each chunk but instead 
#a large line of spaces. as a temp workaround
#we filter for the word Professor which starts each chunk entry anyway.
#this is another oversight and can be addressed in the future.

def load_and_validate_chunks(cleaned_dir: str) -> list[str]:
    all_chunks = []
    
    for filename in os.listdir(cleaned_dir):
        if filename.endswith(".txt"):
            filepath = os.path.join(cleaned_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                
                # Split by standard newlines
                lines = content.split('\n')
                
                # Filter: Keep only the lines that contain actual review data
                # This guarantees zero empty fragments and zero concatenated files
                file_chunks = [line.strip() for line in lines if line.strip().startswith("Professor:")]
                all_chunks.extend(file_chunks)
    
    return all_chunks

if __name__ == "__main__":
    cleaned_directory = "ai201-project1-unofficial-guide-starter/data/cleaned" 
    chunks = load_and_validate_chunks(cleaned_directory)
    
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