# 🚀 Accounting Dashboard - Complete Setup Guide

This guide will walk you through setting up the Accounting Dashboard from scratch, even if you're new to Python.

## 📋 Prerequisites Check

Before starting, verify you have:

- [ ] Computer with Windows, Mac, or Linux
- [ ] Internet connection
- [ ] Administrative/sudo access (for installations)
- [ ] 500MB free disk space

## 🔧 Step 1: Install Python

### Windows

1. **Download Python**
   - Go to https://www.python.org/downloads/
   - Download Python 3.8 or higher
   - Run the installer

2. **IMPORTANT**: Check "Add Python to PATH" during installation

3. **Verify Installation**
   ```cmd
   python --version
   ```
   Should show: `Python 3.x.x`

### Mac

1. **Using Homebrew** (Recommended)
   ```bash
   # Install Homebrew if not installed
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   
   # Install Python
   brew install python
   ```

2. **Verify Installation**
   ```bash
   python3 --version
   ```

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3 python3-pip
python3 --version
```

## 📁 Step 2: Create Project Structure

### Windows (Command Prompt)
```cmd
mkdir accounting-dashboard
cd accounting-dashboard
```

### Mac/Linux (Terminal)
```bash
mkdir accounting-dashboard
cd accounting-dashboard
```

## 📝 Step 3: Create Project Files

Create these three files in your `accounting-dashboard` folder:

### File 1: `app.py`
Copy the entire Streamlit application code into this file.

### File 2: `requirements.txt`
```text
streamlit==1.29.0
pandas==2.1.4
plotly==5.18.0
openpyxl==3.1.2
python-dateutil==2.8.2
```

### File 3: `README.md`
Copy the README documentation into this file.

## 🔨 Step 4: Set Up Virtual Environment (Recommended)

### Why Use Virtual Environment?
- Keeps project dependencies isolated
- Prevents conflicts with other Python projects
- Easy to replicate environment

### Windows
```cmd
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# You should see (venv) in your command prompt
```

### Mac/Linux
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# You should see (venv) in your terminal
```

## 📦 Step 5: Install Dependencies

With your virtual environment activated:

```bash
pip install -r requirements.txt
```

This will install:
- Streamlit (web framework)
- Pandas (data manipulation)
- Plotly (visualizations)
- OpenPyXL (Excel support)
- Python-dateutil (date handling)

**Installation takes 2-5 minutes depending on internet speed**

## ▶️ Step 6: Run the Application

```bash
streamlit run app.py
```

**What happens next:**
1. Streamlit starts a local web server
2. Your default browser opens automatically
3. Dashboard loads at `http://localhost:8501`

**If browser doesn't open automatically:**
- Manually open: http://localhost:8501

## ✅ Step 7: Verify Everything Works

### Test 1: Generate Sample Data
1. Click "🔄 Generate Sample Data" in sidebar
2. You should see charts populate with data
3. KPI cards should show values

### Test 2: Export Reports
1. Scroll to bottom of page
2. Click "📊 Download Excel Report"
3. File should download successfully
4. Open file to verify data

### Test 3: Upload Data
1. Create a test CSV file with columns: Date, Category, Amount, Type
2. Upload via sidebar
3. Dashboard should update with your data

## 🎯 Quick Test CSV

Create `test_data.csv`:

```csv
Date,Category,Amount,Type
2025-10-01,Product Sales,25000,Revenue
2025-10-02,Salaries,15000,Expense
2025-10-05,Consulting,18000,Revenue
2025-10-10,Marketing,5000,Expense
2025-10-15,Services,12000,Revenue
2025-10-20,Rent,8000,Expense
```

Upload this file to test the upload functionality.

## 🐛 Troubleshooting

### Problem: "Command not found: streamlit"

**Solution:**
```bash
# Verify installation
pip list | grep streamlit

# If not installed
pip install streamlit

# Or reinstall
pip install --upgrade streamlit
```

### Problem: "Module not found" errors

**Solution:**
```bash
# Reinstall all dependencies
pip install -r requirements.txt --force-reinstall
```

### Problem: Port 8501 already in use

