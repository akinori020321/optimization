# -*- coding: utf-8 -*-
import math
import random
import matplotlib.pyplot as plt

#random.seed(20220717)


def make_matrix(a, b, fill=0.0): #  NumPy を使って高速に処理する方法がある
    m = []
    for i in range(a):
        m.append([fill]*b)
    return m

class HMM:
    def __init__(self, n, sigma):
        self.n = n
        self.sigma = sigma
        self.S = make_matrix(self.n, 2)
        self.C = make_matrix(self.n, 2)

        self.x = [0]*self.n
        self.xmap = [0]*self.n
        self.y = [0.0]*self.n
        self.myx = [0]*self.n


    def generate_x(self):
        if (random.random() < 0.5):
            self.x[0] = 0
        else:
            self.x[0] = 1

        for i in range(1,self.n):
            r = random.random()
            if ( self.x[i-1] == 0 ):
                if ( r < 0.99 ):
                    self.x[i] = 0
                else:
                    self.x[i] = 1
            else:
                if ( r < 0.97 ):
                    self.x[i] = 1
                else:
                    self.x[i] = 0
        
    def generate_y(self):
        for i in range(0,self.n):
            self.y[i] = random.gauss(self.x[i],self.sigma)

    def compute_xmap(self):
      self.C[0][0] = (self.y[0] - 0)*(self.y[0] - 0)*(-1)
      self.C[0][1] = (self.y[0] - 1)*(self.y[0] - 1)*(-1)

      for i in range(1,self.n):
            #i番目が０の時
            if(self.C[i-1][0] + math.log(0.99) > self.C[i-1][1] + math.log(0.03)):
                self.C[i][0] = self.C[i-1][0] + math.log(0.99) +  (self.y[i] - 0)*(self.y[i] - 0)*(-1)
                self.S[i-1][0] = 0
            else:
                self.C[i][0] = self.C[i-1][1] + math.log(0.03) +  (self.y[i] - 0)*(self.y[i] - 0)*(-1)
                self.S[i-1][0] = 1
            #i番目が1の時
            if(self.C[i-1][0] + math.log(0.01) > self.C[i-1][1] + math.log(0.97)):
                self.C[i][1] = self.C[i-1][0] + math.log(0.01) + (self.y[i] - 1)*(self.y[i] - 1)*(-1)
                self.S[i-1][1] = 0
            else:
                self.C[i][1] = self.C[i-1][1] + math.log(0.97) + (self.y[i] - 1)*(self.y[i] - 1)*(-1)
                self.S[i-1][1] = 1

      self.S[self.n-1][0] = 0
      self.S[self.n-1][1] = 1

      if(self.C[self.n-1][0] > self.C[self.n-1][1]):
            self.xmap[self.n-1] = 3
            for i in range(self.n-1,0,-1):
                if(self.xmap[i] == 3):
                    self.xmap[i-1] = self.S[i-1][0] + 3
                elif(self.xmap[i] == 4):
                    self.xmap[i-1] = self.S[i-1][1] + 3
      else:
            self.xmap[self.n-1] = 4
            for i in range(self.n-1,0,-1):
                if(self.xmap[i] == 3):
                    self.xmap[i-1] = self.S[i-1][0] + 3
                elif(self.xmap[i] == 4):
                    self.xmap[i-1] = self.S[i-1][1] + 3

    def hamming_distance(self):
        for i in range(self.n):
          if(self.x[i] != self.xmap[i]-3):
            self.d += 1
        print(self.d)


def test20():
    n = 200
    m = 20 # m test cases
    sigma = 0.7
    hmm = HMM(n, sigma)
    z = make_matrix(m*2, n) 

    i = 0
    for line in open("r20190702_20_test_cases", "r"):
        if line[0] == "#":
            continue
        data = line.split() # 文字列を空白文字を区切りに分割

        for a in range(0,m):
#            print(a*2, i, len(data))
            z[a*2][i] = float(data[a*2])
            z[a*2+1][i] = float(data[a*2+1])
            
        i=i+1
    # データ読み込み終了    
   
    for a in range(0,m):
        for i in range(0,n):
            hmm.y[i] = z[a*2][i]
        hmm.compute_xmap()
        num_pass = 0
        for i in range(0,n):
#            print(hmm.xmap[i], z[a*2+1][i])
            if ( hmm.xmap[i] != z[a*2+1][i] ):
                print(a,":" , "not passed")
            else:
                num_pass=num_pass+1
        if ( num_pass == n):
            print(a,":" , "Passed !!!")




def demo():

    n = 200
    sigma = 0.7

    hmm = HMM(n, sigma) # 隠れマルコフモデルを作る．n: 入力信号の数
    hmm.generate_x()
    hmm.generate_y()
    hmm.compute_xmap()
        
    t = range(n)

    fig=plt.figure(0)
    plt.plot(t, hmm.x, label='$x$')
    plt.plot(t, hmm.y, '.g', label='$y$') # g は緑色， * は点
    plt.plot(t, hmm.xmap, '-r', label='$x$map')
    
    plt.title('Hidden Markov model') 
    plt.xlabel('$t$', fontsize=14, color='black') # X 軸
    plt.ylabel('$x$, $y$') # Y 軸
    plt.legend() # 描画

    plt.show() # 描画
    fig.savefig('fig_hmm213.pdf')

if __name__ == '__main__':

    demo()