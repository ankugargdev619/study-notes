from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(model="gpt-5-mini", temperature=0)

result = model.invoke("Suggest me 5 indian male names")

print(result.content)
