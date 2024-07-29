import pickle
import os
import time
import boto3
import pandas as pd
from ucimlrepo import fetch_ucirepo
from sklearn.ensemble import RandomForestClassifier


def download_dataset() -> pd.DataFrame:
    print("Dataset loading...")
    automobile = fetch_ucirepo(id=10)

    dataset = automobile.data.features
    # print(automobile.metadata)
    # print(automobile.variables)
    return dataset


def prepare_data(dataset) -> pd.DataFrame:
    columns_to_use = ["highway-mpg", "curb-weight"]
    dataset = dataset[columns_to_use]
    return dataset


def train_random_forest(X: pd.DataFrame, y: pd.Series) -> RandomForestClassifier:
    print("Training the model...")
    model = RandomForestClassifier()
    model.fit(X, y)
    return model


def save_model(model) -> None:
    output_file = "model.pkl"

    # Save the model as a pickle file
    with open(output_file, "wb") as f_out:
        pickle.dump(model, f_out)
    print("Model saved locally as", output_file)

    # Upload the pickle file to localstack S3
    time.sleep(5)
    S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL")
    print(f"S3_ENDPOINT_URL: {S3_ENDPOINT_URL}")
    if S3_ENDPOINT_URL:
        s3 = boto3.client(
            "s3",
            endpoint_url=S3_ENDPOINT_URL,
            aws_access_key_id="abc",
            aws_secret_access_key="xyz",
            region_name="us-east-1",
        )
        bucket_name = "localstack-bucket"
        s3.create_bucket(Bucket=bucket_name)
        print(f"Bucket {bucket_name} created")

        s3.upload_file(output_file, bucket_name, output_file)
        print(f"Model saved and uploaded to {bucket_name}/{output_file}")


def main():
    dataset = download_dataset()
    dataset = prepare_data(dataset)
    model = train_random_forest(X=dataset[["curb-weight"]], y=dataset["highway-mpg"])
    save_model(model)


if __name__ == "__main__":
    main()
