import torch
import numpy as np
from sklearn.metrics import roc_auc_score, f1_score

# AUC
def compute_AUCs(true, pred, n_class) :
    AUCs = []
    for i in range(n_class) :
        try :
            auc = roc_auc_score(true[:,i], pred[:,i])
        except ValueError :
            auc = float('nan')
        AUCs.append(auc)
    return AUCs

# evaluation
def eval(loader, model, device, n_class= 5) :
    trues, preds = [], []
    model.eval()
    with torch.no_grad() :
        for inputs, targets in loader :
            inputs, targets = inputs.to(device), targets.to(device)
            
            outputs = model(inputs)
            trues.append(targets.cpu().numpy())
            preds.append(outputs.cpu().numpy())
    trues = np.vstack(trues)
    preds = np.vstack(preds)
    
    # AUC
    aucs = compute_AUCs(trues, preds, n_class)
    average_auc = np.mean([auc for auc in aucs if not np.isnan(auc)])
    
    # f1
    f1_scores = [f1_score(trues[:, i], np.round(preds[:, i]), average= 'binary') for i in range(n_class)]
    average_f1 = np.mean(f1_scores)
    
    return {'auc': average_auc, 'f1': average_f1}