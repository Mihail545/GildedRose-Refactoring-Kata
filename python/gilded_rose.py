# -*- coding: utf-8 -*-

class ItemUpdater:
    """Base class for item update strategies"""
    
    def update(self, item):
        """Update the item. To be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement update method")
    
    def decrease_sell_in(self, item, amount=1):
        """Decrease sell_in by the specified amount"""
        item.sell_in = item.sell_in - amount

    def increase_quality(self, item, amount=1):
        """Increase quality by the specified amount, capped at 50"""
        item.quality = min(50, item.quality + amount)

    def decrease_quality(self, item, amount=1):
        """Decrease quality by the specified amount, floored at 0"""
        item.quality = max(0, item.quality - amount)

    def set_quality_to_zero(self, item):
        """Set quality to 0"""
        item.quality = 0


class StandardItemUpdater(ItemUpdater):
    """Handles updates for standard items (not Aged Brie, Backstage passes, or Sulfuras)"""
    
    def update(self, item):
        # Decrease quality by 1 before sell date
        self.decrease_quality(item, 1)
        
        # Update sell_in
        self.decrease_sell_in(item, 1)
        
        # After sell date, decrease quality by 1 more (total 2 per day)
        if item.sell_in < 0:
            self.decrease_quality(item, 1)


class AgedBrieUpdater(ItemUpdater):
    """Handles updates for Aged Brie items"""
    
    def update(self, item):
        # Increase quality by 1 before sell date
        self.increase_quality(item, 1)
        
        # Update sell_in
        self.decrease_sell_in(item, 1)
        
        # After sell date, increase quality by 1 more (total 2 per day)
        if item.sell_in < 0:
            self.increase_quality(item, 1)


class BackstagePassUpdater(ItemUpdater):
    """Handles updates for Backstage passes"""
    
    def update(self, item):
        # Always increase by 1 first
        self.increase_quality(item, 1)
        
        # Extra +1 when sell_in < 11 (10 days or less)
        if item.sell_in < 11:
            self.increase_quality(item, 1)
        
        # Another +1 when sell_in < 6 (5 days or less)
        if item.sell_in < 6:
            self.increase_quality(item, 1)
        
        # Update sell_in
        self.decrease_sell_in(item, 1)
        
        # After concert (sell_in < 0 after decrement), quality drops to 0
        if item.sell_in < 0:
            self.set_quality_to_zero(item)


class SulfurasUpdater(ItemUpdater):
    """Handles updates for Sulfuras items"""
    
    def update(self, item):
        # Sulfuras never changes - do nothing
        pass


class ConjuredItemUpdater(ItemUpdater):
    """Handles updates for Conjured items that degrade twice as fast"""
    
    def update(self, item):
        # Decrease quality by 2 before sell date
        self.decrease_quality(item, 2)
        
        # Update sell_in
        self.decrease_sell_in(item, 1)
        
        # After sell date, decrease quality by 2 more (total 4 per day)
        if item.sell_in < 0:
            self.decrease_quality(item, 2)


def get_updater_for(item):
    """Return the appropriate updater for the given item"""
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


class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
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
