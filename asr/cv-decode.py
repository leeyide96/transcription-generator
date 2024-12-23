import requests
import pandas as pd
import shutil

folder_path = "/app/data/cv-valid-dev/"
csv_path = "/app/data/cv-valid-dev.csv"
export_path = "/app/shared-data/cv-valid-dev.csv"
index = "cv-transcriptions"


def generate_transcription(session, file_path):
    """
    Sends an audio file to the ASR API and retrieves its transcription and duration

    Args:
        session (requests.Session): Session object for making API requests
        file_path (str): Path to the audio file

    Returns:
        tuple: Contains the transcription and duration
    """
    url = "http://asr-api:8001/asr"
    with open(file_path, "rb") as f:
        file = { 'file': f }
        response = session.post(url, files=file)
    if response.status_code != 200:
        transcript, duration = None, None
    else:
        response = response.json()
        transcript = response['transcription']
        duration = response['duration']
    return transcript, duration


def update_csv(csv_path, folder_path, export_path):
    """
    Updates a CSV file with transcriptions and durations

    Args:
        csv_path (str): Path to the input CSV file
        folder_path (str): Path to the folder containing audio files
        export_path (str): Path to save the updated CSV file with added columns to
    """
    session = requests.Session()
    df = pd.read_csv(csv_path)
    df[["generated_text", "duration"]] = df["filename"].apply(lambda x: pd.Series(generate_transcription(session, folder_path + x)))
    df.to_csv(export_path, index=False)


def remove_folder(folder_path):
    """
        Removes a folder and all its contents

        Args:
            folder_path (str): Path to the folder to be removed
        """
    shutil.rmtree(folder_path)


if __name__ == "__main__":
    update_csv(csv_path, folder_path, export_path)
    remove_folder(folder_path)