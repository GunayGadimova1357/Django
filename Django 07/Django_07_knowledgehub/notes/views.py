from django.http import HttpRequest, HttpResponse
from django.middleware.csrf import get_token
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import escape

from notes import data


def _html_shell(title: str, body: str) -> str:
    safe_title = escape(title)
    return f"""
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{safe_title}</title>

    <link
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
        rel="stylesheet"
    >

    <style>
        :root {{
            --page-bg: #f5f7fb;
            --surface: rgba(255, 255, 255, 0.94);
            --surface-strong: #ffffff;
            --border-soft: rgba(15, 23, 42, 0.08);
            --text-main: #1f2937;
            --text-muted: #6b7280;
            --brand: #1d4ed8;
            --brand-dark: #173ea6;
            --shadow-soft: 0 18px 45px rgba(15, 23, 42, 0.08);
        }}

        body {{
            min-height: 100vh;
            color: var(--text-main);
            background:
                radial-gradient(circle at top left, rgba(59, 130, 246, 0.10), transparent 30%),
                radial-gradient(circle at bottom right, rgba(14, 165, 233, 0.08), transparent 28%),
                var(--page-bg);
        }}

        .site-header {{
            background: rgba(17, 24, 39, 0.88);
            backdrop-filter: blur(10px);
        }}

        .main-card {{
            border: 1px solid var(--border-soft);
            border-radius: 24px;
            background: var(--surface);
            box-shadow: var(--shadow-soft);
        }}

        .navbar-brand {{
            font-weight: 700;
            letter-spacing: 0.04em;
        }}

        .nav-link {{
            font-weight: 500;
        }}

        .hero-card {{
            max-width: 640px;
            margin: 0 auto;
            padding: 1rem 0;
        }}

        .section-title {{
            font-size: clamp(2rem, 4vw, 2.7rem);
            font-weight: 700;
            letter-spacing: -0.03em;
            margin-bottom: 0.75rem;
        }}

        .section-copy {{
            color: var(--text-muted);
            font-size: 1.05rem;
        }}

        .soft-card {{
            border: 1px solid var(--border-soft);
            border-radius: 18px;
            background: var(--surface-strong);
        }}

        .list-group-item {{
            border-color: var(--border-soft);
            padding-top: 1rem;
            padding-bottom: 1rem;
        }}

        .note-title {{
            color: var(--text-main);
        }}

        .note-title:hover {{
            color: var(--brand);
        }}

        .filter-bar {{
            border: 1px solid var(--border-soft);
            border-radius: 16px;
            background: rgba(248, 250, 252, 0.95);
            padding: 1rem 1.1rem;
        }}

        .form-control {{
            border-radius: 12px;
            border-color: rgba(148, 163, 184, 0.45);
            padding: 0.8rem 0.95rem;
        }}

        .form-control:focus {{
            border-color: rgba(29, 78, 216, 0.45);
            box-shadow: 0 0 0 0.25rem rgba(29, 78, 216, 0.12);
        }}

        textarea {{
            min-height: 150px;
            resize: vertical;
        }}

        .btn {{
            border-radius: 12px;
            font-weight: 600;
        }}

        .btn-primary {{
            background: var(--brand);
            border-color: var(--brand);
        }}

        .btn-primary:hover,
        .btn-primary:focus {{
            background: var(--brand-dark);
            border-color: var(--brand-dark);
        }}

        code {{
            background: #f1f3f5;
            padding: 0.15rem 0.4rem;
            border-radius: 6px;
            color: #b42363;
        }}

        .empty-state {{
            color: var(--text-muted);
            padding: 1.5rem;
            text-align: center;
        }}

        footer {{
            color: var(--text-muted);
            font-size: 0.92rem;
        }}

        @media (max-width: 768px) {{
            main.container {{
                padding-top: 2rem;
                padding-bottom: 2rem;
            }}

            .main-card {{
                border-radius: 20px;
            }}
        }}
    </style>
</head>
<body>

    <nav class="navbar navbar-expand-lg navbar-dark site-header shadow-sm">
        <div class="container">
            <a class="navbar-brand" href="{escape(reverse('home'))}">Knowledge Hub</a>

            <button
                class="navbar-toggler"
                type="button"
                data-bs-toggle="collapse"
                data-bs-target="#mainNavbar"
                aria-controls="mainNavbar"
                aria-expanded="false"
                aria-label="Toggle navigation"
            >
                <span class="navbar-toggler-icon"></span>
            </button>

            <div class="collapse navbar-collapse" id="mainNavbar">
                <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <a class="nav-link" href="{escape(reverse('home'))}">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{escape(reverse('about'))}">About</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{escape(reverse('notes_list'))}">Notes</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{escape(reverse('note_create'))}">Create note</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <main class="container py-5">
        <div class="card main-card">
            <div class="card-body p-4 p-md-5">
                {body}
            </div>
        </div>
    </main>

    <footer class="text-center py-4">
        <div class="container">
            <span>Powered by Nadir Zamanov</span>
        </div>
    </footer>

    <script
        src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js">
    </script>
</body>
</html>
"""


