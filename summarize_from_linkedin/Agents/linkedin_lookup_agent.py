from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from Tools.tools import get_linkedin_tavily

load_dotenv()

def lookup(name:str):
    llm = ChatOpenAI(
        temperature = 0,
        model_name="gpt-4"
    )
    template = """
        Given the full name {name_of_person} of a person, I want you to get me the url link to that specific person's Linkedin profile page. 
        Your answer should contain only an URL.
    """
    prompt_template = PromptTemplate(input_variables =["name_of_person"], template=template)

    tools_for_agent = [
        Tool(
            name= "Crawl Google 4 linkedin profile page",
            func = get_linkedin_tavily,
            description="useful for when you need to get the Linkedin Page URL" # LLM will know whether use this tools or not via looking its description.
        )
    ]
    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt) # This one is like a recipe, tells llm what to do
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)# This one runs the code in runtime
    response = agent_executor.invoke(
        input={"input":prompt_template.format_prompt(name_of_person=name)}# formatting the prompt template and passing it allows us to override react_prompt
    )
    linkedin_url = response["output"]
    return linkedin_url