#This is a comment in Python

import argparse
import utils

#First, we will define our main function
def main():
  #We will be asking for the audio file to transcribe
  parser = argparse.ArgumentParser()
  parser.add_argument('audio_file')
  parser.add_argument('--local', action='store_true')
  args = parser.parse_args()

  #By the way, we will be using a 3rd party API
  #AssemblyAPI to transcribe the audio file that we have, hence we will need 
  #an API Key from the official site.
  api_key = '2dcfd24e6c12428d82ee15b2bdf7a018'

  #Create a header with authorization along with the content-type
  header = {
    'authorization': api_key,
    'content-type' : 'application/json'
  }

  #I forgot to initialize args
  if args.local:
    #Upload the audio file to AssemblyAI
    upload_url = utils.upload_file(args.audio_file, header)
  else:
    upload_url = {
      'upload_url': args.audio_file
    }

  #After uploading the file, we need to request a transcription
  transcript_response = utils.request_transcript(upload_url, header)

  #Then we will create a polling endpoint that will let us check the transcription
  polling_endpoint = utils.make_polling_endpoint(transcript_response)

  #Then we will wait for the transcription is complete
  utils.wait_for_completion(polling_endpoint, header)

  #After completing the transcript, we will request the paragraphs of the transcript
  paragraphs = utils.get_paragraphs(polling_endpoint, header)

  #Now that we have the paragraphs, we need to save and print the file to a txt
  with open(args.audio_file + '.txt', 'w') as f:
    for paragraph in paragraphs:
      print(paragraph['text'] + '\n')
      f.write(paragraph['text'] + '\n')
  
  return

if __name__ == '__main__':
  main()


##That's how you can automate the transcription
##Be Lazy :) hehehehe ..
##Thanks for watching