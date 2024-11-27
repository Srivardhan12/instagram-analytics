import matplotlib
matplotlib.use('Agg')  # Use non-interactive Agg backend

from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import os

# Specify the template folder
app = Flask(__name__, template_folder=os.path.abspath('./'))

# Load CSV data
def load_csv_data(file_path):
    return pd.read_csv(file_path)

# Generate graphs as base64-encoded strings
def create_graph(data, title, x, y):
    plt.figure(figsize=(x, y))
    for column in data.columns[1:]:  # Skip the first column if it's an index/identifier
        plt.plot(data.iloc[:, 0], data[column], label=column)
    plt.xlabel(data.columns[0])
    plt.ylabel("Views")
    plt.title(title)
    plt.legend()
    plt.grid(True)

    # Save plot to a BytesIO buffer
    output = io.BytesIO()
    plt.savefig(output, format="png")
    output.seek(0)
    plt.close()

    # Encode image to base64 string
    encoded_image = base64.b64encode(output.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{encoded_image}"

@app.route('/')
def index():
    # Load data and create graphs for posts
    post_1_data = load_csv_data('data/post_1.csv')
    post_2_data = load_csv_data('data/post_2.csv')
    post_1_predected_data = load_csv_data('data/post_1_predected.csv')
    post_2_predected_data = load_csv_data('data/post_2_predected.csv')
    user_followers_data = load_csv_data('data/user_followers_data.csv')
    user_followers_data_predected = load_csv_data('data/user_followers_data_predected.csv')

    post_1_graph = create_graph(post_1_data, "Acctual Data", 9, 4)
    post_2_graph = create_graph(post_2_data, "Acctual Data", 9, 4)
    post_1_predected_data = create_graph(post_1_predected_data, "Predected Data For Next 6 Months", 9, 4)
    post_2_predected_data = create_graph(post_2_predected_data, "Predected Data For Next 6 Months", 9, 4)
    user_followers_data = create_graph(user_followers_data, "User Followers Data", 13, 5)
    user_followers_data_predected = create_graph(user_followers_data_predected, "User Followers Data Predection For Next 6 Months", 14, 5)

    return render_template(
        'templets/index.html',
        post_1_graph = post_1_graph,
        post_2_graph = post_2_graph,
        post_1_predected_data = post_1_predected_data,
        post_2_predected_data = post_2_predected_data,
        user_followers_data = user_followers_data,
        user_followers_data_predected = user_followers_data_predected
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

