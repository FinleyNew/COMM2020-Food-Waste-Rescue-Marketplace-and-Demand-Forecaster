from app.services import reservation as reservation_service
import pytest
from unittest.mock import MagicMock
from  app.models.enums import ReservationStatus

#Post and reservation class to mimic the real ones and be stored in memory for testing purposes.
class SimplePosting:
    def __init__(self, id, owner_id):
        self.id = id
        self.owner_id = owner_id

class SimpleReservation:
    def __init__(self, id, status, claim_code, posting):
        self.id = id
        self.status = status
        self.claim_code = claim_code
        self.posting = posting

#Tests collect_by_code is functional with a correct claim code and seller.
def test_collection_with_valid_code_success(mock_db):
    post = SimplePosting(id=201, owner_id=2)
    res = SimpleReservation(
        id=101, 
        status="PENDING", 
        claim_code="ABC123",
        posting=post
    )

    import app.crud.reservation as reservation_crud
    
    # Ensures when the mock database is used in the CRUD it returns the reservation with the correct claim code
    def dynamic_get(claim_code, seller_id, db):
        if claim_code == "ABC123":
            return res
        return None 

    reservation_crud.get_reservation_by_claim_code = MagicMock(side_effect=dynamic_get)
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None

    
    reservation_service.collect_by_code(
        claim_code="ABC123",
        seller_id=2,
        db=mock_db
    )

    
    assert res.status == ReservationStatus.COLLECTED 
    mock_db.commit.assert_called_once() 

#tests if the collection fails for the right collection code but wrong seller 

def test_collection_with_wrong_seller(mock_db):
    
    post = SimplePosting(id=201, owner_id=2)
    res = SimpleReservation(
        id=101, 
        status="PENDING", 
        claim_code="ABC123",
        posting=post
    )

    import app.crud.reservation as reservation_crud
    
    # Ensures when the mock database is used in the CRUD it returns the reservation with the correct claim code
    def dynamic_get(claim_code, seller_id, db):
        if claim_code == "ABC123":
            return res
        return None 

    reservation_crud.get_reservation_by_claim_code = MagicMock(side_effect=dynamic_get)
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None

    with pytest.raises(Exception): #Should raise an error because the seller ID does not match the posting owner ID
        reservation_service.collect_by_code(
        claim_code="ABC123",
        seller_id=100,  # Wrong seller ID
        db=mock_db
    )

    
    assert res.status == ReservationStatus.RESERVED
    mock_db.commit.assert_called_once() 


def test_collection_with_invalid_code(mock_db):
    post = SimplePosting(id=201, owner_id=2)
    res = SimpleReservation(
        id=101, 
        status="PENDING", 
        claim_code="ABC123",
        posting=post
    )

    import app.crud.reservation as reservation_crud
    
    # Ensures when the mock database is used in the CRUD it returns the reservation with the correct claim code
    def dynamic_get(claim_code, seller_id, db):
        if claim_code == "ABC123":
            return res
        return None 

    reservation_crud.get_reservation_by_claim_code = MagicMock(side_effect=dynamic_get)

   
    with pytest.raises(Exception): 
        reservation_service.collect_by_code(
            claim_code="WRONGCODE",
            seller_id=2,
            db=mock_db
        )

    
    mock_db.commit.assert_not_called()
     
def test_no_show_count(mock_db):
    #Create a list of reservations with different statuses for a specific posting
    reservations = [
        SimpleReservation(id=1, status="", claim_code="CODE1", posting=SimplePosting(id=201, owner_id=2)),
        SimpleReservation(id=2, status="COLLECTED", claim_code="CODE2", posting=SimplePosting(id=201, owner_id=2)),
        SimpleReservation(id=3, status="", claim_code="CODE3", posting=SimplePosting(id=201, owner_id=2)),
    ]

    import app.crud.reservation as reservation_crud
    
    
    reservation_crud.get_reservations_by_posting = MagicMock(return_value=reservations)
    no_show_count = reservation_service.get_no_show(posting_id=201, db=mock_db)

    
    assert no_show_count == 2