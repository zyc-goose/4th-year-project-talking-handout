from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import time
from . import printMessage


# gcs: Google Cloud Service. 
# Audio files need to be uploaded to Google Cloud.
def transcribe_gcs(gcs_uri):
    """Asynchronously transcribes the audio file specified by the gcs_uri.
    args:
        gcs_uri - URI with format 'gs://<bucket>/<path_to_audio>'
    returns:
        transcript - a list of transcribed sections
    """
    printMessage.begin('Initiating Google Cloud Speech operation')
    client = speech.SpeechClient()

    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=44100,
        language_code='en-GB',
        enable_word_time_offsets=True)

    operation = client.long_running_recognize(config, audio)
    printMessage.end()

    printMessage.begin('Waiting for operation to complete [0%%]')
    while not operation.done():
        time.sleep(1)
        printMessage.begin('Waiting for operation to complete [%s%%]' % operation.metadata.progress_percent)
    response = operation.result(timeout=10)
    printMessage.end()

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    transcript = []
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        best_result = result.alternatives[0]
        start_time = best_result.words[0].start_time
        timestamp_min = start_time.seconds // 60
        timestamp_sec = start_time.seconds % 60
        timestamp_millis = start_time.nanos // (10**6)
        transcript.append({
            'timestamp': '%02d:%02d.%03d' % (timestamp_min, timestamp_sec, timestamp_millis),
            'text': best_result.transcript,
            'confidence': best_result.confidence
        })
    return transcript
