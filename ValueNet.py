import torch
import torch.nn as nn
import torch.functional as F
import torch.optim as optim
from tqdm import tqdm
import numpy as np

channels = 1
DIM = 64
EPOCHS = 10
BATCH_SIZE = 8

if torch.cuda.is_available():
    Device = torch.device("cuda")
else:
    Device = torch.device("cpu")

class ValueNet(nn.Module):

    def __init__(self):
        super().__init__()

        self.flattened_shape = None

        self.convs = nn.Sequential(
            nn.Conv1d(in_channels=channels, out_channels=DIM, kernel_size=4, stride=2, padding=1),
            nn.BatchNorm1d(num_features=DIM, affine=True),
            nn.ReLU(),

            nn.Conv1d(in_channels=DIM, out_channels=2*DIM, kernel_size=4, stride=2, padding=1),
            nn.BatchNorm1d(num_features=2*DIM, affine=True),
            nn.ReLU(),

            nn.Conv1d(in_channels=2*DIM, out_channels=4*DIM, kernel_size=4, stride=2, padding=1),
            nn.BatchNorm1d(num_features=4*DIM, affine=True),
            nn.ReLU()
        )

        self.tail = nn.Sequential(
            nn.Linear(in_features=self.flattened_shape, out_features=1)
            
        )

    def forward(self, x):
        x = self.convs(x)
        x = torch.flatten(x)
        self.flattened_shape = x.size(dim=1)
        x = self.tail(x)
        return x

class TrainModel():
    
    def __init__(self):

        self.model = ValueNet()
        self.model = self.model.double()
        self.model.to(Device)

        self.optimizer = optim.Adam(self.model.parameters(), lr=1e-4)
        self.loss_function = nn.MSELoss()

    def train_model(self):

        training_data_X = np.load("training_data_X.npy")
        training_data_X = torch.tensor(training_data_X).double().to(Device)
        training_data_Y = np.load("training_data_Y.npy")
        training_data_Y = torch.tensor(training_data_Y).double().to(Device)

        test_data_X = np.load("test_data_X.npy")
        test_data_X = torch.tensor(test_data_X).double().to(Device)
        test_data_Y = np.load("test_data_Y.npy")
        test_data_Y = torch.tensor(test_data_Y).double().to(Device)

        minloss = 1e10
        for epoch in range (1, EPOCHS+1):
            for i in tqdm(range(0, len(training_data_X), BATCH_SIZE)):
                BATCH_X = training_data_X[i:i+BATCH_SIZE]
                BATCH_Y = training_data_Y[i:i+BATCH_SIZE]

                self.model.zero_grad()
                output = self.model(BATCH_X)
                loss = self.loss_function(output, BATCH_Y)
                loss.backward()
                self.optimizer.step()

            cumloss = 0
            for i in range (0, len(test_data_Y)):
                with torch.no_grad():
                    X = test_data_X[i]
                    Y = test_data_Y[i]
                    
                    output = self.model(X)
                    loss = self.loss_function(output, Y)
                    cumloss += loss
            if cumloss < minloss:
                minloss = cumloss
                bestepoch = epoch
                bestparams = self.model.state_dict()

        print("Best epoch:", bestepoch)
        torch.save(bestparams, "state_dicts.pt")

training = TrainModel()
training.train_model()
