from flask import Blueprint, render_template, abort, request
from ..models import Content, TeamMember, Page
from .. import CATEGORIES
public_bp = Blueprint("public", __name__)

@public_bp.route("/")
def index():
    page = request.args.get("page", 1, type=int)
    items = (Content.query.filter_by(published=True)
             .order_by(Content.published_at.desc())
             .paginate(page=page, per_page=7))
    return render_template("index.html", items=items)

@public_bp.route("/category/<category>/")
def category(category):
    if category not in CATEGORIES: abort(404)
    page = request.args.get("page", 1, type=int)
    items = (Content.query.filter_by(category=category, published=True)
             .order_by(Content.published_at.desc())
             .paginate(page=page, per_page=10))
    return render_template("category.html", items=items, category=category,
                           label=CATEGORIES[category])

@public_bp.route("/content/<slug>/")
def article(slug):
    item = Content.query.filter_by(slug=slug, published=True).first_or_404()
    return render_template("article.html", item=item)

@public_bp.route("/team/")
def team():
    members = TeamMember.query.order_by(TeamMember.role_group,
              TeamMember.sort_order, TeamMember.name).all()
    groups = {}
    for m in members: groups.setdefault(m.role_group or "Team", []).append(m)
    return render_template("team.html", groups=groups)

@public_bp.route("/<slug>/")
def page(slug):
    pg = Page.query.filter_by(slug=slug).first_or_404()
    return render_template("page.html", pg=pg)
