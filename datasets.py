import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

fake = Faker()


def generate_accounting_data(n=100000):
    start_date = datetime(2022, 1, 1)
    data = []
    for _ in range(n):
        date = start_date + timedelta(days=np.random.randint(0, 1000))
        category = np.random.choice(
            [
                "Sales",
                "Marketing",
                "Rent",
                "Utilities",
                "Salaries",
                "Consulting",
                "Supplies",
            ]
        )
        amount = np.random.uniform(50, 5000)
        ttype = np.random.choice(["Revenue", "Expense"], p=[0.6, 0.4])
        data.append([date.strftime("%Y-%m-%d"), category, round(amount, 2), ttype])
    df = pd.DataFrame(data, columns=["Date", "Category", "Amount", "Type"])
    return df


# Generate sample data
df = generate_accounting_data(50000)
df.to_csv("sample_accounting.csv", index=False)
df.to_excel("sample_accounting.xlsx", index=False)


# Create PDF (summary)
def create_sample_pdf(df):
    summary = df.groupby("Type")["Amount"].sum().reset_index()
    summary["Amount"] = summary["Amount"].map("${:,.2f}".format)

    c = canvas.Canvas("sample_accounting.pdf", pagesize=letter)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 750, "Sample Accounting Report")

    y = 700
    for _, row in summary.iterrows():
        c.setFont("Helvetica", 12)
        c.drawString(50, y, f"{row['Type']}: {row['Amount']}")
        y -= 25
    c.save()


create_sample_pdf(df)
print("✅ Generated sample CSV, Excel, and PDF files successfully!")
