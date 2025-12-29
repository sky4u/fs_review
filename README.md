# 📊 Financial Review App (Streamlit)

A Streamlit-based web application to analyze **yearly financial performance**, compare **Actuals vs Finalization**, and review key expense and supplier data in an interactive and user-friendly dashboard.

---

## 🚀 Features

* Yearly financial overview dashboard
* Comparison of **Actuals vs Finalized figures**
* Supplier-wise and OPEX-wise analysis
* Interactive tables and visual insights
* Clean, management-friendly layout suitable for reviews and board discussions

---

## 🛠️ Tech Stack

* **Python 3.9+**
* **Streamlit** – frontend & UI
* **Pandas** – data manipulation

---

## 📁 Project Structure

```text
financial-review-app/
│
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
└── data/                   # (Optional) Source data files
```

---

## ⚙️ Installation & Setup

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd financial-review-app
   ```

2. **Create a virtual environment (recommended)**

   ```bash
   python -m venv venv
   venv\Scripts\activate   # Windows
   source venv/bin/activate # macOS/Linux
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Running the App

```bash
streamlit run app.py
```

The app will open automatically in your browser at:

```
https://fsreviewdt.streamlit.app/
```

---

## 📊 Usage

* Select the **financial year** to review
* Compare **Actual vs Finalized** numbers
* Review expense categories and supplier-level data
* Use insights for financial close, variance analysis, or management review

---

## 🧾 Sample Use Cases

* Yearly financial review meetings - for now, this can be later updated to Monthly review.
* Pre-audit financial validation
* Management reporting and variance explanation
* Budget vs actual comparison support

---

## ⚠️ Notes & Assumptions

* Data used in the app can be static or manually configured within the code
* Currency formatting assumes consistency across the dataset
* App is designed for **internal financial analysis**, not public deployment

---

## 🔮 Future Enhancements (Optional)

* Upload Excel/CSV financial files
* Automated variance explanations
* Charts & trend analysis
* User authentication
* Export reports to Excel or PDF

---

## 👤 Author

**Yaseen**
Finance Consultant
---

## 📄 License

This project is intended for internal and educational use.
