import json
import os
import pandas as pd

def extract_chunk_texts(input_json_file):
    # Read the JSON file
    with open(input_json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Extract chunkText objects
    chunk_texts = []
    
    def find_chunk_texts(obj):
        if isinstance(obj, dict):
            if 'chunkText' in obj and isinstance(obj['chunkText'], str):
                chunk_texts.append(obj['chunkText'])
            
            for value in obj.values():
                find_chunk_texts(value)
        
        elif isinstance(obj, list):
            for item in obj:
                find_chunk_texts(item)
    
    # Start the recursive search
    find_chunk_texts(data)
    
    # Create DataFrame
    df = pd.DataFrame({'ChunkText': chunk_texts})
    
    # Generate output filename
    base_filename = os.path.splitext(input_json_file)[0]
    output_excel = f"{base_filename}_chunk_texts.xlsx"
    
    # Write to Excel
    df.to_excel(output_excel, index=False)
    
    print(f"Total chunk texts extracted: {len(chunk_texts)}")
    print(f"Excel file saved as: {output_excel}")
    
    return df

# List JSON files in current directory
json_files = [f for f in os.listdir('.') if f.endswith('.json')]
print("Available JSON files:", json_files)

# Example usage (modify the filename as needed)
# Replace 'your_file.json' with the actual filename
df = extract_chunk_texts('elmodata.json')

# Optional: Display first few rows
print(df.head())