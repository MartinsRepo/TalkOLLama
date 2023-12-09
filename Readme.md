![file not found](header.jpg)
# talkollama - "Alexa" like Voice Embedding
**LangChain** based **LLama model** with microphone input and voice output.

## A) OLLama

OLLama is a framework that allows you to get up and running with large language models like Llama 2 locally on your machine. It’s designed to be lightweight, extensible, and user-friendly.

### Quick Links
-   **Homepage**: [OLLama GitHub Repository](https://github.com/jmorganca/ollama)
-   **Model Library**: [OLLama Model Library](https://github.com/jmorganca/ollama)
-   **Installation Guide**: [OLLama Installation](https://github.com/jmorganca/ollama)

### Installation

To install OLLama, you can use the following command for Linux & WSL2:


```sh
curl https://ollama.ai/install.sh | sh
```
For detailed manual installation instructions, please refer to the [installation guide](https://github.com/jmorganca/ollama).

## Usage


Here’s how you can interact with OLLama models:

### Pull a Model

To download or update a model:

```sh
ollama pull <model-name>

```

### Run a Model


To run a model:

```sh
ollama run <model-name>

```

### List Models

To list all available models:

```sh
ollama list

```

### Delete a Model

To remove a model from your system:

```sh
ollama delete <model-name>

```
For more detailed usage and commands, please visit the [OLLama GitHub Repository](https://github.com/jmorganca/ollama). 

## OLLama Langchain Binding

### Usage

To use LangChain with OLLama, you need to install the LangChain package and set up the desired language model. Here’s a quick guide:

### Installation

First, install the LangChain package:

```sh
pip install langchain

```
### Model Setup

Define your model with the OLLama binding:
```python
from langchain.llms import Ollama

# Set your model, for example, Llama 2 7B
llm = Ollama(model="llama2:7b")
```
### Running Queries

Execute queries using the LangChain chain:
```python
from langchain.chains import RetrievalQA

# Create a chain with OLLama as the retriever
qachain = RetrievalQA.from_chain_type(ollama, retriever=vectorstore.as_retriever())

# Run a query
response = qachain({"query": "Your question here"})
```
For more detailed information on setting up and using OLLama with LangChain, please refer to the [OLLama documentation](https://python.langchain.com/docs/integrations/llms/ollama) and [LangChain GitHub repository](https://js.langchain.com/docs/integrations/chat/ollama).



## B) talkollama Installation
### Virtual Python Environment
A virtual environment is a Python environment such that the Python interpreter, libraries and scripts installed into it are isolated from those installed in other virtual environments.

**Prerequisites:** Installation manuals can be found here: 
 - https://www.dedicatedcore.com/blog/install-pyenv-ubuntu/ 

**Install Python 3.11.4**

With `pyenv` installed, you can now install Python 3.11.4:

```sh
pyenv install 3.11.4

```

**Set up the virtual environment**

Next, you’ll want to create a virtual environment using the installed Python version:

```sh
pyenv virtualenv 3.11.4 otalk

```

**Activate the virtual environment**

To activate the ‘otalk’ virtual environment:

```sh
pyenv activate otalk

```

You should now be using Python 3.11.4 within your ‘otalk’ virtual environment. To verify, you can check the Python version:

```sh
python --version

```

The output should show Python 3.11.4. When you’re done working in the virtual environment, you can deactivate it:
```sh
pyenv deactivate

```

For more detailed instructions and troubleshooting, please refer to the [pyenv documentation](https://github.com/pyenv/pyenv) and the [virtualenv documentation](https://virtualenv.pypa.io/en/latest/installation.html).

### Repo Cloning
```sh
git clone 

```

### Installing Dependencies
```sh
pip install -r requirements.txt

```

## C) Models
### 1.  LLAMA Model used
**Samantha AI**

Samantha AI is an artificial intelligence system that has been depicted in various forms of media and technology. It is often personified through a female voice and is designed to interact with users in a natural and intuitive way.

**Usage**

The concept of Samantha AI is used to inspire the development of advanced AI systems that can assist with a variety of tasks, from providing information to offering emotional support. It represents the aspiration to create AI that can understand and respond to human emotions and behaviors in a meaningful way.

For more information on the development and capabilities of AI systems like Samantha, you can refer to the [BBC article on virtual assistants](https://www.bbc.com/news/technology-26147990) and the [Wikipedia page for the film “Her”](https://en.wikipedia.org/wiki/Her_%28film%29). Enjoy exploring the fascinating world of artificial intelligence! 😊

You can find more information about Samantha AI at the following link: [Meet SAMANTHA AI](https://www.meetsamantha.ai/). This website provides insights into the concept and applications of Samantha AI.


### 2. Speech Detection Models
We are using the **Voice Detection** from  [VOSK](https://alphacephei.com/vosk/).
The tested model can be found below, feel free to try out different once from [VOSK Models](https://alphacephei.com/vosk/models).
|            Model    |Link                          |
|------------------------------------|-------------------------------|
|**vosk-model-de-0.21** |https://alphacephei.com/vosk/models/[vosk-model-de-0.21](https://alphacephei.com/vosk/models/vosk-model-de-0.21.zip)

Unpack and move it to the **\languagemodels**.
### 3. Voice Output
The **gTTS (Google Text-to-Speech)** is a Python library and CLI tool that interfaces with Google Translate’s text-to-speech API. [It allows you to convert text into spoken audio, which can be saved as an MP3 file](https://pypi.org/project/gTTS/). 

**Features**
- Customizable speech-specific sentence tokenizer.
- Customizable text pre-processors for pronunciation corrections.
- Supports multiple languages.

**Installation**
To install gTTS, run the following command:
```sh
pip install gTTS (already done in requirements.txt)
```

Here's a simple example of how to use gTTS:

```python
from gtts import gTTS

tts = gTTS('hello')
tts.save('hello.mp3')
```
For more information and examples, visit the [gTTS documentation](http://gtts.readthedocs.org/).

**License**

The MIT License (MIT)


## D) Run the Model

Don't forget to adapt your models and pathes at the marked lines in talkollama.py.
```sh
python talkllama.py

```


> Written with [StackEdit](https://stackedit.io/).
