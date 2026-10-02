# Summary
This covers below:
1. Coding GPT like LLM
2. Normalizing layer activations to stabilize neural network
3. Adding shortcut connections in deep neural networks
4. Implementing transformer blocks to create GPT models of various sizes
5. Computing the number of parameters and storage requirements of GPT models


# Coding an LLM architecture
LLMs are deep neural networks which actually generate new text one word at a time. However despite their size, the model architecture is less complicated than you might think. The major components are repeated. 
In context of deep learning and LLMs like GPT, the term "parameters" refers to trainable weights of the model. These weights are essentially the internal variables of the model that are adjusted and optimized during the training process to minimize a specific loss function. This optimization allows the model to learn from the training data.

                    GPT ARCHITECTURE
                    ===============

                         Text
                          |
                          v
                    +-----------+
                    | Tokenizer |
                    +-----------+
                          |
                       Token IDs
                          |
              +-----------+-----------+
              |                       |
              v                       v
       Token Embedding        Positional Embedding
         [50257,768]             [1024,768]
              |                       |
              +----------+------------+
                         |
                         v
                   Add Embeddings
                         |
                         v
                       Dropout
                         |
                         v
        +---------------------------------------+
        |         TRANSFORMER BLOCK x12         |
        |                                       |
        |  LayerNorm                            |
        |      |                                |
        |      v                                |
        |  Masked Multi-Head Self-Attention     |
        |      |                                |
        |      v                                |
        |  Dropout                              |
        |      |                                |
        |      +-----> Residual Add <-----------+
        |                     |                 |
        |                     v                 |
        |                 LayerNorm             |
        |                     |                 |
        |                     v                 |
        |                Feed Forward            |
        |                768 -> 3072            |
        |                     |                 |
        |                    GELU               |
        |                     |                 |
        |                3072 -> 768            |
        |                     |                 |
        |                  Dropout              |
        |                     |                 |
        |                     +-- Residual Add -+
        +---------------------|-----------------+
                              |
                              v
                       Final LayerNorm
                              |
                              v
                         Linear Head
                        768 -> 50257
                              |
                              v
                           Logits
                              |
                              v
                    Next Token Probability
                              |
                              v
                       Sample Token
                              |
                              v
                       Generated Text




> **GPT-2 vs GPT-3**
> The weights of the pretrained GPT-2 model are publicly available. The fundamental difference between GPT-2 and GPT-3 is that the GPT-2 has 1.5 billion parameters and GPT-3 has 175 billion parameters. GPT-2 is a better option to learn since as per a published report, it would take 665 years to train GPT-3 on a normal consumer laptop.

# Normalizing activations with layer normalization
Training deep neural network with many layers can sometimes prove challenging due to problems like vanishing or exploding gradients. These problems lead to unstable training dynamics and make it difficult for the network to effectively adjust its weights, which means the learning process struggles to find a set of parameters for the neural network that minimizes the loss function. In other words, the network has difficulty learning the underlying patterns in the data to a degree that would allow it to make accurate predictions or decisions.

Let's now implement layer normalization to improve the stability and efficiency of neural network training. The main idea behind layer normalization is to adjust the activations of a neural network layer to have a mean of 0 and a variance of 1, also known as unit variance. This adjustment speeds up the convergence to effective weights and ensures consistent, reliable training.

> Activation function is used as mathematical gate between the input and outputs of the neuron, if activation function is not used then the artificial neural network will be applicable for linear data only.


# Implementing a feed forward network with GELU activations
GELU is preferred over ReLU because the ReLU has a hard pass and it only allows positive values to pass through and doesn't allow negative values so all the information is not passed through. However for GELU the negative values are also allowed to pass but with limited weights, so some information is still passed on to the next layer.

Both GELU and SwiGELU activation functions are smooth activation functions and are used in variety of models which implement this.

**Vanishing gradient problem**
The gradient becomes so small that the neural network never reaches the local minima

