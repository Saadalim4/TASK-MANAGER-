import json
import datetime
from typing import List, Dict, Any
import random

class PersonalFinanceCoach:
    def __init__(self):
        self.users_file = "users.json"
        self.transactions_file = "transactions.json"
        self.goals_file = "goals.json"
        self.load_data()
        
    def load_data(self):
        # Initialize or load user data
        try:
            with open(self.users_file, 'r') as f:
                self.users = json.load(f)
        except FileNotFoundError:
            self.users = {}
            
        try:
            with open(self.transactions_file, 'r') as f:
                self.transactions = json.load(f)
        except FileNotFoundError:
            self.transactions = {}
            
        try:
            with open(self.goals_file, 'r') as f:
                self.goals = json.load(f)
        except FileNotFoundError:
            self.goals = {}
    
    def save_data(self):
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=2)
        with open(self.transactions_file, 'w') as f:
            json.dump(self.transactions, f, indent=2)
        with open(self.goals_file, 'w') as f:
            json.dump(self.goals, f, indent=2)
    
    def register_user(self, username: str, monthly_income: float):
        if username in self.users:
            print(f"User {username} already exists!")
            return False
            
        self.users[username] = {
            'monthly_income': monthly_income,
            'joined_date': datetime.datetime.now().isoformat()
        }
        self.transactions[username] = []
        self.goals[username] = []
        self.save_data()
        print(f"User {username} registered successfully!")
        return True
    
    def add_transaction(self, username: str, amount: float, category: str, description: str):
        if username not in self.users:
            print("User not found! Please register first.")
            return False
            
        transaction = {
            'id': len(self.transactions[username]) + 1,
            'amount': amount,
            'category': category,
            'description': description,
            'date': datetime.datetime.now().isoformat()
        }
        
        self.transactions[username].append(transaction)
        self.save_data()
        print(f"Transaction added: {description} - ${amount}")
        return True
    
    def set_financial_goal(self, username: str, goal_name: str, target_amount: float, timeline_days: int):
        if username not in self.users:
            print("User not found!")
            return False
            
        goal = {
            'id': len(self.goals[username]) + 1,
            'name': goal_name,
            'target_amount': target_amount,
            'current_amount': 0,
            'timeline_days': timeline_days,
            'created_date': datetime.datetime.now().isoformat(),
            'completed': False
        }
        
        self.goals[username].append(goal)
        self.save_data()
        print(f"Goal set: {goal_name} - ${target_amount} in {timeline_days} days")
        return True
    
    def get_spending_analysis(self, username: str):
        if username not in self.transactions:
            return "No transactions found."
            
        transactions = self.transactions[username]
        if not transactions:
            return "No transactions to analyze."
        
        # Calculate spending by category
        category_totals = {}
        total_spent = 0
        
        for transaction in transactions:
            category = transaction['category']
            amount = transaction['amount']
            category_totals[category] = category_totals.get(category, 0) + amount
            total_spent += amount
        
        # Generate insights
        analysis = f"\n--- Spending Analysis for {username} ---\n"
        analysis += f"Total spent: ${total_spent:.2f}\n"
        analysis += "Spending by category:\n"
        
        for category, amount in category_totals.items():
            percentage = (amount / total_spent) * 100 if total_spent > 0 else 0
            analysis += f"  {category}: ${amount:.2f} ({percentage:.1f}%)\n"
        
        # AI-powered insights
        monthly_income = self.users[username]['monthly_income']
        savings_rate = ((monthly_income - total_spent) / monthly_income) * 100 if monthly_income > 0 else 0
        
        analysis += f"\nAI Insights:\n"
        analysis += f"- Monthly savings rate: {savings_rate:.1f}%\n"
        
        if savings_rate < 20:
            analysis += "- 💡 Tip: Try to increase your savings rate to at least 20%\n"
        else:
            analysis += "- ✅ Great job on your savings rate!\n"
            
        # Category-specific tips
        for category, amount in category_totals.items():
            if amount > monthly_income * 0.3:  # If spending > 30% of income in one category
                analysis += f"- ⚠️  High spending in {category}. Consider budgeting this category.\n"
        
        return analysis
    
    def get_goal_progress(self, username: str):
        if username not in self.goals or not self.goals[username]:
            return "No goals set yet."
            
        progress_report = f"\n--- Goal Progress for {username} ---\n"
        
        for goal in self.goals[username]:
            progress = (goal['current_amount'] / goal['target_amount']) * 100
            status = "✅ Completed" if goal['completed'] else "🔄 In Progress"
            
            progress_report += f"\nGoal: {goal['name']}\n"
            progress_report += f"Target: ${goal['target_amount']} | Saved: ${goal['current_amount']}\n"
            progress_report += f"Progress: {progress:.1f}% {status}\n"
            
            # AI suggestions for goals
            if not goal['completed'] and progress < 50:
                daily_saving = goal['target_amount'] / goal['timeline_days']
                progress_report += f"💡 Suggestion: Save ${daily_saving:.2f} daily to reach your goal\n"
        
        return progress_report
    
    def generate_habit_nudge(self, username: str):
        if username not in self.transactions:
            return "Start tracking your expenses to get personalized tips!"
            
        transactions = self.transactions[username]
        if len(transactions) < 5:
            return "Keep adding more transactions for better insights!"
        
        # Simple AI habit detection
        recent_transactions = transactions[-5:]  # Last 5 transactions
        food_count = sum(1 for t in recent_transactions if 'food' in t['category'].lower())
        
        nudges = [
            "💡 Try the 50-30-20 rule: 50% needs, 30% wants, 20% savings",
            "💰 Review your subscriptions - cancel unused services",
            "📱 Use cashback apps for everyday purchases",
            "🍽️ Meal prep on weekends to save on food costs",
            "🚶 Walk or bike for short distances to save transport costs"
        ]
        
        if food_count >= 3:
            nudges.append("🍕 You're eating out frequently. Consider cooking at home to save money!")
        
        return f"💬 Habit Nudge: {random.choice(nudges)}"
    
    def suggest_investment_ideas(self, username: str):
        if username not in self.users:
            return "Please register first!"
            
        monthly_income = self.users[username]['monthly_income']
        transactions = self.transactions.get(username, [])
        total_spent = sum(t['amount'] for t in transactions)
        monthly_savings = monthly_income - total_spent
        
        suggestions = "\n--- Investment Suggestions ---\n"
        
        if monthly_savings < 100:
            suggestions += "Focus on building an emergency fund first (3-6 months of expenses)\n"
        elif monthly_savings < 500:
            suggestions += "Consider starting with:\n- High-yield savings account\n- Roth IRA contributions\n- Low-cost index funds\n"
        else:
            suggestions += "With your savings level, consider:\n- Diversified ETF portfolio\n- Real estate crowdfunding\n- Robo-advisor services\n"
        
        suggestions += "\n📚 Educational Resources:\n"
        suggestions += "- Read 'The Simple Path to Wealth' by JL Collins\n"
        suggestions += "- Learn about compound interest\n"
        suggestions += "- Understand risk tolerance before investing\n"
        
        return suggestions

