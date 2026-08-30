# ===========================
# PROMPT - CUSTOMER COMPLAINTS
# ===========================

COMPLAINT_PROMPT = """
You are a customer of a gas station.

Your task is to write a realistic complaint addressed to the customer service department.

Information:

- Date: {date}
- Station ID: {station_id}
- Station name: {station_name}
- Category: {category}
- Problem encountered: {reason}
- Severity level: {severity}
- Number of affected customers: {affected}

Instructions:

- Write ONE single complaint representing all affected customers.
- The complaint must be natural, realistic, and credible.
- Describe the consequences experienced by the customers.
- Express professional dissatisfaction without being aggressive.
- Do not use a list.
- Do not mention that you are an AI.
- Keep the complaint short, as if it had been written by a real customer.
- Write the entire complaint in French.
- Do not include an English translation.
- Do not add any explanation before or after the complaint.

Complaint:
"""


# ===========================
# PROMPT - MAINTENANCE REPORT
# ===========================

MAINTENANCE_PROMPT = """
You are a maintenance technician working for a gas station network.

Your task is to write a professional technical maintenance report.

Information:

- Date: {date}
- Station ID: {station_id}
- Station name: {station_name}
- Pump: {pump_id}
- Failure type: {failure_type}
- Estimated repair duration: {start_date} to {expected_end_date} day(s)
- Repair completion date: {end_date}
- Technician: {technician}
- Status: {status}

The report must include:

- the context of the intervention
- the symptoms observed
- the diagnosis performed
- the actions carried out
- the validation tests
- any relevant recommendations

Instructions:

- Use a professional and technically accurate style.
- Base the report only on the information provided above.
- Do not invent technical details that are not supported by the provided information.
- Do not mention that you are an AI.
- Write between 150 and 250 words.
- Write the entire report in French.
- Do not include an English translation.
- Do not add any explanation before or after the report.

Maintenance report:
"""
