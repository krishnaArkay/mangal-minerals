from enum import Enum

class JumboBagEntryPurpose(Enum):
    INWARD = 'Inward'
    DAMAGE = 'Damage'
    FILLED = 'Filled'
    DELIVERED = 'Delivered'
class JumboBagWarehouse(Enum):
    INWARD = 'Jumbo Bag Inward - MGSS'
    DAMAGE = 'Rejected Warehouse - MGSS'
