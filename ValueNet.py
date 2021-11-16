import torch
import torch.nn as nn
import torch.optim as optim
from tqdm import tqdm
import numpy as np

channels = 4
DIM = 64
EPOCHS = 25
BATCH_SIZE = 8

if torch.cuda.is_available():
    Device = torch.device("cuda")
else:
    Device = torch.device("cpu")

class ValueNet(nn.Module):

    def __init__(self):
        super().__init__()

        self._to_linear = None

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

        x = torch.rand(1, 4, 81)
        x = self.convs(x)
        self._to_linear = x[0].shape[0] * x[0].shape[1]

        self.tail = nn.Sequential(
            nn.Linear(in_features=self._to_linear, out_features=512),
            nn.Linear(in_features=512, out_features=1)   
        )

    def forward(self, x):
        x = self.convs(x)
        x = x.view(-1, self._to_linear)
        x = self.tail(x)
        return x

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
            data_len = len(training_data_X) // BATCH_SIZE * BATCH_SIZE
            for i in tqdm(range(0, data_len, BATCH_SIZE)):
                BATCH_X = training_data_X[i:i+BATCH_SIZE].view(BATCH_SIZE, 4, 81)
                BATCH_Y = training_data_Y[i:i+BATCH_SIZE].view(-1, 1)

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
