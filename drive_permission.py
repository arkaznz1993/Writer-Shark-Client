import re

import constants
from google_service import google_service

drive_service = google_service(constants.DRIVE)


def get_id_from_url(url):
    doc_id = re.search('/[-\w]{25,}/', url).group()
    doc_id = doc_id.removeprefix('/')
    doc_id = doc_id.removesuffix('/')
    return doc_id


def callback(request_id, response, exception):
    if exception:
        # Handle error
        print(exception)
    else:
        pass


batch = drive_service.new_batch_http_request(callback=callback)


def give_edit_access(docs: list):
    for doc_url in docs:
        file_id = get_id_from_url(doc_url)

        user_permission = {
            'type': 'anyone',
            'role': 'writer',
        }
        batch.add(drive_service.permissions().create(
            fileId=file_id,
            body=user_permission,
            fields='id',
        ))

    batch.execute()


def move_files_for_james(james_articles: list):
    # folder_id needs to be updated every month
    folder_id = '1FTmEPLvhZZvARLSx-EvmiDeLjtAPGrCE'
    for article in james_articles:
        file_id = get_id_from_url(article.final_link)
        # Retrieve the existing parents to remove
        file = drive_service.files().get(fileId=file_id,
                                         fields='parents').execute()
        previous_parents = ",".join(file.get('parents'))
        # Move the file to the new folder
        file = drive_service.files().update(fileId=file_id,
                                            addParents=folder_id,
                                            removeParents=previous_parents,
                                            fields='id, parents').execute()
