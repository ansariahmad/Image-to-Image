from openai import OpenAI
import time

# Initialize the OpenAI client with your API key
assistant_id = "asst_yNytfCc3qCRrdQaqSd7MXf4a"
thread_id = "thread_BkMIZJ7DPbTgobMSLhnTgAcT"
def generate_prompt(api_key, question):
    try:
        client = OpenAI(api_key=api_key)
        # Send the question to the thread
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=question
        )

        # Execute the thread
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id,
        )

        # Retrieve the run result
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id,
        )
        
        while run.status != "completed":
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
    )

        # Get the last message from the thread which is assumed to be the answer
        messages = client.beta.threads.messages.list(
            thread_id=thread_id
        )

        last_message = messages.data[0]
        response = last_message.content[0].text.value
        return response

    except Exception as e:
        print(f"An error occurred: {e}")
        return None