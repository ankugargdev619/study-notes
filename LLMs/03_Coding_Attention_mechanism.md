# Attention mechanism
We will understand the implementation behind the attention mechanism as below:
1. Simplified self-attention
2. Self-attention
3. Casual attention
4. Multi-head attention

## Problem with modeling long sequences
Let us first understand the problems that self-attention mechanism solved.
Let's say that we need a model which translates one sentence from German to english and a basic starting point could be to convert it word by word .

Kannst du mir helfen, diesen Satz zu übersetzen?

Kannst   du    mir   helfen,   diesen   Satz     zu   übersetzen?
  │       │     │       │        │       │        │       │
  │       │     │       │        │       │        │       │
 Can     you   me     help      this   sentence  to    translate

This is the literal translation word by word and it doesn't really makes any sense in english gramatically.

Recurrent Neural Networks (RNNs) were the most popular encoder-decoder architecture for language translation.
In RNNs the output of the previous steps are fed as input to next step.
In encoder-decoder RNN, the input text is fed into the encoder, which processes it sequentially. The encoder updates its hidden state at each step, trying to capture the entire meaning of the input sentence. The decoder takes this final hidden state to start generating the translated sentence one word at a time.

It also updates its hidden state at each step, which is supposed to carry the context necessary for the next-word prediction.

## Capturing data dependencies with attention mechanism
Although RNNs work fine for translating short sentences, they don't work well for longer texts as they don't have direct access to previous words in the input.
One major shortcoming in this approach is that the RNN must remember the entire encoded input in a single hidden state before passing it to decoder.

`Bahdanau` attention mechanism was created by researchers to over this issue. Then it was realised that the RNNs are not required for building neural networks for NLP.
Then the transformer architecture was used along with self-attention mechanism.

> Self-attention is a mechanism that allows each position in the input sequence to consider the relevancy of, or "attend to," all other positions in the same sequence when computing the representation of a sequence. Self-attention is a key component of contemporary LLMs based on the transformer architecture.


## Attending to different parts of the input with self-attention
Attention mechanism is one of the most core concept around which the LLMs are based and understanding this means conquering most toughest part of the book.

> The "self" in self-attention
> In self-attention, the "self" refers to the mechanism's ability to compute attention weights by relating different positions within a single input sequence. It assesses and learns the relationships and dependencies between various parts of the input itself, such words in a sentence or pixels in an image.

### Simple self-attention mechanism without trainable weights
To implement a simple self-attention mechanism, we calculate the similarity between the query token and each input token.
This can be calculated based on the dot product of the vectors, it's mathematical representation of the similarity between 2 vectors.
Once the attention is calculated, the attention weights are calculated to normalize the attention weights.
1. **Usually softmax is used to calculate the attention weight as it can easily handle the extreme values making sure that the negative values are also handled correctly**
2. Context vector by multiplying the embedded input tokens with corresponding attention weights and then summing the resulting vectors

### Computing attention weights for all input tokens
Earlier we computed the context vector for only one input but now we will calculate it for all the inputs at once and the process will remain same

## Implementing self-attention with trainable weights
We want to compute the context vectors as weighted sums over the input vectors specific to a certain input element. The important difference here is the matrices are weighted which are tuned during the training. 

### Computing the attention weights step by step
Self-attention mechanism can be implemented step by step by introducing 3 trainable weight matrices Wq, Wk and Wv. These 3 matrices are used to project the embedded input tokens into query, key and value.

> **Weight parameters vs attention weights**
> Weight parameters are the parameters of the neural network which are optimised during the training. These are not attention weights, attention weights determine the extent to which a context vector depends on the different parts of the input.

The calculated weights are then normalized and normalization is important to improve the training performance by avoiding small gradients which may slow down the training when the gradient nears small numbers.

> **Why the terms query, key and value?**
> The terms "key", "query" and "value" in the context of attention mechanisms are borrowed from the domain of information retrieval and databases where similar concepts are used to store, search and retrieve information.
> A query is analogous to a search query in a database. It represents the current item, the model focuses on or tries to understand. The query is used to probe the other parts of the input sequence to determine how much attention to pay to them.
> The key is like a database key used for indexing and searching. In the attention mechanism, each item in the input sequence has an associated key. These keys are used to match the query.
> The value in this context is similar to the value in a key-value pair in a database. It represents the actual content or representation of the input items. Once the model determines which keys are most relevant to the query, it retrieves the corresponding values.

## Hiding future words with casual attention
For a large variety of LLMs, the self attention mechanism needs to consider only the tokens that appear prior to the current position when predicting the next token in the sequence. It restricts a model to only consider previous and current inputs in a sequence when processing any given token when computing attention scores.
We need to modify the standard self-attention mechanism to a casual attention mechanism.

### Applying a casual attention mask
Our next step is to implement the casual attention mask in code. To implement the steps to apply a casual attention mask to obtain the masked attention weights.
The new weights are calculated and the matrix is renormalised which makes sure that the information from future tokens doesn't contribute to the weights.

> **Dropout** : It is a technique where randomly selected hidden layer units are ignored during training, this helps in getting rid of the over fitting problem. The dropout is applied 2 times: after calculating the attention weights or after applying the attention weights to the value vectors. Here we will apply the dropout mask after computing the attention weights.

While applying the dropout, the half of the items in the zeroes out randomly.
