import argparse
import json
from sklearn.metrics import mean_squared_error, accuracy_score
from scipy.stats import pearsonr

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def main(pred_path, gt_path):
    pred_data = load_json(pred_path)
    gt_data = load_json(gt_path)

    # Align keys
    common_keys = list(set(pred_data.keys()) & set(gt_data.keys()))
    if not common_keys:
        raise ValueError("No overlapping video URLs between prediction and ground truth.")

    preds = [pred_data[k] for k in common_keys]
    gts = [gt_data[k] for k in common_keys]

    # Compute metrics
    acc = accuracy_score(gts, preds)
    mse = mean_squared_error(gts, preds)
    pcc, _ = pearsonr(gts, preds)

    print(f"Evaluation on {len(common_keys)} samples:")
    print(f"  ACC: {acc:.4f}")
    print(f"  MSE: {mse:.4f}")
    print(f"  PCC: {pcc:.4f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path1", type=str, required=True, help="Path to predicted result JSON")
    parser.add_argument("--input_path2", type=str, required=True, help="Path to ground truth JSON")
    args = parser.parse_args()

    main(args.input_path1, args.input_path2)
