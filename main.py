from read import File
from geneticAlgorithm import GeneticAlgorithm

file = File('data.dat')
orders = file.get_orders()

print(len(orders))
ga = GeneticAlgorithm(0.1, 0.2, 100, 20, 100, orders)
ga.genetic_algorithm()