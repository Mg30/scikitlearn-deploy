import typer
import boto3


        

app = typer.Typer()

@app.command()
def create_bucket(name: str):
    try:
        s3 = boto3.resource('s3')
        s3.Bucket(name).create()
        versioning = s3.BucketVersioning(name)
        versioning.enable()
        typer.echo(f"bucket {name} created")
    except Exception as e:
        typer.echo(f"error : {e}")


@app.command()
def delete_bucket(name: str):
    try:
        s3 = boto3.resource('s3')
        s3.Bucket(name).delete()
        typer.echo(f"bucket {name} deleted")
    except Exception as e:
        typer.echo(f"error : {e}")

@app.command()
def list_objects(name: str):
    try:
        s3 = boto3.resource('s3')
        objects = s3.Bucket(name).object_versions.all()
        print(objects)

    except Exception as e:
        typer.echo(f"error : {e}")