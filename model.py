import torch.nn as nn
import torch
import numpy as np
import grad_rever_function

class encoder(nn.Module):

	def __init__(self):
		super(encoder, self).__init__()

		self.cnn = nn.Sequential(
			nn.Conv2d(1, 16, 5, 1, 2),
			nn.BatchNorm2d(16),
			nn.ReLU(True),
			nn.MaxPool2d(2),
			nn.Conv2d(16, 32, 5, 1, 2),
			nn.BatchNorm2d(32),
			nn.ReLU(True),
			nn.MaxPool2d(2),
			nn.Conv2d(32, 64, 5, 1, 2),
			nn.BatchNorm2d(64),
			nn.ReLU(True)
			)

		self.fc = nn.Sequential(
			nn.Linear(7*7*64, 1024),
			nn.BatchNorm1d(1024),
			nn.ReLU(True),
			nn.Dropout(0.5),
			)

		self.cls = nn.Linear(1024, 10)


	def forward(self, x):

		feature = self.cnn(x)
		feature = feature.view(x.size(0), -1)
		feature = self.fc(feature)
		pred = self.cls(feature)

		return pred, feature


class domain_classifier(nn.Module):

	def __init__(self):
		super(domain_classifier, self).__init__()

		self.cls = nn.Sequential(
			nn.Linear(1024, 256),
			nn.BatchNorm1d(256),
			nn.ReLU(True),
			nn.Linear(256, 1)
			)

	def forward(self, feature):
		reverse_feature = grad_rever.grad_reverse(feature)

		return self.cls(reverse_feature)

