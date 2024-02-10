from fastapi import FastAPI, Query
import matplotlib.pyplot as plt
import math
import numpy as np
import os
from fastapi.responses import FileResponse
from starlette.staticfiles import StaticFiles

app = FastAPI()

app.mount("/app", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/plot/{equations}")
async def create_plot_from_equations(equations: str, add: bool = Query(False)):
    def evaluate_equation(equation: str):
        y_values = []
        for x in range(1, 10001):
            y_values.append(eval(equation.replace('N', str(x))))
        return y_values

    def generate_plot(equation: str, y_values):
        plt.plot([x for x in range(0, 10000)], y_values, label=equation)
        plt.title("Big O notation plot")
        plt.ylim([0, 10_000])  # Set y limits
        plt.yticks(np.arange(0, 10_001, step=500))  # Set y-ticks
        plt.legend()

    equations_list = [equation.strip() for equation in equations.split(',')]
    current_directory = os.getcwd()
    image_path = os.path.join(current_directory, f"{equations.replace('/', '').replace(',', '_')}.png")

    if not add:
        plt.clf()

    for equation in equations_list:
        y_values = evaluate_equation(equation)
        generate_plot(equation, y_values)

    plt.savefig(image_path)
    return FileResponse(image_path, media_type="image/png")