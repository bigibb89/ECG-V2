import random
import ast

def generate_question(ptbxl_data, scp_data):
    """
    Generate a random ECG question with multiple choices.

    Parameters:
        ptbxl_data (DataFrame): DataFrame containing the PTB-XL dataset.
        scp_data (DataFrame): DataFrame containing the SCP statements dataset.

    Returns:
        tuple: A tuple containing the question (str), list of options (list of str), and the correct answer (str).
    """
    # Step 1: Choose a random ECG record
    random_record = ptbxl_data.sample(1).iloc[0]
    ecg_id = random_record['ecg_id']
    scp_codes = ast.literal_eval(random_record['scp_codes'])  # Use ast.literal_eval for safety

    # Step 2: Find the main diagnosis from the SCP codes
    main_diagnosis_code = max(scp_codes, key=lambda code: scp_codes[code])
    
    # Step 3: Use scp_data with .loc since index is code
    if main_diagnosis_code in scp_data.index:
        main_diagnosis = scp_data.loc[main_diagnosis_code]['description']
    else:
        main_diagnosis = "Unknown Diagnosis"

    # Step 4: Generate distractors (wrong answers) from other descriptions
    descriptions = scp_data[scp_data.index != main_diagnosis_code]['description'].dropna().unique().tolist()
    distractors = random.sample(descriptions, min(3, len(descriptions)))

    # Step 5: Shuffle the options (including the correct one)
    options = [main_diagnosis] + distractors
    random.shuffle(options)

    # Step 6: Create the question
    question = f"What is the most suitable diagnosis for ECG {ecg_id}?"

    return question, options, main_diagnosis
