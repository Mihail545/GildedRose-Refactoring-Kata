# -*- coding: utf-8 -*-

class ItemUpdater:
    """
    Base class for item update strategies.
    
    Implements the Strategy pattern for updating different types of items
    in the Gilded Rose inventory system. Each item type has its own
    specific update rules implemented in a concrete subclass.
    """
    
    def update(self, item):
        """
        Update the item's sell_in and quality values according to business rules.
        
        Args:
            item: The Item instance to update
            
        Raises:
            NotImplementedError: Must be implemented by subclasses
        """
        raise NotImplementedError("Subclasses must implement update method")
    
    def decrease_sell_in(self, item, amount=1):
        """Decrease sell_in by the specified amount"""
        item.sell_in = item.sell_in - amount

    def increase_quality(self, item, amount=1):
        """Increase the item's quality, automatically capped at maximum of 50."""
        item.quality = min(50, item.quality + amount)

    def decrease_quality(self, item, amount=1):
        """Decrease the item's quality, automatically floored at minimum of 0."""
        item.quality = max(0, item.quality - amount)

    def set_quality_to_zero(self, item):
        """Set the item's quality to 0 (used for expired backstage passes)."""
        item.quality = 0


class StandardItemUpdater(ItemUpdater):
    """
    Updates standard items with normal degradation rules.
    
    Standard items decrease in quality by 1 per day before the sell date,
    and by 2 per day after the sell date has passed.
    """
    
    def update(self, item):
        # Decrease quality by 1 before sell date
        self.decrease_quality(item, 1)
        
        # Update sell_in
        self.decrease_sell_in(item, 1)
        
        # After sell date, decrease quality by 1 more (total 2 per day)
        if item.sell_in < 0:
            self.decrease_quality(item, 1)


class AgedBrieUpdater(ItemUpdater):
    """
    Updates Aged Brie items which improve with age.
    
    Aged Brie increases in quality by 1 per day before the sell date,
    and by 2 per day after the sell date has passed. Quality is capped at 50.
    """
    
    def update(self, item):
        # Increase quality by 1 before sell date
        self.increase_quality(item, 1)
        
        # Update sell_in
        self.decrease_sell_in(item, 1)
        
        # After sell date, increase quality by 1 more (total 2 per day)
        if item.sell_in < 0:
            self.increase_quality(item, 1)


class BackstagePassUpdater(ItemUpdater):
    """
    Updates Backstage passes with complex quality increase rules.
    
    Quality increases by:
    - 1 per day when more than 10 days until concert
    - 2 per day when 6-10 days until concert  
    - 3 per day when 1-5 days until concert
    - 0 (drops to zero) after the concert
    """
    
    def update(self, item):
        # Base quality increase
        self.increase_quality(item, 1)
        
        # Additional increases based on days until concert
        if item.sell_in < 11:  # 10 days or less
            self.increase_quality(item, 1)
        
        if item.sell_in < 6:   # 5 days or less
            self.increase_quality(item, 1)
        
        # Update sell_in
        self.decrease_sell_in(item, 1)
        
        # After concert (sell_in < 0 after decrement), quality drops to 0
        if item.sell_in < 0:
            self.set_quality_to_zero(item)


class SulfurasUpdater(ItemUpdater):
    """
    Updates Sulfuras, the legendary item.
    
    Sulfuras never changes in quality or sell_in value as it is a legendary item
    with a fixed quality of 80 that never degrades.
    """
    
    def update(self, item):
        # Legendary items never change
        pass


class ConjuredItemUpdater(ItemUpdater):
    """
    Updates Conjured items which degrade twice as fast as normal items.
    
    Conjured items decrease in quality by 2 per day before the sell date,
    and by 4 per day after the sell date has passed.
    """
    
    def update(self, item):
        # Decrease quality by 2 before sell date
        self.decrease_quality(item, 2)
        
        # Update sell_in
        self.decrease_sell_in(item, 1)
        
        # After sell date, decrease quality by 2 more (total 4 per day)
        if item.sell_in < 0:
            self.decrease_quality(item, 2)


def get_updater_for(item):
    """
    Factory function that returns the appropriate updater for an item.
    
    Args:
        item: The Item instance to get an updater for
        
    Returns:
        ItemUpdater: The appropriate updater based on the item's name
    """
    if item.name == "Aged Brie":
        return AgedBrieUpdater()
    elif item.name.startswith("Backstage passes"):
        return BackstagePassUpdater()
    elif item.name.startswith("Sulfuras"):
        return SulfurasUpdater()
    elif item.name.startswith("Conjured"):
        return ConjuredItemUpdater()
    else:
        return StandardItemUpdater()


class GildedRose:
    """
    Main class for the Gilded Rose inventory management system.
    
    Manages a collection of items and updates their quality and sell_in
    values according to the specific business rules for each item type.
    """

    def __init__(self, items):
        """
        Initialize the Gilded Rose with a list of items.
        
        Args:
            items: List of Item instances to manage
        """
        self.items = items

    def update_quality(self):
        """
        Update the quality and sell_in values for all items.
        
        Uses the Strategy pattern to delegate to appropriate updaters
        based on each item's type.
        """
        for item in self.items:
            updater = get_updater_for(item)
            updater.update(item)


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