def _csrf_field(request: HttpRequest) -> str:
    token = get_token(request)
    return f'<input type="hidden" name="csrfmiddlewaretoken" value="{escape(token)}">'


def home(request: HttpRequest) -> HttpResponse:
    body = f"""
    <section class="hero-card text-center">
        <span class="badge rounded-pill text-bg-light border mb-3 px-3 py-2">Notes workspace</span>
        <h1 class="section-title">Knowledge Hub</h1>
        <p class="section-copy mb-4">
            because every great idea deserves to be remembered and connected        </p>
        <div class="d-flex justify-content-center gap-2 flex-wrap">
            <a href="{escape(reverse('notes_list'))}" class="btn btn-primary px-4">Open Notes</a>
            <a href="{escape(reverse('note_create'))}" class="btn btn-outline-secondary px-4">Create Note</a>
        </div>
    </section>
"""
    return HttpResponse(_html_shell("Knowledge Hub - home page", body))


def about(request: HttpRequest) -> HttpResponse:
    body = """
    <section class="hero-card text-center">
        <h1 class="section-title">About Project</h1>
        <p class="section-copy mb-3">
            Knowledge Hub is a space designed to turn thoughts into structured knowledge        </p>
        <p class="badge bg-primary-subtle text-primary px-3 py-2 rounded-pill">
            Lesson 7 • Views & Routes
        </p>
    </section>
"""
    return HttpResponse(_html_shell("Knowledge Hub - about page", body))


def notes_list(request: HttpRequest) -> HttpResponse:
    raw_tag = request.GET.get("tag")
    raw_category = request.GET.get("category")

    notes = data.list_notes()

    if raw_tag:
        tag_filter = raw_tag.strip().lower()
        notes = [n for n in notes if n["tag"].lower() == tag_filter]

    if raw_category:
        category_filter = raw_category.strip().lower()
        notes = [n for n in notes if n["category"].lower() == category_filter]

    items: list[str] = []
    for note in notes:
        url = reverse("note_detail", kwargs={"note_id": note["id"]})
        items.append(
            f"""
        <li class="list-group-item d-flex justify-content-between align-items-start">
            <div>
                <a href="{escape(url)}" class="fw-semibold text-decoration-none note-title">
                    {escape(note["title"])}
                </a>
                <div class="small text-muted mt-2">
                    Tag: <span class="badge text-bg-light border">{escape(note["tag"])}</span>
                    Category: <span class="badge bg-secondary-subtle text-dark border">{escape(note["category"])}</span>
                </div>
            </div>
        </li>
"""
        )

    items_html = "\n".join(items) if items else '<li class="list-group-item empty-state">Notes not found</li>'

    filter_hint = f"""
        <p class="small text-muted mb-0">
            Filter example:
            <a href="?tag=django"><code>?tag=django</code></a>
            <a href="?category=backend" class="ms-2"><code>?category=backend</code></a>
            <a href="{escape(reverse('notes_list'))}" class="ms-2 text-decoration-none">Reset filters</a>
        </p>
    """
    body = f"""
    <div class="mx-auto" style="max-width: 760px;">
        <div class="text-center mb-4">
            <h1 class="section-title mb-2">Notes</h1>
            <p class="section-copy mb-0">capture what matters</p>
        </div>
        <div class="soft-card overflow-hidden">
            <div class="card-body p-4">
                <ul class="list-group list-group-flush">
                    {items_html}
                </ul>
            </div>
        </div>
    </div>
    """

    return HttpResponse(_html_shell("Notes list", body))


