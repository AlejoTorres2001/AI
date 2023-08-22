import numpy as np
class Multilayer:
    def __init__(self, n_inputs, n_hidden, n_outputs):
        self.ninput = n_inputs
        self.nhidden = n_hidden
        self.noutput = n_outputs
        
        # Matriz de pesos capa 1: (filas: entradas, columnas: salidas)
        self.W1 = np.random.uniform(-0.5, 0.5, (n_inputs, n_hidden))
        self.b1 = np.random.uniform(-0.5, 0.5, (1, n_hidden))
        # Matriz de pesos capa 2: (filas: entradas, columnas: salidas)
        self.W2 = np.random.uniform(-0.5, 0.5, (n_hidden, n_outputs))
        self.b2 = np.random.uniform(-0.5, 0.5, (1, n_outputs))

    def activation(self, X):
        # Función de activación: función sigmoidal
        return 1 / (1 + np.exp(-X))
    
    def d_activation(self, X):
        # Derivada de la función de activación
        return X * (1 - X)
        
    def inference(self, X):
        if len(X.shape) == 1:
            X = np.expand_dims(X, axis=0)
        # Calculamos la salida de la capa 1
        self.S1 = self.activation(X @ self.W1 + self.b1)
        # Calculamos la salida de la capa 2
        self.S2 = self.activation(self.S1 @ self.W2 + self.b2)
        return self.S2
    
    def learn(self, X, y, alpha):
        if len(X.shape) == 1:
            X = np.expand_dims(X, axis=0)
        # Calculamos cuál es la salida para la entrada suministrada
        ŷ = self.inference(X)
        # Con ella, calculamos el error y la matriz de actualización de la última capa
        d2 = (y - ŷ) * self.d_activation(ŷ)
        dW2 = alpha * self.S1.T @ d2
        db2 = alpha * np.ones((1, d2.shape[0])) @ d2
        # Lo mismo pero con la primera capa
        d1 = d2 @ self.W2.T * self.d_activation(self.S1)
        dW1 = alpha * X.T @ d1
        db1 = alpha * np.ones((1, d1.shape[0])) @ d1
        # Por último, actualizamos los pesos de nuestra red
        self.W1 = self.W1 + dW1
        self.b1 = self.b1 + db1
        self.W2 = self.W2 + dW2
        self.b2 = self.b2 + db2
    
    def train(self, X, y, epochs, alpha, trace=1):
        for epoch in range(0, epochs):
            if epoch % trace == 0:
                accuracy, error = self.measures(X, y)
                print(f'Epoch {epoch}: Accuracy: {accuracy}, RMSE: {error}')
            self.learn(X, y, alpha)
        accuracy, error = self.measures(X, y)
        print(f'End -> {epoch}: Accuracy: {accuracy}, RMSE: {error}')
    
    def measures(self, X, y):
        ŷ = self.inference(X)
        accuracy = (y == ŷ).mean()
        rmse = np.sqrt(np.mean((y - ŷ)**2))
        return accuracy, rmse
    def to_chromosome(self):
        return np.concatenate((self.w1.flatten(), self.b1.flatten(), self.w2.flatten(), self.b2.flatten()))
    def from_chromosome(self, chromosome):
        self.W1 = np.array(chromosome[:self.ninput*self.nhidden]).reshape(self.W1.shape)
        chromosome = chromosome[self.ninput*self.nhidden:]
        self.b1 = np.array(chromosome[:self.nhidden])
        chromosome = chromosome[self.nhidden:]
        self.W2 = np.array(chromosome[:self.nhidden*self.noutput]).reshape(self.nhidden, self.noutput)
        chromosome = chromosome[self.nhidden*self.noutput:]
        self.b2 = np.array(chromosome[:self.noutput])