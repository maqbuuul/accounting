# 💰 Accounting Dashboard

A comprehensive financial analytics and reporting system built with Python and Streamlit. This dashboard provides real-time insights into revenue, expenses, profit margins, and cash flow analysis.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.29.0-FF4B4B.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🎯 Features

### Core Functionality
- ✅ **Revenue & Expense Tracking** - Monitor all financial transactions
- 📊 **Interactive Visualizations** - Dynamic charts using Plotly
- 📈 **Trend Analysis** - Month-over-month growth tracking
- 💰 **Profit Margin Calculation** - Real-time profitability metrics
- 💵 **Cash Flow Analysis** - Track money in and out
- 📥 **Multi-Format Export** - Excel, CSV, and PDF reports

### Key Metrics Dashboard
- Total Revenue with MoM growth
- Total Expenses with percentage of revenue
- Net Profit with profitability status
- Profit Margin with health indicator

### Visualizations
1. **Revenue vs Expenses Trend** - Line chart showing monthly trends
2. **Expense Breakdown** - Pie chart by category
3. **Revenue by Category** - Horizontal bar chart
4. **Monthly Profit/Loss** - Bar chart with color coding
5. **Cash Flow Analysis** - Combined bar and line chart

### Reports
- Summary report with KPIs
- Detailed revenue transactions
- Detailed expense transactions
- Category-wise breakdowns
- Exportable data tables

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or download the project files**
```bash
# Create a project directory
mkdir accounting-dashboard
cd accounting-dashboard
```

2. **Save the files**
   - Save `app.py` (the main Streamlit application)
   - Save `requirements.txt` (dependencies)
   - Save this `README.md` (documentation)

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Running the Application

```bash
streamlit run app.py
```

The dashboard will open automatically in your default web browser at `http://localhost:8501`

## 📖 Usage Guide

### Getting Started

1. **Generate Sample Data**
   - Click "🔄 Generate Sample Data" in the sidebar
   - This creates 12 months of realistic financial data

2. **Upload Your Own Data**
   - Click "📁 Upload Data" in the sidebar
   - Supported formats: CSV, Excel (.xlsx)
   - Required columns: `Date`, `Category`, `Amount`, `Type` (Revenue/Expense)

3. **Filter Data**
   - Use the date range selector:
     - Last 3 Months
     - Last 6 Months
     - Last 12 Months
     - All Time

### Understanding the Dashboard

#### KPI Cards (Top Section)
- **Total Revenue**: Sum of all revenue with month-over-month growth
- **Total Expenses**: Sum of all expenses with percentage of revenue
- **Net Profit**: Revenue minus expenses
- **Profit Margin**: Percentage of revenue retained as profit

#### Charts Section
- **Revenue vs Expenses Trend**: Track financial performance over time
- **Expense Breakdown**: See where your money goes
- **Revenue by Category**: Identify top revenue sources
- **Monthly Profit/Loss**: Visualize profitability by month
- **Cash Flow Analysis**: Understand money movement

#### Reports Section
Four tabs provide detailed data:
1. **Summary**: Category-wise revenue and expense summaries
2. **Revenue**: All revenue transactions
3. **Expenses**: All expense transactions
4. **All Transactions**: Complete transaction history

### Exporting Reports

Three export options available:

1. **📊 Excel Report** - Comprehensive multi-sheet workbook
   - Summary metrics
   - Monthly breakdown
   - Revenue by category
   - Expenses by category
   - All transactions

2. **📄 PDF Summary** - Executive summary with:
   - Key metrics
   - Financial analysis
   - Recommendations

3. **📋 CSV Data** - Raw transaction data for further analysis

## 📁 Data Format

### CSV/Excel Upload Format

Your data should have these columns:

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| Date | Date | Transaction date | 2025-10-15 |
| Category | String | Transaction category | Salaries, Sales, Rent |
| Amount | Number | Transaction amount | 15000.00 |
| Type | String | Revenue or Expense | Revenue |

### Example Data

```csv
Date,Category,Amount,Type
2025-10-01,Product Sales,25000,Revenue
2025-10-01,Salaries,15000,Expense
2025-10-05,Services,18000,Revenue
2025-10-10,Marketing,5000,Expense
```

## 🛠️ Technical Stack

- **Frontend**: Streamlit
- **Data Processing**: Pandas
- **Visualizations**: Plotly Express & Graph Objects
- **Excel Export**: OpenPyXL
- **Date Handling**: Python datetime

## 💡 Use Cases

### For Small Businesses
- Track monthly revenue and expenses
- Monitor profit margins
- Identify cost-saving opportunities
- Generate reports for stakeholders

