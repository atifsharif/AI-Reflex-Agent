
import json


def lookup_domain_info(domain: str) -> str:
    """Retrieve mock company information from a domain."""

    domain = domain.strip().lower()
    print(f"-> TOOL ACTIVATED: Looking up {domain}")

    mock_data = {
        "acmecorp.com": {
            "industry": "Software/SaaS",
            "size": "501-1000 employees",
            "revenue": "$50M - $100M"
        },
        "widgetco.net": {
            "industry": "Manufacturing",
            "size": "100-250 employees",
            "revenue": "$10M - $25M"
        },
        "globalfin.org": {
            "industry": "Financial Services",
            "size": "5000+ employees",
            "revenue": "$1B+"
        }
    }

    info = mock_data.get(domain, {
        "industry": "Unknown",
        "size": "N/A",
        "revenue": "N/A"
    })

    return json.dumps(info)


def check_crm_history(email: str) -> str:
    """Retrieve mock CRM engagement history."""

    email = email.strip().lower()
    print(f"-> TOOL ACTIVATED: Checking CRM for {email}")

    mock_data = {
        "jane@acmecorp.com": {
            "last_contact": "2025-11-15",
            "status": "Cold Lead",
            "notes": "Attended webinar, no follow-up yet."
        },
        "bob@widgetco.net": {
            "last_contact": "2025-12-01",
            "status": "Active Opportunity",
            "notes": "Discussed Q1 budget and product integration."
        },
        "default": {
            "last_contact": "N/A",
            "status": "No Record",
            "notes": "New lead, first contact opportunity."
        }
    }

    history = mock_data.get(email, mock_data["default"])
    return json.dumps(history)


def calculate_lead_score(data_summary: str) -> str:
    """Calculate lead priority from domain and CRM data."""

    print("-> TOOL ACTIVATED: Calculating lead score")

    data = json.loads(data_summary)

    domain_info = data.get("domain_info", {})
    crm_history = data.get("crm_history", {})

    score = "Low"

    if domain_info.get("revenue", "").startswith("$1B+"):
        score = "High"
    elif crm_history.get("status") == "Active Opportunity":
        score = "High"
    elif domain_info.get("revenue", "").startswith("$50M"):
        score = "Medium"

    return json.dumps({"lead_score": score})


# Function registry: maps tool names to Python functions
AVAILABLE_FUNCTIONS = {
    "lookup_domain_info": lookup_domain_info,
    "check_crm_history": check_crm_history,
    "calculate_lead_score": calculate_lead_score
}
