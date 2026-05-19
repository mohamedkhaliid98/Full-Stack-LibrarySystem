import mimetypes
from pathlib import Path

from django.conf import settings
from django.http import FileResponse, Http404
from django.views.decorators.http import require_GET


def _safe_path(rel: str) -> Path:
    base: Path = settings.FRONTEND_DIR
    base_resolved = base.resolve()
    target = (base / rel).resolve()
    try:
        target.relative_to(base_resolved)
    except ValueError as exc:
        raise Http404() from exc
    return target


@require_GET
def serve_frontend(request, path=""):
    rel = path.strip("/").replace("\\", "/")
    if not rel:
        rel = "index.html"

    target = _safe_path(rel)
    if target.is_dir():
        target = target / "index.html"
        if not target.exists():
            raise Http404()

    if not target.exists() or not target.is_file():
        raise Http404()

    ctype, _ = mimetypes.guess_type(str(target))
    return FileResponse(open(target, "rb"), content_type=ctype or "application/octet-stream")
