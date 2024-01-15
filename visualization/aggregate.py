import json

import pandas as pd


def filter_results():
    with open("logs/results.v.2.0.0.json") as f:
        results: dict[str, list[dict]] = json.load(f)
    filtered_list = []
    for dataset_name in results:
        dataset_results = results[dataset_name]
        for result in dataset_results:
            if result['model']['optuna']:
                continue
            if not result['dataset']['standardization']:
                pass


            filtered_list.append({
                'dataset': result['dataset']['name'],
                'model': result['model']['name'],
                'layers': str(result['ae']['layers']),
                'majority': result['result']['majority']['f1'],
                'minority': result['result']['minority']['f1'],
                'macro': result['result']['macro']['f1'],
            })
    df = pd.DataFrame(filtered_list)
    df.to_csv("logs/filtered_results.csv", index=False)

if __name__ == '__main__':
    filter_results()