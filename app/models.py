from django.db import models
import uuid


class Poet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    website = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    phoneNum = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    status = models.BooleanField(default=True)
    zipCode = models.CharField(max_length=255, null=True, blank=True)
    isLaureate = models.BooleanField(default=False)
    photoCredit = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    deletedAt = models.DateTimeField(null=True, blank=True)
    legalFirstName = models.CharField(max_length=255, default="anonymous")
    legalLastName = models.CharField(max_length=255, default="anonymous")
    creditedFirstName = models.CharField(max_length=255, default="anonymous")
    creditedLastName = models.CharField(max_length=255, default="anonymous")
    poetImage = models.CharField(max_length=255, null=True, blank=True)
    poetBiography = models.TextField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "poet"

    def __str__(self):
        return self.legalFirstName + " " + self.legalLastName


class Era(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    deletedAt = models.DateTimeField(blank=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "era"


class PoemType(models.Model):
    poemTypeId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    deletedAt = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "poem_type"


class SpecialTag(models.Model):
    specialTagId = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    name = models.CharField(max_length=255)
    deletedAt = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "special_tag"


class PoemTopic(models.Model):
    poemTopicId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    deletedAt = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "poem_topic"


class Language(models.Model):
    languageId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255, null=True, blank=True)
    deletedAt = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "language"


class Poem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, blank=True, null=True)
    poetId = models.CharField(max_length=255, blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)
    audioLink = models.CharField(max_length=255, blank=True, null=True)
    producerName = models.CharField(max_length=255, blank=True, null=True)
    narratorName = models.CharField(max_length=255, blank=True, null=True)
    recordingDate = models.DateTimeField(blank=True, null=True)
    recordingSource = models.CharField(max_length=255, blank=True, null=True)
    poemEra = models.CharField(max_length=255, blank=True, null=True)
    poemTypes = models.TextField(blank=True, null=True)
    poemTopics = models.TextField(blank=True, null=True)
    # poemSpecialTags = models.TextField(blank=True, null=True)
    language = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=False)
    # optionalLegal = models.TextField(blank=True, null=True)
    isChildrensPoem = models.BooleanField(default=False)
    isAdultPoem = models.BooleanField(default=False)
    deletedAt = models.DateTimeField(blank=True, null=True)
    recordingDuration = models.CharField(max_length=255, blank=True, null=True)
    telepoemNumber = models.CharField(max_length=255, blank=True, null=True)
    copyRights = models.CharField(max_length=255, blank=True, null=True)
    poemText = models.TextField(blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.telepoemNumber == "0":
            self.telepoemNumber = "0"
        super(Poem, self).save(*args, **kwargs)

    class Meta:
        db_table = "poem"


class PoetAndPoem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    poemId = models.UUIDField()
    poetId = models.UUIDField()

    class Meta:
        db_table = "poet_and_poem"

    def __str__(self):
        return f"{self.poetId} - {self.poemId}"


class PoemCollection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    poemCollectionName = models.CharField(max_length=255, blank=True, null=True)
    poemCollectionDescription = models.TextField(blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "poem_collection"

    def __str__(self):
        return self.poemCollectionName


class PoemCollectionAndPoem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    poemCollectionId = models.UUIDField()
    poemId = models.UUIDField()
    deletedAt = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "poem_collection_and_poem"

    def __str__(self):
        return str(self.id)


class PhoneType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    deletedAt = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "phone_type"


class TelepoemBoothType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    deletedAt = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "telepoem_booth_type"


class DirectoryType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    deletedAt = models.DateTimeField(blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "directory_type"


class BoothMaintainer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    phoneNumber = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    deletedAt = models.DateTimeField(blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    zip = models.CharField(max_length=255, blank=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "booth_maintainer"

    def __str__(self):
        return self.name


class Booth(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    boothName = models.CharField(max_length=255)
    number = models.CharField(max_length=255, blank=True, null=True)
    phoneTypeId = models.CharField(max_length=255, blank=True, null=True)
    # boothTypeId = models.CharField(max_length=255, blank=True, null=True)
    directoryTypeId = models.CharField(max_length=255, blank=True, null=True)
    # directoryTabletSerialNumber = models.CharField(
    #     max_length=255, blank=True, null=True
    # )
    physicalAddress = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    zipCode = models.IntegerField(blank=True, null=True)
    installationDate = models.CharField(max_length=255, blank=True, null=True)
    installationType = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=True)
    isADAAccessible = models.BooleanField(default=False)
    # phoneSerialNumber = models.CharField(max_length=255, blank=True, null=True)
    highlightedCriteria = models.CharField(max_length=255, blank=True, null=True)
    # installationNotes = models.TextField(blank=True, null=True)
    deletedAt = models.DateTimeField(blank=True, null=True)
    maintainerName = models.CharField(max_length=255, blank=True, null=True)
    maintainerEmail = models.CharField(max_length=255, blank=True, null=True)
    maintainerNumber = models.CharField(max_length=255, blank=True, null=True)
    # deviceInfo = models.TextField(blank=True, null=True)
    boothImage = models.CharField(max_length=255, blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "booth"

    def __str__(self):
        return self.boothName


class BoothAndPoemCollection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    boothId = models.UUIDField()
    poemCollectionId = models.UUIDField()
    deletedAt = models.DateTimeField(blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "booth_and_poem_collection"

    def __str__(self):
        return str(self.id)
