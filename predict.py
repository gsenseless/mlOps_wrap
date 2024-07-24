import os
import time
import click
import boto3
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier


def download_model() -> RandomForestClassifier:
    input_file = "model.pkl"

    # Download the model from localstack S3
    S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL")
    if S3_ENDPOINT_URL:
        time.sleep(5)
        s3 = boto3.client(
            "s3",
            endpoint_url=S3_ENDPOINT_URL,
            aws_access_key_id="abc",
            aws_secret_access_key="xyz",
            region_name="us-east-1",
        )
        bucket_name = "localstack-bucket"
        s3.download_file(bucket_name, input_file, input_file)
        print(f"Model downloaded from {bucket_name}/{input_file}")
    else:
        print(
            "S3_ENDPOINT_URL not set. Attempting to load model locally from", input_file
        )

    # Load the model from the pickle file
    with open(input_file, "rb") as f_in:
        model = pickle.load(f_in)

    return model


@click.command()
@click.option("--curb_weight", type=int, required=True, help="curb weight")
def main(curb_weight):
    model = download_model()
    prediction = model.predict(pd.DataFrame({"curb-weight": [curb_weight]}))
    print(f"predicted highway MPG is {prediction}")


if __name__ == "__main__":
    main()
