class Task3:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    import torchvision
    import torchvision.transforms as transforms
    import matplotlib.pyplot as plt
    import numpy as np
    


    #device configuration
    device = torch.device('cpu')
    #hyper-parameters
    num_epochs = 5
    batch_size = 32
    learning_rate = 0.001

    
    #define the transform to normalize and convert to a tensor
    transform = transforms.Compose(
        [  
         transforms.ToTensor(),
         transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
    
    #load the dataset
    train_dataset = torchvision.datasets.ImageFolder(root='C:\\Users\Admin\\Desktop\\G11 IntroCS Project\\ProjectTemplate1\\dataset\\resize', transform=transform)
    #create a data loader
    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size,
                                               shuffle=True)
    
    classes = ('daisy', 'dandelion', 'rose', 'sunflower', 'tulip')

    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=32, shuffle=True)

    
    #function to display images
    def imshow(img):
        import matplotlib.pyplot as plt
        import numpy as np
        img = img / 2 + 0.5 #unnormalize
        npimg = img.numpy()
        plt.imshow(np.transpose(npimg, (1, 2, 0)))
        plt.show()
        plt.close()

    #get some random training images
    dataiter = iter(train_loader)
    images, labels = next(dataiter)

    
    # Stack the resized images
    stacked_images = torch.stack([img for img in images])

    #show images
    imshow(torchvision.utils.make_grid(stacked_images))

    conv1 = nn.Conv2d(3, 6, 5)
    pool = nn.MaxPool2d(2, 2)
    conv2 = nn.Conv2d(6, 16, 5)
    print(images.shape)

    

    input_size = 64  # Adjust this to match your input image size
    conv1 = nn.Conv2d(3, 6, 5)
    pool1 = nn.MaxPool2d(2, 2)
    conv2 = nn.Conv2d(6, 16, 5)
    pool2 = nn.MaxPool2d(2, 2)


    #implement conv net
    class ConvNet(nn.Module):
        
        def __init__(self):
            import torch
            import torch.nn as nn
            import torch.nn.functional as F
            super().__init__()

            self.conv1 = nn.Conv2d(3, 6, 5)
            self.pool = nn.MaxPool2d(2, 2)
            self.conv2 = nn.Conv2d(6, 16, 5)
            self.fc1 = nn.Linear(16 * 57 * 77, 120)
            self.fc2 = nn.Linear(120, 84)
            self.fc3 = nn.Linear(84, 5)  # Adjust the output size according to your problem

        def forward(self, x):
            import torch
            import torch.nn as nn
            import torch.nn.functional as F
            x = self.pool(F.relu(self.conv1(x)))
            x = self.pool(F.relu(self.conv2(x)))

            # Flatten the feature map before passing it to the fully connected layer
            x = x.view(-1, 16 * 57 *77)
            
            x = F.relu(self.fc1(x))
            x = F.relu(self.fc2(x))
            x = self.fc3(x)
            return x
    
    
    # Create an instance of the model
    model = ConvNet()
    # Loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

    #total number of steps
    n_total_steps = len(train_loader)

    
    # Training loop
    for epoch in range(num_epochs):
        for i, (images, labels) in enumerate(train_loader):
            # Forward pass
            
            output = model(images)
            loss = criterion(output, labels)


            # Backward pass and optimization
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if (i+1) % 2000 == 0:
                print(f'Epoch [{epoch+1}/{num_epochs}], Step [{i+1}/{n_total_steps}], Loss: {loss.item()}')

    # Evaluation (optional)
    with torch.no_grad():
        # Calculate accuracy, class-specific accuracy, and overall accuracy
        n_correct = 0
        n_samples = 0
        n_class_correct = [0 for i in range(5)]
        n_class_samples = [0 for i in range(5)]
        
        for images, labels in train_loader:
            images = images.to(device)
            labels = labels.to(device)
            outputs = model(images)
            
            _, predicted = torch.max(outputs, 1)
            n_samples += labels.size(0)
            n_correct += (predicted == labels).sum().item()

            for i in range(5):
                label = labels[i]
                pred = predicted[i]
                if (label == pred):
                    n_class_correct[label] += 1
                n_class_samples[label] += 1

        for i in range(5):
            acc = 100.0 * n_class_correct[i] / n_class_samples[i]
            print(f'Accuracy of {classes[i]}: {acc}%')

        overall_acc = 100.0 * n_correct / n_samples
        print(f'Overall Accuracy: {overall_acc:.2f}%')
