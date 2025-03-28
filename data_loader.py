import pandas as pd
from pathlib import Path

def load_ptbxl_data(data_dir=None):
    """
    Load PTB-XL dataset CSV files from the specified directory.
    
    Parameters:
        data_dir (str or Path, optional): Path to the folder containing ptbxl_database.csv and scp_statements.csv.
                                          If not provided, uses the default path.
    
    Returns:
        tuple: (ptbxl_df, scp_df) DataFrames if load is successful, or (None, None) if an error occurred.
    """
    # Default data directory if not provided
    if data_dir is None:
        data_dir = r"C:\Users\ben azulay\Desktop\ecg_project\data\ptbxl"

    data_path = Path(data_dir)
    
    # Check if the data directory exists
    if not data_path.is_dir():
        print(f"Error: Directory '{data_path}' not found.")
        return None, None

    # Define expected file paths
    ptbxl_file = data_path / "ptbxl_database.csv"
    scp_file   = data_path / "scp_statements.csv"

    # Check existence of files
    if not ptbxl_file.is_file():
        print(f"Error: File not found: {ptbxl_file.name} in directory '{data_path}'.")
        return None, None
    if not scp_file.is_file():
        print(f"Error: File not found: {scp_file.name} in directory '{data_path}'.")
        return None, None

    # Try loading ptbxl_database.csv
    try:
        ptbxl_df = pd.read_csv(ptbxl_file)
    except Exception as e:
        print(f"Error: Failed to read '{ptbxl_file.name}'. Exception: {e}")
        return None, None

    # Try loading scp_statements.csv
    try:
        scp_df = pd.read_csv(scp_file, index_col=0)
    except Exception as e:
        print(f"Error: Failed to read '{scp_file.name}'. Exception: {e}")
        return None, None

    # Validate structure of ptbxl_database.csv (required columns)
    required_ptbxl_cols = {"ecg_id", "scp_codes"}
    missing_ptbxl_cols = required_ptbxl_cols - set(ptbxl_df.columns)
    if missing_ptbxl_cols:
        print(f"Error: `{ptbxl_file.name}` is missing required columns: {', '.join(missing_ptbxl_cols)}.")
        return None, None

    # Validate structure of scp_statements.csv (required columns)
    required_scp_cols = {"description", "diagnostic_class"}
    missing_scp_cols = required_scp_cols - set(scp_df.columns)
    if missing_scp_cols:
        print(f"Error: `{scp_file.name}` is missing required columns: {', '.join(missing_scp_cols)}.")
        return None, None

    # If we reach here, data loaded successfully
    print(f"PTB-XL data loaded successfully. Records: {len(ptbxl_df)} ECGs, {len(scp_df)} SCP statements.")
    return ptbxl_df, scp_df

# Example usage (No need to pass data_dir as it's defaulted)
# ptbxl_df, scp_df = load_ptbxl_data()
