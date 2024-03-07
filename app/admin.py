from django.contrib import admin
from .models import (
    Poem,
    Poet,
    PoetAndPoem,
    PoemCollection,
    PoemCollectionAndPoem,
    PhoneType,
    TelepoemBoothType,
    Era,
    PoemType,
    PoemTopic,
    SpecialTag,
    Language,
    DirectoryType,
    BoothMaintainer,
    Booth,
    BoothAndPoemCollection,
)

admin.site.register(Poem)
admin.site.register(Poet)
admin.site.register(PoetAndPoem)
admin.site.register(PoemCollection)
admin.site.register(PoemCollectionAndPoem)
admin.site.register(PhoneType)
admin.site.register(TelepoemBoothType)
admin.site.register(Era)
admin.site.register(PoemType)
admin.site.register(PoemTopic)
admin.site.register(SpecialTag)
admin.site.register(Language)
admin.site.register(DirectoryType)
admin.site.register(BoothMaintainer)
admin.site.register(Booth)
admin.site.register(BoothAndPoemCollection)
