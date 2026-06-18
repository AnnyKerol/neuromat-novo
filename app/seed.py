from datetime import date
from .extensions import db
from .models import Content, TeamMember, Page

def run():
    if Content.query.first():
        print("Ja existe conteudo, pulando seed."); return
    posts = [
        Content(category="news", slug="novo-capitulo-2026", published_at=date(2026,1,15),
            title_pt="Novo capitulo do NeuroMat comeca em 2026",
            title_en="A new chapter of NeuroMat begins in 2026",
            summary_pt="Iniciamos uma nova fase com plataforma renovada e foco em ciencia aberta.",
            summary_en="We start a new phase with a renewed platform and a focus on open science.",
            body_pt="<p>O NeuroMat inicia um novo capitulo com infraestrutura moderna.</p>",
            body_en="<p>NeuroMat begins a new chapter with modern infrastructure.</p>"),
        Content(category="events", slug="workshop-redes-estocasticas", published_at=date(2026,2,1),
            location="Auditorio NeuroMat, Sao Paulo", event_start=date(2026,3,10),
            title_pt="Workshop de Redes Neurais Estocasticas",
            title_en="Workshop on Stochastic Neural Networks",
            summary_pt="Encontro de dois dias sobre modelagem estocastica de redes neurais.",
            summary_en="A two-day meeting on stochastic modeling of neural networks.",
            body_pt="<p>Programacao com palestras nacionais e internacionais.</p>",
            body_en="<p>Program with national and international talks.</p>"),
        Content(category="publications", slug="cadeias-memoria-variavel", published_at=date(2026,1,20),
            authors="Equipe NeuroMat", external_url="https://doi.org/exemplo",
            title_pt="Cadeias estocasticas com memoria de alcance variavel",
            title_en="Stochastic chains with variable-length memory",
            summary_pt="Novo artigo sobre estimacao em cadeias com memoria de alcance variavel.",
            summary_en="A new paper on estimation in variable-length memory chains.",
            body_pt="<p>Resumo do artigo.</p>", body_en="<p>Paper abstract.</p>"),
        Content(category="opportunities", slug="bolsas-pos-doc-2026", published_at=date(2026,2,5),
            deadline=date(2026,4,30),
            title_pt="Bolsas de pos-doutorado 2026", title_en="Postdoctoral fellowships 2026",
            summary_pt="Abertas inscricoes para bolsas de pos-doutorado.",
            summary_en="Applications open for postdoctoral fellowships.",
            body_pt="<p>Detalhes e requisitos.</p>", body_en="<p>Details and requirements.</p>"),
    ]
    db.session.add_all(posts)
    db.session.add_all([
        TeamMember(name="Coordenacao Geral", affiliation="IME/USP", sort_order=1,
                   role_group_pt="Pesquisador principal", role_group_en="Principal investigator"),
        TeamMember(name="Pesquisador(a) Associado(a)", affiliation="UNICAMP", sort_order=1,
                   role_group_pt="Pesquisadores associados", role_group_en="Associate investigators"),
    ])
    db.session.add_all([
        Page(slug="who-we-are", title_pt="Quem somos", title_en="Who we are",
             body_pt="<p>O NeuroMat e um centro dedicado a neuromatematica.</p>",
             body_en="<p>NeuroMat is a center dedicated to neuromathematics.</p>"),
        Page(slug="the-neuromat-project", title_pt="O Projeto NeuroMat", title_en="The NeuroMat Project",
             body_pt="<p>Descricao do projeto.</p>", body_en="<p>Project description.</p>"),
        Page(slug="scientific-project", title_pt="Projeto Cientifico", title_en="Scientific Project",
             body_pt="<p>Projeto cientifico.</p>", body_en="<p>Scientific project.</p>"),
        Page(slug="contact", title_pt="Contato", title_en="Contact",
             body_pt="<p>Matao St., 1010 - Sao Paulo - SP.</p>",
             body_en="<p>Matao St., 1010 - Sao Paulo - SP, Brazil.</p>"),
    ])
    db.session.commit()
    print("Seed bilingue concluido.")
