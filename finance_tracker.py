import streamlit as st

class Transaction:
    def __init__(self, amount, category, t_type, note=""):
        self.amount = amount
        self.category = category
        self.type = t_type  # 'income' or 'expense'
        self.note = note

    def __str__(self):
        return f"{self.type.title()}: {self.amount} in {self.category} - {self.note}"

class Account:
    def __init__(self):
        self.transactions = []

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def get_balance(self):
        balance = 0
        for t in self.transactions:
            if t.type == 'income':
                balance += t.amount
            else:
                balance -= t.amount
        return balance

    def get_transactions(self):
        return self.transactions

class FinanceTrackerApp:
    def __init__(self):
        if 'account' not in st.session_state:
            st.session_state.account = Account()

    def run(self):
        st.title("Personal Finance Tracker")
        menu = st.sidebar.selectbox("Menu", ["Add Transaction", "View Summary"])

        if menu == "Add Transaction":
            self.add_transaction_ui()
        else:
            self.view_summary_ui()

    def add_transaction_ui(self):
        st.header("Add a New Transaction")

        t_type = st.selectbox("Transaction Type", ['income', 'expense'])
        amount = st.number_input("Amount", min_value=0.01, format="%.2f")
        category = st.text_input("Category", value="")
        note = st.text_input("Note (optional)")

        if st.button("Add Transaction"):
            if amount <= 0:
                st.error("Amount must be greater than zero.")
                return
            if not category.strip():
                st.warning("Please enter a category.")
                return

            transaction = Transaction(amount, category.strip(), t_type, note.strip())
            st.session_state.account.add_transaction(transaction)
            st.success(f"{t_type.title()} added successfully!")

    def view_summary_ui(self):
        st.header("Account Summary")

        balance = st.session_state.account.get_balance()
        st.subheader(f"Current Balance: ${balance:.2f}")

        transactions = st.session_state.account.get_transactions()
        if not transactions:
            st.info("No transactions recorded yet.")
            return

        st.subheader("All Transactions")
        for t in transactions:
            st.write(f"- {t}")

if __name__ == "__main__":
    app = FinanceTrackerApp()
    app.run()

