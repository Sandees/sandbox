
%pip install sentence-transformers databricks-genai-inference azure-search-documents


from databricks_genai_inference import ChatCompletion

llm_model = "databricks-meta-llama-3-70b-instruct"

def generate_labels_llama3(subject, email_body):
    prompt = f"""
    Classify the email according to the categories below:

    Categories:
    1. pii_detected: Contains sensitive personal data? (true/false)
    2. external_contacts: Contains contacts outside the Shell network? (true/false)
    3. home_addresses: Contains home addresses? (true/false)
    4. financial_information: Mentions profit margins, pricing, cost structures? (true/false)
    5. client_contracts: Contains client lists, contracts, or sales data? (true/false)
    6. strategic_documents: Mentions marketing plans, product development, or expansion plans? (true/false)

    Email Subject: "{subject}"
    Email Body: "{email_body}"

    Provide your response strictly in JSON format:
    {{
        "pii_detected": bool,
        "external_contacts": bool,
        "home_addresses": bool,
        "financial_information": bool,
        "client_contracts": bool,
        "strategic_documents": bool
    }}
    """

    response = ChatCompletion.create(
        model=llm_model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.0
    )

    # Extract JSON response safely
    import json, re
    json_output = re.search(r'\{.*?\}', response.message).group(0)
    labels = json.loads(json_output)

    return labels




import pandas as pd
from sentence_transformers import SentenceTransformer

# Load embedding model
embedding_model = SentenceTransformer('all-mpnet-base-v2')

# Sample emails dataset
email_data = [
    ("1", "john.doe@shell.com", ["alice@shell.com"], "Pricing Strategy", "We plan to reduce pricing by 20% next quarter."),
    ("2", "emma.watson@shell.com", ["external@yahoo.com"], "Meeting Details", "Meeting at my home, 22 Baker Street."),
]

df_emails = pd.DataFrame(email_data, columns=["email_id", "sender", "recipients", "subject", "email_body"])

# Function to generate embeddings & labels
def process_email(row):
    embedding = embedding_model.encode(row["email_body"]).tolist()
    labels = generate_labels_llama3(row["subject"], row["email_body"])
    return pd.Series({"embedding": embedding, **labels})

# Apply processing
df_labels = df_emails.apply(process_email, axis=1)
df_final = pd.concat([df_emails, df_labels], axis=1)



from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import *
from azure.core.credentials import AzureKeyCredential

endpoint = "https://<your-search-service>.search.windows.net"
key = "<your-admin-api-key>"
index_name = "email-llama3-index"

index_client = SearchIndexClient(endpoint, AzureKeyCredential(key))

fields = [
    SimpleField("email_id", type="Edm.String", key=True, filterable=True),
    SearchField("sender", type="Edm.String", searchable=True, filterable=True),
    SearchField("recipients", type="Collection(Edm.String)", searchable=True),
    SearchField("subject", type="Edm.String", searchable=True),
    SearchField("semantic_vector", type="Collection(Edm.Single)", searchable=True, vector_search_dimensions=768, vector_search_configuration="vector-config"),
    SimpleField("pii_detected", "Edm.Boolean", filterable=True),
    SimpleField("external_contacts", "Edm.Boolean", filterable=True),
    SimpleField("home_addresses", "Edm.Boolean", filterable=True),
    SimpleField("financial_information", "Edm.Boolean", filterable=True),
    SimpleField("client_contracts", "Edm.Boolean", filterable=True),
    SimpleField("strategic_documents", "Edm.Boolean", filterable=True)
]

vector_search = VectorSearch(
    algorithms=[VectorSearchAlgorithmConfiguration(name="vector-config", kind="hnsw")]
)

semantic_config = SemanticConfiguration(
    name="semantic-config",
    prioritized_fields=SemanticPrioritizedFields(
        title_field="subject",
        keywords_fields=["subject"]
    )
)

index = SearchIndex(name=index_name, fields=fields, vector_search=vector_search, semantic_settings=[semantic_config])

index_client.create_or_update_index(index=index)


from azure.search.documents import SearchClient

search_client = SearchClient(endpoint, index_name, AzureKeyCredential(key))

documents = []
for _, row in df_final.iterrows():
    documents.append({
        "email_id": row["email_id"],
        "sender": row["sender"],
        "recipients": row["recipients"],
        "subject": row["subject"],
        "semantic_vector": row["embedding"],
        "pii_detected": row["pii_detected"],
        "external_contacts": row["external_contacts"],
        "home_addresses": row["home_addresses"],
        "financial_information": row["financial_information"],
        "client_contracts": row["client_contracts"],
        "strategic_documents": row["strategic_documents"]
    })

search_client.upload_documents(documents)



# Hybrid search example
query_text = "profit margins pricing"
query_vector = embedding_model.encode(query_text).tolist()

results = search_client.search(
    search_text=query_text,
    query_type="semantic",
    semantic_configuration_name="semantic-config",
    vector_queries=[{
        "vector": query_vector,
        "fields": "semantic_vector",
        "k": 5
    }],
    filter="financial_information eq true",
    select=["email_id", "subject", "sender"],
    top=5
)

print("\nHybrid Search Results:")
for result in results:
    print(f"ID: {result['email_id']}, Subject: {result['subject']}, Sender: {result['sender']}")