### For Freelancers
- Monitor income streams
- Track business expenses
- Calculate quarterly taxes
- Analyze business growth

### For Startups
- Present financial metrics to investors
- Track burn rate
- Forecast cash flow
- Monitor unit economics

### For Accountants
- Client financial overview
- Variance analysis
- Budget vs actual reporting
- Financial trend analysis

## 📊 Sample Insights

The dashboard automatically generates:

### Financial Health Indicators
- Revenue growth trends
- Expense ratios
- Profit margin trends
- Cash flow patterns

### Automated Recommendations
- Growth trajectory assessment
- Cost management evaluation
- Expense-to-revenue ratio analysis

## 🎨 Customization

### Modify Categories

Edit the category lists in `app.py`:

```python
# Revenue categories
revenue_categories = ['Product Sales', 'Services', 'Consulting', 'Subscriptions', 'Other']

# Expense categories
expense_categories = ['Salaries', 'Rent', 'Marketing', 'Utilities', 'Supplies', 
                     'Insurance', 'Technology', 'Travel', 'Maintenance', 'Other']
```

### Adjust Tax Rate

Change the tax calculation (default is 10%):

```python
def calculate_totals(items):
    subtotal = items.reduce((sum, item) => sum + item.amount, 0)
    tax = subtotal * 0.15  # Change to 15%
```

### Color Schemes

Modify chart colors in the visualization functions:

```python
# Revenue color
line=dict(color='#10b981', width=3)  # Green

# Expense color
line=dict(color='#ef4444', width=3)  # Red

# Profit color
line=dict(color='#3b82f6', width=3)  # Blue
```

## 🔒 Security & Privacy

### Data Storage
- All data is stored in-session memory
- No data is sent to external servers
- Data is cleared when you close the browser

### File Uploads
- Files are processed locally
- No persistent storage
- Temporary files are automatically cleaned

### Best Practices
- Don't deploy with sensitive data on public servers
- Use environment variables for any API keys
- Implement authentication for production use

## 🐛 Troubleshooting

### Common Issues

**Issue**: "Module not found" error
```bash
Solution: pip install -r requirements.txt
```

**Issue**: Port already in use
```bash
Solution: streamlit run app.py --server.port 8502
```

**Issue**: Charts not displaying
```bash
Solution: Clear browser cache and refresh
```

**Issue**: File upload fails
```bash
Solution: Check file format matches requirements (CSV/XLSX)
Ensure required columns exist: Date, Category, Amount, Type
```

### Performance Tips

1. **Large Datasets**
   - Filter data by date range
   - Sample data for testing
   - Consider data aggregation

2. **Slow Loading**
   - Use date filters to reduce data
   - Cache repeated calculations
   - Optimize chart rendering

## 📈 Future Enhancements

### Planned Features
- [ ] Budget vs Actual comparison
- [ ] Forecasting with ML models
- [ ] Multi-currency support
- [ ] User authentication
- [ ] Database integration
- [ ] Automated email reports
- [ ] Mobile responsive design
- [ ] Dark mode theme
- [ ] Invoice generation
- [ ] Payment tracking
- [ ] Tax calculation by jurisdiction
- [ ] Multi-company support

### Advanced Analytics
- [ ] Predictive analytics
- [ ] Anomaly detection
- [ ] Seasonal trend analysis
- [ ] Customer segmentation
- [ ] Churn prediction

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see below:

```
MIT License

Copyright (c) 2025 Abdiwahid Hussein Ali

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 👨‍💻 Developer

**Abdiwahid Hussein Ali**  
Data Scientist & Machine Learning Engineer

- 📧 Email: maqbuul@outlook.com
- 📱 Phone: +254 471 777 2131
- 🌍 Location: Nairobi, Kenya
- 💼 [LinkedIn](your-linkedin-url)
- 🐙 [GitHub](your-github-url)

## 🙏 Acknowledgments

- Streamlit team for the amazing framework
- Plotly for interactive visualizations
- Pandas community for data manipulation tools
- Open-source community for inspiration

## 📞 Support

For questions, issues, or feature requests:

1. **GitHub Issues**: [Create an issue](your-repo-url/issues)
2. **Email**: maqbuul@outlook.com
3. **Documentation**: See this README

## 🌟 Show Your Support

If you find this project useful, please:
- ⭐ Star the repository
- 🐛 Report bugs
- 💡 Suggest new features
- 📢 Share with others

---

**Built with ❤️ for accounting professionals and small business owners**

Last Updated: October 2025