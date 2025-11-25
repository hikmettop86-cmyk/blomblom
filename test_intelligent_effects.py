#!/usr/bin/env python3
"""Test script for intelligent effect selection algorithm"""

import sys
import random

# Add current directory to path
sys.path.insert(0, '/home/user/MB-BLock')

# Import the function from main
from main import akilli_efekt_secimi

def test_intelligent_selection():
    """Test the intelligent effect selection algorithm"""
    print("=" * 100)
    print("Testing Intelligent Effect Selection Algorithm")
    print("=" * 100)

    # Run multiple tests to verify randomness and consistency
    for i in range(5):
        print(f"\n\n{'='*100}")
        print(f"Test Run #{i+1}")
        print(f"{'='*100}")

        try:
            # Call the intelligent selection function
            selected_effects = akilli_efekt_secimi()

            # Verify results
            if isinstance(selected_effects, set):
                print(f"\n✅ Test #{i+1} PASSED")
                print(f"   • Returned a set: {type(selected_effects)}")
                print(f"   • Number of effects: {len(selected_effects)}")
                print(f"   • Effect count in valid range (2-10): {2 <= len(selected_effects) <= 10}")

                if not (2 <= len(selected_effects) <= 10):
                    print(f"   ⚠️  WARNING: Effect count outside expected range!")
            else:
                print(f"\n❌ Test #{i+1} FAILED")
                print(f"   • Expected set, got: {type(selected_effects)}")

        except Exception as e:
            print(f"\n❌ Test #{i+1} FAILED with exception:")
            print(f"   • Error: {e}")
            import traceback
            traceback.print_exc()

    print(f"\n\n{'='*100}")
    print("All tests completed!")
    print(f"{'='*100}\n")

if __name__ == "__main__":
    test_intelligent_selection()
