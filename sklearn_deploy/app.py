import typer
import boto3


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
def upload(name: str, model: str):
    try:
        s3 = boto3.client("s3")
        s3.put_object(Bucket=name, Body=model, Key=model)
        typer.echo(f"{model} uploaded")
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