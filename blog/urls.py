from blog import views as view


url_patterns = (
    '/section', view.section,
    '/', view.index,
    '', view.index
    )
