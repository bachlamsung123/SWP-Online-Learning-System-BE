from fastapi import APIRouter, Depends

from ..database.course import CategoryCrud
from ..database.user import UserRole
from ..middleware.auth import exclude_roles, require_existed
from ..schema.base import Detail
from ..schema.course import Category, CategoryCreate, CategoryUpdate

auth_middleware = {
    "dependencies": [Depends(exclude_roles(UserRole.USER))],
    "tags": ["Staff", "Expert", "Category"]
}

category_router = APIRouter()


@category_router.get("", response_model=list[Category], tags=["Category"])
async def read_all_categories(limit: int = 100, offset: int = 0):
    return await CategoryCrud.find_all(limit, offset)


@category_router.post("", response_model=Detail, **auth_middleware)
async def create_category(data: CategoryCreate):
    return {"detail": await CategoryCrud.create(data.dict())}


@category_router.put("/{id}", response_model=Detail, **auth_middleware)
async def update_category_by_id(data: CategoryUpdate, category: CategoryCrud = Depends(require_existed(CategoryCrud))):
    await CategoryCrud.update_by_id(category.id, data.dict(exclude_none=True))
    return {"detail": "Updated"}


@category_router.delete("/{id}", response_model=Detail, **auth_middleware)
async def delete_category_by_id(category: CategoryCrud = Depends(require_existed(CategoryCrud))):
    await CategoryCrud.delete_by_id(category.id)
    return {"detail": "Deleted"}