def note_detail(request: HttpRequest, note_id: int) -> HttpResponse:
    note = data.get_note(note_id)
    if note is None:
        body = f"""
        <div class="hero-card text-center">
            <h1 class="section-title text-danger">Note not found</h1>
            <p class="section-copy mb-3">ID: <code>{escape(str(note_id))}</code></p>
            <p class="text-secondary">The requested note does not exist or was removed.</p>
            <a href="{escape(reverse('notes_list'))}" class="btn btn-primary mt-3">Return to Notes</a>
        </div>
"""
        return HttpResponse(_html_shell("Note not found", body), status=404)

    edit_url = reverse("note_edit", kwargs={"note_id": note["id"]})
    delete_url = reverse("note_delete", kwargs={"note_id": note["id"]})
    list_url = escape(reverse("notes_list"))

    body = f"""
    <div class="mx-auto" style="max-width: 760px;">
        <div class="soft-card">
            <div class="card-body p-4 p-md-5">
                <h1 class="fw-bold mb-3">{escape(note["title"])}</h1>
                <div class="mb-4 text-muted small d-flex gap-2 flex-wrap align-items-center">
                    <span>ID: <code>{note["id"]}</code></span>
                    <span class="badge text-bg-light border">{escape(note["tag"])}</span>
                    <span class="badge bg-secondary-subtle text-dark border">{escape(note["category"])}</span>
                </div>
                <div class="mb-4">
                    <p class="fs-5 mb-0">
                        {escape(note["body"]).replace(chr(10), "<br />")}
                    </p>
                </div>
                <div class="d-flex gap-2 flex-wrap">
                    <a href="{escape(edit_url)}" class="btn btn-primary">Edit</a>
                    <a href="{escape(delete_url)}" class="btn btn-danger">Delete</a>
                    <a href="{list_url}" class="btn btn-outline-primary ms-auto">Back to Notes</a>
                </div>
            </div>
        </div>
    </div>
"""
    return HttpResponse(_html_shell(note["title"], body))


def note_create(request: HttpRequest) -> HttpResponse:
    title_val = ""
    body_val = ""
    tag_val = ""
    category_val = ""
    err = ""

    if request.method == "POST":
        title = request.POST.get("title", "")
        note_body = request.POST.get("body", "")
        tag = request.POST.get("tag", "")
        category = request.POST.get("category", "")

        title_val, body_val, tag_val, category_val = title, note_body, tag, category

        if not title.strip():
            err = "<p class='text-danger small mb-3'>Title cannot be empty.</p>"
        else:
            data.create_note(
                title=title,
                body=note_body,
                tag=tag or "misc",
                category=category or "general",
            )
            return redirect("notes_list")

    form = f"""
    <div class="mx-auto" style="max-width: 640px;">
        <div class="soft-card">
            <div class="card-body p-4 p-md-5">
                <h1 class="fw-bold mb-4 text-center">New Note</h1>
                {err}
                <form method="post" action="{escape(reverse('note_create'))}">
                    {_csrf_field(request)}

                    <div class="mb-3">
                        <label class="form-label">Title</label>
                        <input
                            type="text"
                            name="title"
                            class="form-control"
                            value="{escape(title_val)}"
                            required
                        >
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Text</label>
                        <textarea
                            name="body"
                            class="form-control"
                            rows="6"
                        >{escape(body_val)}</textarea>
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Tag</label>
                        <input
                            type="text"
                            name="tag"
                            class="form-control"
                            value="{escape(tag_val)}"
                            placeholder="django"
                        >
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Category</label>
                        <input
                            type="text"
                            name="category"
                            class="form-control"
                            value="{escape(category_val)}"
                            placeholder="backend"
                        >
                    </div>

                    <div class="d-flex justify-content-between align-items-center mt-4">
                        <a href="{escape(reverse('notes_list'))}" class="text-muted text-decoration-none">
                            Cancel
                        </a>
                        <button type="submit" class="btn btn-success px-4">
                            Save
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
"""
    return HttpResponse(_html_shell("Create note", form))


