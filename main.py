from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import SQLDatabaseToolkit, create_sql_agent


# Replace with your PostgreSQL connection details
db = SQLDatabase.from_uri("postgresql://postgres:reddy1406@localhost/SkillSage_niceone")
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, api_key="sk-proj-WzASEx9XPHuZgVUFyXZ3T3BlbkFJYiMP1pBoTxLY1TaWaPTa" )



toolkit = SQLDatabaseToolkit(db=db, llm=llm)
agent_executor = create_sql_agent(llm=llm, toolkit=toolkit, verbose=True)


# Define your natural language query
user_query = "list the "

# Execute the query using the agent
result = agent_executor.invoke(user_query)

# Output the result
print(result)
