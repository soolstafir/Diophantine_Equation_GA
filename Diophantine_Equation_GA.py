# -*- coding: utf-8 -*-
"""
Spyder Editor

"""

import random

# =======================================
class Param():
    def __init__(self, a = 0, b = 0,
                 c = 0, d = 0, res = 0,
                 iterations_limit = 50):
# There is no type check, but all parameters is Long
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.res = res
        self.iterations_limit = iterations_limit
        
# =======================================
class Gene():
    def __init__(self):
        self.alleles = {};
        self.alleles[0] = 0
        self.alleles[1] = 0
        self.alleles[2] = 0
        self.alleles[3] = 0
        self.fitness = 0;
        self.probability = 0.0
        
# ======================================
    def __eq__(self, other):
        for i in range(len(self.alleles.keys())):
            if(self.alleles[i] != other.alleles[i]):
                return False
        return True
    
# =======================================
class Solver():
    def __init__(self, param):
        self.param = param
        self.population_size = 500;
        self.population = {}
        pass
        
# −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
    def solve(self):
        global_fitness = None
        self._make_first_generation()
        global_fitness = self._count_fitnesses();
        if(0 != global_fitness):
            return global_fitness
        iterations = 0
        while ((0 != global_fitness)
            or ( self.param.iterations_limit != iterations)):
            self._count_parent_probability()
            self._make_generation()
            global_fitness =  self._count_fitnesses()
            if(0 != global_fitness):
                return global_fitness
            iterations += 1
        return None
    
# −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
    def _make_first_generation(self,):
        for i in range(self.population_size):
            self.population[i] = Gene()
            for j in range(4):
                self.population[i].alleles[j] = random.randint(1, self.param.res)
                
# −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
    def _count_fitness(self, gene):
        print("(%s, %s, %s, %s)" %(gene.alleles[0],
                                   gene.alleles[1],
                                   gene.alleles[2],
                                   gene.alleles[3]))
        total = self.param.a * gene.alleles[0] \
        + self.param.b * gene.alleles[1] \
        + self.param.c * gene.alleles[2] \
        + self.param.d * gene.alleles[3]
        gene.fitness = abs(total - self.param.res)
        print("|%s - %s | = %s" %(total, self.param.res,gene.fitness))
        return gene.fitness
    
# −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
    def _count_fitnesses(self):
        sum = 0;
        fitness = 0;
        for i in range(self.population_size):
            fitness = self._count_fitness(self.population[i])
            sum += fitness
            if(0 == fitness):
                print("avgfit ===>", sum / self.population_size)
                return i
        print("avgfit ===>", sum / self.population_size)
        return 0
    
# −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
    def _inverse_sum(self):
        sum = 0
        for i in range(self.population_size):
            sum += 1.0 / self.population[i].fitness
        return sum
    
# −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
    def _count_parent_probability(self):
        inverse_sum = self._inverse_sum();
        procent_factor = 100.0; # may be 1.0
        for i in range(self.population_size):
            self.population[i].probability = \
            ((1.0/self.population[i].fitness) / inverse_sum) \
            * procent_factor
        print("%s & %s" %(i, self.population[i].probability))
        
# −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
    def _get_active_index(self):
        val = random.randint(0, 101)
        last = 0
        for i in range(self.population_size):
            if (last <= val <= self.population[i].probability):
                return i;
            else:
                last = self.population[i].probability
        return 4
    
# −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
    def _make_child(self, p_1, p_2):
        crossover = random.randint(1, 3)
        first = random.randint(0, 128)
        child = Gene()
        for i in self.population[p_1].alleles:
            child.alleles[i] = self.population[p_1].alleles[i]
            initial = 0
            final = 3
            if (64 > first):
                initial = crossover
            else:
                final = crossover+1
            for i in range(initial, final):
                child.alleles[i] = self.population[p_2].alleles[i]
                if (random.randint(0, 666) < 5):
                    child.alleles[i] = random.randint(0, self.param.res)
        print("p_1", self.population[p_1].alleles.values())
        print("p_2", self.population[p_2].alleles.values())
        print("child", child.alleles.values())
        return child
    
# −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
    def _make_generation(self, iterations_limit = 25):
        tmp = {};
        for i in range(self.population_size):
            parent_1 = 0
            parent_2 = 0
            iterations = 0
            while(parent_1 == parent_2
                  or self.population[parent_1] == self.population[parent_2]):
                parent_1 = self._get_active_index()
                parent_2 = self._get_active_index()
                iterations += 1
                if (iterations_limit < iterations):
                    break
            tmp[i] = self._make_child(parent_1, parent_2)
        for i in range(self.population_size):
            self.population[i] = tmp[i]
            
# −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
    def __str__(self):
        res = ""
        fitness = self.solve()
        if(None == fitness):
            return print("No solution found")
        gene = self.population[fitness]
        res += "The solution set to %s a + %s b %s c + %s d = %s is:\n" \
            %(self.param.a,
              self.param.b,
              self.param.c,
              self.param.d,
              self.param.res)
        res += "a = %s" %gene.alleles[0]
        res += "b = %s" %gene.alleles[1]
        res += "c = %s" %gene.alleles[2]
        res += "d = %s" %gene.alleles[3]
        return res + "\n"
if (__name__ == '__main__'):
    print(Solver(Param(1,2,3,4,45)))