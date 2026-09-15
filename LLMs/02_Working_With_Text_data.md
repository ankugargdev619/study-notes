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

## Byte pair encoding
BPE is the tokenization scheme which has been used to tokenise and train LLMs such as GPT-2, GPT-3
We can use a library like tiktoken.
The Byte Pair Encoding Algorithm can be used to encode and decode any words which are out of its vocabulary. The algorithm achieves this by breaking down the larger text into smaller sub words or sometimes even the characters.

This enables the algorithm to have an ability to handle any random unknown words

## Data sampling with a sliding window
The main task of the LLMs is to predict the next word or token based on the input that it has.
To prepare content for the training of the LLM, the input text is divided into the input target pairs.
The input is the list of the tokens which are input and the target is the expected next token or the word.
So this acts as a sliding window
There are few important parameters which play an important role in preparing the data the model training
1. Batch Size : This sets the number of input and target embedding pairs which will be present inside a single batch, a smaller batch uses less memory while training but this leads to a noisy model 
2. Max Length : The chunk size of embedding which means what will decide the number of tokens which will be present
3. Stride : When batch size is more than 1, the stride decides the offset between the tokens of first and second input or target chunk
4. Shuffle : If shuffle is set to true then the chunks inside the batch are not sequential in nature

## Creating token embeddings
This is the last step in preparing the input text for LLM training. In this step, the token ID is converted into vector embedding.
The embedding weights are initialised first with random weights which acts as a starting point for the LLMs.
A continuous vector representation is necessary since GPT like LLMs are deep neural networks trained with the back propagation algorithm.

When a token is retrieved from an embedding layer, it gets the weights of the layer at that index.
Below is an example where we have created an embedding layer of size 6 and dimension 3, which means each token will have dimension of 3 but only 6 tokens are present in the layer
Below is the code snippet

```python
# Creating token embeddings
input_ids = torch.tensor([2,3,5,1])
vocab_size = 6
output_dim = 3

torch.manual_seed(123)
embedding_layer = torch.nn.Embedding(vocab_size, output_dim)
print(embedding_layer.weight)

```
``` 
Output
Parameter containing:
tensor([[ 0.3374, -0.1778, -0.1690],
        [ 0.9178,  1.5810,  1.3010],
        [ 1.2753, -0.2010, -0.1606],
        [-0.4015,  0.9666, -1.1481],
        [-1.1589,  0.3255, -0.6315],
        [-2.8400, -0.7849, -1.4096]], requires_grad=True)
```

# Apply the embedding layer to a token to get the embedding
print(embedding_layer(torch.tensor([5])))

```
tensor([[-2.8400, -0.7849, -1.4096]], grad_fn=<EmbeddingBackward0>)
```
```
```

Notice that the output is getting the vector at the 5th index of the embedding layer


## Encoding position
A problem with the attention mechanism in LLMs is that they don't have a sense of the position.
Each word will be mapped to a token irrespective of the position 
The deterministic position-independent embedding of the token ID is good for reproducibility.
There can be 2 types of position embeddings
1. Absolute Positional Embedding : The embedding is directly associated with the position of the token in a sequence. In this case a unique embedding is added to the input sequence to convey the exact location.
Input Tokens

┌─────┐   ┌─────┐   ┌───────┐
│  I  │   │ am  │   │ happy │
└──┬──┘   └──┬──┘   └───┬───┘
   │         │           │
   ▼         ▼           ▼
 Token      Token       Token
Embedding  Embedding   Embedding
   │         │           │
   +         +           +
   │         │           │
 Pos 0      Pos 1       Pos 2
   │         │           │
   ▼         ▼           ▼
┌──────┐  ┌───────┐  ┌──────────┐
│ I+P₀ │  │ am+P₁ │  │ happy+P₂ │
└──────┘  └───────┘  └──────────┘
     │         │          │
     └─────────┴──────────┘
                │
                ▼
          Transformer

2. Relative Positional Embedding : The embedding focuses on relative position or the distance between 2 tokens. This means that the model learns the relationships in terms of "how far apart" rather than "at which position".

Input Tokens

┌─────┐   ┌─────┐   ┌───────┐
│  I  │   │ am  │   │ happy │
└──┬──┘   └──┬──┘   └───┬───┘
   │         │           │
   └─────────┼───────────┘
             ▼
         Self-Attention
             │
             │
     ┌───────┴────────┐
     │ Relative       │
     │ Positions      │
     └───────┬────────┘
             │
     ┌───────┼───────────────┐
     ▼       ▼               ▼
   I ↔ am   I ↔ happy     am ↔ happy
     │       │               │
    +1      +2              +1
     │       │               │
     └───────┴───────────────┘
             │
             ▼
        Transformer



