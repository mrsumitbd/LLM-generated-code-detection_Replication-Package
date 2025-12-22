def train(args):
    # configure strategy
    import torch
    import torch.nn as nn
    import torch.optim as optim
    from torch.utils.data import DataLoader
    import os
    
    # Set device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # Set random seeds for reproducibility
    torch.manual_seed(args.seed if hasattr(args, 'seed') else 42)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(args.seed if hasattr(args, 'seed') else 42)
    
    # Create model
    model = args.model.to(device)
    
    # Create optimizer
    optimizer = optim.Adam(
        model.parameters(),
        lr=args.learning_rate if hasattr(args, 'learning_rate') else 1e-3,
        weight_decay=args.weight_decay if hasattr(args, 'weight_decay') else 0
    )
    
    # Create loss function
    criterion = nn.CrossEntropyLoss() if hasattr(args, 'criterion') is False else args.criterion
    
    # Create data loaders
    train_loader = args.train_loader if hasattr(args, 'train_loader') else None
    val_loader = args.val_loader if hasattr(args, 'val_loader') else None
    
    # Training loop
    num_epochs = args.num_epochs if hasattr(args, 'num_epochs') else 10
    
    for epoch in range(num_epochs):
        # Training phase
        model.train()
        train_loss = 0.0
        
        if train_loader is not None:
            for batch_idx, (data, target) in enumerate(train_loader):
                data, target = data.to(device), target.to(device)
                
                optimizer.zero_grad()
                output = model(data)
                loss = criterion(output, target)
                loss.backward()
                optimizer.step()
                
                train_loss += loss.item()
        
        # Validation phase
        if val_loader is not None:
            model.eval()
            val_loss = 0.0
            correct = 0
            total = 0
            
            with torch.no_grad():
                for data, target in val_loader:
                    data, target = data.to(device), target.to(device)
                    output = model(data)
                    loss = criterion(output, target)
                    val_loss += loss.item()
                    
                    _, predicted = torch.max(output.data, 1)
                    total += target.size(0)
                    correct += (predicted == target).sum().item()
            
            accuracy = 100 * correct / total if total > 0 else 0
            
            if hasattr(args, 'verbose') and args.verbose:
                print(f'Epoch {epoch+1}/{num_epochs}, '
                      f'Train Loss: {train_loss/len(train_loader):.4f}, '
                      f'Val Loss: {val_loss/len(val_loader):.4f}, '
                      f'Val Accuracy: {accuracy:.2f}%')
    
    # Save model if path is provided
    if hasattr(args, 'save_path') and args.save_path:
        os.makedirs(os.path.dirname(args.save_path) or '.', exist_ok=True)
        torch.save(model.state_dict(), args.save_path)
    
    return model