def main():
    coach = PersonalFinanceCoach()
    
    print("🤖 AI Personal Finance Coach")
    print("=" * 30)
    
    while True:
        print("\nOptions:")
        print("1. Register User")
        print("2. Add Transaction")
        print("3. Set Financial Goal")
        print("4. View Spending Analysis")
        print("5. Check Goal Progress")
        print("6. Get Habit Nudge")
        print("7. Investment Ideas")
        print("8. Exit")
        
        choice = input("\nEnter your choice (1-8): ").strip()
        
        if choice == '1':
            username = input("Enter username: ").strip()
            try:
                income = float(input("Enter monthly income: $"))
                coach.register_user(username, income)
            except ValueError:
                print("Please enter a valid number for income!")
                
        elif choice == '2':
            username = input("Enter username: ").strip()
            try:
                amount = float(input("Enter amount: $"))
                category = input("Enter category (food, transport, entertainment, bills, shopping): ").strip()
                description = input("Enter description: ").strip()
                coach.add_transaction(username, amount, category, description)
            except ValueError:
                print("Please enter valid numbers!")
                
        elif choice == '3':
            username = input("Enter username: ").strip()
            goal_name = input("Enter goal name: ").strip()
            try:
                target = float(input("Enter target amount: $"))
                timeline = int(input("Enter timeline in days: "))
                coach.set_financial_goal(username, goal_name, target, timeline)
            except ValueError:
                print("Please enter valid numbers!")
                
        elif choice == '4':
            username = input("Enter username: ").strip()
            print(coach.get_spending_analysis(username))
            
        elif choice == '5':
            username = input("Enter username: ").strip()
            print(coach.get_goal_progress(username))
            
        elif choice == '6':
            username = input("Enter username: ").strip()
            print(coach.generate_habit_nudge(username))
            
        elif choice == '7':
            username = input("Enter username: ").strip()
            print(coach.suggest_investment_ideas(username))
            
        elif choice == '8':
            print("Thank you for using AI Personal Finance Coach! 💰")
            break
            
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()