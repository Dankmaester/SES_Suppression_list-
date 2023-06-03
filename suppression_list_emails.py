import os
import boto3
import argparse
from datetime import datetime
import pandas as pd


def setup(profile: str = None):
    script_dir = os.path.dirname(__file__)
    rules_file_path = os.path.join(script_dir, "emails.txt")
    session = boto3.Session(profile_name=profile)
    client = session.client('sesv2')
    return client, rules_file_path


def retrieve_suppressed_destinations(client, reasons, start_date, end_date):
    destinations = []
    next_token = None
    while True:
        params = {
            'Reasons': reasons,
            'StartDate': start_date,
            'EndDate': end_date,
            'PageSize': 1000,
        }
        if next_token:
            params['NextToken'] = next_token

        response = client.list_suppressed_destinations(**params)

        destinations += response['SuppressedDestinationSummaries']
        next_token = response.get('NextToken')

        if not next_token:
            break

    return destinations


def main(profile):
    client, rules_file_path = setup(profile)
    suppressed_destinations = retrieve_suppressed_destinations(
        client,
        reasons=['BOUNCE', 'COMPLAINT'],
        start_date=datetime(2015, 1, 1),
        end_date=datetime(2023, 6, 1)
    )

    df = pd.DataFrame(suppressed_destinations)
    df.to_csv('suppression_emails_list.csv', index=False)
    print("CSV file with the emails has been created.")


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--profile", action="store", type=str
    )
    args = arg_parser.parse_args()
    main(args.profile)
