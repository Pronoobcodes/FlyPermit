from .models import ChecklistItem


def create_checklist_items(checklist):
    documents = checklist.visa_type.document_requirements.all()

    ChecklistItem.objects.bulk_create(
        [
            ChecklistItem(
                checklist=checklist,
                document=document
            )
            for document in documents
        ]
    )