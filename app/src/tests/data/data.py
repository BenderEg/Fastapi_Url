from datetime import datetime, UTC

from http import HTTPStatus

from core.config import settings

data = [(datetime(year=88, month=12, day=31, hour=14, minute=54, second=1,
                 microsecond=87, tzinfo=UTC),
        'amFo2bZ'),
        (datetime(year=2057, month=1, day=3, hour=23, minute=29, second=33,
                 microsecond=23889, tzinfo=UTC),
        'HbdxDHP'),
]

parameters_create = [({"incoming_link": "https://google.com/"},
        'https://google.com/'),
        ]

parameters_get = [({'to_cache': 'wefwe31r32f',
                    'value': 'https://google.com/'}, 200)]

parameters_get_not = [(f'{settings.domain}/wefwe31dwqdr32f/', HTTPStatus.NOT_FOUND)]