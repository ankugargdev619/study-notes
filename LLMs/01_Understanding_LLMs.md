# Large Language Models (LLMs)
An LLM is a neural network designed to understand, generate and respond to human like text. These models are deep neural networks trained on massive amounts of text data.
The large in Large Language Model refers to both model's size in terms of parameters and the immense dataset on which it's trained.

## Transformer
LLMs utilize this architecture called the transformers, which allow them to pay selective attention to different parts of the input when making predictions, making them especially adept at handling the nuances and complexities of human language.

## Stages of building LLMs
i) Pre-training : Initial phase where a model like an LLM is trained on a large, diverse dataset too develop a broad understanding of language. This serves as foundational resource that can be further refined through fine-tuning. This is also termed as **unlabeled training**. The model created after this is called `base model` or `foundational model`.
ii) Fine-tuning : This is process of training the LLM on labeled data. Fine-tuning can be categorized into 2 major categories.
a. Instruction Fine-Tuning : This contains instructions and answer pairs.
b. Classification Fine-Tuning : In this we have below have instruction and the classification label associated with the instruction

## Transformer Architecture
This architecture was the foundation stone for the work around LLMs, a research paper called "Attention is all you need" was published which has been the foundation of all the LLMs which are there. A simplified version of this architecture has 2 sub-modules
i) Encoder : This processes the input text and encodes this into a series of numerical representations
ii) Decoder : This module takes the encoded vectors and generates the output text.
Say if the role of the LLM is to translate the text from one language to another language then the encoder will take the text in source language and convert it into embeddings and the decoder would take the encoded vectors into the target language.

                         ┌───────────────────────────────┐
                         │          INPUT TEXT           │
                         │      "This is an example"     │
                         └───────────────┬───────────────┘
                                         │
                                         ▼
                         ┌───────────────────────────────┐
                         │      PREPROCESSING STEPS      │
                         └───────────────┬───────────────┘
                                         │
                                         ▼
                    ┌────────────────────────────────────────┐
                    │               ENCODER                  │
                    │                                        │
                    │  Processes the complete input text     │
                    │  and creates contextual representations│
                    └───────────────────┬────────────────────┘
                                        │
                                        ▼
                         ┌───────────────────────────────┐
                         │          EMBEDDINGS           │
                         │                               │
                         │   Contextual representation   │
                         │   of the input sequence       │
                         └───────────────┬───────────────┘
                                         │
                                         │
                                         ▼
                    ┌────────────────────────────────────────┐
                    │               DECODER                  │
                    │                                        │
                    │     Generates the translated text      │
                    │       one word/token at a time         │
                    └───────────────────┬────────────────────┘
                                        │
                                        ▼
                         ┌───────────────────────────────┐
                         │      OUTPUT LAYERS            │
                         └───────────────┬───────────────┘
                                         │
                                         ▼
                         ┌───────────────────────────────┐
                         │       COMPLETE OUTPUT         │
                         │                               │
                         │   "Das ist ein Beispiel"      │
                         └───────────────────────────────┘


        ┌─────────────────────────────────────────────────────┐
        │                  DECODER LOOP                       │
        │                                                     │
        │  Partial output → Decoder → Next word/token         │
        │       ↑                         │                   │
        │       └─────────────────────────┘                   │
        │                                                     │
        │  Example:                                           │
        │                                                     │
        │  "Das"                                              │
        │    ↓                                                │
        │  "Das ist"                                          │
        │    ↓                                                │
        │  "Das ist ein"                                      │
        │    ↓                                                │
        │  "Das ist ein Beispiel"                             │
        └─────────────────────────────────────────────────────┘


### BERT vs GPT
**BERT** : Bidirectional Encoder Representations from Transformers
- It is bidirectional
- It is used to understand the input text
- It is present on the encoding side

**GPT** : Generative Pre-Trained Transformer
- It is unidirectional
- It is used to generate the next word based on the understanding of previous words
- It is present on the decoding side

### Types of tasks
- Text Completion : It takes the input text and completes the sentence
- Zero-Shot : Completes a task without any explicit example like translation to another language
- Few-Shot : Few training examples are present and the classification

> LLM vs Transformer
> LLMs are based on the transformer architecture but not all LLMs are based on transformer architecture, few are based on convulational architecture.
> Also not all transformers are LLMs, they can be used for computer vision applications as well

## Utilizing large datasets
There are datasets available on the internet which can be used to train the LLMs, the major training dataset used is CommonCrawl.

> Pre-training a model like GPT costs around $4.6 million, since these models are reusable as foundational models this makes it easier for people to fine tune the models.

## GPT Architecture 
GPTs are trained on relatively simple next-word prediction tasks and work really well.
In GPT architecture, the model goes through a lot of iterations through transformer blocks which keeps on predicting the next word.
Each layer consists of below flow
`[ Input Text --> Preprocessing Steps --> Decoder --> Output Layers --> ]`
Output of one block acts as input on another block and this continues for many iterations.

This was originally designed for language  translation, GPT models are also capable of doing tasks other than translation.
**The ability to perform tasks that the model wasn't explicitly trained to perform is called an emergent behavior.**

## Steps in building a Large Language Model
1. Stage 1 : This stage  involves building an LLM and after Pre-Training it becomes a foundation model
a. Data preparation & sampling
b. Attention Mechanism
c. LLMs Architecture
d. Pre-training

2. Stage 2 : In this stage the foundation model is trained and evaluated
a. Training Loop
b. Model Evaluation
c. Load Pre-trained weights
d. Fine Tuning

3. Stage 3 : This stage involves deciding the final use case of the model by fine tuning
Fine tuning can convert foundation model into a personal assistant or classifier depending on the data it is trained on



 
