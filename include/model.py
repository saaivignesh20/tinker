import json
from groq import Groq

# Initialize Groq client
client = Groq(
    api_key="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")


class ConversationMemory:
    def __init__(self, max_turns=5):
        self.messages = []
        self.max_turns = max_turns

    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})
        if len(self.messages) > self.max_turns * 2:
            self.messages = self.messages[-self.max_turns * 2:]

    def get_messages(self):
        return self.messages


class ConversationModel:
    def __init__(self):
        self.memory = ConversationMemory()
        self.model = "gemma2-9b-it"  # Replace with the model you want to use
        # self.model = "llama-3.1-70b-versatile"
        self.messages = [self.get_system_message()]

    def get_system_message(self):
        """Generate the system message to instruct the model on how to respond."""
        return {
            "role": "system",
            "content": (
                # "You are an agent which summarizes the given document and replies in JSON format (starting and ending in braces) No plain-text. "
                # "Your response must contain two keys: 'response' and 'questions'. The 'response' should be a summary of the content provided, "
                # "under 300 words, in one paragraph. The 'questions' should be a list of 3 most important questions based on the provided document. "
                # "I want response from you as JSON. No plain-text."
                '''You are a document summarizer and questions generator. Your response should always be in JSON object within braces. No special formatting needed.
                  Use 'response' key for any message you have to pass on and 'questions' key for any questions. 
                  Also after u summerize. from the content, generate 3 questions that could be asked from the document u obtained. 
                  If no questions. Let the array be empty. Handle all edge cases within this JSON format. 
                  Also after u summerize, from the content, generate 3 questions that could be asked from the document u obtained. 
                  Give all responses in json format.'''
            )
        }

    def get_response(self, document_content):
        """Get response from Groq model based on the given document content."""
        self.memory.add_message("user", document_content)

        # Combine system and user messages
        self.messages = self.messages + self.memory.get_messages()

        # Call Groq API to get response
        chat_completion = client.chat.completions.create(
            messages=self.messages,
            model=self.model,
            temperature=0.7,
            max_tokens=1000,
        )

        # Get the model's response
        response = chat_completion.choices[0].message.content
        print(response)

        # Check if the response is in JSON format
        try:
            response_json = json.loads(response.replace(
                '```json', '').replace('```', ''))  # Try to parse as JSON
            return response_json
        except ValueError as e:
            return {"error": "Failed to parse response as JSON", "details": str(e)}

    def clear_conversation_memory(self):
        """Clear the conversation history."""
        self.memory.messages = [self.get_system_message()]
        self.messages = []
