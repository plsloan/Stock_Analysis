"""
Template for implementing QLearner  (c) 2015 Tucker Balch

Copyright 2018, Georgia Institute of Technology (Georgia Tech)
Atlanta, Georgia 30332
All Rights Reserved

Template code for CS 4646/7646

Georgia Tech asserts copyright ownership of this template and all derivative
works, including solutions to the projects assigned in this course. Students
and other users of this template code are advised not to share it with others
or to make it available on publicly viewable websites including repositories
such as github and gitlab.  This copyright statement should not be removed
or edited.

We do grant permission to share solutions privately with non-students such
as potential employers. However, sharing with other current or future
students of CS 7646 is prohibited and subject to being investigated as a
GT honor code violation.

-----do not edit anything above this line---

Student Name: Phillip Sloan (replace with your name)
GT User ID: psloan31 (replace with your User ID)
GT ID: 903452647 (replace with your GT ID)		  		 			 	 	 		 		 	  		   	  			  	
"""

import numpy as np
import random as rand


class QLearner(object):
    # rar  = random action rate
    # radr = random action decay rate
    def __init__(self, num_states=100, num_actions=4, alpha=0.2,
                 gamma=0.9, rar=0.5, radr=0.99, dyna=200, verbose=False):
        self.num_states = num_states
        self.num_actions = num_actions
        self.alpha = alpha
        self.gamma = gamma
        self.rar = rar
        self.radr = radr
        self.dyna = dyna
        self.verbose = verbose

        self.s = 0
        self.a = 0
        self.Q = np.zeros((num_states, num_actions))
        self.R = np.zeros((num_states, num_actions))
        self.T = np.zeros((num_states, num_actions, num_states))

    def querysetstate(self, s):
        """
        @summary: Update the state without updating the Q-table
        @param s: The new state
        @returns: The selected action
        """
        self.s = s
        action = np.random.randint(self.num_actions)
        self.a = action
        if self.verbose:
            print("s =", s, "/ a =", action)
        return action

    def query(self, s_prime, r, update=True):
        """
        @summary: Update the Q table and return an action
        @param s_prime: The new state
        @param r: The reward
        @returns: The selected action
        """
        s = self.s
        a = self.a
        if rand.uniform(0.0, 1.0) <= self.rar:
            a_prime = np.random.randint(self.num_actions)
        else:
            a_prime = np.argmax(self.Q[s_prime])
        if update:
            self.rar = self.rar * self.radr
            self.Q[s, a] = (1 - self.alpha) * self.Q[s, a] + \
                self.alpha * (r + self.gamma * self.Q[s_prime, a_prime])
            self.T[s, a, s_prime] = self.T[s, a, s_prime] + 1
            self.R[s, a] = (1 - self.alpha) * self.R[s, a] + self.alpha * r
        self.s = s_prime
        self.a = a_prime

        for i in range(self.dyna):
            s = np.random.randint(self.num_states)
            a = np.random.randint(self.num_actions)
            s_prime = np.argmax(self.T[s, a])
            a_prime = np.argmax(self.Q[s_prime])
            r = self.R[s, a]
            if update:
                self.Q[s, a] = (1 - self.alpha) * self.Q[s, a] + \
                    self.alpha * (r + self.gamma * self.Q[s_prime, a_prime])
                self.rar = self.rar * self.radr

        if self.verbose:
            print("s =", s_prime, "/ a =", a_prime, "/ r =", r)
        return self.a


if __name__ == "__main__":
    print("Remember Q from Star Trek? Well, this isn't him.")
