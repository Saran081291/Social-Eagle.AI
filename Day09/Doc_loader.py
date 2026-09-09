from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("Day08\\Assignment\\CAIE_JSON_Prompting_Tamil_Culture_Assignmentt.pdf")
documents = loader.load()
print(documents[0].page_content)