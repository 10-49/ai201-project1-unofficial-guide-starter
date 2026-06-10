import os
import re

def extract_profile_summary(raw_text: str) -> str:
    lines = [line.strip() for line in raw_text.strip().split('\n') if line.strip()]
    
    try:
        overall_rating = lines[0]
        # skip lines to find what we need
        prof_name = lines[3]
        
        # regex or index for percentage and difficulty
        would_take_again = "N/A"
        difficulty = "N/A"
        for i, line in enumerate(lines):
            if "Would take again" in line:
                would_take_again = lines[i-1]
            if "Level of Difficulty" in line:
                difficulty = lines[i-1]
                break

        # compress into a single summary chunk
        summary_chunk = (
            f"Professor: {prof_name} | "
            f"Type: Profile Summary | "
            f"Overall Rating: {overall_rating} | "
            f"Difficulty: {difficulty} | "
            f"Would Take Again: {would_take_again}"
        )
        return summary_chunk
        
    except IndexError:
        return "Error parsing header."

def parse_rmp_reviews(raw_text: str, professor_name: str) -> list[str]:
    """
    parses raw RateMyProfessor text and formats it for RAG ingestion.
    """
    # clean out empty lines to standardize the index
    lines = [line.strip() for line in raw_text.strip().split('\n') if line.strip()]
    formatted_reviews = []
    
    i = 0
    while i < len(lines):
        # 'Quality' is the start delimiter for a new review block
        if lines[i] == "Quality":
            try:
                rating = lines[i+1]
                difficulty = lines[i+3] # Skip the literal string 'Difficulty'
                course = lines[i+4]
                date = lines[i+5]
                
                # advance index
                i += 6
                
                # extract variable metadata (Credit, Attendance, Grade, etc.)
                metadata = {}
                while i < len(lines) and ":" in lines[i]:
                    key, val = lines[i].split(":", 1)
                    metadata[key.strip()] = val.strip()
                    i += 1
                    
                # extract review body. stop when hitting the 'Helpful' UI anchor.
                review_lines = []
                while i < len(lines) and lines[i] != "Helpful" and not lines[i].startswith("Reviewed:"):
                    review_lines.append(lines[i])
                    i += 1
                
                #Ratemyprofessor appends tags to the bottom of the review text
                #tag handling
                RMP_TAGS = [
                "Tough grader", "Lots of homework", "Lecture heavy", "Test heavy", 
                "Graded by few things", "Get ready to read", "Participation matters", 
                "EXTRA CREDIT", "Amazing lectures", "Clear grading criteria", 
                "Inspirational", "Hilarious", "Accessible outside class", "Caring", 
                "Respected", "Skip class? You won't pass.", "Gives good feedback", 
                "Group projects"
                ]

                def is_tag_line(text: str) -> bool:
                    """Evaluates if a string is a categorical tag array or a narrative review."""
                    # 1. Check for the CamelCase smash (e.g., "homeworkLecture")
                    if re.search(r"[a-z][A-Z]", text):
                        return True
                    # 2. Check for an exact match with a single known tag
                    if text in RMP_TAGS:
                        return True
                    return False

                if len(review_lines) > 1:
                    review_text = " ".join(review_lines[:-1])  # Exclude the last line which is a tag
                    raw_tags = review_lines[-1]
                    
                    #utilize regex to split smashed tags 'Tough graderLots of homework' 
                    # 1. Fix the ALL-CAPS boundary specific to "EXTRA CREDIT"
                    cleaned_tags = re.sub(r"(EXTRA CREDIT)([A-Z])", r"\1, \2", raw_tags)

                    # 2. fix the standard lowercase-to-uppercase CamelCase boundary
                    cleaned_tags = re.sub(r"([a-z])([A-Z])", r"\1, \2", cleaned_tags)

                elif len(review_lines) == 1:
                    #edge case: one line, either a review or tag occupying the slot
                    line = review_lines[0]
                    if is_tag_line(line):
                        cleaned_tags = line
                        review_text = "No review text provided."
                        cleaned_tags = re.sub(r"([a-z])([A-Z])", r"\1, \2", cleaned_tags)
                    else:
                        review_text = line
                        cleaned_tags = ""
                else:
                    review_text = "No review text provided."
                    cleaned_tags = ""
                    
                # format into the strict string required for chunking and context
                grade = metadata.get("Grade", "N/A")
                final_string = (
                    f"Professor: {professor_name} | "
                    f"Course: {course} | "
                    f"Rating: {rating} | "
                    f"Difficulty: {difficulty} | "
                    f"Grade: {grade} | "
                    f"Tags: {cleaned_tags} | "
                    f"Review: {review_text}"
                )
                
                formatted_reviews.append(final_string)
                
            except IndexError:
                # truncated or malformed block at the end of the file
                break
        i += 1
        
    return formatted_reviews

# Example Execution
if __name__ == "__main__":
    dir = os.path.dirname(os.path.realpath(__file__))
    with open(r"ai201-project1-unofficial-guide-starter\data\raw\prof_name.txt", "r", encoding="utf-8") as f:
        raw_data = f.read()


    cleaned_data = parse_rmp_reviews(raw_data, "name")
    summary_chunk = extract_profile_summary(raw_data)

    print(summary_chunk)
    print(" " * 50)
    for review in cleaned_data:
        print(review)
        print(" " * 50)