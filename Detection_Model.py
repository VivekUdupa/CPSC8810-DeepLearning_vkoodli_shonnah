# Importing libraries
import torch
import torchvision
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import sys # For command Line arguments

#Defining the CNN
class CNNModel(nn.Module):
    """ A CNN Model for image classification """
    
    def __init__(self,image_size, op_size):
        """ CNN layer to process the image"""
        super(CNNModel, self).__init__() # Super is used to refer to the base class, i.e nn.Module

        # Convolution Layer 1
        self.cnn1 = nn.Conv2d(in_channels=1, out_channels=16, kernel_size=3, stride=1, padding=1)
        self.relu1 = nn.ReLU()

        # Max Pooling 1
        self.maxpool1 = nn.MaxPool2d(kernel_size=2)

        # Convolution Layer 2
        self.cnn2 = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, stride=1, padding=1)
        self.relu2 = nn.ReLU()

        # Max Pooling 2
        self.maxpool2 = nn.MaxPool2d(kernel_size=2)

        # Dropout Regularization
        self.dropout = nn.Dropout(p=0.4)

        # Fully connected linear layer
        #self.fc1 = nn.Linear(32*75*75 , 9)  #32 channels, 75x75 final image size
        self.fc1 = nn.Linear(32*image_size*image_size, 100)  #32 channels, 7x7 final image size
        
        self.relu3 = nn.ReLU()
        
        self.fc2 = nn.Linear(100, 9)  #32 channels, 7x7 final image size
	
	#Image size = 28x28 -> 13x13 after first pooling
	#14x14 after padding = 1
	#7x7 after second pooling

    def forward(self, x):
        """ Forward Propogation for classification """
        
        # Convolution 1
        out = self.cnn1(x)
        out = self.relu1(out)
        
#        print("size of out1:", out.shape)

        # Max pool 1
        out = self.maxpool1(out)
#        print("size of out1 maxpool:", out.shape)

        # Convolution 2
        out = self.cnn2(out)
        out = self.relu2(out)
#        print("size of out2:", out.shape)

        # Max pool 2
        out = self.maxpool2(out)
#        print("size of out2 maxpool:", out.shape)
        
        # Resize the tensor, -1 decides the best dimension automatically
        #out = out.view(out.size(0), -1)
        out = out.view(out.size(0), -1)
#        print("size of out resize:", out.shape)

        # Dropout
        out = self.dropout(out)
#        print("size of out dropout:", out.shape)

        # Fully connected 1
        out = self.fc1(out)

        out = self.relu3(out)

        out = self.fc2(out)
#        print("size of out fc1:", out.shape)
        
        # Return
        return out