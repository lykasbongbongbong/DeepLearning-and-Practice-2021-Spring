'''
class Net:
    #initialization
    W: [None, shape(2, 20), shape(20, 7), shape(1, 7)]
    b: [None, (20,1), (7,1), (1,1)]
    Z: [None, (20,1), (7,1), (1,1)]
    a: [None, (20,1), (7,1), (1,1)]
    learning_rate
    hidden_layer_neuron
    iterations
    main: 
        get data:
            linear / XOR
            divide them into training and testing set (50, 50)
            reshape
    #forward
    #backward
train: 
    forward
    loss 
    backward
    update_weight

test:
    forward
    loss
'''
import numpy as np
import matplotlib.pyplot as plt
def der_sigmoid(y):
    """ First derivative of Sigmoid function.
    The input to this function should be the value that output from sigmoid function.
    """
    return y * (1 - y)

def der_sigmoid(y):
    """ First derivative of Sigmoid function.
    The input to this function should be the value that output from sigmoid function.
    """
    return y * (1 - y)

class Net:
    def __init__(self):
        self.lr = 1.2
        self.hidden_layer_neurons = [20, 7, 1]
        self.epochs = 10000
        self.eps = 1e-3
        self.W = [None, np.random.randn(20, 2), np.random.randn(7, 20), np.random.randn(1, 7)]
        self.b = [None, np.random.randn(20, 1), np.random.randn(7, 1), np.random.randn(1, 1)]
        self.Z = [None, np.random.randn(20, 1), np.random.randn(7, 1), np.random.randn(1, 1)]
        self.a = [None, np.random.randn(20, 1), np.random.randn(7, 1), np.random.randn(1, 1)]
        self.gradW = [None, np.random.randn(20, 2), np.random.randn(7, 20), np.random.randn(1, 7)]
        self.gradb = [None, np.random.randn(20, 1), np.random.randn(7, 1), np.random.randn(1, 1)]
        self.gradZ = [None, np.random.randn(20, 1), np.random.randn(7, 1), np.random.randn(1, 1)]
        self.grada = [None, np.random.randn(20, 1), np.random.randn(7, 1), np.random.randn(1, 1)]
    
    def sigmoid(self, x):
            #這邊不能用import math的math.exp 因為他是array math指支援size-1 arrays 
        return 1/(1+np.exp(-x))

    def forward(self, x, y):
        self.a[0] = x
        #1st hidden layer
        self.Z[1] = np.matmul(self.W[1], self.a[0]) + self.b[1]
        self.a[1] = self.sigmoid(self.Z[1])

        #2nd hidden layer
        self.Z[2] = np.matmul(self.W[2], self.a[1]) + self.b[2]
        self.a[2] = self.sigmoid(self.Z[2])

        #3rd output layer
        self.Z[3] = np.matmul(self.W[3], self.a[2]) + self.b[3]
        self.a[3] = self.sigmoid(self.Z[3]) 
        return self.a[3]

    def calculate_loss(self, y, y_pred):
        #cross entropy: 要算第k筆data分別是0, 1的機率 -y01(log(p(0,1))) + -y11(log(p(1,1)))
        n = y.shape[1]
        loss = 1./n * (-np.matmul(y, np.log(y_pred).T) - np.matmul(1-y, np.log(1-y_pred).T))
        return float(loss)
    
    def backward(self, y, pred_y):
        #no work(need refinement)
        # 
        
        batch_size=y.shape[1]
        
        self.grada[3] = -(np.divide(y, pred_y+self.eps) - np.divide(1-y, 1-pred_y+self.eps))
        

        ##self.grada[3]=-(y/(pred_y+self.eps)-(1-y)/(1-pred_y+self.eps))
        self.gradZ[3] = np.multiply(self.grada[3], der_sigmoid(self.a[3])) 
        self.gradW[3] = np.matmul(self.gradZ[3], self.a[2].T)*(1/batch_size)
        self.gradb[3] = np.sum(self.gradZ[3], axis=1, keepdims=True)*(1/batch_size)

        self.grada[2] = np.matmul(self.W[3].T, self.gradZ[3])
        self.gradZ[2] = np.multiply(self.grada[2], der_sigmoid(self.a[2])) 
        self.gradW[2] = np.matmul(self.gradZ[2], self.a[1].T)*(1/batch_size)
        self.gradb[2] = np.sum(self.gradZ[2], axis=1, keepdims=True)*(1/batch_size)

        self.grada[1] = np.matmul(self.W[2].T,self.gradZ[2])
        self.gradZ[1] = np.multiply(self.grada[1], der_sigmoid(self.a[1])) 
        self.gradW[1] = np.matmul(self.gradZ[1], self.a[0].T)*(1/batch_size)
        self.gradb[1] = np.sum(self.gradZ[1], axis=1, keepdims=True)*(1/batch_size)
        
        return 

        
    def update_weight(self):
        
        for i in range(1,4):
            # print(i)
            # print(self.gradW[i].shape)
            self.W[i] -= self.lr * self.gradW[i]
            self.b[i] -= self.lr * self.gradb[i]
        return
        

def generate_linear(n=100):
    pts = np.random.uniform(0,1,(n,2))  
    inputs = []
    labels = []
    for pt in pts:
        inputs.append([pt[0], pt[1]])
        if pt[0] > pt[1]:
            labels.append(0)
        else:
            labels.append(1)
    return np.array(inputs), np.array(labels).reshape(n,1)


def show_result(x, y, pred_y):
    plt.subplot(1,2,1)
    plt.title('Ground Truth', fontsize=18)
    for i in range(x.shape[1]):
        if y[i] == 0:
            plt.plot(x[0][i], x[1][i], 'ro')
        else:
            plt.plot(x[0][i], x[1][i], 'bo')
    plt.show()
    plt.subplot(1,2,1)
    plt.title('Predict Result', fontsize=18)
    for i in range(x.shape[1]):
        if pred_y[i] == 0:
            plt.plot(x[0][i], x[1][i], 'ro')
        else:
            plt.plot(x[0][i], x[1][i], 'bo')
    plt.show()
    return 


def main():
    #get data and parse them into training and testing set
    x, y = generate_linear()
    x_train, y_train, x_test, y_test = np.array(x[:50].T), np.array(y[:50].T), np.array(x[50:].T), np.array(y[50:].T)
   
    model = Net()
    
    #train
    
    for i in range(model.epochs):
        y_pred = model.forward(x_train, y_train)
        loss = model.calculate_loss(y_train, y_pred)
        model.backward(y_train, y_pred)
        model.update_weight()

        if i % 1000 == 0:
            acc=(1.-np.sum(np.abs(y_train-np.round(y_pred)))/y_train.shape[1])*100
            print(f"Epochs {i}: loss={loss} accuracy={acc}%")
    # print(x_train[1].shape)
    show_result(x_train, y_train[0], np.round(y_pred[0]))

if __name__ == '__main__':
    main()