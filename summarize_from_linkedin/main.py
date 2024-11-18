from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from linkedin import scrape_linkedin_profile
from Agents.linkedin_lookup_agent import lookup
from output_parsers import summary_parser

def summarizer_from_linkedin(name:str):
    summary_template = """
            an Linkedin information about a person is given below, inside 3 backticks. I want you to create:
            1- a short summary
            2- two interesting facts about them
            from text.

            Information: '''
                {information}
            '''
            \n{format_instructions}
        """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"],
        template=summary_template,
        partial_variables={"format_instructions":summary_parser.get_format_instructions()}
    )
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    linkedin_data = scrape_linkedin_profile(lookup(name), mock=False)

    chain = summary_prompt_template | llm | summary_parser # OR chain = LLMChain(llm=llm, prompt=summary_prompt_template)
    res = chain.invoke(input={"information": linkedin_data})
    return res


if __name__ == '__main__':
    load_dotenv()
    print(summarizer_from_linkedin(""))

