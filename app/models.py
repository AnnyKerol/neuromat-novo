from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import g
from .extensions import db, login_manager


def _localized(obj, base):
    """Retorna o campo no idioma ativo (g.lang), com fallback para PT."""
    lang = getattr(g, "lang", "pt")
    val = getattr(obj, f"{base}_{lang}", None)
    return val or getattr(obj, f"{base}_pt", None) or getattr(obj, f"{base}_en", None) or ""


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    name = db.Column(db.String(150))
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=True)
    def set_password(self, pw): self.password_hash = generate_password_hash(pw)
    def check_password(self, pw): return check_password_hash(self.password_hash, pw)


@login_manager.user_loader
def load_user(user_id): return User.query.get(int(user_id))


class Content(db.Model):
    __tablename__ = "content"
    id = db.Column(db.Integer, primary_key=True)
    # campos bilingues
    title_pt = db.Column(db.String(300), nullable=False)
    title_en = db.Column(db.String(300))
    summary_pt = db.Column(db.Text)
    summary_en = db.Column(db.Text)
    body_pt = db.Column(db.Text)
    body_en = db.Column(db.Text)
    # campos neutros (iguais nos dois idiomas)
    slug = db.Column(db.String(320), unique=True, nullable=False)
    category = db.Column(db.String(50), nullable=False, index=True)
    authors = db.Column(db.String(400))
    media_embed = db.Column(db.Text)
    external_url = db.Column(db.String(500))
    location = db.Column(db.String(300))
    event_start = db.Column(db.Date)
    event_end = db.Column(db.Date)
    deadline = db.Column(db.Date)
    featured_image = db.Column(db.String(500))
    published = db.Column(db.Boolean, default=True, index=True)
    published_at = db.Column(db.Date, default=date.today, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # acessores que devolvem o idioma ativo
    @property
    def title(self): return _localized(self, "title")
    @property
    def summary(self): return _localized(self, "summary")
    @property
    def body(self): return _localized(self, "body")


class TeamMember(db.Model):
    __tablename__ = "team_members"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    affiliation = db.Column(db.String(300))
    role_group_pt = db.Column(db.String(120), index=True)
    role_group_en = db.Column(db.String(120))
    status = db.Column(db.String(80))
    sort_order = db.Column(db.Integer, default=0)
    @property
    def role_group(self): return _localized(self, "role_group")


class Page(db.Model):
    __tablename__ = "pages"
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(150), unique=True, nullable=False)
    title_pt = db.Column(db.String(300), nullable=False)
    title_en = db.Column(db.String(300))
    body_pt = db.Column(db.Text)
    body_en = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    @property
    def title(self): return _localized(self, "title")
    @property
    def body(self): return _localized(self, "body")
