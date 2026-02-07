# Import the main SQLModel metadata
from sqlmodel import SQLModel 

# Import every single model class you've created
from app.models.bundlePosting import BundlePosting # noqa
from app.models.consumer import Consumer # noqa
from app.models.forecast import Forecast # noqa
from app.models.record import Record # noqa
from app.models.reservation import Reservation # noqa
from app.models.seller import Seller # noqa
from app.models.user import User # noqa

# Now, when you call this metadata elsewhere, 
# it includes all the models listed above.
metadata = SQLModel.metadata