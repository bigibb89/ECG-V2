def provide_explanation(selected_answer, correct_answer, ecg_id, scp_data):
    """
    Provide a detailed explanation for the selected answer.

    Parameters:
        selected_answer (str): The answer selected by the user.
        correct_answer (str): The correct diagnosis.
        ecg_id (str): The ECG record ID.
        scp_data (DataFrame): DataFrame containing the SCP statements dataset.

    Returns:
        str: A detailed explanation for the selected answer.
    """

    # Step 1: Check if the selected answer is correct
    if selected_answer == correct_answer:
        explanation = f"Correct! ECG {ecg_id} shows {correct_answer}. This is the most suitable diagnosis."
    else:
        explanation = f"Incorrect. ECG {ecg_id} actually shows {correct_answer}. Here's why:\n"
        explanation += f"The correct diagnosis was {correct_answer} because it matches the key features in the ECG pattern."

    # Step 2: Add detailed clinical explanation from the SCP dataset
    try:
        row = scp_data[scp_data['description'] == correct_answer].iloc[0]
        explanation += f"\nDescription from SCP: {row['description']}"
    except IndexError:
        explanation += "\nNote: No matching description found in SCP data."

    # Step 3: Return the explanation
    return explanation
