# BudgetBuddy Agent 💸

An AI-powered financial coaching application that helps you set savings goals, track income/expenses, and get personalized financial advice.

## 🌟 Features

- **🎯 Savings Target Calculator**: Set personalized monthly savings goals based on your financial situation
- **📊 Monthly Tracking**: Track income and expenses across all 12 months
- **📈 Visualization Dashboard**: View savings progress with interactive charts and metrics  
- **🤖 AI Financial Analysis**: Get personalized advice and savings target recommendations
- **💾 Data Persistence**: Your financial data is automatically saved between sessions

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- AWS Account with Bedrock access
- AWS CLI configured with credentials

### Installation

1. **Clone and setup**:
```bash
git clone <your-repo>
cd agenticai
python -m venv venv
venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Configure environment**:
Create a file called `.env` in the project root with:
```env
AWS_ACCESS_KEY_ID=your_aws_access_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=anthropic.claude-3-haiku-20240307-v1:0
```

### Running the Application

```bash
streamlit run src\app.py
```

Open your browser to `http://localhost:8501`

## 📁 Project Structure

```
budgetbuddy-agent/
├── src/
│   ├── app.py                 # Main application
│   ├── agent.py               # AI agent implementation
│   └── components/
│       ├── savings_recommender.py    # Savings goal calculator
│       ├── income_expense_tracker.py # Monthly tracking
│       ├── visualization.py          # Charts & dashboards
│       |── tips_review.py            # AI analysis
|       └── utils/
|           └── storage.py            # Data persistence 
├── tests/
│   └── test.py                # Basic functionality tests
├── data/                      # Auto-created data storage
├── .env                       # Environment variables
└── requirements.txt           # Python dependencies
```

## 🎯 How to Use

1. **Set Your Savings Target**: 
   - Go to the "Savings Target" tab
   - Enter your age, income, and retirement goals
   - Get AI-recommended monthly savings target

2. **Track Monthly Finances**:
   - Navigate to "Monthly Tracking" 
   - Fill out income and expenses for each month
   - Input actual savings amounts

3. **View Progress**:
   - Check "Visualization" tab for charts
   - See how you're tracking against your goals

4. **Get AI Advice**:
   - Visit "Tips & Review" for personalized analysis
   - Get savings target adjustments based on your data

## 🔧 Configuration

### AWS Setup

1. **Install AWS CLI** (if not already installed):
```bash
pip install awscli
```

2. **Configure AWS credentials**:
```bash
aws configure
```

3. **Enter your credentials when prompted**:
```
AWS Access Key ID: YOUR_ACCESS_KEY
AWS Secret Access Key: YOUR_SECRET_KEY
Default region name: us-east-1
Default output format: json
```

### Environment Variables

The application will look for a `.env` file with these variables:
- `AWS_ACCESS_KEY_ID`: Your AWS access key
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret key  
- `AWS_REGION`: AWS region (default: us-east-1)
- `BEDROCK_MODEL_ID`: Bedrock model ID (default: anthropic.claude-3-haiku-20240307-v1:0)

## 🧪 Testing

Run basic functionality tests:

```bash
python tests\test.py
```

Expected output:
```
🚀 Running simple tests...
----------------------------------------
✅ All imports successful
✅ Agent creation successful
----------------------------------------
📊 Results: 2/2 tests passed
🎉 All tests passed!
```

## 💾 Data Storage

Your financial data is automatically saved in the `data\` directory as JSON files. The application creates a `test_user.json` file that stores:
- Your profile information (age, income, risk tolerance)
- Monthly income and expense data
- Savings targets and actual savings

## 🐛 Troubleshooting

### Common Issues

1. **AWS Credentials Error**:
   - Ensure your AWS CLI is properly configured
   - Check that your `.env` file has correct credentials

2. **Import Errors**:
   - Make sure you're running from the project root directory
   - Verify all dependencies are installed: `pip install -r requirements.txt`

3. **Streamlit Port Already in Use**:
   ```bash
   streamlit run src\app.py --server.port 8502
   ```

### Getting Help

If you encounter issues:
1. Check that all requirements are installed
2. Verify your AWS credentials have Bedrock access
3. Ensure you're running commands from the project root directory

## 📝 License

This project is created for educational and demonstration purposes.

## 🤝 Contributing

This is a demonstration project. Feel free to fork and modify for your own use!

---

**Note**: This application uses AWS Bedrock, which may incur costs based on usage. Please monitor your AWS usage and costs.