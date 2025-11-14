# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose


class GildedRoseTest(unittest.TestCase):
    
    # Standard Item Tests
    def test_standard_item_before_sell_date_decreases_quality_by_one(self):
        """Standard item before sell date should decrease quality by 1"""
        items = [Item("Standard Item", 5, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(4, items[0].sell_in)
        self.assertEqual(9, items[0].quality)
    
    def test_standard_item_after_sell_date_decreases_quality_by_two(self):
        """Standard item after sell date should decrease quality by 2"""
        items = [Item("Standard Item", 0, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(-1, items[0].sell_in)
        self.assertEqual(8, items[0].quality)
    
    def test_standard_item_quality_never_goes_negative(self):
        """Standard item quality should never go below 0"""
        items = [Item("Standard Item", 5, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(4, items[0].sell_in)
        self.assertEqual(0, items[0].quality)
    
    def test_standard_item_quality_never_goes_negative_after_sell_date(self):
        """Standard item quality should never go below 0 even after sell date"""
        items = [Item("Standard Item", 0, 1)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(-1, items[0].sell_in)
        self.assertEqual(0, items[0].quality)
    
    # Aged Brie Tests
    def test_aged_brie_increases_quality_before_sell_date(self):
        """Aged Brie should increase in quality before sell date"""
        items = [Item("Aged Brie", 5, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(4, items[0].sell_in)
        self.assertEqual(11, items[0].quality)
    
    def test_aged_brie_increases_quality_twice_after_sell_date(self):
        """Aged Brie should increase in quality by 2 after sell date"""
        items = [Item("Aged Brie", 0, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(-1, items[0].sell_in)
        self.assertEqual(12, items[0].quality)
    
    def test_aged_brie_quality_capped_at_50(self):
        """Aged Brie quality should be capped at 50"""
        items = [Item("Aged Brie", 5, 50)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(4, items[0].sell_in)
        self.assertEqual(50, items[0].quality)
    
    def test_aged_brie_quality_capped_at_50_after_sell_date(self):
        """Aged Brie quality should be capped at 50 even after sell date"""
        items = [Item("Aged Brie", 0, 49)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(-1, items[0].sell_in)
        self.assertEqual(50, items[0].quality)
    
    # Sulfuras Tests
    def test_sulfuras_never_changes_sell_in(self):
        """Sulfuras should never change its sell_in value"""
        items = [Item("Sulfuras, Hand of Ragnaros", 5, 80)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(5, items[0].sell_in)
        self.assertEqual(80, items[0].quality)
    
    def test_sulfuras_never_changes_quality(self):
        """Sulfuras should never change its quality value"""
        items = [Item("Sulfuras, Hand of Ragnaros", 0, 80)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(0, items[0].sell_in)
        self.assertEqual(80, items[0].quality)
    
    def test_sulfuras_never_changes_after_sell_date(self):
        """Sulfuras should never change even after sell date"""
        items = [Item("Sulfuras, Hand of Ragnaros", -1, 80)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(-1, items[0].sell_in)
        self.assertEqual(80, items[0].quality)
    
    # Backstage Passes Tests
    def test_backstage_passes_increase_by_1_when_more_than_10_days(self):
        """Backstage passes should increase quality by 1 when more than 10 days left"""
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 15, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(14, items[0].sell_in)
        self.assertEqual(11, items[0].quality)
    
    def test_backstage_passes_increase_by_2_when_10_days_or_less(self):
        """Backstage passes should increase quality by 2 when 10 days or less"""
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 10, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(9, items[0].sell_in)
        self.assertEqual(12, items[0].quality)
    
    def test_backstage_passes_increase_by_2_when_6_to_10_days(self):
        """Backstage passes should increase quality by 2 when 6-10 days left"""
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 6, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(5, items[0].sell_in)
        self.assertEqual(12, items[0].quality)
    
    def test_backstage_passes_increase_by_3_when_5_days_or_less(self):
        """Backstage passes should increase quality by 3 when 5 days or less"""
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 5, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(4, items[0].sell_in)
        self.assertEqual(13, items[0].quality)
    
    def test_backstage_passes_increase_by_3_when_1_day_left(self):
        """Backstage passes should increase quality by 3 when 1 day left"""
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 1, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(0, items[0].sell_in)
        self.assertEqual(13, items[0].quality)
    
    def test_backstage_passes_drop_to_zero_after_concert(self):
        """Backstage passes should drop to 0 quality after the concert"""
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 0, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(-1, items[0].sell_in)
        self.assertEqual(0, items[0].quality)
    
    def test_backstage_passes_quality_capped_at_50(self):
        """Backstage passes quality should be capped at 50"""
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 5, 49)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(4, items[0].sell_in)
        self.assertEqual(50, items[0].quality)
    
    def test_backstage_passes_quality_capped_at_50_with_10_days(self):
        """Backstage passes quality should be capped at 50 even with +2 bonus"""
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 10, 49)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(9, items[0].sell_in)
        self.assertEqual(50, items[0].quality)
    
    # Edge Cases
    def test_multiple_items_updated_independently(self):
        """Multiple items should be updated independently"""
        items = [
            Item("Standard Item", 5, 10),
            Item("Aged Brie", 5, 10),
            Item("Sulfuras, Hand of Ragnaros", 5, 80)
        ]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        
        # Standard item
        self.assertEqual(4, items[0].sell_in)
        self.assertEqual(9, items[0].quality)
        
        # Aged Brie
        self.assertEqual(4, items[1].sell_in)
        self.assertEqual(11, items[1].quality)
        
        # Sulfuras
        self.assertEqual(5, items[2].sell_in)
        self.assertEqual(80, items[2].quality)

    # Conjured Item Tests
    def test_conjured_item_before_sell_date_decreases_quality_by_two(self):
        """Conjured item before sell date should decrease quality by 2"""
        items = [Item("Conjured Mana Cake", 5, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(4, items[0].sell_in)
        self.assertEqual(8, items[0].quality)
    
    def test_conjured_item_after_sell_date_decreases_quality_by_four(self):
        """Conjured item after sell date should decrease quality by 4"""
        items = [Item("Conjured Mana Cake", 0, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(-1, items[0].sell_in)
        self.assertEqual(6, items[0].quality)
    
    def test_conjured_item_quality_never_goes_negative(self):
        """Conjured item quality should never go below 0"""
        items = [Item("Conjured Mana Cake", 5, 1)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(4, items[0].sell_in)
        self.assertEqual(0, items[0].quality)
    
    def test_conjured_item_quality_never_goes_negative_after_sell_date(self):
        """Conjured item quality should never go below 0 even after sell date"""
        items = [Item("Conjured Mana Cake", 0, 3)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(-1, items[0].sell_in)
        self.assertEqual(0, items[0].quality)
    
    def test_conjured_item_quality_floor_with_minimal_quality(self):
        """Conjured item with quality 1 should not go negative after multiple updates"""
        items = [Item("Conjured Mana Cake", 1, 1)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(0, items[0].sell_in)
        self.assertEqual(0, items[0].quality)
        
        # Update again to ensure it stays at 0
        gilded_rose.update_quality()
        self.assertEqual(-1, items[0].sell_in)
        self.assertEqual(0, items[0].quality)
    
    def test_conjured_item_with_different_name_variations(self):
        """Conjured items with different names should all degrade twice as fast"""
        items = [
            Item("Conjured Sword", 3, 8),
            Item("Conjured Health Potion", 2, 6)
        ]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        
        # Conjured Sword
        self.assertEqual(2, items[0].sell_in)
        self.assertEqual(6, items[0].quality)
        
        # Conjured Health Potion
        self.assertEqual(1, items[1].sell_in)
        self.assertEqual(4, items[1].quality)


if __name__ == '__main__':
    unittest.main()
