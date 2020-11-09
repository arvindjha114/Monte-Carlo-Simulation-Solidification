# -*- coding: utf-8 -*-
"""CAS.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xyzuy-sgaKXC8C2oWN_SuiT6JSnGPr_8
"""

import numpy as np
import matplotlib.pyplot as plt
from google.colab.patches import cv2_imshow
import cv2
import math

class Solidification():
  def __init__(self, p0 = 0.5):
    self.constituent = np.zeros((400,400))
    self.state = np.zeros((400,400))
    self.p0 = p0
    self.mu_a_nvkt = -5.0
    self.mu_b_nvkt = 5.0
    self.theta = 0.10
    self.tou_s = 1.0
    self.eaa_kt = -2.0
    self.ebb_kt = -2.0
    self.eab_kt = -0.1
    self.e_kt = 2.0

  def form_sample(self):
    '''
    assign each lattice to be one of the constituents A or B
    '''
    for i in range(400):
      for j in range(400):
        self.constituent[i][j] = (np.random.uniform()<self.p0)
  
  def display_constituent(self):
    '''
    display the sample showing the constituent, white if B and black if A
    '''
    cv2_imshow(self.constituent*255)
    cv2.waitKey(5000)
  
  def display_state(self):
    '''
    display the sample showing the state, white if solid, black if liquid
    '''
    cv2_imshow(self.state*255)
    cv2.waitKey(5000)
  
  def is_valid(self,x,y):
    '''
    When exploring the neighbouring lattice, to make sure there is a neighbour at that position
    '''
    if(x>-1 and y>-1 and x<400 and y<400):
      return 1
    else:
      return 0

  def sample_point(self):
    '''
    To sample a lattice where solidification might take place
    '''
    return(int(np.random.uniform(0,399.99)),int(np.random.uniform(0,399.99)))

  def display_sample(self):
    '''
    To display the sample, white means solidifed, otherwise liquid
    Black if A and gray if B
    '''
    sample = np.zeros((400,400))
    for i in range(400):
      for j in range(400):
        sample[i][j] = max(self.state[i][j],0.5*self.constituent[i][j])
    cv2_imshow(sample*255.0)
    cv2.waitKey(5000)
  
  def check_solid_around(self,x,y):
    '''
    Check around x,y to see if there is a solid atom
    '''
    solid_atoms = []
    for i in range(-1,2):
      for j in range(-1,2):
        if(i==0 and j==0):
          continue
        if(self.is_valid(x+i,y+j) and self.state[x+i][y+j]==1):
          solid_atoms.append((x+i,y+j))
    if(len(solid_atoms)==0):
      return((-1,-1))
    else:
      return(solid_atoms[int(np.random.uniform(0,len(solid_atoms)))])  

  def sample_nearest(self,x,y):
    '''
    Sample one of the nearest liquid atom
    '''
    points = []
    for i in range(-1,2):
      for j in range(-1,2):
        if(not (i*j==0)):
          continue
        if(i==0 and j==0):
          continue
        if(self.is_valid(x+i,y+j) and self.constituent[x][y]!=self.constituent[x+i][y+j] and self.state[x+i][y+j]==0):
          points.append((x+i,y+j))
    if(len(points)==0):
      return((-1,-1))
    return(points[int(np.random.uniform(0,len(points)))])

  def count_ab(self,x,y):
    '''
    count nearest A-B bonds
    '''
    count = 0
    for i in range(-1,2):
      for j in range(-1,2):
        if(not (i*j==0)):
          continue
        if(i==0 and j==0):
          continue
        if(self.is_valid(x+i,y+j) and self.constituent[x+i][y+j]!=self.constituent[x][y] and self.state[x+i][y+j]==0):
          count += 1
    return (count)

  def count_ab_n(self,x,y):
    '''
    count next-nearest A-B bonds
    '''
    count = 0
    for i in range(-1,2):
      for j in range(-1,2):
        if(i*j==0):
          continue
        if(self.is_valid(x+i,y+j) and self.constituent[x+i][y+j]!=self.constituent[x][y] and self.state[x+i][y+j]==0):
          count += 1
    return count

  def count_aa(self,x,y):
    '''
    count nearest A-A bonds
    '''
    count = 0
    for i in range(-1,2):
      for j in range(-1,2):
        if(not (i*j==0)):
          continue
        if(i==0 and j==0):
          continue
        if(self.is_valid(x+i,y+j) and self.constituent[x+i][y+j]==0 and self.state[x+i][y+j]==0):
          count += 1
    return count
   
  def count_aa_n(self,x,y):
    '''
    count second nearest A-A bonds
    '''
    count = 0
    for i in range(-1,2):
      for j in range(-1,2):
        if(i*j==0):
          continue
        if(self.is_valid(x+i,y+j) and self.constituent[x+i][y+j]==0 and self.state[x+i][y+j]==0):
          count += 1
    return count

  def count_bb(self,x,y):
    '''
    count nearest B-B bonds
    '''
    count = 0
    for i in range(-1,2):
      for j in range(-1,2):
        if(not (i*j==0)):
          continue
        if(i==0 and j==0):
          continue
        if(self.is_valid(x+i,y+j) and self.constituent[x+i][y+j]==1 and self.state[x+i][y+j]==0):
          count += 1
    return count
   
  def count_bb_n(self,x,y):
    '''
    count second nearest B-B bonds
    '''
    count = 0
    for i in range(-1,2):
      for j in range(-1,2):
        if(i*j==0):
          continue
        if(self.is_valid(x+i,y+j) and self.constituent[x+i][y+j]==1 and self.state[x+i][y+j]==0):
          count += 1
    return count

  def count_bonds(self, x, y):
    '''
    count nearest solid liquid bonds
    '''
    count = 0
    for i in range(-1,2):
      for j in range(-1,2):
        if(not (i*j==0)):
          continue
        if(i==0 and j==0):
          continue
        if(self.is_valid(x+i,y+j) and self.state[x+i][y+j]==0):
          count += 1
    return count
   
  def count_bonds_n(self, x, y):
    '''
    count next solid liquid bonds
    '''
    count = 0
    for i in range(-1,2):
      for j in range(-1,2):
        if(i*j==0):
          continue
        if(self.is_valid(x+i,y+j) and self.state[x+i][y+j]==0):
          count += 1
    return count
   
  def G_T(self, x, y):
    '''
    Calculate the free energy change at the location x, y
    '''
    
    if (self.constituent[x][y]==0):
      G_T = self.mu_a_nvkt + (self.count_aa(x,y) + self.theta * self.count_aa_n(x,y))*self.eaa_kt + (self.count_ab(x,y)+ 
                                                                                                     self.theta*self.count_ab_n(x,y))*self.eab_kt 
      + (self.count_bonds(x,y) + self.theta*self.count_bonds_n(x,y))*self.e_kt
    else:
      G_T = self.mu_b_nvkt + (self.count_bb(x,y) + self.theta * self.count_bb_n(x,y))*self.ebb_kt + (self.count_ab(x,y)+ 
                                                                                                     self.theta*self.count_ab_n(x,y))*self.eab_kt 
      + (self.count_bonds(x,y) + self.theta*self.count_bonds_n(x,y))*self.e_kt
    return G_T

  def calculate_prob_solidify(self,x,y):
    '''
    Calculate the probability to solidify at x,y using the G_T function
    '''
    prob = (1/self.tou_s)*math.exp(-self.G_T(x,y))/(1+math.exp(-self.G_T(x,y))) 
    return (prob)

  def calculate_prob_melt(self,x,y):
    '''
    Calculate the probability to solidify at x,y using the G_T function
    '''
    prob = (1/self.tou_s)*math.exp(self.G_T(x,y))/(1+math.exp(self.G_T(x,y)))
    return (prob)

  def one_step_transform(self):
    '''
    Do all the tranformations at 1 time step, it maybe doing nothing if the point sample is solid, or may see if solidification is possible or maybe just
    a transport between two atoms of different constituents
    '''
    for i in range(400*400):
      x, y = self.sample_point()
      if(self.state[x][y]==1): 
        continue
      x_, y_ = self.check_solid_around(x,y)
      if (x_ == -1):
        near_x, near_y = self.sample_nearest(x,y)
        if(near_x == -1):
          continue
        temp = self.constituent[x][y]
        self.constituent[x_][y_] = temp
        self.constituent[x][y] = 1-temp
      else:
        prob_solidify = self.calculate_prob_solidify(x,y)
        prob_melt = self.calculate_prob_melt(x,y)
        if(prob_solidify>prob_melt):
          self.state[x][y] = 1
    return  

  def solidify(self,steps):
    '''
    Assume a point which will act as the nucleation site and the growth starts from there for 'steps' number of time steps
    '''
    x, y = int(np.random.uniform()*50+175) , int(np.random.uniform()*50+175)
    self.state[x][y] = 1
    for n in range(steps):
      self.one_step_transform()
      if(not(n%5==0)):
        continue
      print("step ", n)
      self.display_sample()
    return

