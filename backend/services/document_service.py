from datetime import date
from fastapi import HTTPException
from repositories.document_repository import DocumentRepository


class DocumentService:
    def __init__(self, db):
        self.document_repo = DocumentRepository(db)

    def create_document(self, document_data: dict):
        return self.document_repo.create_document(document_data)

    def get_all_documents(self, user_id: int):
        return self.document_repo.get_documents_by_user(user_id)

    def get_expired_documents(self, user_id: int):
        documents = self.document_repo.get_documents_by_user(user_id)
        today = date.today()
        return [doc for doc in documents if doc.expiry_date and doc.expiry_date < today]

    def get_expiring_soon_documents(self, user_id: int):
        documents = self.document_repo.get_documents_by_user(user_id)
        today = date.today()
        expiring_soon = []

        for doc in documents:
            if doc.expiry_date:
                days_left = (doc.expiry_date - today).days
                if 0 <= days_left <= doc.reminder_days_before:
                    expiring_soon.append(doc)

        return expiring_soon

    def delete_document(self, document_id: int):
        document = self.document_repo.get_document_by_id(document_id)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")

        self.document_repo.delete_document(document)
        return {"message": "Document deleted successfully"}