# Connecting attention and linear layers in a transformer block
Next step is to create transformer block, this will be a fundamental block of LLMs. This block combines multi-head attention, layer normalization, dropout, feed forward layers and GELU activations.

```py
class TransformerBlock(nn.Module):
  def __init__(self, cfg):
    super().__init()
    self.att = MultiHeadAtention(
        d_in = cfg["emb_dim"],
        d_out = cfg["emb_dim"],
        context_length=cfg["context_length"],
        num_heads=cfg["n_heads"],
        dropout=cfg["drop_rate"],
        qkv_bias=cfg["qkv_bias"])
    self.ff = FeedForward(cfg)
    self.norm1 = LayerNorm(cfg["emb_dim"])
    self.norm2 = LayerNorm(cfg["emb_dim"])
    self.drop_shortcut = nn.Dropout(cfg["drop_rate"])

  def forward(self, x):
    shortcut = x
    x = self.norm1(x)
    x = self.att(x)
    x = self.drop_shortcut(x)
    x = x + shortcut

    shortcut = x
    x = self.norm2(x)
    x = self.ff(x)
    x = self.drop_shortcut(x)
    x = x + shortcut
    return x
```

LayerNorm is applied before each of the components and dropout is applied after them to regularize the model and prevent overfitting. This is also know as Pre-LayerNorm.


# Coding the GPT model
We will code a full GPT-2 model. The number of transformer layers is repeated 12 times, which is specified in the n_layers entry in the GPT_CONFIG_124M dictionary.

```py
class GPTModel(nn.Module):
  def __init__(self, cfg):
    super().__init__()
    self.tok_emb = nn.Embedding(cfg["vocab_size"], cfg["emb_dim"])
    self.pos_emb = nn.Embedding(cfg["context_length"], cfg["emb_dim"])
    self.drop_emb = nn.Dropout(cfg["drop_rate"])

    self.trf_blocks = nn.Sequential(
        *[TransformerBlock(cfg) for _ in range(cfg["n_layers"])]
    )

    self.final_norm = LayerNorm(cfg["emb_dim"])
    self.out_head = nn.Linear(
        cfg["emb_dim"], cfg["vocab_size"], bias=False
    )

  def forward(self, in_idx):
    batch_size, seq_len = in_idx.shape
    tok_embeds = self.tok_emb(in_idx)

    pos_embeds = self.pos_emb(
        torch.arange(seq_len, device=in_idx.devices)
    )

    x = tok_embeds + pos_embeds
    x = self.drop_emb(x)
    x = self.trf_blocks(x)
    x = self.final_norm(x)
    logits = self.out_head(x)
    return logits
```

The `__init__` constructor of this GPTModel class initializes the token and positional embedding layers using the configurations passed in via a Python dictionary, cfg. These embeddings layers are responsible for converting input token indices into dense vectors and adding positional information.

Next the `__init__` method creates a sequential stack of `TransformerBlock` modules equal to the number of layers specified in `cfg`. Following the transformer blocks, a `LayerNorm` layer is applied, standardizing the outputs from the transformer blocks to stablize the learning process.

# Generating text
We will now implement the code that converts the tensor outputs of the GPT model back into text. Before we get started, let's briefly review how a generative model like an LLM generates text one word at a time.

The process by which a GPT model goes from output tensors to generated text involves several steps. These steps include decoding the output tensors, selecting tokens based on a probability distribution and converting those token s into hum-readable text.

GPT model generates the next token given its input. In each step, the model outputs a matrix with vectors representing potential next tokens. The vector corresponding to the next token is extracted and converted into a probability distribution via the softmax function.

Within the vector containing the resulting probability scores, the index of the highest value is located, which translates to the token ID. This token ID is then decoded back into text, producing the next token ID.

After this step, we are able to generate the text however the output will still be gibberish since the model has not been trained yet.
