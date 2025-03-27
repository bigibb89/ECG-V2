import pandas as pd
import logging

# הגדרת לוגים
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/ecg_generator.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# טען את הנתונים מהקובץ הראשי
try:
    ptbxl_data = pd.read_csv("C:\\Users\\ben azulay\\Desktop\\ecg_project\\data\\ptbxl\\ptbxl_database.csv")
    logging.info("The main data file has been loaded successfully.")
except Exception as e:
    logging.error(f"Error loading the main data file: {e}")
    raise

# הסרת רווחים מיותרים בשם העמודות
ptbxl_data.columns = ptbxl_data.columns.str.strip()

# וודא שהעמודה 'filename_lr' קיימת בקובץ
if 'filename_lr' not in ptbxl_data.columns:
    logging.error("The 'filename_lr' column was not found in the file.")
else:
    logging.info("The 'filename_lr' column exists and is complete.")

# נוודא שהנתיב קיים
if not ptbxl_data['filename_lr'].isnull().any():
    logging.info("All 'filename_lr' data is complete.")
else:
    logging.warning("There are records where 'filename_lr' data is missing.")

# יצירת שאלה לדוגמה, בהנחה ששאר העמודות קיימות
def generate_quiz_entry(row, metadata):
    try:
        # לדוגמה, יצירת שאלה על בסיס הנתונים של filename_lr
        filename = row['filename_lr']
        logging.info(f"Processing row with identifier: {filename}")
        
        # חיפוש קבצים לפי שם
        if filename:
            logging.info(f"Finding the ECG chart for {filename}")
            
            # שלב יצירת השאלה והסברים על פי `report` ו-`scp_codes`
            report = row['report'] if pd.notnull(row['report']) else "No description available"
            scp_codes = row['scp_codes'] if pd.notnull(row['scp_codes']) else "No code available"
            heart_axis = row['heart_axis'] if pd.notnull(row['heart_axis']) else "No heart axis information available"
            
            explanation = f"Diagnosis: {report} | Code: {scp_codes} | Heart Axis: {heart_axis}"
            
            return {'filename': filename, 'question': 'Sample question', 'answer': explanation}
        else:
            logging.warning(f"Row for {filename} is missing the following fields: filename_lr, skipping this question.")
            return None
    except Exception as e:
        logging.error(f"Error generating question for {row['filename_lr']}: {e}")
        return None

# דוגמה לריצה עם מטא-דאטה
metadata = pd.read_csv("C:\\Users\\ben azulay\\Desktop\\ecg_project\\data\\ptbxl\\scp_statements.csv")

# יצירת השאלות
missing_data = []
quiz_entries = []
for index, row in ptbxl_data.iterrows():
    quiz_entry = generate_quiz_entry(row, metadata)
    if quiz_entry is None:
        missing_data.append(row['filename_lr'])
    else:
        quiz_entries.append(quiz_entry)

# שמירת השאלות לקובץ CSV
def save_to_csv(df, output_file):
    encodings = ['utf-8', 'ISO-8859-1', 'latin1', 'utf-16']
    for encoding in encodings:
        try:
            logging.info(f"Trying to save with encoding: {encoding}")
            df.to_csv(output_file, index=False, encoding=encoding)
            logging.info(f"File saved successfully with encoding {encoding}")
            break
        except Exception as e:
            logging.error(f"Error saving with encoding {encoding}: {e}")

# המרת את הרשומות לרשימה של דיפי (dataframe)
quiz_df = pd.DataFrame(quiz_entries)

# שמירה לקובץ החדש
save_to_csv(quiz_df, 'ecg_quiz.csv')

# סיום הריצה
logging.info("Quiz question generation finished successfully.")
