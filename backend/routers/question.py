from fastapi import APIRouter

router = APIRouter()

@router.get("/questions")
def get_questions():
    # TODO: Get questions from the database
    pass

@router.post("/create")
def create_question():
    # TODO: Create a new question
    pass

@router.put("/update")
def update_question():
    # TODO: Update a question
    pass

@router.delete("/delete")
def delete_question():
    # TODO: Delete a question
    pass