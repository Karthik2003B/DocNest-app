from sqlalchemy.orm import Session
from models.document import Document


class DocumentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_document(self, data: dict):
        document = Document(**data)
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        return document

    def get_documents_by_user(self, user_id: int):
        return self.db.query(Document).filter(Document.user_id == user_id).all()

    def get_document_by_id(self, document_id: int):
        return self.db.query(Document).filter(Document.id == document_id).first()

    def delete_document(self, document):
        self.db.delete(document)
        self.db.commit()