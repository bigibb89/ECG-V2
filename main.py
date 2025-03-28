import os
from data_loader import load_ptbxl_data
from question_generator import generate_question
from generate_ecg_image import generate_ecg_image
from provide_explanation import provide_explanation

# נתיב ברירת המחדל למאגר הנתונים (PTB-XL)
DATA_DIRECTORY = r"C:\Users\ben azulay\Desktop\ecg_project\data\ptbxl"

def main():
    # שלב 1: טעינת מערך הנתונים
    ptbxl_data, scp_data = load_ptbxl_data(DATA_DIRECTORY)
    if ptbxl_data is None or scp_data is None:
        print("Error loading the dataset. Exiting...")
        return

    # הדפסת 5 השורות הראשונות מכל מאגר כבדיקת הצלחה
    print("Loaded PTB-XL Data (first 5 rows):")
    print(ptbxl_data.head(5))
    print("\nLoaded SCP Data (first 5 rows):")
    print(scp_data.head(5))

    # לולאה ראשית למתן אפשרות למספר שאלות ללא טעינה חוזרת
    while True:
        # שלב 2: יצירת שאלה אקראית חדשה
        question, options, correct_answer = generate_question(ptbxl_data, scp_data)

        # שלב 3: יצירת תמונת ECG עבור השאלה
        # הפקת מזהה ה-ECG מתוך נוסח השאלה (הנחת פורמט: "ECG ####")
        ecg_id_token = question.split()[-1]
        # הסרת תווי שאלה/נקודה אפשריים מהמזהה בסוף המשפט
        ecg_id = ecg_id_token.strip("?.!:")
        print(f"\nDisplaying ECG {ecg_id}...")

        image_path = generate_ecg_image(DATA_DIRECTORY, ecg_id)
        if image_path is None:
            print("Error generating ECG image. Exiting...")
            return  # יציאה מהתוכנית במקרה של שגיאה ביצירת התמונה

        # שלב 4: הצגת השאלה ואפשרויות התשובה למשתמש
        print(f"\n{question}")
        for idx, option in enumerate(options, 1):
            print(f"{idx}. {option}")

        # שלב 5: קליטת תשובת המשתמש
        try:
            user_choice = int(input("\nEnter the number of your answer: ").strip())
            if user_choice < 1 or user_choice > len(options):
                raise ValueError
        except ValueError:
            print("Invalid choice. Please enter a number corresponding to the options.")
            continue  # חוזר לתחילת הלולאה עם שאלה חדשה

        selected_answer = options[user_choice - 1]

        # שלב 6: הפקת הסבר על בסיס התשובה הנבחרת והתשובה הנכונה
        explanation = provide_explanation(selected_answer, correct_answer, ecg_id, scp_data)
        print("\nExplanation:")
        print(explanation)

        # שלב 7: בדיקה אם המשתמש מעוניין בשאלה נוספת
        try_another = input("\nWould you like to try another question? (y/n): ").strip().lower()
        if try_another != 'y':
            print("Goodbye!")
            break  # יציאה מהלולאה והסיום

# הפעלת הפונקציה הראשית
if __name__ == "__main__":
    main()
