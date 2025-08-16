from typing import Any, Dict
from bson import ObjectId

def to_object_id(value: str) -> ObjectId:
	return ObjectId(value)


def stringify_id(doc: Dict[str, Any]) -> Dict[str, Any]:
	if not doc:
		return doc
	if isinstance(doc.get("_id"), ObjectId):
		doc["id"] = str(doc.pop("_id"))
	return doc


def stringify_many(docs: list[Dict[str, Any]]) -> list[Dict[str, Any]]:
	return [stringify_id(d) for d in docs]