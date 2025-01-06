import threading
from whisper_live.client import TranscriptionClient
import time
from langchain_ollama.chat_models import ChatOllama
from langchain.prompts import PromptTemplate

llm = ChatOllama(model="cow/gemma2_tools:2b")

template = """
For the given conversation summarize the conversation in short.
Given Text: {conversastion}
Summary: {}
"""
prompt = PromptTemplate.from_template(template)

llm_agent = (prompt | llm)


GLOBAL_TEXT = ""





def handle_live_transcription(update):
    global GLOBAL_TEXT
    if update:
        print(f">>> {update[-1]}")
        GLOBAL_TEXT = GLOBAL_TEXT +" "+ update[-1]
    else:
        print("no update")    



def main():
    client = TranscriptionClient(host="localhost", port=9090, lang="en", model="tiny",
                                 handle_callback=handle_live_transcription)

    def start_transcription():
        # client.compile("/home/wpnx/Downloads/American accent in 10 seconds.mp3")
        client.compile("../samples/dr_pt_conv.wav")

    transcription_thread = threading.Thread(target=start_transcription, daemon=True)
    transcription_thread.start()
    transcription_thread.join()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
    
    print("GG",GLOBAL_TEXT)














# import threading
# import time
# from whisper_live.client import TranscriptionClient


# # Initialize the TranscriptionClient
# client = TranscriptionClient(
#     host="localhost",
#     port=9090,
#     lang="en",
#     # save_output_recording=True,
#     # output_recording_filename="live_audio.wav",
#     model="tiny"
# )


# def run_transcription():
#     # client.compile()  # Begin transcription (live audio recording)
#     client.compile("../samples/F_0101_15y2m_1.wav")

# def fetch_transcriptions():
#     while True:
#         text = client.client.get_transcription()
#         if text:
#             print("Live Transcription:", text)
#         time.sleep(1)  # Adjust polling interval as needed



# # Start threads for transcription and live updates
# transcription_thread = threading.Thread(target=run_transcription, daemon=True)
# # fetch_thread = threading.Thread(target=fetch_transcriptions, daemon=True)

# if __name__ == "__main__":

#     transcription_thread.start()
#     # fetch_thread.start()
#     # .
#     # # Keep the main thread alive
#     # try:
#     transcription_thread.join()
# # except KeyboardInterrupt:
# #     print("Stopping transcription...")

