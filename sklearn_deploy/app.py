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
def upload(name: str, model: str, tag: str = typer.Option(...)):
    try:
        key = os.path.basename(model)
        s3 = boto3.client("s3")
        s3.upload_file(model, name, key)
        typer.echo(f"{model} uploaded")
        objects = s3.list_object_versions(Bucket=name)
        latest = [obj for obj in objects["Versions"] if obj["IsLatest"]].pop()
        version_id = latest["VersionId"]
        s3.put_object_tagging(
            Bucket=name,
            Key=key,
            Tagging={
                "TagSet": [
                    {
                        "Key": "Version",
                        "Value": tag,
                    }
                ],
            },
            VersionId=version_id,
        )
    except Exception as e:
        typer.echo(f"error : {e}")


@app.command()
def list_objects(name: str):
    try:
        client = boto3.client("s3")
        objects = client.list_object_versions(Bucket=name)
        for version in objects["Versions"]:
            key = version["Key"]
            version_id = version["VersionId"]
            response = client.get_object_tagging(
                Bucket=name, Key=key, VersionId=version_id
            )
            typer.echo(
                f"Key: {key} VersionId: {version_id} IsLatest: {version['IsLatest']} LastModified: {version['LastModified']} Tag: {response['TagSet']}"
            )
    except Exception as e:
        typer.echo(f"error : {e}")

@app.command()
def update_lambda(func_name:str, version_id:str):
    try:
        client = boto3.client("lambda")
        response = client.get_function_configuration(
            FunctionName=func_name,
        )
        old_env = response["Environment"]["Variables"]
        old_env["MODEL_VERSION"] = version_id
        response = client.update_function_configuration(
            FunctionName=func_name,
            Environment={
                'Variables': old_env
            }
        )
        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            typer.echo("Updated")
        else:
            raise ValueError(response)
    except Exception as e:
        typer.echo(f"error : {e}")