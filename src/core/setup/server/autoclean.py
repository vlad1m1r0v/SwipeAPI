from src.core.utils import attach_file_cleanup

from src.user.models import User

from src.admin.models import Notary

from src.builder.models import ComplexGallery, Document


def setup_autoclean():
    attach_file_cleanup(User, ["photo"])

    attach_file_cleanup(Notary, ["photo"])

    attach_file_cleanup(ComplexGallery, ["photo"])
    attach_file_cleanup(Document, ["file"])
