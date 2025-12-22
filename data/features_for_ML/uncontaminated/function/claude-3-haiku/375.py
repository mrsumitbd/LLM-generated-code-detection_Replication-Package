import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from tqdm import tqdm

def train(args):
    # Configure the model
    model = nn.Sequential(
        nn.Linear(args.input_size, args.hidden_size),
        nn.ReLU(),
        nn.Linear(args.hidden_size, args.output_size)
    )

    # Configure the loss function and optimizer
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=args.learning_rate)

    # Configure the dataloader
    train_dataset = args.train_dataset
    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True)

    # Train the model
    for epoch in range(args.num_epochs):
        running_loss = 0.0
        for inputs, labels in tqdm(train_loader, desc=f"Epoch {epoch+1}/{args.num_epochs}", leave=False):
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
        print(f"Epoch {epoch+1}/{args.num_epochs}, Loss: {running_loss / len(train_loader):.4f}")

    return model