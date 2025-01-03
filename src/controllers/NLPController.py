from .BaseController import BaseController
from models.db_schemes import Project, DataChunks
from stores.llm.LLMEnums import DocumentTypeEnum
from typing import List
import json

class NLPController(BaseController):

    def __init__(self, vectordb_client, generation_client, 
                 embedding_client, template_parser):
        super().__init__()

        self.vectordb_client = vectordb_client
        self.generation_client = generation_client
        self.embedding_client = embedding_client
        self.template_parser = template_parser

    def create_collection_name(self, project_id: str):
        return f"collection_{project_id}".strip()
    
    def reset_vector_db_collection(self, project: Project):
        collection_name = self.create_collection_name(project_id=project.project_id)
        return self.vectordb_client.delete_collection(collection_name=collection_name)
    
    def get_vector_db_collection_info(self, project: Project):
        collection_name = self.create_collection_name(project_id=project.project_id)
        collection_info = self.vectordb_client.get_collection_info(collection_name=collection_name)

        return json.loads(
            json.dumps(collection_info, default=lambda o: o.__dict__) # convert object to dict for json serialization
        )

    def index_into_vector_db(self,project: Project,chunks_ids:List[int] ,data_chunks: List[DataChunks], do_reset: bool = False):
        # step 1:get collection name
        collection_name = self.create_collection_name(project_id=project.project_id)

        # step 2:manage items in the collection
        texts=[c.chunk_text for c in data_chunks]
        metadata=[c.chunk_metadata for c in data_chunks]
        vectors=[
            self.embedding_client.embed_text(text=text,document_type=DocumentTypeEnum.DOCUMENT.value)

            for text in texts
        ]
        

        # step 3: create collection in vector db if not existed
        _ = self.vectordb_client.create_collection(
            collection_name=collection_name,
            embedding_size=self.embedding_client.embedding_size,
            do_reset=do_reset
        )

        # step 4: insert data chunks into vector db
        _ = self.vectordb_client.insert_many(
            collection_name=collection_name,
            texts=texts,
            vectors=vectors,
            metadata=metadata,
            record_ids=chunks_ids
            )
        return True
    
    # search_vector_db_collection for search route in nlp.py
    def search_vector_db_collection(self, project: Project, query: str, limit: int = 5):

        # step 1 :get collection name
        collection_name = self.create_collection_name(project_id=project.project_id)
        # step 2: get text embeddings from vector db
        vector = self.embedding_client.embed_text(text=query, document_type=DocumentTypeEnum.QUERY.value)
        if not vector:
            return False
        # step 3: semantic search in vector db
        search_results = self.vectordb_client.search_by_vector(
            collection_name=collection_name,
            vector=vector,
            limit=limit
        )
        if not search_results:
            return False
        return search_results

    def answer_rag_question(self, project: Project, query: str, limit: int = 10):

        answer,full_prompt,chat_history = None,None,None
        # step 1: retrieve related documents
        retrived_documents = self.search_vector_db_collection(project=project, query=query, limit=limit)

        if not retrived_documents or len(retrived_documents) == 0:
            return  answer,full_prompt,chat_history
        
        # step 2: construct LLM prompt
        system_prompt = self.template_parser.get_template(group="rag",key="system_prompt")

        document_prompts ="\n".join([
            self.template_parser.get_template(group="rag",key="document_prompt",vars={
                    "doc_num":idx+1,
                    "chunk_text":doc.text
                    })
            for idx,doc in enumerate(retrived_documents)
        ])

        footer_prompt = self.template_parser.get_template(group="rag",key="footer_prompt")

        chat_history = [
            self.generation_client.construct_prompt(
                prompt=system_prompt,
                role=self.generation_client.enums.SYSTEM.value),
        ]

        full_prompt ="\n\n".join([document_prompts,footer_prompt])

        answer = self.generation_client.generate_text(
            prompt=full_prompt,
            chat_history=chat_history,
            max_output_tokens=200,
            temperature=float(0.5)
        )

        return answer,full_prompt,chat_history

