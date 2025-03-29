import os
import audio_recorder
import transcription

def main():
    # Define the available categories
    categories = {
        1: "Kindheit",
        2: "Jugend",
        3: "Familie",
        4: "Arbeit",
        5: "Prägendes",
        6: "Sonstiges"
    }

    # Initialize recording counts for each category
    recording_counts = {cat: 0 for cat in categories.keys()}

    # Greeting and category selection
    print("Hallo! Welche Geschichten willst Du heute erzählen?")
    for num, name in categories.items():
        print(f"{num}: {name}")

    while True:
        try:
            selected = int(input("Bitte wähle eine Kategorie (1-6): "))
            if selected in categories:
                break
            else:
                print("Ungültige Kategorie. Bitte wähle eine Zahl zwischen 1 und 6.")
        except ValueError:
            print("Ungültige Eingabe. Bitte gib eine Zahl ein.")

    current_category = selected

    # Main process loop
    while True:
        current_category_name = categories[current_category]
        print(f"\nAktuelle Kategorie: {current_category} - {current_category_name}")
        print("Optionen:")
        print("  s: Neue Aufnahme starten")
        print("  n: Zur nächsten Kategorie wechseln")
        print("  p: Zur vorherigen Kategorie wechseln")
        print("  f: Biographie beenden")
        
        choice = input("Bitte wähle eine Option: ").strip().lower()

        if choice == 's':
            # Increase the recording count for the current category
            recording_counts[current_category] += 1
            count = recording_counts[current_category]
            # Create output filename in the format "CategoryNr_CategoryName_n"
            output_filename = f"{current_category}_{current_category_name}_{count}"
            # Define the recordings folder path (assumed to be a subfolder of the main folder)
            #output_path = os.path.join(os.getcwd(), "recordings")
            output_path = os.path.join("C:/Users/marti/Documents/Programmieren/DigitaleAutobiografie/recordings")
            # Ensure the folder exists, if not, create it
            os.makedirs(output_path, exist_ok=True)
            print(f"Aufnahme wird gespeichert als: {output_filename}.wav in {output_path}")
            # Start recording using the audio_recorder module
            audio_recorder.start_recording(output_path, output_filename)
            
        elif choice == 'n':
            if current_category < 6:
                current_category += 1
            else:
                print("Dies ist bereits die höchste Kategorie.")
        elif choice == 'p':
            if current_category > 1:
                current_category -= 1
            else:
                print("Dies ist bereits die niedrigste Kategorie.")
        elif choice == 'f':
            print("Biographie beendet.")
            break
        else:
            print("Ungültige Option. Bitte wähle 's', 'n', 'p' oder 'f'.")

    #Transcription
    # Define paths
    recordings_folder = os.path.join("C:/Users/marti/Documents/Programmieren/DigitaleAutobiografie/recordings")
    transcribed_folder = os.path.join("C:/Users/marti/Documents/Programmieren/DigitaleAutobiografie/transcribed_recordings")

    # Ensure the transcribed_recordings folder exists
    os.makedirs(transcribed_folder, exist_ok=True)

    # Iterate over the files in the recordings folder
    for file in os.listdir(recordings_folder):
        # Process only .wav files
        if file.lower().endswith(".wav"):
            audio_file_path = os.path.join(recordings_folder, file)
            # Remove the file extension to get the base name for the output file
            base_name = os.path.splitext(file)[0]
            
            print(f"Transcribing {file}...")
            transcription.transcribe_audio(audio_file_path, transcribed_folder, base_name)

if __name__ == "__main__":
    main()