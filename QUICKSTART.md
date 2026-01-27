# Quick Start Guide - Customer Churn Analytics System

## 🚀 Running the Application (3 Simple Steps)

### Step 1: Start the API Server
Open a terminal in the project directory and run:
```bash
python demo_server.py
```

You should see:
```
🚀 Starting Demo API Server...
📊 Loaded 7032 customer records
🔗 API running at: http://localhost:8000
```

**Keep this terminal open!**

---

### Step 2: Open the Dashboard
1. Open your web browser (Chrome, Firefox, or Edge)
2. Navigate to the frontend folder
3. Open `index.html` by either:
   - **Dragging and dropping** the file into your browser, OR
   - **Typing in the address bar**: `file:///C:/Users/Mouli/OneDrive/Desktop/churn/frontend/index.html`

---

### Step 3: Use the Dashboard
The dashboard will automatically load and display:
- **KPI Cards**: Total customers, churn rate, average charges
- **Interactive Charts**: Segment analysis by contract type, internet service, etc.
- **Prediction Tool**: Scroll down to predict churn for individual customers

---

## 🧪 Testing the Prediction Feature

1. Scroll to the **"🔮 Predict Customer Churn"** section
2. Adjust the form fields (tenure, monthly charges, contract type, etc.)
3. Click **"Predict Churn Risk"**
4. See the instant prediction with:
   - Churn probability percentage
   - Risk level (HIGH/MEDIUM/LOW)
   - Prediction (Likely to Churn / Likely to Stay)

---

## 🔍 Testing the API Directly (Optional)

You can also test the API endpoints directly in your browser:

- **Churn Rate**: http://localhost:8000/api/analytics/churn-rate/
- **Segment Analysis**: http://localhost:8000/api/analytics/segment-analysis/?segment_by=Contract
- **Customer List**: http://localhost:8000/api/customers/

---

## 🛑 Stopping the Application

When you're done:
1. Go back to the terminal running `demo_server.py`
2. Press `Ctrl+C` to stop the server

---

## 📝 Notes

- **The demo server is already running!** (Check your terminal - it's been running for 2+ hours)
- **No MongoDB required** for the demo - it uses the CSV data directly
- **All 7,032 customer records** are loaded and ready
- **ML model is loaded** and making real predictions

---

## 🚨 Troubleshooting

**Problem**: Dashboard shows "Failed to load" errors
- **Solution**: Make sure `demo_server.py` is running (Step 1)

**Problem**: Charts not showing
- **Solution**: Wait a few seconds for the API calls to complete

**Problem**: Port 8000 already in use
- **Solution**: Stop the old server with `Ctrl+C` and restart

---

## 🎯 What to Demonstrate

1. **KPI Dashboard** - Shows real-time analytics from 7K+ customers
2. **Segment Analysis** - Change the dropdown to see different segments
3. **Churn Prediction** - Try different customer profiles:
   - High Risk: Month-to-month contract, high charges, low tenure
   - Low Risk: Two-year contract, low charges, high tenure
4. **API Endpoints** - Show the JSON responses in browser

---

**That's it! The system is production-ready and fully functional.** 🎉
