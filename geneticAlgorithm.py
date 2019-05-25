from population import Population, crossover
import random
import numpy as np


class GeneticAlgorithm(object):

    def __init__(self, alpha, gama, pop_size, pool_size, max_iter, orders):

        self.alpha = alpha
        self.gama = gama
        self.pop_size = pop_size
        self.pool_size = pool_size
        self.max_iter = max_iter
        self.orders = orders

    def genetic_algorithm(self):

        pop = Population(self.pop_size, self.pool_size, orders=self.orders)
        count = 0
        crossover_probs = [0.6, 0.7, 0.8, 0.9]
        mutation_probs = [0.05, 0.1, 0.2, 0.25]
        Q_co = np.zeros(shape=(len(crossover_probs), len(crossover_probs)))  # Q values for reinforcement learning part
        Q_mu = np.zeros(shape=(len(mutation_probs), len(mutation_probs)))  # Q values for reinforcement learning part
        best_val = - 1000
        prev_state_co = 0 # randomly selected state for co
        prev_state_mu = 0 # randomly selected state for mu
        state_co = 0  # randomly selected state for co
        state_mu = 0  # randomly selected state for mu
        while count < 100:

            mating_pool = pop.form_pool()

            offsprings = []
            count2 = 0
            while count2 < self.pool_size:

                sol1 = random.choice(mating_pool)
                sol2 = random.choice(mating_pool)
                if random.random() <= crossover_probs[state_co]:
                    off1, off2 = crossover(sol1, sol2)
                    offsprings.append(off1)
                    offsprings.append(off2)
                    count2 += 1

            all_sol = []
            for sol in pop.solutions:
                all_sol.append(sol)

            for sol in offsprings:
                all_sol.append(sol)

            next_sols = tournament_selection(all_sol, self.pop_size)
            pop = Population(self.pop_size, self.pool_size, orders=self.orders, solutions=next_sols)

            if random.random() < mutation_probs[state_mu]:
                r = random.random()
                if r <= 0.33:
                    pop.mutation1()
                elif r <= 0.66:
                    pop.mutation2()
                else:
                    pop.mutation3(self.orders)

            if pop.best_val()[1] > best_val:
                best_sol, best_val = pop.best_val()
                print(best_val)
                best_sol.w_()

            # Q value update
            Q_co[prev_state_co, state_co] += \
                self.alpha*(best_val+self.gama*np.max(Q_co[state_co, :])-Q_co[prev_state_co, state_co])
            Q_mu[prev_state_mu, state_mu] += \
                self.alpha * (best_val + self.gama * np.max(Q_mu[state_mu, :]) - Q_mu[prev_state_mu, state_mu])

            # Save this iteration as a previous iteration
            prev_state_co = state_co
            prev_state_mu = state_mu

            # Next Policy with Epsilon-Greedy Algorithm for CO

            if random.random() < 0.05:
                state_co = random.randint(0, len(crossover_probs)-1)
            else:
                state_co = np.argmax(Q_co[state_co, :])

            # Next Policy with Epsilon-Greedy Algorithm for Mutation

            if random.random() < 0.05:
                state_mu = random.randint(0, len(mutation_probs)-1)
            else:
                state_mu = np.argmax(Q_mu[state_mu, :])
            count += 1


def tournament_selection(solutions, n_sol):

    count = 0
    selection = []
    while count < n_sol:

        sol1 = random.choice(solutions)
        sol2 = random.choice(solutions)

        sol = sol1
        if sol2.obj() > sol1.obj():
            sol = sol2

        selection.append(sol)
        count += 1

    return selection