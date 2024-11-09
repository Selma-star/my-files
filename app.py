from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Required to use flash messages

class BudgetApp:
    def __init__(self):
        self.budget = {}

    def add_expense(self, category, amount):
        if category in self.budget:
            self.budget[category] += amount
        else:
            self.budget[category] = amount

    def remove_expense(self, category, amount):
        if category not in self.budget:
            return f"Category '{category}' does not exist."
        elif self.budget[category] < amount:
            return f"Insufficient funds in category '{category}'."
        else:
            self.budget[category] -= amount
            return f"Removed ${amount} from {category}."

    def get_total(self):
        return sum(self.budget.values())

    def get_budget(self):
        return self.budget


budget_app = BudgetApp()

@app.route('/')
def index():
    return render_template('index.html', budget=budget_app.get_budget(), total=budget_app.get_total())

@app.route('/add', methods=['POST'])
def add_expense():
    category = request.form['category']
    amount = float(request.form['amount'])
    budget_app.add_expense(category, amount)
    flash(f"Added ${amount} to {category}.", "success")
    return redirect(url_for('index'))

@app.route('/remove', methods=['POST'])
def remove_expense():
    category = request.form['category']
    amount = float(request.form['amount'])
    message = budget_app.remove_expense(category, amount)
    flash(message, "error" if "does not exist" in message or "Insufficient funds" in message else "success")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
