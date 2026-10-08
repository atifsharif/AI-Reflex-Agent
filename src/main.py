
import json
from openai import OpenAI

from config import OPENAI_API_KEY
from functions import AVAILABLE_FUNCTIONS
from tools_schema import tools_schema


if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is missing")

client = OpenAI(api_key=OPENAI_API_KEY)


SYSTEM_PROMPT = """
You are an expert CRM Lead Qualifier Agent.

Follow these steps:
1. Extract the company domain from the lead's email.
2. Call lookup_domain_info and check_crm_history.
3. Collect the company and CRM information.
4. Call calculate_lead_score using the collected data.
5. Return a clear lead qualification summary.

Do not invent company or CRM information.
"""


def run_agent(user_prompt: str):
    """Execute the CRM Lead Qualifier Agent."""

    print("\n--- Running Lead Qualifier Agent ---")

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt}
    ]

    collected_data = {}

    for _ in range(10):
        print("\n[AI Thinking...]")

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=tools_schema,
            tool_choice="auto"
        )

        response_message = response.choices[0].message
        messages.append(response_message)

        if not response_message.tool_calls:
            print("\n--- FINAL AGENT SUMMARY ---")
            print(response_message.content)
            return response_message.content

        for tool_call in response_message.tool_calls:
            print("printitng tool call",tool_call,tool_call.function.name,tool_call.function.arguments)

            function_name = tool_call.function.name
            function_to_call = AVAILABLE_FUNCTIONS.get(function_name)

            try:
                if function_to_call is None:
                    raise ValueError(
                        f"Unknown function: {function_name}"
                    )

                function_args = json.loads(
                    tool_call.function.arguments
                )

                if function_name == "calculate_lead_score":
                    if not all(
                        key in collected_data
                        for key in ("domain_info", "crm_history")
                    ):
                        raise ValueError(
                            "Domain and CRM information must "
                            "be collected before scoring."
                        )

                    # Use verified tool results instead of
                    # relying on model-generated summary data.
                    function_args = {
                        "data_summary": json.dumps(collected_data)
                    }

                function_result = function_to_call(
                    **function_args
                )

                if function_name == "lookup_domain_info":
                    collected_data["domain_info"] = json.loads(
                        function_result
                    )

                elif function_name == "check_crm_history":
                    collected_data["crm_history"] = json.loads(
                        function_result
                    )

                elif function_name == "calculate_lead_score":
                    collected_data["lead_score"] = json.loads(
                        function_result
                    )

            except (ValueError, TypeError, KeyError) as error:
                function_result = json.dumps({
                    "error": str(error)
                })

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": function_result
            })

    raise RuntimeError("Agent exceeded maximum iterations")


if __name__ == "__main__":
    email = input("Enter lead email: ").strip()

    if not email or "@" not in email:
        raise ValueError("Enter a valid lead email")

    run_agent(f"Qualify this sales lead: {email}")
