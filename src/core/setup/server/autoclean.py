from src.core.utils import attach_file_cleanup

from src.users.models import User

from src.admins.models import Notary

from src.builders.models import ComplexGallery, Document


def setup_autoclean():
    attach_file_cleanup(User, ["photo"])

    attach_file_cleanup(Notary, ["photo"])

    attach_file_cleanup(ComplexGallery, ["photo"])
    attach_file_cleanup(Document, ["file"])
