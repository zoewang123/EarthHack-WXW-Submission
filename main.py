import os
import dotenv
import streamlit as st
from openai import OpenAI
import requests
import csv
import json

# Run following if you want to create a new file and header for each columns
with open('response_record.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['User Idea', 'Materials', 'Energy', 'Value', 
                                   'Health_Wellbeing', 'Society_Culture', 
                                   'Biodiversity', 'Water', 'Overall_Score'
])

def makeMD(tx):
    file_path = "output.md"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(tx)
    print(f"Markdown content has been written to {file_path}")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # if the key already exists in the environment variables, it will use that, otherwise it will use the .env file to get the key
if not OPENAI_API_KEY:
    dotenv.load_dotenv(".env")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

style_answer = '''
    1. Materials in the economy are cycled at continuous high value.\n
    Score: ...\n
    Rationale: ...\n
    2. Energy is based on renewable sources.\n
    Score: ...\n
    Rationale: ...\n
    3. Value is generated in measures beyond just financial.\n
    Score: ...\n
    Rationale: ...\n
    4. Health & Wellbeing of humans and other species is tructurally supported.\n
    Score: ...\n
    Rationale: ...\n
    5. Society & Culture are preserved through social governance.\n
    Score: ...\n
    Rationale: ...\n
    6. Biodiversity is structurally supported and enhanced.\n
    Score: ...\n
    Rationale: ...\n
    7. Water is extracted at a sustainable rate and resource recovery is maximized.\n
    Summary Section\n
    Final Score: ...\n
    General Evaluation: ...\n
    Refined Proposal:\n
    ...
    '''

template = '''
    You are a environmental and economics analyst that provide a score of the circular economy idea or proposal I provide based on rubric items:\n
    1. Materials in the economy are cycled at continuous high value.\n
    2. Energy is based on renewable sources.\n
    3. Value is generated in measures beyond just financial.\n
    4. Health & Wellbeing of humans and other species is tructurally supported.\n
    5. Society & Culture are preserved through social governance.\n
    6. Biodiversity is structurally supported and enhanced.\n
    7. Water is extracted at a sustainable rate and resource recovery is maximized.\n
    The general grading rule for a specific rubric item is that:
    1. If you think this circular economy idea does not relate to this rubric item,
    you should give N/A score to this item and generally comment that this rubric item does not relate.\n
    2. If you think this circular economy idea need to take care of this rubric item but does not state clear
    or did poor on this related rubric item you should give a lower score on this rubric item
    and provid an improvement suggestion on this item based the economy idea.\n
    3. If you think this circular economy idea did really good on a rubric item,
    you should give a higher score and praise the idea with a reason.
    4. Each rubric item should have a score in 0~10 or N/A score as I stated before.\n
    6. Finally give a general score by taking an average on all the available rubric items score
    together with a general evaluation comment.
    7. Special Case: If you think the user's idea is not related to sustainability/circular economy or does not provide
    a positive and constructive idea to help environmental sustainability or climate change, etc. You can directly
    output your result as 0 score and a feedback that tell why user's idea is not qualified.\n
    8. Finally, generate a refined and rephrased formal sustainability program proposal based user's idea.
    You should put your response into the template as following:\n
    ''' + style_answer + " Finally! summary score into a python dictionary in code"

