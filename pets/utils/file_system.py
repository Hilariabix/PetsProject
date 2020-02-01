import os
import uuid

from pets import app
from werkzeug.utils import secure_filename

from pets.utils.consts import Consts


class FileSystem(object):
    @staticmethod
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in Consts.ALLOWED_EXTENSIONS

    @staticmethod
    def upload_photo_from_request(request, element_name, upload_subdir):
        # check if the post request has the file part
        file = request.files.get(element_name)
        if file and file.filename and FileSystem.allowed_file(file.filename):
            file_name = "{}-{}".format(uuid.uuid4(), secure_filename(file.filename))
            file_path = os.path.join("static", "img", upload_subdir, file_name)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_path))
            return "/" + file_path
        return None
