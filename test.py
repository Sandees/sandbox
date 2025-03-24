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