def parseResponse(tx, original):
  endI = 0
  startI = 0
  for i in range(len(tx)-1,-1,-1):
    if tx[i]=="}":
      endI = i
    if tx[i]=="{":
      startI = i
      break
  take_split = ((tx[startI:endI+1]).replace("'", "\"")).replace("\n", "")

  parsed_dict = json.loads(take_split)
  write_in = [original]

  for _,v in parsed_dict.items():
    write_in.append(v)
    if len(write_in) == 9:
      with open('response_record.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(write_in)
  return

def main():
  # if 'txx' not in locals():
  #   txx = "Empty"
  
  # txx = st.session_state.messages.data[0].content[0].text.value
  
  if 'uploaded_button_clicked' not in st.session_state:
    st.session_state['uploaded_button_clicked'] = False
  if 'messages' not in st.session_state:
    st.session_state['messages'] = []
  if 'thread' not in st.session_state:
     st.session_state['thread'] = None
  if 'assistant' not in st.session_state:
     st.session_state['assistant'] = None

  client = OpenAI()

  uploaded_files = st.file_uploader("You can upload multiple PDF files.", 
                                  type=["pdf"], 
                                  accept_multiple_files=True,
                                  label_visibility='visible')
  
  if st.button("Output evaluation to MarkDown File"):
    if (st.session_state['thread'] != None):
      messages = client.beta.threads.messages.list(thread_id=st.session_state['thread'].id)
      txx = messages.data[0].content[0].text.value # get the most recent message
      makeMD(txx)
      # original = messages.data[1].content[0].text.value # get the most recent message
      # parseResponse(txx, original)
  if st.button("Output score to CSV"):
    if (st.session_state['thread'] != None):
      messages = client.beta.threads.messages.list(thread_id=st.session_state['thread'].id)
      txx = messages.data[0].content[0].text.value # get the most recent message
      # makeMD(txx)
      original = messages.data[1].content[0].text.value # get the most recent message
      parseResponse(txx, original)

  # Button to trigger the file upload process
  if len(uploaded_files)>=0:
    st.write("After uploading all the files, please click the button below to create an assistant to answer questions about the files.\n" 
             + "IMPORTANT: Please do not click the following button again once the conversation starts!")
    if st.button('Upload Files') and (st.session_state['uploaded_button_clicked'] == False):
      file_ids = []
      uploaded_logs = []
      st.session_state['uploaded_button_clicked'] = True
      with st.spinner('Uploading Files...'):
        for uploaded_file in uploaded_files:
            # Read the content of the uploaded file
            file_content = uploaded_file.read()

            # Upload a file with an "assistants" purpose
            oai_uploaded_file = client.files.create(
                file=file_content,
                purpose='assistants'
            )
            uploaded_log = {"file_name": uploaded_file.name, "file_id": oai_uploaded_file.id}
            uploaded_logs.append(uploaded_log)
            # st.write(uploaded_log)
            file_ids.append(oai_uploaded_file.id)
        # st.write(uploaded_logs)
            
      with st.spinner('Creating Assistant...'):
        # Add the file to the assistant
        assistant = client.beta.assistants.create(
          instructions=f"""
          You need to provide evaluation by first understanding some files. 
          Here\'s your file_id and file_name mapping:
        
          {str(uploaded_logs)}

          Next, I will tell you what is your job as following:
          """ + template, # instructions to the assistant to understand the context and purpose of the assistant
          model="gpt-4-1106-preview",
          # model="gpt-3.5-turbo-1106",
          tools=[{"type": "retrieval"}], # augment with your own custom tools!
          file_ids=file_ids
        ) # you need to pass the file_ids as a list when creating the assistant
        st.session_state['assistant'] = assistant
        
        # st.write(st.session_state['assistant'])

        thread = client.beta.threads.create(
          messages=st.session_state.messages
        ) # thread is a collection of messages between the user and the assistant

        # st.write(thread)
        st.session_state['thread'] = thread

  # display chat history 
  for message in st.session_state.messages:  # this is to show the chat history
      if message["role"] == "assistant":
          st.chat_message("assistant").write(message["content"])
      else:
          st.chat_message("user").write(message["content"])

  # chat input 
  if st.session_state['assistant']:
    if prompt := st.chat_input(placeholder="Drop your sustainability business plan idea!"):
        # st.write("prompt", prompt)

        user_message = {
          "role": "user",
          "content": prompt
        }

        # Add the user's response to the chat - frontend
        st.session_state.messages.append(user_message)
        # Add the user's response to the thread - backend
        message = client.beta.threads.messages.create(
            thread_id=st.session_state['thread'].id,
            role="user",
            content=prompt
          ) # you can add the user's message to the thread using the thread_id
        
        # display chat
        st.chat_message("user").write(prompt)  # this is to show the user's input

        with st.chat_message("assistant"):
            with st.spinner():
                # Run the assistant
                run = client.beta.threads.runs.create(
                  thread_id=st.session_state['thread'].id,
                  assistant_id=st.session_state['assistant'].id
                ) # after adding the user's message to the thread, you can run the assistant to get the assistant's response
                
                while run.status != "completed":
                  run = client.beta.threads.runs.retrieve(
                    thread_id=st.session_state['thread'].id,
                    run_id=run.id
                  ) # you can retrieve the assistant's response when the status is "completed". This part is to make sure that the assistant has completed its response.

                messages = client.beta.threads.messages.list(thread_id=st.session_state['thread'].id)
                assistant_response = messages.data[0].content[0].text.value # get the most recent message
                

                st.session_state.messages.append(
                    {
                      "role": "assistant", 
                      "content": assistant_response # messages are stored in the "data" key with the latest message at the first index
                    })
                st.write(assistant_response.replace("$", "\$")) # display the assistant's response
