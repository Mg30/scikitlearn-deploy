from distutils.version import Version
import typer
import boto3
import os

app = typer.Typer()


@app.command()
def create_bucket(name: str):
    try:
        s3 = boto3.resource("s3")
        s3.Bucket(name).create()
        versioning = s3.BucketVersioning(name)
        versioning.enable()
        typer.echo(f"bucket {name} created")
    except Exception as e:
        typer.echo(f"error : {e}")


@app.command()
def delete_bucket(name: str):
    try:
        s3 = boto3.resource("s3")
        s3.Bucket(name).delete()
        typer.echo(f"bucket {name} deleted")
    except Exception as e:
        typer.echo(f"error : {e}")


@app.command()
def upload(name: str, model: str, tag:str):
    try:
        key = os.path.basename(model)
        s3 = boto3.client("s3")
        s3.upload_file(model, name, key)
        typer.echo(f"{model} uploaded")
        objects = s3.list_object_versions(Bucket=name)
        (latest,) = [obj for obj in objects["Versions"] if obj[" IsLatest"]]
        s3.put_object_tagging(
            Bucket=name,
            Key=key,
            Tagging={
                "TagSet": [
                    {
                        "Key": "Key3",
                        "Value": tag,
                    }
                ],
            },
            VersionId=latest
        )
    except Exception as e:
        typer.echo(f"error : {e}")


@app.command()
def list_objects(name: str):
    try:
        client = boto3.client("s3")
        objects = client.list_object_versions(Bucket=name)
        for version in objects["Versions"]:
            print(
                f"Key: {version['Key']} VersionId: {version['VersionId']} IsLatest: {version['IsLatest']} LastModified: {version['LastModified']}"
            )
    except Exception as e:
        typer.echo(f"error : {e}")