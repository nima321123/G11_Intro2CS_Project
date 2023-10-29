# Import the module
import torchvision
from torchvision.datasets import ImageFolder
from torchvision import transforms
from torch.utils.data import DataLoader
import torch.nn as nn
import torch
import torch.optim as optim
import torchmetrics

# Download resnet18
model = torchvision.models.resnet18(pretrained=True)

# Define transformation and Data augmentation for Train data
train_transform = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(45),
    transforms.ToTensor(),
    transforms.Resize((224, 224)),
])
dataset_train = ImageFolder(
    "C:\\Users\\Admin\\Desktop\\G11 IntroCS Project\\ProjectTemplate1\\dataset\\flowers",
    transform = train_transform,
)

# Data augmentation for test data
test_transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Resize((224, 224)),
])
dataset_test = ImageFolder(
    "C:\\Users\\Admin\Desktop\\G11 IntroCS Project\\ProjectTemplate1\\dataset\\smaller dataset\\flowers_test",
    transform = test_transform
)   

# Use Pytorch's DataLoader function to create a data loader
dataloader_train = DataLoader(
    dataset_train,
    shuffle=True,
    batch_size=32,
)

dataloader_test = DataLoader(
    dataset_test,
    shuffle=True,
    batch_size=32,
)

# Freeze all the layers bar the last one
for param in model.parameters():
    param.requires_grad = False

# Change the number of output units
# Classifier: more than one linear layer
model.fc = nn.Sequential(
   nn.Linear(512, 1024), # First linear layer
   nn.ReLU(),           # Activation function
   nn.Linear(1024, 512), # Second linear layer
   nn.ReLU(),           # Activation function
   nn.Linear(512, 5)    # Output layer with 5 units (for 5 flower species)
)

# Define a loss function and an optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.001, momentum=0.9)

# Train the network
for epoch in range(5):  # loop over the dataset multiple times

    running_loss = 0.0
    for i, data in enumerate(dataloader_train, 0):
        # get the inputs; data is a list of [inputs, labels]
        inputs, labels = data

        # zero the parameter gradients
        optimizer.zero_grad()

        # forward + backward + optimize
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        # print statistics
        running_loss += loss.item()
        
    print(f'Epoch {epoch + 1}, Loss: {running_loss / len(dataloader_train)}')

print('Finished Training')

# Calculate precision for each class after training
class_correct = list(0. for i in range(5))
class_total = list(0. for i in range(5))
with torch.no_grad():
    for i, data in enumerate(dataloader_test):
        images, labels = data
        outputs = model(images)
        _, predicted = torch.max(outputs, 1)
        c = (predicted == labels).squeeze()

        # Update the class-wise total count inside of the for loop.
        class_total[labels.item()] += 1



# Calculate precision for each class after training
class_correct = list(0. for i in range(5))
class_total = list(0. for i in range(5))
with torch.no_grad():
    for data in dataloader_test:
        images, labels = data
        outputs = model(images)
        _, predicted = torch.max(outputs, 1)
        c = (predicted == labels).squeeze()
        label = labels.item()
        class_correct[label] += c.item()
        class_total[label] += 1
classes = ['daisy', 'dandelion', 'rose', 'sunflower', 'tulip']

for i in range(5):
    print('Precision of %5s : %2d %%' % (
        classes[i], 100 * class_correct[i] / class_total[i]))


