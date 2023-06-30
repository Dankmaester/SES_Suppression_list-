import csv
import boto3
import click
from mypy_boto3_sesv2.client import SESV2Client


def setup(profile: str = None) -> SESV2Client:
    # Setup AWS client
    session = boto3.Session(profile_name=profile)
    client = session.client("sesv2")

    return client

#getting the emails from SES 
def get_suppressed_destinations(ses: SESV2Client) -> list[dict]:
    response = ses.list_suppressed_destinations()
    destinations = response["SuppressedDestinationSummaries"]

    while response.get("NextToken"):
        response = ses.list_suppressed_destinations(NextToken=response.get("NextToken"))
        destinations.extend(response["SuppressedDestinationSummaries"])

    return list(destinations)

#write the emails to a CSV file 
def write_to_csv(destinations: list[dict]):
    with open(file="suppressed.csv", mode="w", encoding="utf8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=list(destinations[0].keys()))
        writer.writeheader()
        writer.writerows(destinations)


@click.command()
@click.option(
    "--profile", type=str, default=None, show_default=True, help="Optional AWS profile"
)
def main(profile: str):
    ses = setup(profile)
    destinations = get_suppressed_destinations(ses)
    write_to_csv(destinations)


if __name__ == "__main__":
    main()
