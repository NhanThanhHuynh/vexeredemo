def transcribe_audio_core(audio_path: str) -> str:
    return "Tôi muốn đổi giờ vé"

def synthesize_speech_core(text: str, out_path="output.wav"):
    with open(out_path, "wb") as f:
        f.write(b"FAKEWAVE")
    return out_path