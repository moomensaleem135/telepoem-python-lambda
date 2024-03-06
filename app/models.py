from django.db import models
import uuid


class Poet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    website = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    phoneNum = models.CharField(
        max_length=255, blank=True, null=True, db_column="phoneNum"
    )
    city = models.CharField(max_length=255, blank=True, null=True)
    status = models.BooleanField(default=False, blank=True, null=True)
    zipCode = models.CharField(
        max_length=255, blank=True, null=True, db_column="zipCode"
    )
    isLaureate = models.BooleanField(default=False)
    photoCredit = models.CharField(
        max_length=255, blank=True, null=True, db_column="photoCredit"
    )
    state = models.CharField(max_length=255, blank=True, null=True)
    deletedAt = models.DateTimeField(blank=True, null=True)
    legalFirstName = models.CharField(max_length=255, default="anonymous")
    legalLastName = models.CharField(max_length=255, default="anonymous")
    creditedFirstName = models.CharField(max_length=255, default="anonymous")
    creditedLastName = models.CharField(max_length=255, default="anonymous")
    poetImage = models.CharField(max_length=255, blank=True, null=True)
    poetBiography = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "poet"

    def __str__(self):
        return self.legalFirstName + " " + self.legalLastName


class Era(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    deletedAt = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "era"


class PoemType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    deletedAt = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "poem_type"


class SpecialTag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    deletedAt = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "special_tag"


class PoemTopic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    deletedAt = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "poem_topic"


class Language(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    deletedAt = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "language"


class Poem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    poetId = models.ForeignKey(Poet, on_delete=models.CASCADE)
    image = models.CharField(max_length=255, blank=True, null=True)
    audioLink = models.CharField(max_length=255, blank=True, null=True)
    producerName = models.CharField(max_length=255, blank=True, null=True)
    narratorName = models.CharField(max_length=255, blank=True, null=True)
    recordingDate = models.DateTimeField(blank=True, null=True)
    recordingSource = models.CharField(max_length=255, blank=True, null=True)
    poemEra = models.ForeignKey(Era, on_delete=models.CASCADE)
    poemTypes = models.CharField(max_length=255, blank=True, null=True)
    poemTopics = models.CharField(max_length=255, blank=True, null=True)
    poemSpecialTags = models.CharField(max_length=255, blank=True, null=True)
    language = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=False)
    optionalLegal = models.TextField(blank=True, null=True)
    isChildrenPoem = models.BooleanField(default=False, db_column="isChildrenPoem")
    isAdultPoem = models.BooleanField(default=False)
    deletedAt = models.DateTimeField(blank=True, null=True)
    recordingDuration = models.CharField(max_length=255, blank=True, null=True)
    telepoemNumber = models.CharField(max_length=255, blank=True, null=True)
    copyRights = models.CharField(max_length=255, blank=True, null=True)
    poemText = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "poem"


class PoetAndPoem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    poemId = models.ForeignKey(Poem, on_delete=models.CASCADE)
    poetId = models.ForeignKey(Poet, on_delete=models.CASCADE)

    class Meta:
        db_table = "poet_and_poem"

    def __str__(self):
        return f"{self.poetId} - {self.poemId}"


class PoemCollection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    poemCollectionName = models.CharField(max_length=255)
    poemCollectionDescription = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "poem_collection"

    def __str__(self):
        return self.poemCollectionName


class PoemCollectionAndPoem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    poemCollectionId = models.ForeignKey(PoemCollection, on_delete=models.CASCADE)
    poemId = models.ForeignKey(Poem, on_delete=models.CASCADE)
    deletedAt = models.DateField(blank=True, null=True)

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
    deletedAt = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "telepoem_booth_type"


class DirectoryType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    deletedAt = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "directory_type"


class BoothMaintainer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    phoneNumber = models.CharField(max_length=255)
    email = models.EmailField()
    createdAt = models.DateTimeField(auto_now_add=True)
    deletedAt = models.DateTimeField(null=True, blank=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip = models.CharField(max_length=255)

    class Meta:
        db_table = "booth_maintainer"

    def __str__(self):
        return self.name


class Booth(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    boothName = models.CharField(max_length=255)
    number = models.CharField(max_length=255, null=True, blank=True)
    phoneType = models.ForeignKey(PhoneType, on_delete=models.CASCADE, null=True)
    boothType = models.ForeignKey(
        TelepoemBoothType, on_delete=models.CASCADE, null=True
    )
    directoryType = models.ForeignKey(
        DirectoryType, on_delete=models.CASCADE, null=True
    )
    boothMaintainer = models.ForeignKey(
        BoothMaintainer, on_delete=models.CASCADE, null=True
    )
    directoryTabletSerialNumber = models.CharField(
        max_length=255, null=True, blank=True
    )
    physicalAddress = models.CharField(max_length=255, null=True, blank=True)
    updateDate = models.DateTimeField(auto_now=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    zipCode = models.IntegerField(null=True, blank=True)
    installationDate = models.CharField(max_length=255, null=True, blank=True)
    installationType = models.CharField(max_length=255, null=True, blank=True)
    active = models.BooleanField(default=True)
    isADAAccessible = models.BooleanField(default=False)
    phoneSerialNumber = models.CharField(max_length=255, null=True, blank=True)
    highlightedCriteria = models.CharField(max_length=255, null=True, blank=True)
    installationNotes = models.TextField(null=True, blank=True)
    deletedAt = models.DateTimeField(null=True, blank=True)
    deviceInfo = models.TextField(null=True, blank=True)
    boothImage = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "booth"

    def __str__(self):
        return self.boothName


class BoothLoggingHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    boothId = models.ForeignKey(Booth, on_delete=models.CASCADE)
    boothState = models.CharField(max_length=255)
    loggingDateTime = models.DateTimeField()
    active = models.BooleanField(default=True)

    class Meta:
        db_table = "booth_logging_history"

    def __str__(self):
        return str(self.id)


class BoothAndPoemCollection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE)
    poemCollection = models.ForeignKey(PoemCollection, on_delete=models.CASCADE)
    deletedAt = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "booth_and_poem_collection"

    def __str__(self):
        return str(self.id)
