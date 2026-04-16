from qdrant_client.async_qdrant_client import AsyncQdrantClient
from qdrant_client.models import Batch, Distance, VectorParams, HnswConfigDiff, PayloadSchemaType, UuidIndexParams, UuidIndexType,ExtendedPointId
from qdrant_client.common.client_exceptions import QdrantException

from typing import Any, List, Dict



async def createCollection(asynClient: AsyncQdrantClient, payload_m: int, m: int, vecSize: int, dist: Distance, name: str):
    if not await asynClient.collection_exists(name):
        await asynClient.create_collection(
            collection_name=name,
            vectors_config=VectorParams(size=vecSize, distance=dist, on_disk=True),
            hnsw_config=HnswConfigDiff(
                payload_m=payload_m,
                m=m
            ),
        )

        await asynClient.create_payload_index(
            collection_name=name,
            field_name="user_uid",
            field_schema=UuidIndexParams(
                type=UuidIndexType.UUID,
                is_tenant=True
            )
        )
        await asynClient.create_payload_index(
            collection_name=name,
            field_name="book_uid",
            field_schema=PayloadSchemaType.UUID
        )
        return True
    
    return False

async def batchUpsert(asynClient: AsyncQdrantClient, collection: str, identifiers: List[ExtendedPointId], payloads: List[Dict[str, Any]], vectors: List[List[float]]):
    if not await asynClient.collection_exists(collection_name=collection):
        return False
    await asynClient.upsert(
        collection_name=collection,
        points=Batch(
            ids=identifiers,
            payloads=payloads,
            vectors=vectors
        )
    )
    return True



