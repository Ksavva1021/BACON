import yaml
import argparse
import subprocess
import json


def create_jsons(args):
    with open(f'samples/{args.year}.yaml') as f:
        samples = yaml.load(f, Loader=yaml.FullLoader)

    subprocess.run(['gfal-mkdir', f'{args.destination_path}/Run3/{args.year}'])
    for sample in samples:
        subprocess.run(['gfal-mkdir', f'{args.destination_path}/Run3/{args.year}/{sample}'])

    for sample in samples:
        source_sample_path = f'{args.source_path}/{args.year}/{sample}'

        result = subprocess.run(['gfal-ls', source_sample_path], capture_output=True, text=True, check=True)
        files = result.stdout.splitlines()

        data = {
            "files": []
        }

        for file in files:
            file_entry = {
                "sources": [f'{source_sample_path}/{file}'],
                "destinations": [f'{args.destination_path}/Run3/{args.year}/{sample}/{file}']
            }
            data["files"].append(file_entry)

        
        with open(f'jsons/{args.year}/{sample}.json', 'w') as f:
            json.dump(data, f, indent=4)
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create JSONs from YAMLs')
    parser.add_argument('--year', required=True, help='Year to process')
    parser.add_argument('--destination_path', required=False, help='Path to create directories on dcache', default='davs://gfe02.grid.hep.ph.ic.ac.uk:2880/pnfs/hep.ph.ic.ac.uk/data/cms/store/user/ksavva')
    parser.add_argument('--source_path', required=False, help='Path to sample root files', default='davs://eoscms.cern.ch/eos/cms/store/group/phys_higgs/HLepRare/skim_2024_v1')
    args = parser.parse_args()

    create_jsons(args) 

