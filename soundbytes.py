import pyaudio
import sys
import wave


def load_sound(path, start=0, end=None):
    with wave.open(path, mode='rb') as audio:
        if end is None:
            end = get_total_duration(audio)

        start_offset = get_num_frames(audio, start)
        total_frames = get_num_frames(audio, end-start)
        fast_forward(audio, start_offset)
        return (audio.getparams(),
                read_frames(audio, total_frames))


def fast_forward(audio, num_frames):
    while num_frames > 0:
        chunk = audio.readframes(num_frames)
        num_frames -= len(chunk)


def read_frames(audio, total_frames):
    byteses = []
    while total_frames > 0:
        chunk = audio.readframes(total_frames)
        byteses.append(chunk)
        total_frames -= len(chunk)
    return b''.join(iter(byteses))


def get_total_duration(audio):
    return audio.getnframes() * 1.0 / audio.getframerate()


def get_num_frames(audio, offset_secs):
    hz = audio.getframerate()
    return int(hz * offset_secs)


def write_wav(path, params, raw_audio):
    with wave.open(path, 'wb') as out:
        out.setparams(params)
        out.writeframes(raw_audio)


def play_sound(params, raw_audio):
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(2),
            channels=1,
            rate=44100,
            output=True)
    stream.write(raw_audio)
    stream.stop_stream()
    stream.close()
    p.terminate()
