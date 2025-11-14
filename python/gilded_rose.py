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
    """Handles updates for all items using the original complex logic"""
    
    def update(self, item):
        # First phase: handle quality changes before sell_in update
        if item.name != "Aged Brie" and item.name != "Backstage passes to a TAFKAL80ETC concert":
            if item.quality > 0:
                if item.name != "Sulfuras, Hand of Ragnaros":
                    self.decrease_quality(item, 1)
        else:
            if item.quality < 50:
                self.increase_quality(item, 1)
                if item.name == "Backstage passes to a TAFKAL80ETC concert":
                    if item.sell_in < 11:
                        if item.quality < 50:
                            self.increase_quality(item, 1)
                    if item.sell_in < 6:
                        if item.quality < 50:
                            self.increase_quality(item, 1)
        
        # Update sell_in
        if item.name != "Sulfuras, Hand of Ragnaros":
            self.decrease_sell_in(item, 1)
        
        # Second phase: handle quality changes after sell_in update (after sell date)
        if item.sell_in < 0:
            if item.name != "Aged Brie":
                if item.name != "Backstage passes to a TAFKAL80ETC concert":
                    if item.quality > 0:
                        if item.name != "Sulfuras, Hand of Ragnaros":
                            self.decrease_quality(item, 1)
                else:
                    self.set_quality_to_zero(item)
            else:
                if item.quality < 50:
                    self.increase_quality(item, 1)


def get_updater_for(item):
    """Return the appropriate updater for the given item"""
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
