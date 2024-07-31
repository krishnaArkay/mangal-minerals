from enum import Enum

class JumboBagEntryPurpose(Enum):
    INWARD = 'Inward'
    DAMAGE = 'Damage'
    FILLED = 'Filled'
    DELIVERED = 'Delivered'
class JumboBagWarehouse(Enum):
    INWARD = 'Empty Jumbo Bag - MGSS'
    DAMAGE = 'Rejected Warehouse - MGSS'
