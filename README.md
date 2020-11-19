# Supermarket Simulation 
This program simulates the path a customer takes when entering a supermarket, based on a Monte Carlo Markov Chain simulation and A* path finding algorithm. 

![visualization](./supermarket.gif)

# How is this simulation working? 
1. Based on the Monday data, a transition probability matrix is calculated: this allows us to know once the customer enters the supermarket, what are the probabiltiy that they will go to a station ('dairy', 'drinks', 'fruit', 'spices', and 'checkout') and once they are at a station, the probabilities that they move to another station. 
2. From this Matrix, a simulation path is calculated based on Monte Carlo Markov Chains, for example: 'drinks, fruit, fruit, spices, dairy, dairy, dairy, dairy, dairy, dairy, dairy, dairy, spices, fruit, checkout'
3. From this path, the coordinate path is calculated using A* algorithm, knowing the coordinates of each station, and that our customers will move in steps of one either up, down, left or right, for example: [[(4, 7), (5, 7), (6, 7), (7, 7), (7, 8), (7, 9), (7, 10), (8, 10), (8, 11)]]
4. Finally, the customer is visualized on a customized supermarket map and is moved depending on the coordinates path previously calculated. 

# Scripts:
- EDA.ipynb: Analysis of the Data, answering business related questions with visualisations
![visualization](./Pictures/data_vis.png)

# Keywords:


# Usage: 


# Next steps: 

