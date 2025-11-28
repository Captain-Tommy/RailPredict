# 🚄 RailPredict | Next-Gen Waitlist Intelligence

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-black?style=for-the-badge&logo=flask&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-Deployed-000000?style=for-the-badge&logo=vercel&logoColor=white)

**RailPredict** is a premium, AI-powered application designed to predict the confirmation probability of Indian Railways waitlisted tickets. Combining advanced machine learning with a stunning, responsive Glassmorphism UI, it delivers next-generation travel intelligence.

---

## ✨ Key Features

- **🔮 AI-Powered Prediction**: Uses a Random Forest Classifier to estimate confirmation chances based on historical trends, current waitlist status, and journey timing.
- **🎨 Premium Glassmorphism UI**: A modern, sleek interface featuring blurred backgrounds, floating orbs, and smooth animations.
- **📱 Fully Responsive**: Optimized for all devices—from large desktop dashboards to mobile screens.
- **⚡ Real-Time Data**: Scrapes live train details (schedule, route, composition) to provide context-rich analysis.
- **📊 Smart Dashboard**: Visualizes data with circular progress charts, factor analysis tables, and impact badges.

---

## 🚀 Tech Stack

- **Backend**: Python, Flask, SQLite
- **ML Engine**: Scikit-Learn (Random Forest), NumPy
- **Frontend**: HTML5, CSS3 (Glassmorphism, Fluid Typography), JavaScript
- **Deployment**: Docker, Vercel

---

## 🛠️ Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/Captain-Tommy/RailPredict.git
    cd RailPredict
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Application**
    ```bash
    python app.py
    ```

4.  **Access the App**
    Open your browser and visit `http://127.0.0.1:5001`

---

## 🧠 How It Works

1.  **Input Details**: Enter the Train Number, current Waitlist Status, and Journey Date.
2.  **Data Processing**: The app calculates the days remaining and fetches train details.
3.  **ML Prediction**: The pre-trained model analyzes factors like:
    - Current Waitlist Number
    - Days to Journey
    - Weekend/Holiday Travel
4.  **Result**: You get a percentage probability of confirmation along with a detailed breakdown of positive and negative factors.

---

## ⚠️ Disclaimer

> **Note**: This application provides **estimates** based on historical patterns and synthetic data. Indian Railways reservation dynamics are complex and subject to last-minute changes (chart preparation, emergency quotas, etc.).
>
> **The results are NOT guaranteed.** Please use your judgment and consider official sources before making travel plans.

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork the repository and submit pull requests.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

---

<div align="center">

**Made with ❤️ by [Captain Tommy](https://github.com/Captain-Tommy)**

</div>
