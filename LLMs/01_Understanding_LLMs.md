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



