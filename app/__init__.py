from flask import Flask, g, request, session
from .config import Config
from .extensions import db, migrate, login_manager

SUPPORTED_LANGS = ("pt", "en")

# Rotulos fixos da interface (nav, botoes, etc.) nos dois idiomas
TRANSLATIONS = {
    "pt": {
        "about": "Sobre o NeuroMat", "who_we_are": "Quem somos",
        "the_project": "O Projeto NeuroMat", "team": "Equipe",
        "reports": "Relatorios", "contact": "Contato",
        "research": "Pesquisa", "scientific_project": "Projeto Cientifico",
        "publications": "Publicacoes", "lectures": "Palestras",
        "innovation": "Inovacao", "dissemination": "Difusao",
        "news": "Noticias", "videos": "Videos", "radio": "Radio",
        "newsletter": "Newsletter", "events": "Eventos",
        "opportunities": "Oportunidades", "read_more": "Leia mais",
        "search": "Buscar", "subscribe": "Inscrever-se",
        "related_projects": "Projetos Relacionados", "follow_us": "Siga-nos",
        "supported_by": "Apoio FAPESP", "hosted_by": "Sediado na USP",
        "page_of": "Pagina", "of": "de",
    },
    "en": {
        "about": "About NeuroMat", "who_we_are": "Who we are",
        "the_project": "The NeuroMat Project", "team": "Team",
        "reports": "Reports", "contact": "Contact",
        "research": "Research", "scientific_project": "Scientific Project",
        "publications": "Publications", "lectures": "Lectures",
        "innovation": "Innovation", "dissemination": "Dissemination",
        "news": "News", "videos": "Videos", "radio": "Radio",
        "newsletter": "Newsletter", "events": "Events",
        "opportunities": "Opportunities", "read_more": "Read more",
        "search": "Search", "subscribe": "Subscribe",
        "related_projects": "Related Projects", "follow_us": "Follow Us",
        "supported_by": "Supported by FAPESP", "hosted_by": "Hosted by USP",
        "page_of": "Page", "of": "of",
    },
}

CATEGORIES = {
    "news": {"pt": "Noticias", "en": "News"},
    "events": {"pt": "Eventos", "en": "Events"},
    "publications": {"pt": "Publicacoes", "en": "Publications"},
    "lectures": {"pt": "Palestras", "en": "Lectures"},
    "videos": {"pt": "Videos", "en": "Videos"},
    "radiocast": {"pt": "Radio", "en": "Radio"},
    "opportunities": {"pt": "Oportunidades", "en": "Opportunities"},
}


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app); migrate.init_app(app, db); login_manager.init_app(app)

    from .public.routes import public_bp
    from .admin.routes import admin_bp
    from .auth.routes import auth_bp
    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(auth_bp, url_prefix="/auth")

    from . import cli
    cli.register(app)

    @app.before_request
    def set_language():
        lang = request.args.get("lang")
        if lang in SUPPORTED_LANGS:
            session["lang"] = lang
        g.lang = session.get("lang", "pt")

    @app.context_processor
    def inject_globals():
        lang = getattr(g, "lang", "pt")
        def t(key): return TRANSLATIONS.get(lang, {}).get(key, key)
        def cat_label(c): return CATEGORIES.get(c, {}).get(lang, c)
        return {"CATEGORIES": CATEGORIES, "lang": lang, "t": t,
                "cat_label": cat_label, "SUPPORTED_LANGS": SUPPORTED_LANGS}

    return app
