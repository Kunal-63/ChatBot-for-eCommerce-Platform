import spacy

# Load the SpaCy English model
nlp = spacy.load("en_core_web_sm")

def parse_user_prompt(prompt):
    # Define a dictionary to store extracted entities
    extracted_info = {
        'category': None,
        'lower_price_limit': None,
        'upper_price_limit': None
    }

    # Process the user prompt using SpaCy
    doc = nlp(prompt.lower())

    # Extract nouns from the prompt
    nouns = [token.text for token in doc if token.pos_ == 'NOUN']
    print("Nouns:", nouns)

    # Check if any of the extracted nouns match known categories
    categories = [
        't-shirts', 'shirts', 'hoodies', 'jeans', 'trousers', 
        'blazers', 'jackets', 'suits', 'shorts', 'shoes', 
        'bags', 'accessories', 'perfumes', 'beauty', 
        'polo', 'overshirts', 'swimwear'
    ]
    for noun in nouns:
        if noun in categories:
            extracted_info['category'] = noun
            break

    # Extract price limits
    for token in doc:
        if token.like_num and not extracted_info['lower_price_limit']:
            extracted_info['lower_price_limit'] = int(token.text)
        elif token.text == 'and':
            continue
        elif token.like_num:
            extracted_info['upper_price_limit'] = int(token.text)
            break

    return extracted_info

# Test the function
user_prompt = "Show me cool shirts less than 100 "
parsed_info = parse_user_prompt(user_prompt)
print(parsed_info)
