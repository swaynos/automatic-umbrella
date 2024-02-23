# reference: https://docs.llamaindex.ai/en/stable/examples/llm/ollama.html
from llama_index.legacy.llms import Ollama

# replies can take a long time on lower spec'd hardware
# request_timeout specifies how long to wait.
llm = Ollama(model="llama2", request_timeout=120.0)

prompt = (
  "Create a REST controller class in Java for a Spring Boot 3.2 application. "
  "This class should handle GET and POST requests, and include security and "
  "configuration annotations."
)

response = llm.complete(prompt)
print(response)