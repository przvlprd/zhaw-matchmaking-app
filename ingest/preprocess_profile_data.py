import re


def preprocess_profile(raw_data: str):
    # Remove all obsolete whitespace
    cleaned_str = re.sub(r'\s+', ' ', raw_data)

    # Remove the final "Zurück" in every profile
    cleaned_str = cleaned_str.replace('Zurück', '')

    # Insert whitespace between numbers and letters
    # (when they got lost from the original html)
    pattern = r'([a-zA-Z])(\d)'
    cleaned_str = re.sub(pattern, r'\1 \2', cleaned_str)

    return cleaned_str
