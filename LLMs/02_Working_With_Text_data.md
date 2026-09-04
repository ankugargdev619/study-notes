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
3. Add ability to convert tokens into text
There should be an ability to convert the tokens from id to text later

## Adding special context tokens
The tokenizer is trained on limited vocabulary but there might be words which are available in the tokenizer so the tokenizer needs to be modified to handle the unknown words.
For example we add <|unk|> to handle the unknown words in end of the vocabulary and <|endoftext|> token that can use to separate two unrelated text sources e.g. when LLM is trained on 2 different books then the end of book one will be marked with <|endoftext|>.
Some models include more such special tokens like below
i. `[BOS]` : Beginning of sequence => This signifies to LLM that a piece of text begins.
ii. `[EOS]` : End of sequence => This token is positioned at the end of a text and is especially useful when concatenating multiple unrelated texts and is similar to `<|endoftext|>`
iii. `[PAD}` : When training LLMs with batch size greater than 1, the batch might contain texts of varying lengths. This can be understood with help of an example.
Suppose we have different sentences with varying length. One approach could be to train them one by one but GPU perform better with multiple sequences as well.
So data is usually processed in batches. But there is one problem with that, while processing sentences in batches the tensors which are created are of uneven size.
E.g.
Batch 1
─────────────────────────────────────
"I love pizza"
"Machine learning is really interesting"
"Hello"
"I like cats"
─────────────────────────────────────
Embedding will look like below
[12, 45, 91]              ← length 3
[81, 32, 56, 73, 19]      ← length 5
[25]                      ← length 1
[12, 67, 88]              ← length 3

Tensor will look like this
[
    [12, 45, 91],
    [81, 32, 56, 73, 19],
    [25],
    [12, 67, 88]
]

This is where the pad comes in and the tensor is converted into
[
 [12, 45, 91, PAD, PAD],
 [81, 32, 56, 73, 19 ],
 [25, PAD, PAD, PAD, PAD],
 [12, 67, 88, PAD, PAD]
]
