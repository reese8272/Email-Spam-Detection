# TensorFlow Project

This project is built using TensorFlow and Python. Follow these steps to set it up locally.

## 👥 Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### 2️⃣ Set Up a Virtual Environment

#### **Windows (CMD)**
```cmd
python -m venv .venv
.venv\Scripts\activate
```

#### **Mac/Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3️⃣ Install Dependencies
```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### 4️⃣ Verify Installation
Run the following command to ensure TensorFlow is installed correctly:
```bash
python -c "import tensorflow as tf; print(tf.__version__)"
```

---

## 🛠 Running the Project

To start the script, run:
```bash
streamlit run src/main.py
```

If you are using **Jupyter Notebooks**, start it with:
```bash
jupyter notebook
```

---

## ✅ Troubleshooting
- **Error: `ModuleNotFoundError`?** Ensure you activated the virtual environment.
  ```bash
  source .venv/bin/activate  # (Mac/Linux)
  .venv\Scripts\activate     # (Windows)
  ```
- **GPU Acceleration Not Working?** Install TensorFlow with GPU support.
  ```bash
  pip install tensorflow-gpu
  ```

---

## 🔨 Automating Setup (Optional)
If you want to automate the setup process, you can use the provided setup scripts.

### **Windows (`setup.bat`)**
```bat
@echo off
python -m venv .venv
call .venv\Scripts\activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
echo "Setup complete! Run 'python src/main.py' to start the project."
```

### **Mac/Linux (`setup.sh`)**
```bash
#!/bin/bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
echo "Setup complete! Run 'python src/main.py' to start the project."
```

Run the script to set up the environment automatically:
```bash
./setup.sh  # Mac/Linux
setup.bat   # Windows
```

---

