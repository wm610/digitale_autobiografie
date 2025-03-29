from faster_whisper import WhisperModel

model_size = "small"

# Run on GPU with FP16
model = WhisperModel(model_size, device="cpu", compute_type="float32")

# or run on GPU with INT8
# model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
# or run on CPU with INT8
# model = WhisperModel(model_size, device="cpu", compute_type="int8")

segments, info = model.transcribe("C:/Users/marti/Documents/Programmieren/DigitaleAutobiografie/Test/Generated_audio_files/recording.wav", beam_size=5, vad_filter=True)
print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

# Define the path for the output text file
output_file_path = "C:/Users/marti/Documents/Programmieren/DigitaleAutobiografie/transcribed_recordings/transcription.txt"

# Write the transcribed text to the file
with open(output_file_path, 'w', encoding='utf-8') as file:
    for segment in segments:
        file.write(f"{segment.text}\n")

print(f"Transcription saved to {output_file_path}")

# Print the transcribed segments - segment iterator can only be accessed once, so iterated line file.write grabs the text already
#for segment in segments:
#   print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))