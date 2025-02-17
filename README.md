# AirBNBDataVisualization

![example](https://github.com/user-attachments/assets/9b42a570-077a-4a3c-9ca3-f543546a3acd)

This is a data visualization dashboard which won the business track for the ["Kent Hack Enough" 2025 Hackathon](https://khe.io/). It takes in data from the [Airbnb Open Dataset](https://www.kaggle.com/datasets/arianazmoudeh/airbnbopendata/data) and provides analytics to help users understand the data better. View the devpost submission [here](https://devpost.com/software/air-o-lyze).

## Credits

Amber Martino - Front-End

Eva Powlison - Data Back-End

Peyton Fazio - Front-End

## Usage

Use the New York state heatmap to find the density of Airbnb rentals in each county. 

Select a county to view additional information.

The parallel coordinates plot provides insights into clusters of data. Each distinct cluster is colored differently. Each thread in the plot represents a different point of data. 

Select two axes of data to view a linear regression chart and associated coefficient of regression. 

## Installation 

1. Clone this repository and change directory into it.

```git clone https://github.com/peytonfazio/AirBNBDataVisualization.git && cd AirBNBDataVisualization```

2. Create a new Python virtual environment.

  ```python -m venv.```

3. [Download the dataset](https://www.kaggle.com/datasets/arianazmoudeh/airbnbopendata/data) and place it into the same directory.

4. Run the code.

  ```streamlit run streamlit_graph.py```
