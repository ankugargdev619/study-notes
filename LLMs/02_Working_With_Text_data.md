This focuses on Data Preparation and sampling.

## Understanding word embeddings
Deep neural networks including LLMs cannot process raw text directly. Since text is categorical, it isn't compatible with the mathematical operations.
There we need a way to convert this text into a mathematical representation. The process of converting these words into a mathematical representation is called embedding.

There are different embedding models designed for different tasks. While word embeddings are most commonly used embedding, there are also embeddings for sentences, paragraphs or whole documents. Sentence or paragraph embeddings are popular for Retrieval Augmented Generation (RAG).

There are multiple approaches to generate embeddings
**Word2Vec** : The main idea behind Word2Vec is that the words that appear in a similar context tend to have similar meanings. Consequently when projected into 2 dimensional word embeddings, the similar words are clustered together.

More dimensions mean more efficiency but at the trade of more cost.

## Tokenizing text
How we split input text into individual tokens, a required preprocessing step for creating embeddings for an LLM.
These tokens can be individual words or special characters including punctuation characters.

### Steps in tokenizing the text
1. Split the text to obtain a list of tokens
A common and easy approach can to split the text with words. There are multiple ways of tokenisation and usually it's not so simple.
2. Converting tokens into token IDs
Now each token requires converting it into a corresponding token ID representation. This is an intermediate step which we take before converting it into vectors.


