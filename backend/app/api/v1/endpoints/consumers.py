
@router.get("/me", response_model = ConsumerPublic)
def get_current_consumer(current_consumer: ConsumerDep)