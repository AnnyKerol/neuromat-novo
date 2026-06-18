from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from slugify import slugify
from ..extensions import db
from ..models import Content
from .. import CATEGORIES
admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/")
@login_required
def dashboard():
    counts = {c: Content.query.filter_by(category=c).count() for c in CATEGORIES}
    return render_template("admin/dashboard.html", counts=counts)

@admin_bp.route("/content")
@login_required
def list_content():
    category = request.args.get("category")
    q = Content.query
    if category in CATEGORIES: q = q.filter_by(category=category)
    items = q.order_by(Content.published_at.desc()).all()
    return render_template("admin/list.html", items=items, category=category)

@admin_bp.route("/content/new", methods=["GET", "POST"])
@admin_bp.route("/content/<int:item_id>/edit", methods=["GET", "POST"])
@login_required
def edit_content(item_id=None):
    item = Content.query.get_or_404(item_id) if item_id else Content()
    if request.method == "POST":
        f = request.form
        item.title_pt = f["title_pt"]; item.title_en = f.get("title_en")
        item.summary_pt = f.get("summary_pt"); item.summary_en = f.get("summary_en")
        item.body_pt = f.get("body_pt"); item.body_en = f.get("body_en")
        item.category = f["category"]
        item.slug = f.get("slug") or slugify(f["title_pt"])
        item.authors = f.get("authors"); item.media_embed = f.get("media_embed")
        item.external_url = f.get("external_url"); item.location = f.get("location")
        item.published = bool(f.get("published"))
        if not item.id: db.session.add(item)
        db.session.commit()
        flash("Conteudo salvo / Content saved.", "success")
        return redirect(url_for("admin.list_content"))
    return render_template("admin/form.html", item=item)
