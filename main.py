%pip install --upgrade requests langchain databricks-langchain langchain-databricks langchain-community
import requests
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.chat_models import ChatDatabricks
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import Tool, initialize_agent

llm = ChatDatabricks(endpoint="databricks-llama-4-maverick",temperature=0.1)
def search_clinical_trials(query: str) -> str:
    url = "https://clinicaltrials.gov/api/v2/studies"
    params = {"query.term": query, "pageSize": 3}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        studies = data.get("studies", [])
        
        if not studies:
            return f"No studies found for '{query}'."
        
        result = f"Top studies for '{query}':\n"
        for i, study in enumerate(studies, 1):
            protocol = study.get("protocolSection", {})
            title = protocol.get("identificationModule", {}).get("officialTitle", "N/A")
            nct_id = protocol.get("identificationModule", {}).get("nctId", "N/A")
            result += f"{i}. Title: {title}\n   NCT ID: {nct_id}\n"
        return result.strip()
    except Exception as e:
        return f"Error: {str(e)}"
def extract_relevant_fields_from_query(query: str) -> str:
    known_fields = [
        "nctId", "officialTitle", "briefTitle", "conditions", "interventions", 
        "locations", "phase", "enrollmentCount", "startDate", "completionDate",
        "studyType", "studyStatus", "gender", "minimumAge", "maximumAge",
        "sponsor", "locationCity", "locationCountry", "collaborators", 
        "primaryOutcome", "secondaryOutcome"
    ]
    
    prompt = f"""
    Analyze the query: "{query}"
    From this list of ClinicalTrials.gov fields: {", ".join(known_fields)},
    return only a comma-separated list of field names directly relevant to the query.
    """
    
    try:
        extracted_fields = llm.predict(prompt).strip()
        return f"Relevant fields: {extracted_fields}"
    except Exception as e:
        return f"Error extracting fields: {str(e)}"

from langchain.agents import Tool

tools = [
    Tool(
        name="SearchStudies",
        func=search_clinical_trials,
        description="Search ClinicalTrials.gov for studies by disease, condition, or keyword. Returns study titles and NCT IDs."
    ),
    Tool(
        name="GetRelevantStudyFields",
        func=extract_relevant_fields_from_query,
        description="Extract relevant ClinicalTrials.gov field names based on the user's query."
    )
]
# Custom System Prompt for Clarity
system_prompt = """
You are an assistant that helps users explore clinical trials from ClinicalTrials.gov. 
Given a user query:
1. Use 'SearchStudies' to find relevant studies based on the user query.
2. Use 'GetRelevantStudyFields' to identify relevant field names based on the user query.
3. Generate response to the user query.
Stop after using both tools once and provide the response.
"""
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent_type="zero-shot-react-description",
    verbose=True,
    system_prompt=system_prompt  # Custom prompt for better guidance
)
response = agent.run("What are the studies relating to lung cancer?")
print(response)
