import google.generativeai as genai

api_key = "your_api_key"
def generate_customer_insights(customer,risk_category,products):
    genai.configure(api_key=api_key)

    prompt = f"""
    Generate detailed, personalised insights about the following customer based on the data given below:
    
    Customer Details:
    Age : {customer['age']},
    Yearly Salary : Rs. {customer['yearly_salary']:,.2f},
    Total Investment : Rs. {customer['total_investment']:,.2f},
    Total Loans : Rs. {customer['total_loans']:,.2f},
    and has a {risk_category} risk profile 
    
    Also reason why the following products must be recommended: {products}
    """

    try:
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating insights: {str(e)}"