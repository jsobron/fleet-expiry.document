{
    'name': 'Documentos de Vehiculos',
    'version': '0.0.0',
    'category': 'Human Resources/Fleet',
    'summary': """Manages Employee Documents With Expiry Notifications.""",
    'description': 'Manages Employee Related Documents'
                   ' with Expiry Notifications.',
    'author': 'Jsobron',
    'website': "https://www.instagram.com/juansobron",
    'depends': ['fleet'],
    'data': [
        'views/expiry_document_views.xml',
        'data/ir_cron.xml',
    ],
    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
    
}