sample = Solidification()
sample.form_sample()
sample.display_constituent()
sample.solidify(100)
sample.display_sample()

def count_aa(self,x1,y1,x2,y2):
    count = 0
    for i in range(x1, x2+1):
      for j in range(y1,y2+1):
        if (self.constituent[i][j]==1 or self.state[i][j]==1):
          continue
        else:
          i_, j_ = i, j+1
          if(i_ <= x2 and j_<=y2 and self.constituent[i_][j_] == 0 and self.state[i_][j_] == 0):
            count++
          i_, j_ = i+1, j
          if(i_ <= x2 and j_<=y2 and self.constituent[i_][j_] == 0 and self.state[i_][j_] == 0):
            count++
    return count
          
  def count_ab(self,x1,y1,x2,y2):
    count = 0
    for i in range(x1, x2+1):
      for j in range(y1,y2+1):
        if (self.state[i][j]==1):
          continue
        else:
          i_, j_ = i, j+1
          if(i_ <= x2 and j_<=y2 and self.constituent[i_][j_] != self.constituent[i][j] and self.state[i_][j_] == 0):
            count++
          i_, j_ = i+1, j
          if(i_ <= x2 and j_<=y2 and self.constituent[i_][j_] != self.constituent[i][j] and self.state[i][j] == 0):
            count++
    return count
    
  def count_bb(self,x1,y1,x2,y2):
    count = 0
    for i in range(x1, x2+1):
      for j in range(y1,y2+1):
        if (self.constituent[i][j]==0 or self.state[i][j]==1):
          continue
        else:
          i_, j_ = i, j+1
          if(i_ <= x2 and j_<=y2 and self.constituent[i_][j_] == 1 and self.state[i_][j_] == 0):
            count++
          i_, j_ = i+1, j
          if(i_ <= x2 and j_<=y2 and self.constituent[i_][j_] == 1 and self.state[i_][j_] == 0):
            count++
    return count