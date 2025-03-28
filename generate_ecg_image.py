import os
from pathlib import Path
import wfdb
import matplotlib.pyplot as plt

def generate_ecg_image(base_dir, ecg_id):
    """
    Generate and save an ECG image for a given ECG record ID.

    Parameters:
        base_dir (str): Path to the folder containing the PTB-XL data.
        ecg_id (int): ECG record ID.

    Returns:
        str: Path to the saved ECG image.
    """
    subdir = f"{int(ecg_id):05d}"[:5]
    record_path = Path(base_dir) / "records100" / subdir / f"{int(ecg_id):05d}_lr"

    try:
        record = wfdb.rdrecord(str(record_path))
        fig, ax = plt.subplots(figsize=(12, 4))
        for i in range(len(record.p_signal[0])):
            ax.plot(record.p_signal[:, i], label=f"Lead {i+1}")

        ax.set_title(f"ECG Record {ecg_id}")
        ax.set_xlabel("Time (samples)")
        ax.set_ylabel("Amplitude (mV)")
        ax.legend(loc='upper right')

        output_dir = Path(base_dir) / "ecg_images"
        output_dir.mkdir(exist_ok=True)
        image_path = output_dir / f"ecg_{ecg_id}.png"
        plt.savefig(image_path)
        plt.close(fig)

        return str(image_path)

    except FileNotFoundError:
        print(f"Error: ECG file for ID {ecg_id} not found at {record_path}.")
        return None
    except Exception as e:
        print(f"Unexpected error while generating ECG image: {e}")
        return None

# Example usage (for testing purposes only):
if __name__ == "__main__":
    test_base_dir = r"C:\\Users\\ben azulay\\Desktop\\ecg_project\\data\\ptbxl"
    test_ecg_id = 5
    image_file = generate_ecg_image(test_base_dir, test_ecg_id)
    if image_file:
        print(f"ECG image saved to: {image_file}")
