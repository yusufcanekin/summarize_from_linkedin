from langchain_community.tools.tavily_search import TavilySearchResults
def get_linkedin_tavily(name:str):
    search = TavilySearchResults()
    res = search.run(str(name))
    return res