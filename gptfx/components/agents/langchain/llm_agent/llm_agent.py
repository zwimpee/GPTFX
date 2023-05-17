import asyncio

import click
import tensorflow as tf
from langchain.agents import initialize_agent, AgentType, load_tools
from langchain.callbacks import Callbacks, PrintCallback
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from gptfx.pipeline.configs import Config


@click.command()
@click.option('--config_path', type=str)
def llm_agent(config_path: str) -> None:
    # Load the configuration file
    with tf.io.gfile.GFile(config_path, 'rb') as f:
        config_data = f.read()
    config = Config.from_json_dict(config_data)

    # Initialize the language models
    chat = ChatOpenAI(temperature=0.9)
    llm = OpenAI(temperature=0.9)

    # Load some tools to use. Note that the `llm-math` tool uses an LLM, so we need to pass that in.
    tools = load_tools(config.tools, llm=llm)

    # Generate the chat prompt
    system_message_prompt = SystemMessagePromptTemplate.from_template("You are a helpful assistant.")
    human_message_prompt = HumanMessagePromptTemplate.from_template("{task}")
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    # Initialize the agent
    agent = initialize_agent(
        tools=tools,
        llm=chat,
        agent=config.agent_type or AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=config.verbose or True
    )

    # Create an agent chain
    chain = LLMChain(llm=agent, prompt=chat_prompt)

    # Define a print callback for logging
    callbacks = Callbacks([PrintCallback()])

    # Save the result of the agent's operation
    task = config.task or ''
    output_path = tf.io.gfile.join(config.data_root, 'llm_agent', 'llm_agent.txt')
    with tf.io.gfile.GFile(output_path, 'w') as f:
        result = asyncio.run(chain.apredict(callbacks=callbacks, task=task))  # Use async method
        f.write(result)


if __name__ == '__main__':
    llm_agent()
