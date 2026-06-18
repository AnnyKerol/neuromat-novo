import click
from getpass import getpass
from .extensions import db
from .models import User

def register(app):
    @app.cli.command("create-admin")
    @click.option("--email", prompt=True)
    @click.option("--name", prompt=True)
    def create_admin(email, name):
        if User.query.filter_by(email=email).first():
            click.echo("Usuario ja existe."); return
        pw = getpass("Senha: ")
        u = User(email=email, name=name, is_admin=True)
        u.set_password(pw); db.session.add(u); db.session.commit()
        click.echo("Admin criado.")

    @app.cli.command("seed")
    def seed():
        from .seed import run; run()
