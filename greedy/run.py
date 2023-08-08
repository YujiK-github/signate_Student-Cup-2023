import argparse
import multiprocessing
import warnings
warnings.simplefilter("ignore")
from utils import seed_everything, load_data, kfold
from feature_engineering import preprocessing, preprocessing_per_fold
from greedy import simple_greedy_selection, greedy_forward_selection


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=42, required=False)
    parser.add_argument("--greedy_type", type=str, default="simple", required=False, choices=["simple", "full"])
    parser.add_argument("--greedy_seed", type=int, default=42, required=False,
                        help="seed for simple greedy")
    parser.add_argument("--greedy_fold", type=int, default=0, required=False,
                        help="evaluate fold for simple greedy")
    parser.add_argument("--n_splits", type=int, default=5, required=False)
    parser.add_argument("--data_dir", type=str, default="G:/マイドライブ/signate_StudentCup2023/data/", required=False)
    parser.add_argument("--target_bins", type=int, default=20, required=False)
    parser.add_argument("--year_bins", type=int, default=20, required=False)
    parser.add_argument("--num_boost_round", type=int, default=10000, required=False)
    parser.add_argument("--stopping_rounds", type=int, default=1500, required=False)
    parser.add_argument("--save_dir", type=str, default="G:/マイドライブ/signate_StudentCup2023/data/", required=False)
    parser.add_argument("--base_features", type=str, nargs="*", default=['year', "odometer"], required=False)
    parser.add_argument("--debug", action="store_true", required=False)
    args = parser.parse_args()
    args.num_cores = multiprocessing.cpu_count()
    args.categorical_features = [
        "fuel", "title_status", "type", "state", "region", "manufacturer", "condition", "cylinders", "transmission", "drive", "size", "paint_color"
        ]
    if args.debug:
        args.num_boost_round = 5
        args.stopping_rounds = 1
        args.categorical_features = ["fuel"]
    args.candidate_features = []
    return args
    
    
def main(args):
    seed_everything(args.seed)
    all_data = load_data(args)
    all_data = preprocessing(all_data)
    train = kfold(args, all_data)    
    X_train, X_valid = preprocessing_per_fold(args, train, test=None, fold=args.greedy_fold, predict=False)
    if args.greedy_type == "simple":
        simple_greedy_selection(args, X_train, X_valid)
    elif args.greedy_type == "full":
        greedy_forward_selection(args, X_train, X_valid)
    return 
    
    
    
if __name__ == "__main__":
    print("="*80)
    args = parse_args()
    for k, v in vars(args).items():
        print(f"{k}: {v}")
    main(args)