import torch
import torch.nn as nn
import torch.functional as F
import torch.optim as optim
from tqdm import tqdm
import numpy as np

channels = 4
DIM = 64
EPOCHS = 50
BATCH_SIZE = 8

if torch.cuda.is_available():
    Device = torch.device("cuda")
else:
    Device = torch.device("cpu")

class ValueNet(nn.Module):

    def __init__(self):
        super().__init__()

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
            nn.Linear(in_features=2560, out_features=1)   
        )

    def forward(self, x):
        x = self.convs(x)
        x = x.view(-1, 2560)
        x = self.tail(x)
        return torch.clamp(x, min=-1, max=1)

class TrainModel():
    
    def __init__(self):

        self.model = ValueNet()
        self.model = self.model.double()
        self.model.to(Device)

        self.optimizer = optim.Adam(self.model.parameters(), lr=1e-5)
        self.loss_function = nn.MSELoss()

    def train_model(self):

        data_X = np.load("training_data_X.npy")
        data_X = torch.tensor(data_X).double().to(Device)
        data_Y = np.load("training_data_Y.npy")
        data_Y = torch.tensor(data_Y).double().to(Device)

        border_ind = int(0.9*len(data_X))

        training_data_X = data_X[0:border_ind]
        training_data_Y = data_Y[0:border_ind]

        test_data_X = data_X[border_ind:len(data_X)]
        test_data_Y = data_Y[border_ind:len(data_Y)]

        minloss = 1e10
        for epoch in range (1, EPOCHS+1):
            print(epoch)
            cumloss_train = 0
            for i in tqdm(range(0, len(training_data_X), BATCH_SIZE)):
                leftover = min(i+BATCH_SIZE, len(training_data_X))
                BATCH_X = training_data_X[i:leftover]
                BATCH_Y = training_data_Y[i:leftover].view(-1, 1)

                self.model.zero_grad()
                output = self.model(BATCH_X)
                loss = self.loss_function(output, BATCH_Y)
                cumloss_train += loss
                loss.backward()
                self.optimizer.step()

            cumloss_val = 0
            for i in range (0, len(test_data_Y)):
                with torch.no_grad():
                    X = test_data_X[i].view(-1, 4, 81)
                    Y = test_data_Y[i].view(-1, 1)
                    output = self.model(X)
                    loss = self.loss_function(output, Y)
                    cumloss_val += loss
            if cumloss_val < minloss:
                minloss = cumloss_val
                bestepoch = epoch
                bestparams = self.model.state_dict()
            print("epoch:", "training loss:", cumloss_train, "validation loss:", cumloss_val)

        print("Best epoch:", bestepoch)
        torch.save(bestparams, "state_dicts.pt")

training = TrainModel()
training.train_model()
