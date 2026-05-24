from nicegui import ui


def inject_head_html() -> None:
    """Inject common head HTML (fonts, tailwind) in a style that avoids long lines.

    The HTML is split into multiple shorter string literals so style checkers
    don't complain about very long lines.
    """
    html = (
        '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        '<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700'
        '&family=Source+Sans+3:wght@400;500;600&display=swap" rel="stylesheet">\n'
        '<script src="https://cdn.tailwindcss.com"></script>\n'
        '<style>\n'
        '    body {\n'
        '        @apply bg-orange-200;\n'
        '    }\n'
        '</style>\n'
    )
    ui.add_head_html(html)


__all__ = ["inject_head_html"]
