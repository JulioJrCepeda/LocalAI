import nltk as nltk
import fitz as fitz
import ast as ast
import numpy as np
import json as json

def count_sentences(text):
    # Tokenize the text into sentences
    sentences = nltk.sent_tokenize(text)
    # Return the number of sentences
    return len(sentences)

def get_sentences(text):
    # Tokenize the text into sentences
    sentences = nltk.sent_tokenize(text)
    # Return the number of sentences
    return sentences

def find_top_three(vector, memoryDict):

    vector_list = list(memoryDict.keys())

    # Convert the input list of tuples to a NumPy array
    vector_matrix = np.asarray(vector_list)
    
    # Check and reshape if necessary
    if vector_matrix.ndim == 1:
        vector_matrix = vector_matrix.reshape(1, -1)
    
    # Convert the input vector tuple to a NumPy array
    vector_np = np.array(vector)
    
    # Calculate the dot products
    dot_products = np.dot(vector_matrix, vector_np.T)
    
    # Calculate the absolute differences from 1
    differences = np.abs(dot_products - 1)
    
    # Find the indices of the top three closest values to 1
    top_three_indices = np.argsort(differences.flatten())[:3]
    
    # Extract the corresponding vectors

    closest_vectors = [vector_list[i] for i in top_three_indices]
    
    # Extract the corresponding strings form the vectors
    context = [memoryDict[vec] for vec in closest_vectors]
    
    return list_to_string(context)

def find_best_matches(vector, memoryDict):
    vector_list = list(memoryDict.keys())

    # Convert the input list of tuples to a NumPy array
    vector_matrix = np.asarray(vector_list)
    
    # Check and reshape if necessary
    if vector_matrix.ndim == 1:
        vector_matrix = vector_matrix.reshape(1, -1)
    
    # Convert the input vector tuple to a NumPy array
    vector_np = np.array(vector)
    
    # Calculate the dot products
    dot_products = np.dot(vector_matrix, vector_np.T)
    
    # Calculate the absolute differences from 1
    differences = np.abs(dot_products - 1)
    
    # Find the indices of the top three closest values to 1
    top_three_indices = np.argsort(differences.flatten())[:3]
    
    # Extract the corresponding vectors
    closest_vectors = [vector_list[i] for i in top_three_indices]
  
    return closest_vectors


def dot_product(vec1, vec2):
    if is_all_numbers(vec1) and is_all_numbers(vec2):
        return sum(float(a) * float(b) for a, b in zip(vec1, vec2))
    else:
        return 0.0

def is_all_numbers(lst):
    return all(isinstance(item, (int, float)) for item in lst)

def combine_lines(input_list, lines_per_group):
    # Initialize an empty list to store the combined strings
    combined_list = []
    
    # Iterate through the input list in chunks of 'lines_per_group'
    for i in range(0, len(input_list), lines_per_group):
        # Combine the current chunk into a single string
        combined_string = "\n".join(input_list[i:i + lines_per_group])
        # Append the combined string to the combined_list
        combined_list.append(combined_string)
    
    return combined_list

def list_to_string(lst):
    # Join the list items with a space separator
    return " ".join(lst)


def extract_text_from_pdf(pdf_path):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    text = ""

    # Iterate through each page
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        text += page.get_text()

    return text

def save_dict(dictionary, filename):
    # Convert the dictionary to a JSON-compatible format with string keys
    json_compatible_dict = {str(k): v for k, v in dictionary.items()}
    
    # Convert the dictionary to a JSON string
    json_string = json.dumps(json_compatible_dict, indent=4)
    
    # Write the JSON string to a text file
    with open(filename, 'w') as file:
        file.write(json_string)

def load_dict(filename):
    # Read the JSON string from the text file
    with open(filename, 'r') as file:
        json_string = file.read()
    
    if json_string:
        # Convert the JSON string back to a dictionary with string keys
        json_compatible_dict = json.loads(json_string)
        
        # Convert the string keys back to tuples
        original_dict = {ast.literal_eval(k): v for k, v in json_compatible_dict.items()}
        
        print(f"Dictionary loaded from {filename}")
        return original_dict
    return {}

def clean_up_memory(memoryDict, embedAI):
    currentDict = memoryDict.copy()
    keysToAddDict = {}

    for key in list(currentDict.keys()):
        if key in currentDict:
            value = currentDict[key]
            currentValue = remove_period_lines(value)
            currentDict[key] = currentValue
            
            if count_sentences(currentValue) < 3:
                tempDict = currentDict.copy()
                tempDict.pop(key, None)
                similarkeys = find_best_matches(key, tempDict)
                
                for similarkey in similarkeys:
                    if count_sentences(currentDict[similarkey]) < 15:
                        addedValue = currentDict[similarkey] + " " + currentValue
                        newKey = embedAI.runSingle(addedValue)
                        keysToAddDict[tuple(newKey)] = addedValue
                        currentDict.pop(similarkey, None)
                        currentDict.pop(key, None)
                        break

    currentDict.update(keysToAddDict)
    return currentDict

def simple_clean(memoryDict):
    currentDict = memoryDict
    
    for key, value in currentDict.items():
        newValue = remove_period_lines(value)
        currentDict[key] = newValue

    return currentDict


def remove_period_lines(text):
    # Split the text into lines
    lines = text.splitlines()
    
    # Filter out lines that consist solely of periods
    filtered_lines = [line for line in lines if line.strip() != "."]
    
    # Join the filtered lines back into a single string
    result = "\n".join(filtered_lines)
    
    return result

def ensure_parentheses(string):
    # Remove any leading or trailing whitespace
    string = string.strip()
    
    # Check if the string starts and ends with parentheses
    if (string.startswith("(") and string.endswith(")")):
       return True
    else:
        return False

