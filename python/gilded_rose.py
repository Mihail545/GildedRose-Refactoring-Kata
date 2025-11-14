# -*- coding: utf-8 -*-

class GildedRose(object):

    def __init__(self, items):
        self.items = items

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

    def update_quality(self):
        for item in self.items:
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
            if item.name != "Sulfuras, Hand of Ragnaros":
                self.decrease_sell_in(item, 1)
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


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
