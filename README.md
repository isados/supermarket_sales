# Supermarket Sales (Streamlit App)

## Requirements
```bash
pipenv install
```

## Install & Run Source
```bash
pip install -r requirements.txt
streamlit run main.py
```

## Build Docker Image and Run

```bash
# Build
sudo docker build -t supermarket_dash:v1 .
sudo docker build -f Dockerfile.dev -t supermarket_dash:dev .

# Run
sudo docker run -p 127.0.0.1:8501:8501 supermarket_dash:v1

# Run (with Binded Mount for Dev)
sudo docker run -itp 127.0.0.1:8501:8501 --mount type=bind,src="`pwd`",target='/app'  supermarket_dash:dev bash
```