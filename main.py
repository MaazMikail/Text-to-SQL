from langchain.chat_models import ChatOpenAI
from langchain.prompts import (

        ChatPromptTemplate,
        HumanMessagePromptTemplate,
        MessagesPlaceholder
)
from langchain.schema import SystemMessage
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from tools.sql import run_query_tool, list_tables, describe_table_tool
from report import html_tool
from chat_model_start_handler import ChatModelStartHandler


from dotenv import load_dotenv
load_dotenv()

memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)

tables = list_tables()
handler = ChatModelStartHandler()
chat = ChatOpenAI(

        callbacks=[handler]
)
prompt = ChatPromptTemplate(

        messages=[
                SystemMessage(content=
                              
            ("You are an AI that has access to a SQLite database \n"
             f"The database has tables of: {tables}\n"
             "Do not make any assumptions about what tables exists "
             "or what columns exists. Instead, use the 'describe_tables' fuction" 
                           
                )),
                MessagesPlaceholder(variable_name='chat_history'),
                HumanMessagePromptTemplate.from_template("{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad")
        ]
)

tools = [run_query_tool, describe_table_tool, html_tool]

agent = OpenAIFunctionsAgent(

    llm=chat,
    prompt=prompt,
    tools=tools
)

agent_executor = AgentExecutor(

        agent=agent,
       # verbose=True,
        tools=tools,
        memory=memory
)

#agent_executor("How many users in our database have provided a shipping address?")
agent_executor("Summarize the top 5 most popular products")
#agent_executor("How many orders are there? Write results to an HTML report")
