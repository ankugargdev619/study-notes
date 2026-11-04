The pre-training is very expensive task and therefore it is not feasible for everyone to do this.
We can use an already pre-trained model which can be fine tuned for a specific task later.

## Different categories of fine-tuning
The most common ways to fine-tune language models are instruction fine-tuning and classification fine-tuning. Instruction fine tuning involves training a language model on a set of tasks using specific instructions to improve its ability to understand and execute tasks described in natural language prompts.

> Choosing the right approach for fine-tuning
> Instruction fine-tuning improves a model's ability to understand and generate responses based on specific user instructions. Instruction fine-tuning is best suited for models that need to handle a variety of tasks based on complex user instructions, improving flexibility and interaction quality. Classification fine-tuning is ideal for projects requiring precise categorization of data into predefined classes, such as sentiment analysis or spam detection.

# Preparing the dataset
The dataset needs to be cleaned and prepared for the fine tuning the pre-trained model.
It has below steps
1. Doaloading the datset
2. Preprocessing the dataset
3. Create data loaders

# Creating data loaders
Now the processed data has to be loaded for training. Earlier we used sliding window approach for preparing the dataset however now we don't need this for classification training because each example acts as a standalone example.
 
With this new training data, a new problem arises. The length of the training data is not always same. To deal with this, we have 2 options:
i) Truncate all messages to the length of the shortest message
ii) Pad all messages to the length of the longest message 
Option (i) is cheaper but results in inaccurate results due to lost context so in our case we will use option (ii)

We can use `<|endoftext|>` as a padding token.

# Adding classification head
We must modify the pretrained LLM to prepare it for classification fine-tuning. To do so, we replace the original output layer, which maps the hidden representation to a vocabulary, with smaller output layer that maps to two classes: 0 and 1. We use the same model as before, except we replace the output layer.

> Output layer nodes
> We could technically use a single output node since we are dealing with a binary classification task. It would require modifying the loss function. We choose a more general approach where the number of output nodes matches the number of classes. For example, for a three-class problem, such as classifying news articles as "Technology", "Sports" or "Politics" we would use three output nodes.


# Fine-tuning the model on supervised data
We must define and use the training function to fine-tune the pretrained LLM and improve its spam classification accuracy. The training loop is same overall training loop we used for pre-training, the only difference is that we calculate the classification accuracy instead of generating a sample text to evaluate the model.
