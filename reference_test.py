from llama_index.legacy.llms import Ollama

llm = Ollama(model="llama2")

prompt = (
  "Create a REST controller class in Java for a Spring Boot 3.2 application. "
  "This class should handle GET and POST requests, and include security and "
  "configuration annotations."
)

response = llm.complete(prompt)
print(response)