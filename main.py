from fastapi import FastAPI

app = FastAPI

@app.get('/')
def main():
    return({1: "Hello"})