
tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "lookup_domain_info",
            "description": (
                "Retrieve company industry, employee size "
                "and revenue using its domain."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "domain": {
                        "type": "string",
                        "description": "Company domain, e.g. acmecorp.com"
                    }
                },
                "required": ["domain"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_crm_history",
            "description": (
                "Check CRM history, lead status "
                "and previous engagement notes."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "Full email address of the lead"
                    }
                },
                "required": ["email"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_lead_score",
            "description": (
                "Calculate lead priority using combined "
                "company and CRM information."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "data_summary": {
                        "type": "string",
                        "description": (
                            "JSON string containing domain_info "
                            "and crm_history objects"
                        )
                    }
                },
                "required": ["data_summary"]
            }
        }
    }
]
