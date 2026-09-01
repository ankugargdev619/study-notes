import re

text = "Hello, world. Is this-- a test?"
result = re.split(r"(\s)", text)
print(result)
# Remove punctuations
result = re.split(r"([,.] | \s)", text)
print(result)
# Remove the whitespace
result = [item for item in result if item.strip()]
print(result)
# Extend it to more punctuations
result = re.split(r'([,.:;?_!"()\']|--|\s)', text)
result = [item.strip() for item in result if item.strip()]
print(result)