def note_edit(request: HttpRequest, note_id: int) -> HttpResponse:
    note = data.get_note(note_id)
    if note is None:
        body = f"""
        <div class="hero-card text-center">
            <h1 class="section-title text-danger">Can't edit note</h1>
            <p class="section-copy">Note id: <code>{escape(str(note_id))}</code> not found.</p>
            <p><a href="{escape(reverse('notes_list'))}" class="btn btn-outline-primary mt-3">Return to Notes List</a></p>
        </div>
"""
        return HttpResponse(_html_shell("404 not found", body), status=404)

    err = ""

    if request.method == "POST":
        title = request.POST.get("title", "")
        note_body = request.POST.get("body", "")
        tag = request.POST.get("tag", "")
        category = request.POST.get("category", "")

        if not title.strip():
            err = "<p class='text-danger small mb-3'>Title cannot be empty.</p>"
            note = {
                **note,
                "title": title,
                "body": note_body,
                "tag": tag,
                "category": category,
            }
        else:
            data.update_note(
                note_id,
                title=title,
                body=note_body,
                tag=tag or "misc",
                category=category or "general",
            )
            return redirect("note_detail", note_id=note_id)

    title_e = escape(note["title"])
    note_e = escape(note["body"])
    tag_e = escape(note["tag"])
    category_e = escape(note["category"])

    form = f"""
    <div class="mx-auto" style="max-width: 640px;">
        <div class="soft-card">
            <div class="card-body p-4 p-md-5">
                <h1 class="fw-bold mb-4 text-center">Edit Note</h1>
                {err}
                <form method="post" action="{escape(reverse('note_edit', kwargs={'note_id': note_id}))}">
                    {_csrf_field(request)}

                    <div class="mb-3">
                        <label class="form-label">Title</label>
                        <input
                            type="text"
                            name="title"
                            class="form-control"
                            value="{title_e}"
                            required
                        >
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Text</label>
                        <textarea
                            name="body"
                            class="form-control"
                            rows="6"
                        >{note_e}</textarea>
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Tag</label>
                        <input
                            type="text"
                            name="tag"
                            class="form-control"
                            value="{tag_e}"
                        >
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Category</label>
                        <input
                            type="text"
                            name="category"
                            class="form-control"
                            value="{category_e}"
                        >
                    </div>

                    <div class="d-flex justify-content-between align-items-center mt-4">
                        <a href="{escape(reverse('note_detail', kwargs={'note_id': note_id}))}" class="text-muted text-decoration-none">
                            Cancel
                        </a>
                        <button type="submit" class="btn btn-success px-4">
                            Save
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
"""
    return HttpResponse(_html_shell("Edit note", form))


def note_delete(request: HttpRequest, note_id: int) -> HttpResponse:
    note = data.get_note(note_id)
    if note is None:
        body = f"""
        <div class="hero-card text-center">
            <h1 class="section-title text-danger">Can't delete note</h1>
            <p class="section-copy">Note id: <code>{escape(str(note_id))}</code> not found.</p>
            <p><a href="{escape(reverse('notes_list'))}" class="btn btn-outline-primary mt-3">Return to Notes List</a></p>
        </div>
"""
        return HttpResponse(_html_shell("404 not found", body), status=404)

    if request.method == "POST":
        data.delete_note(note_id)
        return redirect("notes_list")

    body = f"""
    <div class="mx-auto" style="max-width: 620px;">
        <div class="soft-card">
            <div class="card-body p-4 p-md-5 text-center">
                <h1 class="fw-bold text-danger mb-3">Delete note</h1>
                <p class="text-muted mb-4">
                    Are you sure you want to delete
                    <strong>{escape(note["title"])}</strong>?
                </p>

                <form method="post" action="{escape(reverse('note_delete', kwargs={'note_id': note_id}))}">
                    {_csrf_field(request)}

                    <div class="d-flex justify-content-center gap-3">
                        <a href="{escape(reverse('note_detail', kwargs={'note_id': note_id}))}" class="btn btn-outline-secondary">
                            Cancel
                        </a>
                        <button type="submit" class="btn btn-danger">
                            Delete
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
"""
    return HttpResponse(_html_shell("Delete note", body))
