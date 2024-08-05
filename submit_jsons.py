import subprocess
import argparse
import yaml


def submit_jsons(args):
    results = subprocess.run(['ls', f'jsons/{args.year}'], capture_output=True, text=True, check=True)
    jsons = results.stdout.splitlines()

    yaml_dict = {}
    for json_file in jsons:

        submission_results = subprocess.run(f'fts-rest-transfer-submit -s https://fts00.grid.hep.ph.ic.ac.uk:8446 -f jsons/{args.year}/{json_file}', shell=True, capture_output=True, text=True, check=True)
        print(submission_results.args)
        yaml_dict[json_file] = submission_results.stdout

    with open(f'submissions/{args.year}.yaml', 'w') as f:
        yaml.dump(yaml_dict, f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Submit Transfer')
    parser.add_argument('--year', required=True, help='Year to process')
    args = parser.parse_args()

    submit_jsons(args)