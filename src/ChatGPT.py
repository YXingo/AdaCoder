import time
import openai
from openai import OpenAI

client = OpenAI(api_key='your api key')


class ChatGPT:

    def __init__(self):
        self.conversation = [
            {"role": "system", "content": "You are an expert programming assistant."}]

    def ask_gpt(self, user_input: str, max_tokens) -> str:
        self.conversation.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.conversation,
            max_tokens=max_tokens
        )

        answer = response.choices[0].message.content

        self.conversation.append({"role": "assistant", "content": answer})

        return answer

    def safe_ask_gpt(self, user_input: str, max_tokens, max_retries=20, retry_delay=3):
        for attempt in range(max_retries):
            try:
                response = self.ask_gpt(user_input, max_tokens)
                return response
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                else:
                    raise e

    def manual_add_response(self, response: str):
        self.conversation.append({"role": "assistant", "content": response})

    def clear_context_conversion(self):
        self.conversation = [
            {"role": "system", "content": "You are an expert programming assistant."}]

    def __str__(self):
        output = ""
        for conversation in self.conversation:
            output += str(conversation) + "\n"
        output = output.rstrip('\n')
        return output


if __name__ == '__main__':
    gpt = ChatGPT()