**Solution:**
```bash
# Use different port
streamlit run app.py --server.port 8502
```

### Problem: Charts not displaying

**Solution:**
```bash
# Clear Streamlit cache
streamlit cache clear

# Restart the application
```

### Problem: Virtual environment won't activate

**Windows Solution:**
```cmd
# Enable script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate
venv\Scripts\activate
```

**Mac/Linux Solution:**
```bash
# Make sure you have permissions
chmod +x venv/bin/activate

# Then activate
source venv/bin/activate
```

## 🔄 Daily Usage

### Starting the Dashboard

1. **Navigate to project folder**
   ```bash
   cd accounting-dashboard
   ```

2. **Activate virtual environment**
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

3. **Run application**
   ```bash
   streamlit run app.py
   ```

### Stopping the Dashboard

- Press `Ctrl + C` in terminal
- Close the browser tab
- Deactivate virtual environment: `deactivate`

## 📊 Using with Real Data

### Prepare Your Data

1. **Export from accounting software**
   - Export transactions to CSV or Excel
   - Ensure columns: Date, Category, Amount, Type

2. **Clean your data**
   - Remove empty rows
   - Ensure dates are in YYYY-MM-DD format
   - Verify Amount column is numeric
   - Type column should be "Revenue" or "Expense"

3. **Upload to dashboard**
   - Use sidebar upload button
   - Dashboard updates automatically

### Data Template

Download this template: `accounting_template.xlsx`

| Date | Category | Amount | Type |
|------|----------|--------|------|
| 2025-10-01 | Sales | 10000 | Revenue |
| 2025-10-01 | Salaries | 5000 | Expense |

## 🚀 Advanced Configuration

### Change Default Port

Create `.streamlit/config.toml`:
```toml
[server]
port = 8502
```

### Enable Wide Mode by Default

In `app.py`, change:
```python
st.set_page_config(
    layout="wide"  # This enables wide mode
)
```

### Custom Theme

Create `.streamlit/config.toml`:
```toml
[theme]
primaryColor="#3b82f6"
backgroundColor="#ffffff"
secondaryBackgroundColor="#f3f4f6"
textColor="#1f2937"
font="sans serif"
```

## 📱 Access from Other Devices

### On Same Network

1. **Find your IP address**
   - Windows: `ipconfig`
   - Mac/Linux: `ifconfig` or `ip addr`

2. **Run with network access**
   ```bash
   streamlit run app.py --server.address 0.0.0.0
   ```

3. **Access from other device**
   - Open browser
   - Go to: `http://YOUR_IP:8501`
   - Example: `http://192.168.1.100:8501`

## 🔐 Security Notes

### For Personal Use
- Default setup is safe for local use
- Data stays on your computer

### For Team Use
Consider:
- Add password protection
- Use HTTPS
- Deploy on secure server
- Implement user authentication

## 📚 Learning Resources

### Streamlit Documentation
- https://docs.streamlit.io/

### Pandas Tutorials
- https://pandas.pydata.org/docs/

### Plotly Examples
- https://plotly.com/python/

## 🎓 Next Steps

1. **Customize categories** for your business
2. **Add your real data**
3. **Create custom reports**
4. **Share with stakeholders**
5. **Explore advanced features**

## 💡 Tips for Success

1. **Start with sample data** to learn the interface
2. **Export reports regularly** to track history
3. **Use date filters** for focused analysis
4. **Keep data backed up** before uploading
5. **Update regularly** with latest transactions

## 📞 Getting Help

If you encounter issues:

1. **Check this guide** for solutions
2. **Review error messages** carefully
3. **Search online** for specific errors
4. **Contact developer**: maqbuul@outlook.com

## ✨ Success Checklist

- [ ] Python installed and verified
- [ ] Project folder created
- [ ] All files in place
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Application runs successfully
- [ ] Sample data loads
- [ ] Charts display correctly
- [ ] Reports export properly
- [ ] Custom data uploads

**Congratulations! Your Accounting Dashboard is ready to use! 🎉**

---

For detailed feature documentation, see `README.md`

Last Updated: October 2025